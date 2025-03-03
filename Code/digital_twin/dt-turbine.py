import vtk
import threading

# Names of files
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
rotation_speed = 1  # Default rotation speed

# Function to update the rotation
def rotate_model(obj, event):
    global angle
    angle += rotation_speed  # Increment angle by the set speed
    transform.Identity()  # Reset transform
    transform.RotateY(angle)  # Apply rotation around Y-axis
    actors[0].SetUserTransform(transform)  # Update actor with new transform
    renderWindow.Render()  # Refresh window

# Function to allow user input for rotation speed
def input_rotation_speed():
    global rotation_speed
    while True:
        try:
            speed = float(input("Enter rotation speed: "))
            rotation_speed = max(0, speed)  # Ensure non-negative speed
        except ValueError:
            print("Invalid input. Please enter a number.")

# Start a thread to handle user input without blocking VTK
input_thread = threading.Thread(target=input_rotation_speed, daemon=True)
input_thread.start()

# Set up the interactor to update rotation on a timer
renderWindowInteractor.Initialize()
renderWindowInteractor.AddObserver('TimerEvent', rotate_model)
renderWindowInteractor.CreateRepeatingTimer(10)  # 10 ms interval

# Start interaction
renderWindow.Render()
renderWindowInteractor.Start()
