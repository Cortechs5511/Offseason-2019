import wpilib
from wpilib import timedrobot
import SmartDashboard

class AnalogInputVoltage(timedrobot):
    
    def robotInit:
        analoginput = wpilib.AnalogInput 

    def robotPeriodic:
        SmartDashboard.putNumber("Analog Input Voltage", AnalogInputVoltage.analoginput.getVoltage())

        