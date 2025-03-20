import vtk
import serial
import threading
import time

# Serial Port Configuration (Change this to match your device)
SERIAL_PORT = "/dev/ttys004"  # Replace with correct port, e.g., "/dev/ttys004" for macOS
BAUD_RATE = 115200

# STL Files
filenames = ["dynamic_base_turbine.stl", "static_base_turbine.stl"]

# Read the STL file
actors = []
for name in filenames:
    reader = vtk.vtkSTLReader()
    reader.SetFileName(name)

    # Create a mapper for the STL data
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Create an actor for the STL model
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actors.append(actor)

# Create axes and set their length
axes = vtk.vtkAxesActor()
axes.SetTotalLength(100, 100, 100)

# Create a renderer, render window, and interactor
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(2000, 2000)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

for actor in actors:
    # Add the actor and axes to the scene
    renderer.AddActor(actor)

# Set background color
renderer.SetBackground(1, 1, 1)

# Create a transform to handle rotation
transform = vtk.vtkTransform()

# Initialize rotation speed and angle
angle = 0
rotation_speed = 0  # Start with zero speed

# Function to read rotation speed from serial
def read_serial():
    global rotation_speed
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
    except serial.SerialException:
        print(f"Failed to connect to {SERIAL_PORT}. Running without serial input.")
        return

    while True:
        if ser.in_waiting > 0:
            try:
                rpm = float(ser.readline().decode().strip())
                rotation_speed = (rpm * 360) / 60  # Convert RPM to degrees per second
                print(f"Received RPM: {rpm}, Rotation Speed: {rotation_speed}°/s")
            except ValueError:
                print("Invalid data received from serial.")
        time.sleep(0.1)  # Avoid CPU overload

# Function to update the rotation
def rotate_model(obj, event):
    global angle
    angle += rotation_speed / 30  # Convert speed to frame rate (30 FPS)
    transform.Identity()  # Reset transform
    transform.RotateY(angle)  # Apply rotation around Y-axis
    actors[0].SetUserTransform(transform)  # Update actor with new transform
    renderWindow.Render()  # Refresh window

# Start a thread to read serial data
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

# Set up the interactor to update rotation on a timer
renderWindowInteractor.Initialize()
renderWindowInteractor.AddObserver('TimerEvent', rotate_model)
renderWindowInteractor.CreateRepeatingTimer(33)  # ~30 FPS

# Start interaction
renderWindow.Render()
renderWindowInteractor.Start()
