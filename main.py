import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5 import (QtCore, QtWidgets, QtGui)
from PyQt5.QtCore import Qt
import numpy as np
from ultralytics import YOLO
from camera_manager import CameraManager

from ui.birdview_ui import Ui_MainWindow
from ui.birdview_modal import Ui_Modal

from lxml import objectify, etree
import cv2
import os

import re

from copy import deepcopy

import logging
logging.getLogger('ultralytics').setLevel(logging.ERROR)

pageSizes = {
  'navigation': (425, 150),
  'cameraStatus': (425, 200),
  'floorPlanSetup': (425, 290),
  'aiModel': (425, 170),
  'monitoring': (589, 267),
  'popupModal': (322, 83)
}

QWIDGETSIZE_MAX = 16777215

config_fname = "config.xml"
config = objectify.parse(config_fname)

class MainWindow(QMainWindow):
  def __init__(self, config):
    super(MainWindow, self).__init__()

    self.config = config.getroot()
    self.temp_config = deepcopy(self.config)
    self.no_cameras = False

    self.setWindowTitle('Birdview')

    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.modal_window = QtWidgets.QMainWindow(self)
    self.modal_ui = Ui_Modal()
    self.modal_ui.setupUi(self.modal_window)

    # Disable maximize button
    self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint)

    # Center screen coords
    self.screen_center = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
    self.centerScreen()

    # Initial window size (navigation page size)
    self.resize(*pageSizes['navigation'])
    self.setFixedSize(*pageSizes['navigation'])

    # Set first page
    self.ui.mainStackedWidget.setCurrentIndex(0)

    self.initHandlers()
    self.loadConfig()

  def saveToConfig(self, section, fields, success_message, disable_button=None):
    section_config = getattr(self.temp_config, section, None)

    if section_config is None:
      self.showMessageBox(
          title="Error",
          message=f"Section '{section}' not found in temp config.",
          icon=QtWidgets.QMessageBox.Critical
        )
      return

    changes_made = False
    for field in fields:
      value = getattr(section_config, field, '')
      if value != '':
        setattr(getattr(self.config, section), field, value)
        changes_made = True

    if changes_made:
      with open(config_fname, "wb") as f:
        tree = etree.ElementTree(self.config)
        tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8")

      self.showMessageBox(
        title="Success",
        message=success_message,
        icon=QtWidgets.QMessageBox.Information
      )

      if disable_button:
        disable_button.setDisabled(True)

    else:
      self.showMessageBox(
        title="No Changes Made",
        message=f"No changes were made to the {section} settings.",
        icon=QtWidgets.QMessageBox.Warning
      )

  def makeResizable(self):
    self.setMinimumSize(0, 0)
    self.setMaximumSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)

  def centerScreen(self):
    self.frame_geom = self.frameGeometry()
    self.frame_geom.moveCenter(self.screen_center)
    self.move(self.frame_geom.topLeft())

  def showInputPopupModal(self, label='Enter value:', default_value=''):
    self.modal_ui.label.setText(label)
    self.modal_ui.modalInputBox.setPlainText(default_value)

    frame_geom = self.modal_window.frameGeometry()
    frame_geom.moveCenter(self.screen_center)
    self.modal_window.move(frame_geom.topLeft())

    self.modal_window.show()

  def showMessageBox(self, title, message, icon=QtWidgets.QMessageBox.Information):
    msg_box = QtWidgets.QMessageBox(self)
    msg_box.setWindowTitle('Birdview - ' + title)
    msg_box.setIcon(icon)
    msg_box.setText(title)
    msg_box.setInformativeText(message)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)

    msg_box.buttonClicked.connect(lambda: (msg_box.close(), self.modal_window.close()))
    msg_box.exec()

  def _getAvailableCameras(self, verbose=False):
    manager = CameraManager()

    if not verbose:
      with manager.suppress_stdout_stderr():
        result = manager.get_available_cameras(verbose=verbose, test_frame=False)
    else:
      result = manager.get_available_cameras(verbose=verbose, test_frame=True)

    return list(result.keys()) if isinstance(result, dict) else result

  def diagnose_camera_issues(self):
    manager = CameraManager()
    return manager.diagnose_camera_issues()

  def cameraConnectionSetup(self):
    print('Loading camera config...')
    self.ui.cameraSetupSaveChangesBtn.setDisabled(True)

    self.temp_config.camera.source = self.config.camera.source
    self.temp_config.camera.type = self.config.camera.type

    # Camera Connection Page Config
    available_cameras = self._getAvailableCameras()
    print(available_cameras)

    self.camera_mapping = {}

    if len(available_cameras) == 0:
      self.no_cameras = True
      self.ui.cameraSelectionCombobox.clear()
      self.ui.cameraSelectionCombobox.addItem('No cameras available')
      self.ui.cameraSelectionCombobox.setDisabled(True)
      self.ui.cameraSelectionCombobox.setCurrentIndex(0)

    else:
      self.no_cameras = False
      self.ui.cameraSelectionCombobox.clear()

      for i, camera in enumerate(available_cameras):
        camera_name = f"Camera {i}"  # Dropdown display name (replace with actual name if known)
        self.camera_mapping[camera_name] = i  # Map to index or path
        self.ui.cameraSelectionCombobox.addItem(camera_name)

      # Set current selection to match saved camera name (if available)
      saved_camera_name = getattr(self.config.camera, 'name', None)
      if saved_camera_name is not None and saved_camera_name.text.strip():
          name_text = saved_camera_name.text
          index = self.ui.cameraSelectionCombobox.findText(name_text)
          if index >= 0:
              self.ui.cameraSelectionCombobox.setCurrentIndex(index)

      self.ui.cameraSelectionCombobox.setEnabled(True)

    if self.config.camera.source != '':
      if hasattr(self.config.camera, 'name') and self.config.camera.name.text.strip():
        self.ui.currentCameraValue.setText(self.config.camera.name.text)
      else:
        self.ui.currentCameraValue.setText(self.config.camera.source.text)

      if self.config.camera.type.text == 'RTSP':
        self.ui.useRSTPCheckbox.setChecked(True)
        self.ui.RSTPBtn.setEnabled(True)
        self.ui.cameraSelectionCombobox.setDisabled(True)
      else:
        self.ui.useRSTPCheckbox.setChecked(False)
        self.ui.cameraSelectionCombobox.setEnabled(True)

  def floorPlanSetup(self):
    print('Loading floor plan config...')
    self.fp_default_width = 400
    self.fp_default_height = 203
    self.ui.floorPlanSetupSaveChangesBtn.setDisabled(True)

    self.temp_config.floorplan.image = self.config.floorplan.image

    # Floor Plan Setup Page Config
    if self.config.floorplan.image != '':
      file_name = self.config.floorplan.image.text
      pixmap = QtGui.QPixmap(file_name)
      self.ui.floorPlanImageBox.setPixmap(pixmap)
      self.ui.floorPlanImageBox.setScaledContents(True)
      self.ui.floorPlanImageBox.setMinimumSize(0, 0)
      self.ui.floorPlanImageBox.setMaximumSize(self.fp_default_width, self.fp_default_height)

      # Update the floor plan path in the config
      self.temp_config.floorplan.image = file_name

      self.floorPlanImageChanged()

  def aiModelSetup(self):
    print('Loading AI model config...')
    self.ui.aiModelSaveChangesBtn.setDisabled(True)

    self.temp_config.model.path = self.config.model.path.text

    if self.config.model.path != '':
      self.ui.selectedAIModelValue.setText(self.config.model.path.text)

  def loadConfig(self):
    self.cameraConnectionSetup()
    self.floorPlanSetup()
    self.aiModelSetup()

  def resizeWindow(self, size):
    self.makeResizable()
    self.resize(*size)
    self.setFixedSize(*size)

  def backToNavigationPage(self):
    self.centerScreen()

    # Set the window size to the navigation page size
    self.resizeWindow(pageSizes['navigation'])

    # Set the current page to the navigation page
    self.ui.mainStackedWidget.setCurrentIndex(0)

  # --- Event Handlers --- #
  def initHandlers(self):
    # Camera Connection Widget functions
    self.ui.cameraConnectionWidget.clicked.connect(self.cameraConnectionClicked)
    self.ui.cameraStatusPageBackBtn.clicked.connect(self.backToNavigationPage)
    self.ui.useRSTPCheckbox.toggled.connect(self.isRTSPCheckboxUnchecked)
    self.ui.RSTPBtn.clicked.connect(self.onRTSPButtonPressed)
    self.modal_ui.modalInputBox.installEventFilter(self)
    self.ui.testCameraBtn.clicked.connect(self.testCameraPressed)
    self.ui.cameraSelectionCombobox.currentIndexChanged.connect(self.currentCameraValueChanged)
    self.ui.cameraSetupSaveChangesBtn.clicked.connect(self.cameraSetupSaveChangesPressed)

    # Floor Plan Setup Widget functions
    self.ui.floorPlanSetupWidget.clicked.connect(self.floorPlanSetupClicked)
    self.ui.floorPlanSetupPageBackBtn.clicked.connect(self.backToNavigationPage)
    self.ui.floorPlanSetupPageBackBtn.clicked.connect(self.floorPlanSetupPageBackBtnPressed)
    self.ui.uploadFloorPlanImageBtn.clicked.connect(self.floorPlanUploadBtnPressed)
    self.ui.previewFloorPlanImageBtn.clicked.connect(self.floorPlanPreviewBtnPressed)
    self.ui.floorPlanSetupSaveChangesBtn.clicked.connect(self.floorPlanSetupSaveChangesPressed)

    # AI Model Widget functions
    self.ui.selectModelWidget.clicked.connect(self.selectModelClicked)
    self.ui.aiModelPageBackBtn.clicked.connect(self.backToNavigationPage)
    self.ui.aiModelChooseBtn.clicked.connect(self.aiChooseBtnPressed)
    self.ui.aiModelSaveChangesBtn.clicked.connect(self.aiModelSaveChangesPressed)

    # Monitoring Widget functions
    self.ui.liveMonitoringWidget.clicked.connect(self.monitoringClicked)
    self.ui.monitoringPageBackBtn.clicked.connect(self.backToNavigationPage)
    self.ui.worldPointsBtn.clicked.connect(self.worldPointsBtnPressed)
    self.ui.cameraPointsBtn.clicked.connect(self.cameraPointsBtnPressed)
    self.ui.startMonitoringBtn.clicked.connect(self.startMonitoringPressed)

  # CAMERA CONNECTION PAGE
  def cameraConnectionClicked(self):
    self.centerScreen()

    # Set the window size to the camera status page size
    self.resizeWindow(pageSizes['cameraStatus'])

    # Set the current page to the camera status page
    self.ui.mainStackedWidget.setCurrentIndex(1)

    # Reload camera config
    self.cameraConnectionSetup()

  def currentCameraValueChanged(self):
    selected_camera = self.ui.cameraSelectionCombobox.currentText()
    if selected_camera and selected_camera != 'No cameras available':
      self.temp_config.camera.source = self.camera_mapping.get(selected_camera, '')
      self.temp_config.camera.name = selected_camera
      self.ui.currentCameraValue.setText(selected_camera)

      # Compare names, not just source index
      current_name = getattr(self.config.camera, 'name', None)
      current_name = current_name.text if current_name is not None else ""

      if current_name != selected_camera:
        self.ui.cameraSetupSaveChangesBtn.setEnabled(True)
      else:
        self.ui.cameraSetupSaveChangesBtn.setDisabled(True)

  def isRTSPCheckboxUnchecked(self):
    if self.ui.useRSTPCheckbox.isChecked():
      self.temp_config.camera.type = 'RTSP'
      self.ui.cameraSelectionCombobox.setDisabled(True)
    else:
      self.temp_config.camera.type = 'Default'
      self.ui.cameraSelectionCombobox.setDisabled(False)

      # Force update from currently selected dropdown item
      self.currentCameraValueChanged()

  def onRTSPButtonPressed(self):
    self.showInputPopupModal(label='Enter RTSP URL:', default_value=self.ui.currentCameraValue.text())

  def eventFilter(self, obj, event):
    if obj == self.modal_ui.modalInputBox and event.type() == QtCore.QEvent.KeyPress:
      if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
        self.onRTSPInputKeyPressed()
        return True
        # Optional: return True to block further handling
    return super().eventFilter(obj, event)

  def onRTSPInputKeyPressed(self):
    rtsp_url = self.modal_ui.modalInputBox.toPlainText().strip()

    # Simplified regex that allows "rtsp://IP:port/anything"
    rtsp_regex = re.compile(r'^rtsp:\/\/[^\s\/:]+(?::\d+)?(?:\/[^\s]*)?$')
    if not rtsp_regex.match(rtsp_url):
      print(f"[✗] Invalid RTSP URL: {rtsp_url}")
      self.showMessageBox(
        title="Invalid RTSP URL",
        message="Please enter a valid RTSP URL (e.g., rtsp://192.168.1.1:554/stream).",
        icon=QtWidgets.QMessageBox.Warning
      )
      return

    # Set RTSP source and name
    self.temp_config.camera.source = rtsp_url
    self.temp_config.camera.name = rtsp_url
    self.temp_config.camera.type = 'RTSP'

    self.ui.currentCameraValue.setText(rtsp_url)
    self.ui.cameraSetupSaveChangesBtn.setEnabled(True)

    self.modal_ui.modalInputBox.clear()
    self.modal_window.close()

  def testCamera(self, camera_index):
    # Test camera connection
    cap = cv2.VideoCapture(camera_index)

    if cap.isOpened():

      # Show camera window
      cv2.namedWindow("Camera Test", cv2.WINDOW_NORMAL)
      cv2.resizeWindow("Camera Test", 640, 480)

      while True:

        ret, frame = cap.read()

        if not ret:
          print("[✗] Failed to read from camera")
          self.showMessageBox(
            title="Camera Error",
            message="Failed to read from camera. Please check the connection.",
            icon=QtWidgets.QMessageBox.Warning
          )
          break

        cv2.imshow("Camera Test", frame)

        # Wait for 'q' key to exit or close button pressed
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Camera Test", cv2.WND_PROP_VISIBLE) < 1:
          break

      cap.release()
      cv2.destroyAllWindows()

    else:
        print(f"[✗] Camera {self.temp_config.camera.source.text} connection failed")
        self.showMessageBox(
          title="Camera Error",
          message="Failed to connect to the camera. Please check the connection.",
          icon=QtWidgets.QMessageBox.Warning
        )
        cap.release()

  def testCameraPressed(self):
    selected_text = self.ui.currentCameraValue.text().strip()
    print(f"Testing camera from current value: {selected_text}")

    if self.ui.useRSTPCheckbox.isChecked():
      # Use RTSP directly
      self.testCamera(selected_text)
    else:
      # Try lookup via dropdown mapping
      if selected_text in self.camera_mapping:
        camera_index = self.camera_mapping[selected_text]
        self.testCamera(camera_index)
      elif selected_text.isdigit():
        self.testCamera(int(selected_text))
      else:
        self.showMessageBox(
          title="Camera Error",
          message="Invalid camera source. Please check your selection.",
          icon=QtWidgets.QMessageBox.Warning
        )

  def cameraSetupSaveChangesPressed(self):
    if self.ui.useRSTPCheckbox.isChecked():
        # RTSP mode: directly use the current value as RTSP source
        rtsp_url = self.ui.currentCameraValue.text()
        self.temp_config.camera.source = rtsp_url
        self.temp_config.camera.name = rtsp_url  # You may optionally use 'RTSP Stream' as name
        self.temp_config.camera.type = 'RTSP'
    else:
        # Default (dropdown) mode
        selected_camera_name = self.ui.currentCameraValue.text()

        if selected_camera_name in self.camera_mapping:
            camera_index = self.camera_mapping[selected_camera_name]
            self.temp_config.camera.source = str(camera_index)
            self.temp_config.camera.name = selected_camera_name
            self.temp_config.camera.type = 'Default'
        else:
            self.showMessageBox(
                title="Error",
                message="Invalid camera selection. Please select a valid camera.",
                icon=QtWidgets.QMessageBox.Warning
            )
            return

    # Save to config
    self.saveToConfig(
        section='camera',
        fields=['source', 'type', 'name'],
        success_message="Camera settings saved successfully.",
        disable_button=self.ui.cameraSetupSaveChangesBtn
    )

  # FLOOR PLAN SETUP PAGE
  def floorPlanSetupClicked(self):
    self.centerScreen()

    # Set the window size to the floor plan setup page size
    self.resizeWindow(pageSizes['floorPlanSetup'])

    # Set the current page to the floor plan setup page
    self.ui.mainStackedWidget.setCurrentIndex(2)

    # Reload floor plan config
    self.floorPlanSetup()

  def floorPlanUploadBtnPressed(self):
    # Show file dialog to select floor plan image
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.ReadOnly
    file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Floor Plan Image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)

    if file_name:
      # Load the selected image
      pixmap = QtGui.QPixmap(file_name)

      # Set the image to the label
      self.ui.floorPlanImageBox.setPixmap(pixmap)

      # Resize the label to fit the image
      self.ui.floorPlanImageBox.setScaledContents(True)
      self.ui.floorPlanImageBox.setMinimumSize(0, 0)
      self.ui.floorPlanImageBox.setMaximumSize(self.fp_default_width, self.fp_default_height)

      # Update the floor plan path in the config
      self.temp_config.floorplan.image = file_name

      self.floorPlanImageChanged()

  def floorPlanImageChanged(self):
    if self.temp_config.floorplan.image != '':
      # Enable the save changes button if the image has been changed
      self.ui.previewFloorPlanImageBtn.setEnabled(True)
    else:
      # Disable the save changes button if no image is selected
      self.ui.previewFloorPlanImageBtn.setDisabled(True)

    # Check if the floor plan image has been changed
    if self.config.floorplan.image != self.temp_config.floorplan.image:
      self.ui.floorPlanSetupSaveChangesBtn.setEnabled(True)
    else:
      self.ui.floorPlanSetupSaveChangesBtn.setDisabled(True)

  def floorPlanSetupPageBackBtnPressed(self):
    self.temp_config.floorplan.image = ''
    self.ui.floorPlanImageBox.clear()

    self.floorPlanImageChanged()

  def floorPlanPreviewBtnPressed(self):
    if self.temp_config.floorplan.image != '':
      # Show selected image in full screen using cv2
      img = cv2.imread(self.temp_config.floorplan.image.text)

      if img is None:
        self.showMessageBox(
          title="Image Error",
          message="Failed to load the image. Please check the file path.",
          icon=QtWidgets.QMessageBox.Warning
        )
        return

      full_w, full_h = QtWidgets.QApplication.primaryScreen().availableGeometry().getRect()[2:]

      cv2.namedWindow("Floor Plan Preview", cv2.WINDOW_NORMAL)
      cv2.resizeWindow("Floor Plan Preview", full_w, full_h)
      cv2.setWindowProperty("Floor Plan Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
      cv2.imshow("Floor Plan Preview", img)

      cv2.waitKey(0)
      cv2.destroyAllWindows()

  def floorPlanSetupSaveChangesPressed(self):
    self.saveToConfig(
      section='floorplan',
      fields=['image'],
      success_message="Floor plan settings saved successfully.",
      disable_button=self.ui.floorPlanSetupSaveChangesBtn
    )

  # AI MODEL PAGE
  def selectModelClicked(self):
    self.centerScreen()

    # Set the window size to the AI model page size
    self.resizeWindow(pageSizes['aiModel'])

    # Set the current page to the AI model page
    self.ui.mainStackedWidget.setCurrentIndex(3)

    # Reload AI model config
    self.aiModelSetup()

  def aiChooseBtnPressed(self):
    # Show file dialog to select AI model
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.ReadOnly
    file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select AI Model", "", "Models (*.pt)", options=options)

    if file_name:
      # Load the selected model
      self.ui.selectedAIModelValue.setText(file_name)

      # Update the AI model path in the config
      self.temp_config.model.path = file_name

      # Enable the save changes button if the model has been changed
      self.ui.aiModelSaveChangesBtn.setEnabled(True)

  def aiModelSaveChangesPressed(self):
    self.saveToConfig(
      section='model',
      fields=['path'],
      success_message="AI model settings saved successfully.",
      disable_button=self.ui.aiModelSaveChangesBtn
    )

  # MONITORING PAGE
  def monitoringClicked(self):
    # Set the window size to the monitoring page size
    self.resizeWindow(pageSizes['monitoring'])

    self.centerScreen()

    # Set the current page to the monitoring page
    self.ui.mainStackedWidget.setCurrentIndex(4)

    self.monitoringPageSetup()

  def monitoringPageSetup(self):
    self.ui.monitoringCameraStatusValue.setText(self.config.camera.name.text if self.config.camera.name != '' else self.config.camera.source.text)
    self.ui.monitoringFloorPlanStatusValue.setText(self.config.floorplan.image.text)

    if (self.config.camera.source == None or self.config.camera.source.text == ''):
      self.ui.cameraPointsBtn.setDisabled(True)
    else:
      self.ui.cameraPointsBtn.setEnabled(True)

    if (self.config.floorplan.image == None or self.config.floorplan.image.text == ''):
      self.ui.worldPointsBtn.setDisabled(True)
    else:
      self.ui.worldPointsBtn.setEnabled(True)

    self.updateWorldPointsValue()
    self.updateCameraPointsValue()

  def worldPointsBtnPressed(self):
    # Load the floor plan image
    img_path = self.config.floorplan.image.text

    if not img_path or not os.path.exists(img_path):
      self.showMessageBox(
        title="Image Error",
        message="Floor plan image not found. Please upload a valid image.",
        icon=QtWidgets.QMessageBox.Warning
      )
      return

    img = cv2.imread(img_path)
    height, width = img.shape[:2]
    self.temp_config.floorplan.resolution = f"{width},{height}"
    if img is None:
      self.showMessageBox(
          title="Image Error",
          message="Failed to load the image. Please check the file path.",
          icon=QtWidgets.QMessageBox.Warning
      )
      return

    # Variables to store points and history for undo/redo
    points = []
    undo_stack = []

    windowName = "Select World Points"

    def draw_points(image, points):
      """Draw points with numbers on the image."""
      for idx, point in enumerate(points):
        cv2.circle(image, point, 5, (0, 0, 255), -1)  # Draw a red dot

        # Place the number at the center of the dot
        text_size = cv2.getTextSize(str(idx + 1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        text_x = point[0] - text_size[0] // 2
        text_y = point[1] + text_size[1] // 2
        cv2.putText(image, str(idx + 1), (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        # Place the coordinates outside the dot (below the dot)
        coord_text = f"({point[0]},{point[1]})"
        coord_size = cv2.getTextSize(coord_text, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)[0]
        coord_x = max(0, min(point[0] - coord_size[0] // 2, image.shape[1] - coord_size[0]))
        coord_y = min(image.shape[0] - 5, point[1] + 15 + coord_size[1])
        cv2.putText(image, coord_text, (coord_x, coord_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

    def mouse_callback(event, x, y, flags, param):
      """Handle mouse events for point selection."""
      nonlocal points, undo_stack

      if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
          points.append((x, y))
          undo_stack.clear()  # Clear redo stack on new action
        else:
          print("Maximum of 4 points allowed.")
      elif event == cv2.EVENT_RBUTTONDOWN and points:
        undo_stack.append(points.pop())  # Undo last point

      elif event == cv2.EVENT_MBUTTONDOWN and undo_stack:
        points.append(undo_stack.pop())  # Redo last undone point

      # Redraw the image with updated points
      temp_img = img.copy()
      draw_points(temp_img, points)
      cv2.imshow(windowName, temp_img)

    # Display the image and set the mouse callback
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, 1280, 720)
    cv2.setMouseCallback(windowName, mouse_callback)

    # Show the image and wait for the user to finish
    while True:
      temp_img = img.copy()
      draw_points(temp_img, points)
      cv2.imshow(windowName, temp_img)

      key = cv2.waitKey(1) & 0xFF
      if key == ord('q'):  # Quit on 'q'
        break
      elif key == ord('c'):  # Clear all points on 'c'
        points.clear()
        undo_stack.clear()

    cv2.destroyAllWindows()

    if len(points) == 4:
      # Save the points to the config
      points_str = ';'.join([f"{p[0]},{p[1]}" for p in points])
      self.temp_config.floorplan.points = points_str
      self.saveToConfig(
        section='floorplan',
        fields=['points', 'resolution'],
        success_message="World points saved successfully.",
      )
    else:
      self.showMessageBox(
        title="Error",
        message="Please select exactly 4 points.",
        icon=QtWidgets.QMessageBox.Warning
      )
      return

    # Update the world points value
    self.updateWorldPointsValue()

  def cameraPointsBtnPressed(self):
    corner_points = []
    dragging_point = None

    def click_event(event, x, y, flags, param):
      nonlocal corner_points, dragging_point

      # If left mouse button is clicked, check if it's near a point to start dragging
      if event == cv2.EVENT_LBUTTONDOWN:
        min_dist = float('inf')
        closest_point = None

        for i, point in enumerate(corner_points):
          dist = np.linalg.norm(np.array([x, y]) - np.array(point))
          if dist < min_dist:
            min_dist = dist
            closest_point = i

        # Start dragging if a point is close enough to the click
        if closest_point is not None and min_dist < 10:  # 10 pixels threshold
          dragging_point = closest_point

      # If the mouse is moving and a point is being dragged
      elif event == cv2.EVENT_MOUSEMOVE:
        if dragging_point is not None:
          corner_points[dragging_point] = [x, y]  # Update the dragged point's coordinates

      # If the left mouse button is released, stop dragging
      elif event == cv2.EVENT_LBUTTONUP:
        dragging_point = None  # Stop dragging

    # Load a camera source
    source = self.config.camera.source.text

    # Grab a frame from the source
    cap = cv2.VideoCapture(int(source) if source.isdigit() else source)
    ret, frame = cap.read()
    cap.release()

    if not ret:
      self.showMessageBox(
        title="Camera Error",
        message="Failed to read from camera. Please check the connection.",
        icon=QtWidgets.QMessageBox.Warning
      )
      return

    frame_copy = frame.copy()

    orig_scale_factor = 0.5  # Adjust this value to control the scaling (e.g., 0.5 for half the size)
    scaled_width = int(frame.shape[1] * orig_scale_factor)
    scaled_height = int(frame.shape[0] * orig_scale_factor)
    resized_frame = cv2.resize(frame_copy, (scaled_width, scaled_height), interpolation=cv2.INTER_AREA)

    frame_copy = resized_frame.copy()
    frame_h, frame_w = frame_copy.shape[:2]

    originalWindow = "Select Camera Points"
    transformedWindow = "Transformed Image"

    cv2.namedWindow(originalWindow, cv2.WINDOW_NORMAL)  # Make the window resizable
    cv2.resizeWindow(originalWindow, scaled_width, scaled_height)  # Set the initial size
    cv2.moveWindow(originalWindow, 1000, 0)
    cv2.setMouseCallback(originalWindow, click_event)

    cv2.namedWindow(transformedWindow, cv2.WINDOW_NORMAL)  # Make the window resizable
    cv2.resizeWindow(transformedWindow, scaled_width, scaled_height)  # Set the initial size
    cv2.moveWindow(transformedWindow, 10, 0)

    # Define initial arbitrary corner points for the resized image
    initial_points = [[50, 50], [frame_w - 100, 50], [frame_w - 100, frame_h - 100], [50, frame_h - 100]]
    corner_points = deepcopy(initial_points)

    while True:
      # Show the resized image with the current corner points
      frame_copy = resized_frame.copy()

      # Draw the points and the lines between them
      for i in range(len(corner_points)):
        cv2.circle(frame_copy, tuple(corner_points[i]), 5, (0, 0, 255), -1)
        cv2.circle(frame_copy, tuple(corner_points[i]), 15, (42, 255, 255), 1)

        if i > 0:
          cv2.line(frame_copy, tuple(corner_points[i-1]), tuple(corner_points[i]), (0, 255, 0), 2)

      # Close the rectangle if all 4 points are selected
      cv2.line(frame_copy, tuple(corner_points[3]), tuple(corner_points[0]), (0, 255, 0), 2)

      # Define the source points for perspective transform (resize coordinates accordingly)
      src_points = np.float32(corner_points)

      # Define the destination points (to a square, but this will be adjusted later)
      dst_points = np.float32([[0, 0], [frame_w, 0], [frame_w, frame_h], [0, frame_h]])

      # Compute the perspective transform matrix
      matrix = cv2.getPerspectiveTransform(src_points, dst_points)

      # Transform the corners of the original image to determine output size
      h, w = resized_frame.shape[:2]
      original_corners = np.float32([[0,0], [w,0], [w,h], [0,h]]).reshape(-1,1,2)
      transformed_corners = cv2.perspectiveTransform(original_corners, matrix)

      # Calculate the bounding box of the transformed corners
      x_coords = transformed_corners[:,0,0]
      y_coords = transformed_corners[:,0,1]
      min_x, max_x = np.min(x_coords), np.max(x_coords)
      min_y, max_y = np.min(y_coords), np.max(y_coords)

      # Compute required output size and adjust the matrix to avoid cropping
      output_width = max(w, int(np.ceil(max_x - min_x)))
      output_height = max(h, int(np.ceil(max_y - min_y)))
      adjustment_matrix = np.array([[1, 0, -min_x], [0, 1, -min_y], [0, 0, 1]], dtype=np.float32)
      adjusted_matrix = adjustment_matrix @ matrix

      # Apply the perspective warp with computed output size and padding
      warped_frame = cv2.warpPerspective(resized_frame, adjusted_matrix, (output_width, output_height), borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))

      scale_factor = 0.3  # Adjust this value to control the scaling (e.g., 0.5 for half the size)
      scaled_width = int(warped_frame.shape[1] * scale_factor)
      scaled_height = int(warped_frame.shape[0] * scale_factor)
      scaled_warped_frame = cv2.resize(warped_frame, (scaled_width, scaled_height), interpolation=cv2.INTER_AREA)

      # Show the original image with corner points
      cv2.imshow(originalWindow, frame_copy)

      # Show the warped image
      cv2.resizeWindow(transformedWindow, scaled_width, scaled_height)
      cv2.imshow(transformedWindow, scaled_warped_frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.destroyAllWindows()
    cap.release()

    # Save the points to the config if the corner points are not the initial points
    if corner_points == initial_points:
      self.showMessageBox(
        title="No Changes",
        message="Camera points not updated.",
        icon=QtWidgets.QMessageBox.Information
      )
      return

    original_corner_points = []
    for point in corner_points:
      original_x = int(point[0] / orig_scale_factor)
      original_y = int(point[1] / orig_scale_factor)
      original_corner_points.append((original_x, original_y))

    points_str = ';'.join([f"{p[0]},{p[1]}" for p in original_corner_points])
    self.temp_config.camera.points = points_str

    original_resolution = f"{frame.shape[1]},{frame.shape[0]}"  # width,height
    self.temp_config.camera.resolution = original_resolution

    self.saveToConfig(
      section='camera',
      fields=['points', 'resolution'],
      success_message="Camera points saved successfully.",
    )

    self.updateCameraPointsValue()

  def updateWorldPointsValue(self):
    points = self.temp_config.floorplan.points.text.split(';')
    points_str = ', '.join([f"({p})" for p in points])
    self.ui.worldPointsValue.setText(f'[{points_str}]')

  def updateCameraPointsValue(self):
    points = self.temp_config.camera.points.text.split(';')
    points_str = ', '.join([f"({p})" for p in points])
    self.ui.cameraPointsValue.setText(f'[{points_str}]')

  def intelligent_resize(self, frame, target_width, target_height):
    # Use INTER_AREA for downscaling (best quality for size reduction)
    return cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)

  def startMonitoringPressed(self):
    floorplanWindow = 'Floor Plan Heatmap and Camera Feed'

    full_w, full_h = QtWidgets.QApplication.primaryScreen().availableGeometry().getRect()[2:]

    cv2.namedWindow(floorplanWindow, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(floorplanWindow, full_w, full_h)
    cv2.setWindowProperty(floorplanWindow, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

    # Function to enhance contrast (adaptive)
    def enhance_contrast_adaptive(frame):
      """Applies adaptive histogram equalization to enhance contrast."""
      ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
      y, cr, cb = cv2.split(ycrcb)
      clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
      y_eq = clahe.apply(y)
      ycrcb_eq = cv2.merge([y_eq, cr, cb])
      return cv2.cvtColor(ycrcb_eq, cv2.COLOR_YCrCb2BGR)

    # Function to apply gamma correction
    def apply_gamma_correction(image, gamma=1.5):
      """Applies gamma correction to the input image."""
      inv_gamma = 1.0 / gamma
      table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(256)]).astype("uint8")
      return cv2.LUT(image, table)

    # Function to detect low lit areas by gray thresholding
    def is_night_scene(frame, threshold=60):
      """Determines if the scene is likely a night scene based on average brightness."""
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      return np.mean(gray) < threshold

    # Function to generate proximity density heatmap
    def generate_proximity_density_heatmap(points, shape, kernel_size=75, sigma=20, base_intensity=0.5):
      """
      Generates a density heatmap where overlapping kernels from nearby people accumulate intensity.
      """
      heatmap = np.zeros(shape[:2], dtype=np.float32)

      # Create a base Gaussian kernel
      ax = np.linspace(-(kernel_size // 2), kernel_size // 2, kernel_size)
      xx, yy = np.meshgrid(ax, ax)
      kernel = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
      kernel = (kernel / kernel.max()) * base_intensity

      k_half = kernel_size // 2
      h, w = shape[:2]

      for y, x in points:
          # Calculate initial slice coordinates
          x1, x2 = int(x - k_half), int(x + k_half + (1 if kernel_size % 2 == 1 else 0))
          y1, y2 = int(y - k_half), int(y + k_half + (1 if kernel_size % 2 == 1 else 0))

          # Calculate kernel slice indices
          kx1 = max(0, -x1)
          ky1 = max(0, -y1)
          kx2 = kernel_size - max(0, x2 - w)
          ky2 = kernel_size - max(0, y2 - h)

          # Calculate heatmap slice indices
          x1 = max(0, x1)
          y1 = max(0, y1)
          x2 = min(w, x2)
          y2 = min(h, y2)

          # Ensure slices have same dimensions
          slice_width = x2 - x1
          slice_height = y2 - y1
          kernel_width = kx2 - kx1
          kernel_height = ky2 - ky1

          # If dimensions don't match, adjust them
          if slice_width != kernel_width:
              if x2 < w:  # Can extend right
                  x2 = x1 + kernel_width
              else:  # Must reduce kernel
                  kx2 = kx1 + slice_width

          if slice_height != kernel_height:
              if y2 < h:  # Can extend down
                  y2 = y1 + kernel_height
              else:  # Must reduce kernel
                  ky2 = ky1 + slice_height

          # Only add if the resulting slice has a positive area
          if (y2 > y1) and (x2 > x1) and (ky2 > ky1) and (kx2 > kx1):
              try:
                  heatmap[y1:y2, x1:x2] += kernel[ky1:ky2, kx1:kx2]
              except ValueError as e:
                  # For debugging
                  print(f"Shape mismatch: heatmap[{y1}:{y2}, {x1}:{x2}] shape {(y2-y1, x2-x1)} vs kernel[{ky1}:{ky2}, {kx1}:{kx2}] shape {(ky2-ky1, kx2-kx1)}")
                  continue

      heatmap = np.clip(heatmap, 0, 1)
      heatmap = (heatmap * 255).astype(np.uint8)
      return cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Load points
    camera_points = self.temp_config.camera.points.text.split(';')
    camera_points = [tuple(map(int, p.split(','))) for p in camera_points]
    camera_points = np.array(camera_points)

    world_points = self.temp_config.floorplan.points.text.split(';')
    world_points = [tuple(map(int, p.split(','))) for p in world_points]
    world_points = np.array(world_points)

    # Load floor plan image
    floorplan_img = cv2.imread(self.config.floorplan.image.text)
    if floorplan_img is None:
      self.showMessageBox(
        title="Image Error",
        message="Failed to load the image. Please check the file path.",
        icon=QtWidgets.QMessageBox.Warning
      )
      return

    # Load camera source
    source = self.config.camera.source.text
    if source is None:
      self.showMessageBox(
        title="Camera Error",
        message="Failed to load the camera source. Please check the configuration.",
        icon=QtWidgets.QMessageBox.Warning
      )
      return

    cap = cv2.VideoCapture(int(source) if source.isdigit() else source)
    if not cap.isOpened():
      self.showMessageBox(
        title="Camera Error",
        message="Failed to open the camera. Please check the connection.",
        icon=QtWidgets.QMessageBox.Warning
      )
      return

    # OPTIMIZATION: Get original camera resolution and setup scaling
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Original camera resolution: {original_width}x{original_height}")

    # Define target resolution for YOLO processing (balance between speed and accuracy)
    TARGET_WIDTH = 1280
    TARGET_HEIGHT = 720

    # Calculate scale factors
    scale_x = TARGET_WIDTH / original_width
    scale_y = TARGET_HEIGHT / original_height
    scale = min(scale_x, scale_y)  # Use uniform scaling to maintain aspect ratio

    # Calculate actual resize dimensions
    resize_width = int(original_width * scale)
    resize_height = int(original_height * scale)

    print(f"Processing resolution: {resize_width}x{resize_height}")
    print(f"Scale factor: {scale:.3f}")

    scaled_reso_str = f'{resize_width},{resize_height}'
    self.temp_config.model.scaledresolution = scaled_reso_str
    self.temp_config.model.scalefactor = f'{scale:.3f}'

    self.saveToConfig(
      section='camera',
      fields=['scaledresolution', 'scalefactor'],
      success_message="Scaled resolution saved successfully."
    )

    # Scale camera points to match resized image
    src_points_scaled = camera_points * scale

    # Get homography matrices
    H_scaled = cv2.findHomography(src_points_scaled, world_points)[0]  # For scaled processing
    H_original = cv2.findHomography(camera_points, world_points)[0]    # For original warping

    if H_scaled is None or H_original is None:
      self.showMessageBox(
        title="Homography Error",
        message="Failed to compute homography. Please check the points.",
        icon=QtWidgets.QMessageBox.Warning
      )
      return

    print("Homography matrices calculated for both original and scaled coordinates")

    # Load AI Model
    model_path = self.config.model.path.text
    ai = YOLO(model_path)

    # Save scaled homography to config for reference
    if H_original is not None:
      H_str = ';'.join(map(str, H_original.flatten()))
      self.temp_config.model.homography = H_str  # Update main config

      # Immediately save to config
      self.saveToConfig(
        section='model',
        fields=['homography'],
        success_message="Homography saved successfully."
      )

    # Save scaled homography to config for reference
    if H_scaled is not None:
      H_scaled_str = ';'.join(map(str, H_scaled.flatten()))
      self.temp_config.model.scaledhomography = H_scaled_str  # Update main config

      # Immediately save to config
      self.saveToConfig(
        section='model',
        fields=['scaledhomography'],
        success_message="Scaled homography saved successfully."
      )

    print(f"Scaled Homography matrix: {H_scaled}")

    paused = False
    frame_count = 0

    print("Starting optimized monitoring...")
    print("Press 'p' to pause/resume, 'q' to quit")

    while True:
      key = cv2.waitKey(1) & 0xFF

      if key == ord('q') or cv2.getWindowProperty(floorplanWindow, cv2.WND_PROP_VISIBLE) < 1:
          print('Exiting monitoring...')
          break

      if key == ord('p'):
          paused = not paused
          print('Monitoring paused.' if paused else 'Monitoring resumed.')
          continue

      if paused:
          continue  # Skip processing, but still allow quitting or unpausing

      # Frame processing
      ret, frame = cap.read()
      if not ret:
          self.showMessageBox(
              title="Camera Error",
              message="Failed to read from camera. Please check the connection.",
              icon=QtWidgets.QMessageBox.Warning
          )
          break

      # OPTIMIZATION: Resize frame for YOLO processing
      frame_resized = self.intelligent_resize(frame, resize_width, resize_height)

      floor_display = floorplan_img.copy()

      # Apply enhancements to resized frame
      enhanced = enhance_contrast_adaptive(frame_resized)
      if is_night_scene(enhanced):
          enhanced = apply_gamma_correction(enhanced, gamma=1.8)  # brighten for night

      # YOLO processing on resized frame
      result = ai(enhanced, classes=0) # Add device=0 if GPU available

      # Create annotated frame for display (scale back up for visualization)
      annotated_resized = result[0].plot()
      # Scale annotated frame back to original size for display
      annotated = cv2.resize(annotated_resized, (original_width, original_height), interpolation=cv2.INTER_LINEAR)

      transformed_points = []

      # Process detections using scaled homography
      for r in result:
        keypoints = r.keypoints
        if keypoints is not None:
          # Extract keypoints data
          kpts = keypoints.data  # Shape: [batch, num_keypoints, 3] where 3 is [x, y, confidence]

          for person_kpts in kpts:
            # COCO keypoint indices for hips
            # 11: left hip, 12: right hip
            left_hip = person_kpts[0]   # [x, y, confidence] // 0 and 1 from the custom model
            right_hip = person_kpts[1]  # [x, y, confidence]

            # Check if both hips are detected (confidence > threshold)
            confidence_threshold = 0.5
            if left_hip[2] > confidence_threshold and right_hip[2] > confidence_threshold:
              # Calculate center point between the two hips
              x_center = int((left_hip[0] + right_hip[0]) / 2)
              y_center = int((left_hip[1] + right_hip[1]) / 2)

              # Use scaled homography for transformation
              src_pt = np.array([[[x_center, y_center]]], dtype=np.float32)
              dst_pt = cv2.perspectiveTransform(src_pt, H_scaled)[0][0]
              fx, fy = int(dst_pt[0]), int(dst_pt[1])

              transformed_points.append((fy, fx)) # Note the order (y, x) for heatmap generation
              cv2.circle(floor_display, (fx, fy), 8, (0, 0, 255), -1)

              # For annotation, scale detection back to original coordinates
              x_center_orig = int(x_center / scale)
              y_center_orig = int(y_center / scale)
              cv2.circle(annotated, (x_center_orig, y_center_orig), 8, (0, 0, 255), -1)

            # Optional: Handle case where only one hip is detected
            elif left_hip[2] > confidence_threshold:
              x_center, y_center = int(left_hip[0]), int(left_hip[1])

              src_pt = np.array([[[x_center, y_center]]], dtype=np.float32)
              dst_pt = cv2.perspectiveTransform(src_pt, H_scaled)[0][0]
              fx, fy = int(dst_pt[0]), int(dst_pt[1])

              transformed_points.append((fy, fx))
              cv2.circle(floor_display, (fx, fy), 6, (0, 255, 255), -1)  # Yellow for single hip

              x_center_orig = int(x_center / scale)
              y_center_orig = int(y_center / scale)
              cv2.circle(annotated, (x_center_orig, y_center_orig), 6, (0, 255, 255), -1)

            elif right_hip[2] > confidence_threshold:
              x_center, y_center = int(right_hip[0]), int(right_hip[1])

              src_pt = np.array([[[x_center, y_center]]], dtype=np.float32)
              dst_pt = cv2.perspectiveTransform(src_pt, H_scaled)[0][0]
              fx, fy = int(dst_pt[0]), int(dst_pt[1])

              transformed_points.append((fy, fx))
              cv2.circle(floor_display, (fx, fy), 6, (0, 255, 255), -1)  # Yellow for single hip

              x_center_orig = int(x_center / scale)
              y_center_orig = int(y_center / scale)
              cv2.circle(annotated, (x_center_orig, y_center_orig), 6, (0, 255, 255), -1)

        # Keep existing box processing as fallback
        boxes = r.boxes
        if boxes is not None and keypoints is None:  # Only use boxes if no keypoints available
          for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x_center = int((x1 + x2) / 2)
            y_center = int((y1 + y2) / 2)

            # Use scaled homography for transformation
            src_pt = np.array([[[x_center, y_center]]], dtype=np.float32)
            dst_pt = cv2.perspectiveTransform(src_pt, H_scaled)[0][0]
            fx, fy = int(dst_pt[0]), int(dst_pt[1])

            transformed_points.append((fy, fx)) # Note the order (y, x) for heatmap generation
            cv2.circle(floor_display, (fx, fy), 8, (0, 0, 255), -1)

            # For annotation, scale detection back to original coordinates
            x_center_orig = int(x_center / scale)
            y_center_orig = int(y_center / scale)
            cv2.circle(annotated, (x_center_orig, y_center_orig), 8, (0, 0, 255), -1)

      # Adjust these parameters to control the heatmap appearance
      kernel_size = 101
      sigma = 25.2

      density_map = generate_proximity_density_heatmap(transformed_points, floor_display.shape, kernel_size=kernel_size, sigma=sigma)
      blended = cv2.addWeighted(floor_display, 0.7, density_map, 0.3, 0)

      annotated_resized = cv2.resize(annotated, (blended.shape[1], blended.shape[0]))
      combined_display = np.concatenate((blended, annotated_resized), axis=1)
      cv2.imshow(floorplanWindow, combined_display)

      frame_count += 1

      # Print performance info every 60 frames
      if frame_count % 60 == 0:
          print(f"Processed {frame_count} frames with optimization")

    cap.release()
    cv2.destroyAllWindows()

  def cleanup(self):
    print('Cleaning up...')
    cv2.destroyAllWindows()
    self.modal_window.close()
    self.close()
    print('Clean up done...')

def run(app, window):
  ret_code = app.exec_()
  window.cleanup()
  return ret_code

def main():
  try:
    app = QApplication(sys.argv)
    window = MainWindow(config=config)
    window.show()
    sys.exit(run(app, window))

  except KeyboardInterrupt:
    print('Keyboard interrupt detected. Exiting...')
    window.cleanup()
    sys.exit(0)

if __name__ == '__main__':
  main()
