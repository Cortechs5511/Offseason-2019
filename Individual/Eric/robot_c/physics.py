from pyfrc.physics import tankmodel
from pyfrc.physics import drivetrains
from pyfrc.physics import motor_cfgs
from pyfrc.physics.units import units
from subsystems import Drive


class PhysicsEngine: # Nothing works yet
    def __init__(self, controller):
        self.controller = controller
        self.drivetrain = tankmodel.TankModel.theory(motor_cfgs.MOTOR_CFG_MINI_CIM,
                                                     robot_mass= 125 * units.lbs, # using some example units
                                                     gearing = 9, nmotors = 6,
                                                     x_wheelbase = 3.0 * units.feet,
                                                     wheel_diameter = 6 * units.inch)
        self.deadZone = 0.1

    def update_sim(self, hal_data, now, tm_diff):
        '''
        lr_motor = hal_data["pwm"][10]["value"]
        rr_motor = hal_data["pwm"][20]["value"]

        x, y, angle = self.drivetrain.get_distance(lr_motor, rr_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)
        '''
        pass
