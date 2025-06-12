# Birdview

Human crowd density visualization from camera feed to floor plan.

## Getting Started

To get started, create a new Python virtual environment by running the script:

```bash
$ python -m venv .venv
```

> This will create a folder to contain Python packages and scripts specific to this project

Activate the virtual environment:

```bash
$ /.venv/Scripts/activate
```

Install the dependencies:

```bash
$ (.venv) pip install -r requirements.txt
```

## Usage

Run the main application:
```
$ (.venv) python main.py
```

## FAQ

1. **How do I use an `mp4` file?** <br />
  Open the `config.xml` file and change `camera > source` value to your file path.

2. **Key points out of bounds error** <br />
  The application has initially set the key points indices to be `left_hip = person_kpts[0]` and `right_hip = person_kpts[1]`.

  > See line 1177 and 1178.

3. **How do I use the GPU?** <br />
  Make sure you have the NVIDIA drivers for PyTorch to identify your graphics processing unit. Set `device=0` (if you only have on graphics card), in `result = ai(enhanced, classes=0, device=0)`.

  > See line 1158.

## Feedback

For bugs and errors, please file an issue [here](https://github.com/shnmyklsnc/birdview/issues) or contact [shnmyklsnc@gmail.com](mailto:shnmyklsnc@gmail.com).
