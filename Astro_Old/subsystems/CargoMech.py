import wpilib
from wpilib import SmartDashboard

from wpilib.command.subsystem import Subsystem
from wpilib.command import Command

import ctre
from commands.cargo.wristIntake import WristIntake
from commands.cargo.wristMove import WristMove
from commands.cargo import setSpeedCargo
import map
class CargoMech(Subsystem):
    def __init__(self, Robot):
        #Create all physical parts used by subsystem.
        super().__init__('Cargo')
        self.debug = True
        self.robot = Robot
        #fix
        if not wpilib.RobotBase.isSimulation():
            self.motorIntake.configFactoryDefault()
        self.motorIntake = ctre.WPI_TalonSRX(map.intake)
        self.motorWrist = ctre.WPI_TalonSRX(map.wrist)
        self.motorIntake.setName("Cargo","Motor Intake")
        self.motorWrist.setName("Cargo", "Motor Wrist")
        self.SetSpeedCargo = setSpeedCargo.SetSpeedCargo

    def intake(self, mode):
        ''' Intake/Outtake/StopIntake the balls (turn wheels inward)'''
        if mode == "intake":
            self.motorIntake.set(0.9)
        elif mode == "outtake":
            self.motorIntake.set(-0.9)
        elif mode == "stop":
            self.motorIntake.set(0)

    def wrist(self, mode):
        '''Moves or stops the wrist'''
        if mode == "up":
            self.motorWrist.set(0.5)
        elif mode == "down":
            self.motorWrist.set(-0.5)
        elif mode == "stop":
            self.motorWrist.set(0)

    def dashboardInit(self):
        pass

    def initDefaultCommand(self):
        self.setDefaultCommand(self.SetSpeedCargo(timeout = 300))

    def subsystemInit(self):
        r = self.robot

    def disable(self):
        self.intake("stop")
        self.wrist("stop")

    def dashboardPeriodic(self):
        pass
