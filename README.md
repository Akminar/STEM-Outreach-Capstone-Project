# Digital Twin - STEM Outreach Project

## Overview
This repository contains the code, models, and documentation for the Digital Twin STEM Outreach project. The project includes an Arduino-based magnet detection system that interacts with a virtual representation of a rotating system using VTK.

## Repository Structure

### Code
- **arduino/**
  - `detect_magnet.ino`: Uses a Hall Effect sensor to detect magnets and convert detections into RPM values for the digital twin.
  - `magnet_test.ino`: Tests whether a magnet is detected by the Hall Effect sensor.
- **digital_twin/**
  - `dt_match.py`: The main application, which runs the digital twin by connecting to an Arduino or using a simulated serial port.
  - `dt_turbine.py`: Uses VTK to display and rotate the models at a specified RPM.
  - `simulate_rpm.py`: Simulates a serial port and randomly generates RPM values.
  - `dynamic_base.stl`: STL model of the rotating part of the digital twin (generator, shaft, gear, and turbine).
  - `static_base.stl`: STL model of the stationary part of the digital twin.

### Documents
- Contains project documentation, instructions, and setup guides.

### Images
- **3D_prints/**: Images of 3D-printed parts.
- **diagrams/**: Diagrams of hydroelectric components.
- **measurements/**: Images of Nick’s model with associated measurements.
- **models/**: Images of 3D models designed for this project.

### Weekly Update Slides
- Contains slides from project update meetings.

### Models
- **blend_files/**: Blender files for all 3D models.
- **glb_files_for_ppt/**: GLB files used in presentations.
- **stl_files/**: STL files for 3D printing or visualization.
- **Turntable, 18cm, marble bearings - 2763216**: Turntable sourced from Thingiverse, licensed under Creative Commons.

---
## Installation and Setup

### Model Setup
The following models are required for the system:
| Model Name | Dimensions (X-Y-Z) | Layer Height |
|------------|--------------------|--------------|
| generator_support_yoke | 127-127-57.2 mm | 0.24mm |
| magnetic_pole_v1 | 215.9-215.9-63.5 mm | 0.2mm |

- The generator slides onto the shaft and should be secured to the turntable (hot glue recommended).
- The magnetic pole slides into place on the generator.

### Arduino Setup
1. **Breadboard Wiring**
   - Connect **VCC** to **5V**
   - Connect **GND** to **GND**
   - Connect **DAT** to **pin 2**
   - Insert a **10k resistor** between **VCC and DAT**

   > The Hall Effect sensor must be placed close to the neodymium magnets.

2. **Attach Neodymium Magnets**
   - Each prong of the gear should have a neodymium magnet attached.
   - If the number of prongs changes, update the `magnetsPerRevolution` value in `detect_magnet.ino`.
   - The **direction of the magnet matters**! Use `magnet_test.ino` to verify detection.

3. **Mounting the Arduino**
   - Attach the Arduino securely to the base (hot glue or rubber bands recommended).
   - Position the **Hall Effect sensor** as close as possible to the magnets.

---
## Running the Application

### Testing
#### 1. Test Magnet Detection
- Open `magnet_test.ino` in the **Arduino IDE (version 2.3.4)**.
- Upload `magnet_test.ino` to the Arduino.
- Hold a magnet near the Hall Effect Sensor:
  - **"Magnet detected!"** → Sensor is working.
  - **"No magnet detected."** → Adjust magnet position.

#### 2. Test Python Application with a Virtual Serial Port
- **Install `socat`**
  ```sh
  brew install socat
  ```
- **Create a virtual serial port**
  ```sh
  socat -d -d pty,raw,echo=0 pty,raw,echo=0
  ```
- This will generate **two serial ports** (e.g., `/dev/ttys003` and `/dev/ttys004`).
- **Assign ports in the code:**
  - Set the first port in `dt_match.py` (`SERIAL_PORT`)
  - Set the second port in `simulate_rpm.py` (`SIMULATED_PORT`)

- **Run the simulation:**
  ```sh
  python simulate_rpm.py &
  python dt_match.py
  ```
  - `dt_match.py` will read the generated RPM values and visualize rotation using VTK.

### Running with a Real Arduino
- **Find the correct serial port**:
  ```sh
  ls /dev/tty.*
  ```
- **Update `dt_match.py` to use the correct port**:
  ```python
  SERIAL_PORT = "/dev/ttyUSB0"  # Change this to match your system
  ```
- **Run the application:**
  ```sh
  python dt_match.py
  ```

---
## License
This project includes models and code licensed under **Creative Commons** and open-source licenses. See `LICENSE` for details.

## Contributors
- **Alea Minar** - CS410 Capstone Project (STEM Outreach) - March 19, 2025

---
For any issues or questions, please create an issue in the repository or contact the contributors.

