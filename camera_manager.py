import cv2
import os
import sys
import platform
import subprocess
import re
import ctypes
from contextlib import contextmanager

class CameraManager:
  """Cross-platform camera detection and management class"""

  def __init__(self):
    self.os_type = platform.system()  # 'Windows', 'Linux', or 'Darwin'

  @contextmanager
  def suppress_stdout_stderr(self):
    """Context manager to suppress stdout and stderr"""
    with open(os.devnull, 'w') as devnull:
      # Save the current file descriptors
      old_stdout_fd = os.dup(sys.stdout.fileno())
      old_stderr_fd = os.dup(sys.stderr.fileno())

      # Redirect stdout and stderr to devnull
      os.dup2(devnull.fileno(), sys.stdout.fileno())
      os.dup2(devnull.fileno(), sys.stderr.fileno())

      try:
        yield  # Execute the code block inside the with statement
      finally:
        # Restore the file descriptors
        os.dup2(old_stdout_fd, sys.stdout.fileno())
        os.dup2(old_stderr_fd, sys.stderr.fileno())
        os.close(old_stdout_fd)
        os.close(old_stderr_fd)

  def get_system_cameras(self):
    """
    Get camera information from system without activating cameras.
    Returns dict with camera names and potential indices.
    """
    cameras = {}

    if self.os_type == "Windows":
      cameras = self._get_windows_camera_names()
    elif self.os_type == "Linux":
      cameras = self._get_linux_camera_names()
    elif self.os_type == "Darwin":  # macOS
      cameras = self._get_macos_camera_names()

    return cameras

  def _get_windows_camera_names(self):
    """Get Windows camera names without activating them"""
    cameras = {}
    try:
      # Multiple approaches to find cameras on Windows
      methods = [
        # Method 1: Search by caption/name containing camera
        '''powershell -Command "Get-CimInstance Win32_PnPEntity | Where-Object {($_.Caption -like '*camera*') -or ($_.Caption -like '*webcam*') -or ($_.Name -like '*camera*') -or ($_.Name -like '*webcam*')} | Where-Object {$_.Status -eq 'OK'} | Select-Object Name, Caption, DeviceID, Status | ConvertTo-Json"''',

        # Method 2: Search by USB video service
        '''powershell -Command "Get-CimInstance Win32_PnPEntity | Where-Object {$_.Service -eq 'usbvideo'} | Where-Object {$_.Status -eq 'OK'} | Select-Object Name, Caption, DeviceID, Status | ConvertTo-Json"''',

        # Method 3: Search by PNP class
        '''powershell -Command "Get-CimInstance Win32_PnPEntity | Where-Object {($_.PNPClass -eq 'Camera') -or ($_.PNPClass -eq 'Image')} | Where-Object {$_.Status -eq 'OK'} | Select-Object Name, Caption, DeviceID, Status | ConvertTo-Json"''',

        # Method 4: Search imaging devices
        '''powershell -Command "Get-CimInstance Win32_PnPEntity | Where-Object {($_.ClassGuid -eq '{6bdd1fc6-810f-11d0-bec7-08002be2092f}') -or ($_.ClassGuid -eq '{ca3e7ab9-b4c3-4ae6-8251-579ef933890f}')} | Where-Object {$_.Status -eq 'OK'} | Select-Object Name, Caption, DeviceID, Status | ConvertTo-Json"'''
      ]

      for method in methods:
        try:
          result = subprocess.run(method, capture_output=True, text=True, shell=True, timeout=10)

          if result.returncode == 0 and result.stdout.strip():
            import json
            try:
              data = json.loads(result.stdout)
              # Handle both single device (dict) and multiple devices (list)
              if isinstance(data, dict):
                data = [data]

              for i, device in enumerate(data):
                # Use Caption first, then Name as fallback
                device_name = device.get('Caption') or device.get('Name', f'Camera {i}')
                cameras[i] = {
                  'name': device_name,
                  'device_id': device.get('DeviceID', ''),
                  'status': 'Available'
                }

              if cameras:  # If we found cameras, break out of method loop
                break

            except json.JSONDecodeError:
              continue
        except Exception:
          continue

      # Ultimate fallback - try DirectShow enumeration
      if not cameras:
        cameras = self._get_windows_directshow_cameras()

    except Exception as e:
      # Silent fallback - create at least one generic camera entry
      cameras = {0: {'name': 'Camera 0', 'device_id': '', 'status': 'Unknown'}}

    return cameras

  def _get_windows_directshow_cameras(self):
    """Fallback method to get DirectShow cameras on Windows"""
    cameras = {}
    try:
      # Try different approaches for DirectShow camera enumeration
      methods = [
        # Method 1: Use WMI with different filters
        '''powershell -Command "Get-WmiObject Win32_PnPEntity | Where-Object {$_.Caption -match 'camera'} | Select-Object Name, Caption, DeviceID | ConvertTo-Json"''',

        # Method 2: Look for USB video devices
        '''powershell -Command "Get-WmiObject -Class Win32_PnPEntity | Where-Object {$_.service -eq 'usbvideo'} | Select-Object Name, Caption, DeviceID | ConvertTo-Json"''',

        # Method 3: Search device manager camera category
        '''powershell -Command "Get-PnpDevice -Class Camera | Where-Object {$_.Status -eq 'OK'} | Select-Object Name, FriendlyName, DeviceID | ConvertTo-Json"'''
      ]

      for method in methods:
        try:
          result = subprocess.run(method, capture_output=True, text=True, shell=True, timeout=8)

          if result.returncode == 0 and result.stdout.strip():
            import json
            try:
              data = json.loads(result.stdout)
              if isinstance(data, dict):
                data = [data]

              for i, device in enumerate(data):
                # Prefer FriendlyName, then Caption, then Name
                device_name = (device.get('FriendlyName') or
                              device.get('Caption') or
                              device.get('Name', f'Camera {i}'))

                cameras[i] = {
                  'name': device_name,
                  'device_id': device.get('DeviceID', ''),
                  'status': 'Available'
                }

              if cameras:
                break
            except json.JSONDecodeError:
              continue
        except Exception:
          continue

    except Exception:
      pass

    return cameras

  def _get_linux_camera_names(self):
    """Get Linux camera names from V4L2 devices"""
    cameras = {}
    try:
      # List video devices
      result = subprocess.run(['find', '/dev', '-name', 'video*', '-type', 'c'],
                            capture_output=True, text=True, timeout=5)

      video_devices = result.stdout.strip().split('\n') if result.stdout.strip() else []

      for device_path in video_devices:
        if not device_path:
          continue

        device_num = re.search(r'video(\d+)', device_path)
        if device_num:
          index = int(device_num.group(1))

          # Get device name using v4l2-ctl
          try:
            name_result = subprocess.run(['v4l2-ctl', '--device', device_path, '--info'],
                                        capture_output=True, text=True, timeout=3)

            device_name = f"Video Device {index}"
            for line in name_result.stdout.split('\n'):
              if 'Card type' in line:
                device_name = line.split(':', 1)[1].strip()
                break

            cameras[index] = {
              'name': device_name,
              'device_path': device_path,
              'status': 'Available'
            }
          except (FileNotFoundError, subprocess.TimeoutExpired):
            # v4l2-ctl not available or timeout, use generic name
            cameras[index] = {
              'name': f"Video Device {index}",
              'device_path': device_path,
              'status': 'Available'
            }

    except Exception as e:
      # Silent fallback
      cameras = {0: {'name': 'Camera 0', 'device_path': '/dev/video0', 'status': 'Unknown'}}

    return cameras

  def _get_macos_camera_names(self):
    """Get macOS camera names from system profiler"""
    cameras = {}
    try:
      cmd = "system_profiler SPCameraDataType -json"
      result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)

      if result.returncode == 0:
        import json
        data = json.loads(result.stdout)

        camera_data = data.get('SPCameraDataType', [])
        for i, camera in enumerate(camera_data):
          cameras[i] = {
            'name': camera.get('_name', f'Camera {i}'),
            'model': camera.get('spcamera_model-id', ''),
            'status': 'Available'
          }

    except Exception as e:
      # Silent fallback
      cameras = {0: {'name': 'Camera 0', 'model': '', 'status': 'Unknown'}}

    return cameras

  def get_available_cameras(self, max_index=10, verbose=False, test_frame=False):
    """
    Check for available cameras with minimal hardware interaction.

    Args:
        max_index (int): Maximum camera index to check
        verbose (bool): Whether to print detailed information
        test_frame (bool): Whether to test grabbing a frame (causes camera activation)

    Returns:
        dict: Dictionary mapping camera indices to their properties
    """
    available = {}

    # First get system camera information without activating cameras
    system_cameras = self.get_system_cameras()

    if verbose:
      print(f"\n=== System Cameras on {self.os_type} ===")
      for idx, info in system_cameras.items():
        print(f"Camera {idx}: {info['name']} - {info['status']}")

    # Only test OpenCV camera access if explicitly requested or no system info available
    if test_frame or not system_cameras:
      if verbose:
        print("\n=== Testing OpenCV Camera Access ===")

      for i in range(max_index):
        try:
          # Use suppress context to minimize visual feedback
          with self.suppress_stdout_stderr():
            # Try different camera APIs based on platform
            if self.os_type == "Windows":
              cap = cv2.VideoCapture(i, cv2.CAP_DSHOW if hasattr(cv2, 'CAP_DSHOW') else 0)
            elif self.os_type == "Linux":
              cap = cv2.VideoCapture(i, cv2.CAP_V4L2 if hasattr(cv2, 'CAP_V4L2') else 0)
            else:
              cap = cv2.VideoCapture(i)

            if cap.isOpened():
              # Get basic properties without reading frames
              props = {}
              props['width'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
              props['height'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
              props['fps'] = cap.get(cv2.CAP_PROP_FPS)

              try:
                backend_name = cap.getBackendName()
                props['backend'] = backend_name
              except AttributeError:
                props['backend'] = "unknown"

              # Use system name if available, otherwise generic
              if i in system_cameras:
                props['name'] = system_cameras[i]['name']
              else:
                props['name'] = f"Camera {i}"

              # Only test frame capture if explicitly requested
              if test_frame:
                ret, frame = cap.read()
                props['frame_test'] = "Success" if ret else "Failed"
              else:
                props['frame_test'] = "Skipped"

              available[i] = props

              if verbose:
                print(f"[✓] {props['name']}: {props['width']}x{props['height']} @ {props['fps']:.1f}fps")
                if test_frame:
                  print(f"    Backend: {props['backend']}, Frame test: {props['frame_test']}")
            elif verbose:
              camera_name = system_cameras.get(i, {}).get('name', f'Camera {i}')
              print(f"[✗] {camera_name} not accessible via OpenCV")

            cap.release()

        except Exception as e:
          if verbose:
            camera_name = system_cameras.get(i, {}).get('name', f'Camera {i}')
            print(f"[✗] Error testing {camera_name}: {str(e)}")
    else:
      # Just return system camera info without OpenCV testing
      for idx, info in system_cameras.items():
        available[idx] = {
          'name': info['name'],
          'status': info['status'],
          'frame_test': 'Skipped',
          'backend': 'System Detection'
        }

    return available

  def list_cameras_simple(self, verbose=False):
    """Simple method to list cameras without any activation"""
    cameras = self.get_system_cameras()
    if verbose:
      print(f"\nFound {len(cameras)} camera(s) on {self.os_type}:")
      for idx, info in cameras.items():
        print(f"  {idx}: {info['name']}")
    return cameras

  # Keep existing diagnostic methods unchanged
  def _check_system_cameras(self, verbose):
    """Platform-specific checks for camera hardware"""
    if self.os_type == "Windows":
      self._check_windows_cameras(verbose)
    elif self.os_type == "Linux":
      self._check_linux_cameras(verbose)
    elif self.os_type == "Darwin":  # macOS
      self._check_macos_cameras(verbose)

  def _check_windows_cameras(self, verbose):
    """Check for cameras on Windows systems"""
    try:
      # Use PowerShell to list connected camera devices
      cmd = "powershell -Command \"Get-PnpDevice -Class 'Camera' | Format-Table -Property Status, Class, FriendlyName -AutoSize\""
      result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

      if verbose:
        print("Windows Camera Devices:")
        print(result.stdout)

        # Try to get more detailed DirectShow device information
        try:
          # This will only work if the user has DirectShow filter graph editor installed
          dshow_cmd = "powershell -Command \"Get-CimInstance Win32_PnPEntity | Where-Object {$_.Caption -like '*camera*' -or $_.Caption -like '*webcam*'} | Format-Table Caption, DeviceID, Status -AutoSize\""
          dshow_result = subprocess.run(dshow_cmd, capture_output=True, text=True, shell=True)
          print("\nDirectShow Camera Details:")
          print(dshow_result.stdout)
        except Exception:
          pass
    except Exception as e:
      print(f"Error checking Windows camera devices: {e}")

  def _check_linux_cameras(self, verbose):
    """Check for cameras on Linux systems"""
    try:
      # Check video devices
      result = subprocess.run(['ls', '-l', '/dev/video*'], capture_output=True, text=True)
      print("Linux Video Devices:")
      print(result.stdout)

      # Check v4l2 devices if v4l-utils is installed
      try:
        v4l_result = subprocess.run(['v4l2-ctl', '--list-devices'],
                                    capture_output=True, text=True)
        print("\nV4L2 Devices:")
        print(v4l_result.stdout)
      except Exception:
        print("v4l2-ctl not available. Install with: sudo apt install v4l-utils")
    except Exception as e:
      print(f"Error checking Linux camera devices: {e}")

  def _check_macos_cameras(self, verbose):
    """Check for cameras on macOS systems"""
    try:
      # Use system_profiler to get camera information
      cmd = "system_profiler SPCameraDataType"
      result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
      print("macOS Camera Devices:")
      print(result.stdout)
    except Exception as e:
      print(f"Error checking macOS camera devices: {e}")

  def diagnose_camera_issues(self):
    """
    Run comprehensive diagnostics on camera setup (cross-platform)
    """
    print(f"=== Camera Diagnostics ({self.os_type}) ===")

    # Platform-specific diagnostics
    if self.os_type == "Windows":
      self._diagnose_windows_cameras()
    elif self.os_type == "Linux":
      self._diagnose_linux_cameras()
    elif self.os_type == "Darwin":  # macOS
      self._diagnose_macos_cameras()

    # Check OpenCV build information (cross-platform)
    print("\nOpenCV build information:")
    print(f"Version: {cv2.__version__}")

    # Check OpenCV build components if getBuildInformation is available
    try:
      build_info = cv2.getBuildInformation()
      print(f"Has FFMPEG: {'FFMPEG' in build_info}")
      print(f"Has V4L: {'V4L' in build_info}")
      print(f"Has DirectShow: {'DirectShow' in build_info}")
      print(f"Has AVFoundation: {'AVFoundation' in build_info}")
    except AttributeError:
      print("OpenCV build information not available in this version")

    # Test cameras with our function (cross-platform)
    print("\nTesting cameras:")
    cameras = self.get_available_cameras(max_index=5, verbose=True)
    print(f"\nFound {len(cameras)} working cameras")

    return cameras

  def _diagnose_windows_cameras(self):
    """Windows-specific camera diagnostics"""
    # Check if process has admin rights
    try:
      is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
      print(f"Running with admin privileges: {'Yes' if is_admin else 'No'}")
    except Exception:
      print("Could not determine admin status")

    # Check Windows Device Manager for camera devices
    try:
      print("\nChecking camera devices in Device Manager:")
      cmd = "powershell -Command \"Get-PnpDevice -Class 'Camera','Image' | Format-Table -Property Status, Class, FriendlyName -AutoSize\""
      result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
      print(result.stdout)

      # Check for any problem devices
      problem_cmd = "powershell -Command \"Get-PnpDevice | Where-Object {$_.Status -ne 'OK'} | Format-Table -Property Status, Class, FriendlyName -AutoSize\""
      problem_result = subprocess.run(problem_cmd, capture_output=True, text=True, shell=True)
      if problem_result.stdout.strip():
        print("\nProblem devices found:")
        print(problem_result.stdout)
    except Exception as e:
      print(f"Error checking Windows devices: {e}")

  def _diagnose_linux_cameras(self):
    """Linux-specific camera diagnostics"""
    # Check user permissions
    try:
      current_user = subprocess.run(['whoami'], capture_output=True, text=True).stdout.strip()
      video_group_check = subprocess.run(['groups', current_user], capture_output=True, text=True).stdout

      print(f"Current user: {current_user}")
      if 'video' in video_group_check:
        print("✓ User is in video group")
      else:
        print("✗ User is NOT in video group. Run: sudo usermod -a -G video $USER")
    except Exception as e:
      print(f"Error checking user groups: {e}")

    # Check video devices
    try:
      devices = subprocess.run(['ls', '-l', '/dev/video*'], capture_output=True, text=True).stdout
      print("\nVideo devices:")
      print(devices)
    except Exception as e:
      print(f"Error listing video devices: {e}")

    # Check kernel modules
    try:
      modules = subprocess.run(['lsmod | grep -E "uvc|video"'], shell=True, capture_output=True, text=True).stdout
      print("\nRelevant kernel modules:")
      print(modules)
    except Exception as e:
      print(f"Error checking kernel modules: {e}")

    # Check V4L2 device info
    try:
      v4l_devices = subprocess.run(['v4l2-ctl', '--list-devices'], capture_output=True, text=True).stdout
      print("\nV4L2 devices:")
      print(v4l_devices)

      # Get detailed info about first device if it exists
      device_match = re.search(r'/dev/video\d+', v4l_devices)
      if device_match:
        first_device = device_match.group(0)
        print(f"\nDetailed info for {first_device}:")
        device_info = subprocess.run(['v4l2-ctl', '--device', first_device, '--all'],
                                    capture_output=True, text=True).stdout
        print(device_info)
    except Exception as e:
      print(f"Error getting V4L2 info: {e}")

  def _diagnose_macos_cameras(self):
    """MacOS-specific camera diagnostics"""
    # Check camera permissions in macOS
    try:
      print("\nChecking system camera information:")
      cmd = "system_profiler SPCameraDataType"
      result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
      print(result.stdout)

      # Check for camera permissions
      print("\nCamera permissions may need to be granted in System Preferences -> Security & Privacy -> Privacy -> Camera")
    except Exception as e:
      print(f"Error checking macOS camera info: {e}")
