from pyfrc.physics import tankmodel
from pyfrc.physics import motor_cfgs
from pyfrc.physics.units import units
class PhysicsEngine:
    def __init__(self, physics_controller):
        self.physics_controller = physics_controller
        self.drivetrain = tankmodel.TankModel.theory(motor_cfgs.MOTOR_CFG_MINI_CIM,
                                                     robot_mass= 105 * units.lbs, # using some example units
                                                     gearing = 9, nmotors = 4,
                                                     x_wheelbase = 3.0 * units.feet,
                                                     wheel_diameter = 4 * units.inch)
        '''self.drivetrain = tankmodel.TankModel.theory(motor_cfgs.MotorModelConfig(name='NEO',
         nominalVoltage = (12, 'volt'),
         freeSpeed=(5676, 'counts_per_minute'),
         freeCurrent=(1.8, 'ampere'),
         stallTorque=(2.6, 'N_m'),
         stallCurrent=(105, 'ampere')),
             robot_mass= 105 * units.lbs, # using some example units
             gearing = 9, nmotors = 4,
             x_wheelbase = 3.0 * units.feet,
             wheel_diameter = 4 * units.inch'''
        self.deadZone = 0.05

    def update_sim(self, hal_data, now, tm_diff): # Nothing has worked yet.
        lr_motor = hal_data["pwm"][0]["value"]
        rr_motor = hal_data["pwm"][2]["value"]

        x, y, angle = self.drivetrain.get_distance(lr_motor, rr_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)
