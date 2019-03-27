import wpilib
from wpilib import SmartDashboard
from wpilib import Spark
from wpilib import Joystick

class MyRobot(wpilib.TimedRobot):
    """
    Small program to operate just the legs on 2019 roboto Astro using
    PWM controlled NEO motors.
    """

    def robotInit(self):
      # Assumes Spark Max controllers are in PWM mode
      self.gamepad: Joystick = Joystick(2)
      self.frontLeg: Spark = Spark(0)
      self.backLeg: Spark = Spark(1)
      self.frontExtendPower: float = 0.5
      self.frontRetractPower: float = -0.5
      self.backExtendPower: float = 0.6
      self.backRetractPower: float = -0.6
      # Update power values (in case old settings available on dashboard)
      self.loadRetractPowerValues()
      self.loadExtendPowerValues()

    @staticmethod
    def getNumber(key: str, defVal: float) -> float:
      """ Pulls value from dashboard, if not found adds to dashboard. """
      val = SmartDashboard.getNumber(key, None)
      if val == None:
        val = defVal
        SmartDashboard.putNumber(key, val)
      return val

    @staticmethod
    def deadZoneCheck(axis: float) -> float:
      """ Returns value passed in or 0.0 if value passed is close to zero. """
      if abs(axis) < 0.1:
        return 0
      return axis

    def loadRetractPowerValues(self):
      """ Reads power values to retract legs from dashboard. """
      self.frontRetractPower = MyRobot.getNumber("Front Retract Power", self.frontRetractPower)
      self.backRetractPower = MyRobot.getNumber("Back Retract Power", self.backRetractPower)

    def loadExtendPowerValues(self):
      """ Reads power values to extend legs from dashboard. """
      self.frontExtendPower = MyRobot.getNumber("Front Extend Power", self.frontExtendPower)
      self.backExtendPower = MyRobot.getNumber("Back Extend Power", self.backExtendPower)
      
    def teleopPeriodic(self):
      if self.gamepad.getRawButton(1):
        # Let A button on gamepad lower robot (retract legs)
        self.loadRetractPowerValues()
        self.frontLeg.set(self.frontRetractPower)
        self.backLeg.set(self.backRetractPower)
      elif self.gamepad.getRawButton(4):
        # Let Y button lift robot (extend legs)
        self.loadExtendPowerValues()
        self.frontLeg.set(self.frontExtendPower)
        self.backLeg.set(self.backExtendPower)
      else:
        # Use Y axis on gamepad to control leg motors
        frontPower: float = MyRobot.deadZoneCheck(-self.gamepad.getRawAxis(1))
        backPower: float = MyRobot.deadZoneCheck(-self.gamepad.getRawAxis(3))
        self.frontLeg.set(frontPower)
        self.backLeg.set(backPower)

if  __name__ == '__main__':
    wpilib.run(MyRobot)
