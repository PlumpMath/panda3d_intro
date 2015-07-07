from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from math import pi, sin, cos
import sys


class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        # self.environ is now a NodePath, or a handler for the node (the actual model)
        # could load the same model several times with different NodePaths
        print('NodePath', self.environ)
        print('Node', self.environ.node())
        # Reparent the NodePath to render, so the engine knows to show it in the scene.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the NodePath.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)
        # disable the mouse so it does not interfere with camera
        base.disableMouse()
        # set up some keyboard input
        self.accept("escape", sys.exit)  # Escape quits
        self.accept("space", self.toggle_camera_spin)  # spacebar
        
        # set up a variable to keep track of camera toggle
        self.spin_camera = True
        # variable to keep track of total time spinning
        self.spin_time = 0
        # go ahead and start camera spinning
        self.toggle_camera_spin()

    def toggle_camera_spin(self):
        if self.spin_camera:
            self.spin_task = self.taskMgr.add(self.spin_camera_task, "SpinCameraTask")
            # set up task variable to use to determine dt
            self.spin_task.last = 0
        else:
			self.taskMgr.remove("SpinCameraTask")
        self.spin_camera = not self.spin_camera
        
    def spin_camera_task(self, task):
        # Define a method to move the camera.
        dt = task.time - task.last
        task.last = task.time
        self.spin_time += dt
        angle_degrees = self.spin_time * 6.0
        angle_radians = angle_degrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angle_radians), -20.0 * cos(angle_radians), 3)
        self.camera.setHpr(angle_degrees, 0, 0)
        return task.cont

if __name__ == "__main__":
    app = MyApp()
    app.run()
