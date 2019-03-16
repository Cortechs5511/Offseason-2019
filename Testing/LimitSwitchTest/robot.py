import wpilib
from wpilib import TimedRobot
from wpilib import SmartDashboard as sd
from ctre import WPI_TalonSRX as Talon
from wpilib import Joystick

class MyRobot(TimedRobot):
    def robotInit(self):
        self.joystick  = Joystick(0)
        self.motor = Talon(10)
        self.motor.configClearPositionOnLimitF(True)
    def teleopPeriodic(self):
        self.y = self.joystick.getRawAxis(1)
        if abs(self.y) <0.1:
            self.y = 0
        self.motor.set(self.y)
    def robotPeriodic(self):
        sd.putNumber('Forward closed',self.motor.isFwdLimitSwitchClosed())
        sd.putNumber('Back closed', self.motor.isRevLimitSwitchClosed())
        sd.putNumber('motor position', self.motor.getQuadraturePosition())
if __name__ == "__main__":
    wpilib.run(MyRobot)