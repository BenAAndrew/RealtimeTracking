# RealtimeTracking

Real time face tracking for webcam/Raspberry Pi with feedback to motors for pan & tilt control

## Face tracking setup

### Raspberry Pi
1. Enable Raspberry Pi camera in Configuration->Interfaces
2. [Install Python & OpenCV](https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/) 
3. Install the requirements by running `pip install -r requirements_raspberrypi.txt`
4. Run the app with `python3 main.py -m raspberrypi`

### PC & Webcam
1. [Install Python](https://www.python.org/downloads/)
2. Install the requirements by running `pip install -r requirements_webcam.txt`
3. Run the app with `python main.py -m webcam`

### Optional arguments
- `--arduino_port`: Port for arduino connection
- `--arduino_baudrate`: Arduino baudrate
- `--haarcascade_path`: Path to Haar cascade classifier file (xml)
- `--min_face_scale`: Minimum face size relative to video size (percentage). Using smaller values decreases performance. Default is 30%
- `--preview`: Whether to show the video stream (on by default)
- `--draw_box`: Whether to draw a box around the face (on by default)
- `--fps`: Whether to show fps counter (off by default)

You can add these arguments onto the `main.py` (i.e. `python3 main.py -m rasperrypi --fps 1`)

## Motor control setup
1. Upload `motorcontrol.ino` to your arduino
2. Add the port and baudrate to the `main.py` command (i.e. `python3 main.py -m rasperrypi -a COM3 -b 9600`)
