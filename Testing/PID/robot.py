import math
import wpilib

from wpilib import SmartDashboard

class MyRobot(wpilib.TimedRobot):
  """
  This class demonstrates how to use the PIDController, PIDSource
  and PIDOutput API.
  """

    def __init__(self):
        super().__init__()
        # Since MyRobot implements all of the methods required
        # to be a PIDSource and PIDOutput, it can be passed
        # as the last two parameter to the PIDController object.
        pc = wpilib.PIDController(0.01, 0.0, 0.0, 0.0, self, self)

        # Putting the PIDController to the SmartDashboard allows
        # you to experiment with the values on the dashboard
        SmartDashboard.putData(pc)
        self.pc = pc
        # Fake sensor reading
        self.sensor = 5.0
        self.output = 0.0
        # Create a motor controller to apply power to so we
        # can see something in the simulator
        self.spark = wpilib.Spark(1)

    def pidWrite(self, output):
      # The PIDController will keep calling this method with the
      # output power to apply
      SmartDashboard.putNumber("Output", output)
      self.spark.set(output)
      self.output = output

    def pidGet(self):
      # The PIDController will keep calling this method to read
      # the sensor
      self.sensor = self.sensor + self.output * 0.01
      SmartDashboard.putNumber("Sensor", self.sensor)
      return self.sensor

    def getPIDSourceType(self):
      # We need to implement this method in order to be a PIDSource
      # Return 0 for a distance type situation
      # Return 1 for a rate/velocity type situation
      return 0

    def setPIDSourceType(self, type):
      # We need to implement this in order to be a PIDSource, however
      # we ignore any request to change
      pass

    def robotInit(self):
        pass
      
    def teleopInit(self):
      self.sensor = 0
      self.pc.setSetpoint(50.0)
      self.pc.setEnabled(True)

    def teleopPeriodic(self):
      # We don't need to do anything periodically, enabling
      # the PID controller will cause our pidGet() and
      # pidWrite() methods to be called in the background
      # by the PIDController thread.
      pass

if __name__ == "__main__":
    wpilib.run(MyRobot)
