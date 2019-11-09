from pyfrc.physics import tankmodel
from pyfrc.physics import motor_cfgs
from pyfrc.physics.units import units
class PhysicsEngine:
    def __init__(self, controller):
        self.controller = controller
        self.drivetrain = tankmodel.TankModel.theory(motor_cfgs.MOTOR_CFG_MINI_CIM,
                                                     robot_mass= 5 * units.lbs, # using some example units
                                                     gearing = 0.7, nmotors = 4,
                                                     x_wheelbase = 3.0 * units.feet,
                                                     wheel_diameter = 32 * units.inch)
        self.deadZone = 0.05

    def update_sim(self, hal_data, now, tm_diff): # Nothing has worked yet.
        pass
