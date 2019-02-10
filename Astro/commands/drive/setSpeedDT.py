import math
import wpilib
#from robot import MyRobot
#from subsystems.Drive import Drive

from wpilib.command import Command
from wpilib.command import TimedCommand
from wpilib import SmartDashboard
from wpilib.drive.differentialdrive import DifferentialDrive
class SetSpeedDT(TimedCommand):

    def __init__(self, timeout = 0):
        super().__init__('SetSpeedDT', timeoutInSeconds = timeout)
        self.robot = self.getRobot()
        self.requires(self.robot.drive)
        self.DT = self.robot.drive

        self.Joystick0 = self.robot.joystick0
        self.Joystick1 = self.robot.joystick1
        SmartDashboard.putNumber("gain",1)
        self.maxspeed = 1.00 #In addition to normal reducing factor in Drive.py
        self.diffDrive = DifferentialDrive(self.DT.left,self.DT.right)
        self.diffDrive.setSafetyEnabled(False)

    def initialize(self):
        self.DT.setDirect()

    def execute(self):
        left = -self.Joystick0.getY()
        right = -self.Joystick1.getY()
        flip = self.DT.isFlipped()
#half-speed
        if self.robot.readDriverRightButton(3):
            left = left / 2
            right = right / 2
# brakes
        if self.robot.readDriverLeftButton(3):
            left = left / 1000
            right = right / 1000

# TURBO MODE POTENTIAL DANGER ONLY USE IN DIRE INSTANCES
     #  if self.robot.readDriverLeftButton(4):
      #     left = left*1000
       #    right = right*1000
        
#double speed maybe useful 
        if self.robot.readDriverLeftButton(5):
            left = left*2
            right = right*2


        if (abs(left)<0.025) and (abs(right)<0.025):


            gain = SmartDashboard.getNumber("gain",1)
            #diff drive is messed up
            power = -(self.robot.operatorAxis(1))
            rotation = self.robot.operatorAxis(4)*.75
            #quickTurn = self.robot.readOperatorButton(10)
            #self.diffDrive.curvatureDrive(power,rotation,quickTurn)
            self.diffDrive.arcadeDrive(rotation, power)
            #self.DT.tankDrive(power*gain,power)
        else:
            if flip == True:
                self.DT.tankDrive (-right * self.maxspeed ,-left * self.maxspeed)
            else:
        self.DT.tankDrive(left * self.maxspeed ,right * self.maxspeed)


    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
