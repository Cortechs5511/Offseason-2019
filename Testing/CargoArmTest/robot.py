import wpilib
from wpilib import TimedRobot
from wpilib import SmartDashboard
from ctre import WPI_TalonSRX as Talon
from wpilib import Joystick

class MyRobot(TimedRobot):
    """ Used to test power levels to move cargo arms. """

    def robotInit(self):
        self.maxVolts = 10
        self.joystick  = Joystick(0)
        self.motor: Talon = Talon(31)
        self.motor.configClearPositionOnLimitF(True)
        self.motor.configVoltageCompSaturation(self.maxVolts)

    def getNumber(self, key: str, defVal) -> float:
      val = SmartDashboard.getNumber(key, None)
      if val == None:
        val = defVal
        SmartDashboard.putNumber(key, val)
      return val
  
    def teleopPeriodic(self):
        power = 0
        if self.joystick.getRawButton(4):
          power = self.getNumber("Up Volts", 2.5) / self.maxVolts
        elif self.joystick.getRawButton(1):
          power = self.getNumber("Down Volts", -1.0) / self.maxVolts
        else:
          power = -self.joystick.getRawAxis(1)
          if abs(power) < 0.1:
            power = 0

        self.motor.set(power)
  
    def robotPeriodic(self):
        SmartDashboard.putBoolean('Fwd closed',self.motor.isFwdLimitSwitchClosed())
        SmartDashboard.putBoolean('Rev closed', self.motor.isRevLimitSwitchClosed())
        SmartDashboard.putNumber('Motor position', self.motor.getQuadraturePosition())
        SmartDashboard.putNumber("Motor power", self.motor.getMotorOutputPercent())
        SmartDashboard.putNumber("Motor volts", self.motor.getMotorOutputVoltage())
        SmartDashboard.putNumber("Motor current", self.motor.getOutputCurrent())

if __name__ == "__main__":
    wpilib.run(MyRobot)