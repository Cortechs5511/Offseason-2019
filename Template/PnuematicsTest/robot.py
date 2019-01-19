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
        self.piston = wpilib.Solenoid(0)

    def teleopInit(self):
        self.count = 0

    def autonomousInit(self):
    #creates a time to run
        self.count = 0
        self.autonTimer = wpilib.Timer()
        self.autonTimer.start()
    def autonomousPeriodic(self):
        state = False
        if self.autonTimer.get() < 5:
            state = False
        else:
            state = True
        if self.autonTimer.get() > 10:

            self.autonTimer.reset()


        self.piston.set(state)

    '''def teleopPeriodic(self):

        ticks = (self.left_encoder.getDistance())*255
        sd.putNumber("Ticks",ticks)
        self.count+= 1
        sd.putNumber("Count",self.count)

        left = self.rightJoystick.getRawAxis(1)
        right = self.leftJoystick.getRawAxis(1)
        if abs(left) < 0:
            left = 0
        if abs(right) < 0:
            "right = 0
        left = left*0.2
        right = right*0.2
        self.drive(left, right) '''



    '''def Leftdrivecontrol(self, leftPower):
        sd.putNumber("leftspeed", leftPower)
        self.Leftdrive1.set(leftPower)
        self.Leftdrive2.set(leftPower)

    def Rightdrivecontrol(self, rightPower):
        sd.putNumber("rightspeed", rightPower)
        self.Rightdrive1.set(rightPower)
        self.Rightdrive2.set(rightPower)

    def drive(self, leftPower,rightPower):
        self.Leftdrivecontrol(leftPower)
        self.Rightdrivecontrol(rightPower)'''

if  __name__ == '__main__':
    wpilib.run(MyRobot)
