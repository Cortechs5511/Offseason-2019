from wpilib import SmartDashboard
from ctre import WPI_TalonSRX as Talon

import map

class CargoMech():
    def cargoInit(self, robot):
        self.robot = robot
        self.xbox = map.getJoystick(2)
        self.intake = Talon(map.intake)

        self.intakeSpeed = 0.9

    def intake(self, mode):
        ''' Intake/Outtake/Stop Intake the cargo (turn wheels inward)'''
        if mode == "intake": self.motorIntake.set(self.intakeSpeed)
        elif mode == "outtake": self.motorIntake.set(-1 * self.intakeSpeed)
        elif mode == "stop": self.motorIntake.set(0)

    def periodic(self):
        deadband = 0.4

        if self.xbox.getRawAxis(map.intakeCargo)>deadband: self.intake("intake")
        elif self.xbox.getRawAxis(map.outtakeCargo)>deadband: self.intake("outtake")
        else: self.intake("stop")

    def disable(self): self.intake("stop")
    
    def dashboardInit(self): pass
    def dashboardPeriodic(self): pass
