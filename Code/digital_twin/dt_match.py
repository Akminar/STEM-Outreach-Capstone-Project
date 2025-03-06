import vtk
import serial
import time
import argparse

class DigitalTwin:
    def __init__(self, port_name = "/dev/ttyUSB0", baud_rate = 115200, filenames = None, testing_mode = False):
        self.port_name = "dev/ttyS0" if testing_mode else port_name
        self.baud_rate = baud_rate
        self.filenames = filenames if filenames else ["dynamic_base_turbine.stl", "static_base_turbine.stl"]
        self.testing_mode = testing_mode

        # Initialize Arduino communication
        self.ser = self.init_serial_connection()

        # Initialize rotation speed
        self.rotation_speed = 0

        # Initialize vtk components
        self.actors = self.load_stl_files()
        self.renderer, self.render_window, self.render_interactor = self.setup_renderer()

        # Start rendering loop
        self.start_rendering()

    def init_serial_connection(self):
        try:
            ser = serial.Serial(self.port_name, self.baud_rate, timeout = 1)
            mode = "TESTING MODE (simulate_rpm.py" if self.testing_mode else "REAL MODE (Arduino)"
            print(f"Connected to Arduino through {self.port_name} ({mode})")
            return ser
        except serial.SerialException:
            print(f"Failed to connect to {self.port_name}. Running without serial information")
            return None

    def load_stl_files(self):
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
        return actors

    def setup_renderer(self):
        renderer = vtk.vtkRenderer()
        render_window = vtk.vtkRenderWindow()
        render_window.SetSize(2000, 2000)
        render_window.AddRenderer(renderer)
        render_interactor = vtk.vtkRenderWindowInteractor()
        render_interactor.SetRenderWindow(render_window)

        for actor in self.actors:
            # Add the actor and axes to the scene
            renderer.AddActor(actor)

        # Set background color
        renderer.SetBackground(1, 1, 1)

        return renderer, render_window, render_interactor

    def update_rotation(self, obj, event):
        if self.ser and self.ser.in_waiting > 0:
            try:
                rpm = float(self.ser.readline().decode().strip())
                rotation_speed = (rpm * 360) / 60 # Degrees per second conversion
            except ValueError:
                pass
    
        # Update rotation
        self.actors[0].RotateY(rotation_speed / 30) # 30 FPS
        self.render_window.Render()
        self.render_interactor.CreateRepeatingTimer(33)

    def start_rendering(self):
        self.render_interactor.Initialize()
        self.render_interactor.AddObserver('TimerEvent', self.update_rotation)
        self.render_window.Render()
        self.render_interactor.Start()


if __name__ == "__main__":
    # Names of model files
    filenames = ["dynamic_base_turbine.stl", "static_base_turbine.stl"]

    parser = argparse.ArgumentParser(description = "Running the DT in testing mode")
    parser.add_argument("--test", action = "store_true", help = "Enable testing mode with a fake serial port")
    args = parser.parse_args()

    digital_twin = DigitalTwin(port_name = "/dev/ttyUSB0", filenames = filenames, testing_mode = args.test)


