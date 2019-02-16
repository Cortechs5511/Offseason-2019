import wpilib
from wpilib import TimedRobot
from wpilib import SmartDashboard

class MyRobot(TimedRobot):
    
    def robotInit(self):
        self.analoginput = wpilib.AnalogInput(0) 

    def robotPeriodic(self):
        SmartDashboard.putNumber("Analog Input Voltage", self.analoginput.getVoltage())

if __name__ == "__main__":
    wpilib.run(MyRobot)