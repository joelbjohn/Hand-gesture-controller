 ![](Hand-gesture-controller/WhatsApp Video 2026-05-17 at 16.49.49.mp4)
 
 # Hand-gesture-controller

This project allows you to control forza horizon or any racing games which support xbox controller using hand gestures via your webcam. By leveraging **MediaPipe** for hand tracking and **vgamepad** for Xbox 360 controller emulation, your hands effectively become a virtual gamepad.



## 🎮 How it Works

The script detects two hands and maps their movement to specific controller inputs:

* **Right Hand (Triggers):** * Measures the distance between your **Thumb tip (4)** and **Index tip (8)**.
    * Horizontal distance maps to the **Right Trigger** (Acceleration).
    * Vertical distance maps to the **Left Trigger** (Brake/Reverse).
    * So pinch and widen horizontally for acceleration and vertically for brake
* **Left Hand (Steering):**
    * Calculates the angle between your **Wrist (0)** and **Thumb tip (4)**.
    * Maps the angle to the **Left Joystick (X-axis)** for steering left or right.
    * Make a thumps up facing the camera and rotate the wrist 90 degrees left or right for steering

## 🛠️ Installation & Setup

### 1. Prerequisites
* **Python:** Version 3.10 or higher (Check `.python-version` for exact version).
* **ViGEmBus Driver:** Required for `vgamepad` to work on Windows. [Download it here](https://github.com/ViGEm/ViGEmBus/releases). Do this after pip install vgamepad alone isnt working. Im not sure about this step and it worked for me with just pip install

### 2. Create Virtual Environment
Open your terminal in the project folder and run:
```bash
python -m venv .venv
```

### 3. Activate environment
Open your terminal in the project folder and run:
```bash
.venv\Scripts\activate
```

### 4. Install dependencies
Open your terminal in the project folder and run:
```bash
pip install -r requirements.txt
```

### 5. Run
Open your terminal in the project folder and run:
```bash
python Together1.py
```
Together1.py depends on HandTrackingModule.py, the other codes i made to test the libraries and controlls.
