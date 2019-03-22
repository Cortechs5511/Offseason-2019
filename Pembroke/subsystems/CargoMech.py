from wpilib import SmartDashboard
from ctre import WPI_TalonSRX as Talon

import map
import oi

class CargoMech():

    def initialize(self):
        self.xbox = oi.getJoystick(2)
        self.motor = Talon(map.intake)

        self.intakeSpeed = 0.9

    def intake(self, mode):
        ''' Intake/Outtake/Stop Intake the cargo (turn wheels inward)'''
        if mode == "intake": self.motor.set(self.intakeSpeed)
        elif mode == "outtake": self.motor.set(-1 * self.intakeSpeed)
        elif mode == "stop": self.motor.set(0)

    def periodic(self):
        deadband = 0.4

        if self.xbox.getRawAxis(map.intakeCargo)>deadband: self.intake("intake")
        elif self.xbox.getRawAxis(map.outtakeCargo)>deadband: self.intake("outtake")
        else: self.intake("stop")

    def disable(self): self.intake("stop")

    def dashboardInit(self): pass

    def dashboardPeriodic(self): pass
