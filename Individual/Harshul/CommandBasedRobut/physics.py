from pyfrc.physics import tankmodel
from pyfrc.physics import drivetrains
from pyfrc.physics import motor_cfgs
from pyfrc.physics.units import units
from subsystems import Drive


class PhysicsEngine: # Nothing works yet
    def __init__(self, controller):
        self.controller = controller
        self.drivetrain = self.drivetrain = drivetrains.FourMotorDrivetrain(deadzone=drivetrains.linear_deadzone(0.05))
        self.deadZone = 0.05

    def update_sim(self, hal_data, now, tm_diff): # Nothing has worked yet.
        #speed, rotation = self.drivetrain.get_vector(1, 1)
        #self.physics_controller.drive(speed, rotation, tm_diff)
        pass
