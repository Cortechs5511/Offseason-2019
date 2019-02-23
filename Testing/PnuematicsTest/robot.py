#imports important packages for running
import wpilib
import wpilib.drive
from wpilib import SmartDashboard as sd
import ctre
import math

#class of robot
class MyRobot(wpilib.TimedRobot):
    #declares the motors in existence
    def robotInit(self):
        self.piston = wpilib.DoubleSolenoid(0,1)
        self.operator = wpilib.Joystick(0)
        self.preferences = wpilib.Preferences.getInstance()
        
    def teleopInit(self):
        self.count = 0

    def autonomousInit(self):
    #creates a time to run
        self.count = 0
        self.autonTimer = wpilib.Timer()
        self.autonTimer.start()

    def autonomousPeriodic(self):
        state = wpilib.DoubleSolenoid.Value.kForward
        if self.autonTimer.get() < 5:
            state = wpilib.DoubleSolenoid.Value.kReverse
        else:
            state = wpilib.DoubleSolenoid.Value.kForward
        if self.autonTimer.get() > 10:

            self.autonTimer.reset()


        self.piston.set(state)
        sd.putNumber("Piston",state)
        sd.putNumber("practice", self.preferences.getBoolean("practice" , False))
        



        """ Adds subsystem specific commands. """
        """if self.debug:
            SmartDashboard.putData("Eject Hatch", EjectHatch())
            SmartDashboard.putData("Hatch Mech", self)
            SmartDashboard.putData("Ejector Toggle" , EjectToggle())
        self.retractEjector()
        r = self.robot
        b : wpilib.buttons.JoystickButton = r.operatorButton(3)
        b.whenPressed(EjectHatch())
        b : wpilib.buttons.JoystickButton = r.operatorButton(5)
        b.whenPressed(EjectToggle())
        b : wpilib.buttons.JoystickButton = r.operatorButton(6)
        b.whenPressed(SlideToggle())'''"""

    def teleopPeriodic(self):

        state1 = self.piston.get()
        
        if self.operator.getButton(1):
            state1 = wpilib.DoubleSolenoid.Value.kForward
        elif self.operator.getButton(2):
            state1 = wpilib.DoubleSolenoid.Value.kReverse

        self.piston.set(state1)
        sd.putNumber("Piston",state1)



    '''def drive(self, leftPower,rightPower):
        self.Leftdrivecontrol(leftPower)
        self.Rightdrivecontrol(rightPower)'''

if  __name__ == '__main__':
    wpilib.run(MyRobot)
