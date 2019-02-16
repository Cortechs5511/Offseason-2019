import wpilib
from wpilib import SmartDashboard
from wpilib import TimedRobot

class MyRobot(TimedRobot):

    def robotInit(self):

        self.Compressor = wpilib.Compressor(0)
        self.Solenoid = wpilib.Solenoid(0)

    def robotPeriodic(self):

        SmartDashboard.putNumber("Compressor Current", self.Compressor.getCompressorCurrent())
        SmartDashboard.putNumber("Compressor Current Too High Fault", self.Compressor.getCompressorCurrentTooHighStickyFault())
        SmartDashboard.putNumber("Compressor Current Too High Sticky Fault", self.Compressor.getCompressorCurrentTooHighStickyFault())
        SmartDashboard.putNumber("Compressor Not Connected Fault", self.Compressor.getCompressorNotConnectedFault())
        SmartDashboard.putNumber("Compressor Not Connected Sticky Fault", self.Compressor.getCompressorNotConnectedStickyFault())
        SmartDashboard.putNumber("Compressor Shorted Fault", self.Compressor.getCompressorShortedFault())
        SmartDashboard.putNumber("Compressor Shorted Sticky Fault", self.Compressor.getCompressorShortedStickyFault())
        SmartDashboard.putBoolean("Pressure Switch", self.Compressor.getPressureSwitchValue())
        
        print("self.Solenoid.set(True)")        


if __name__ == "__main__":
    wpilib.run(MyRobot)
