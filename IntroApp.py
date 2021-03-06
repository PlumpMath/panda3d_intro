from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, LVector3, KeyboardButton
from math import pi, sin, cos
import sys


class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        # self.environ is now a NodePath, or a handler for the node (the actual model)
        # could load the same model several times with different NodePaths
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

        # Load and transform the panda actor.
        self.panda_actor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.panda_actor.setScale(0.005, 0.005, 0.005)
        self.panda_actor.reparentTo(self.render)
        # Loop the animation.
        self.panda_actor.loop("walk")

        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        panda_pos_interval1 = self.panda_actor.posInterval(13,
                                                        Point3(0, -10, 0),
                                                        startPos=Point3(0, 10, 0))
        panda_pos_interval2 = self.panda_actor.posInterval(13,
                                                        Point3(0, 10, 0),
                                                        startPos=Point3(0, -10, 0))
        panda_hpr_interval1 = self.panda_actor.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr=Point3(0, 0, 0))
        panda_hpr_interval2 = self.panda_actor.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr=Point3(180, 0, 0))

        # Create and play the sequence that coordinates the intervals.
        self.panda_pace = Sequence(panda_pos_interval1,
                                  panda_hpr_interval1,
                                  panda_pos_interval2,
                                  panda_hpr_interval2,
                                  name="pandaPace")
        self.panda_pace.loop()

        # Add a smiley for fun.
        self.smiley = self.loader.loadModel("models/smiley")
        self.smiley.setPos(0, 0, 1)
        self.smiley.reparentTo(self.render)

        # velocity adjustment
        self.vel_base = 3
        # add task to allow smiley movement
        self.taskMgr.add(self.game_loop_task, "GameLoop")

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

    def game_loop_task(self, task):
        dt = globalClock.getDt()
        velocity = self.poll_keyboard()
        # print velocity
        self.move_smiley(dt, velocity)
        return task.cont

    def poll_keyboard(self):
        x_speed = 0.5
        y_speed = 0.5
        velocity = LVector3(0)
        # poorly named, checks keyboard, not mouse, in this case
        is_down = base.mouseWatcherNode.is_button_down
        if is_down(KeyboardButton.up()):
            velocity.y += y_speed
        if is_down(KeyboardButton.down()):
            velocity.y -= y_speed
        if is_down(KeyboardButton.left()):
            velocity.x -= x_speed
        if is_down(KeyboardButton.right()):
            velocity.x += x_speed
        return velocity

    def move_smiley(self, dt, velocity):
        # print 'velocity', self.velocity
        # this makes for smooth (correct speed) diagonal movement
        # print 'velocity', self.velocity
        magnitude = max(abs(velocity[0]), abs(velocity[1]))
        move = None
        if velocity.normalize():
            velocity *= magnitude
            move = velocity * self.vel_base * dt
            # this makes for smooth movement
            self.smiley.setFluidPos(self.smiley, move)
        return move


if __name__ == "__main__":
    app = MyApp()
    app.run()
