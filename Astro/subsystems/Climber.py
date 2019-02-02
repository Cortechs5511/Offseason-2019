import wpilib
from wpilib import SmartDashboard

from wpilib.command.subsystem import Subsystem
from wpilib.command import Command
import wpilib.encoder
import ctre
from commands.climber.liftRobot import LiftRobot
from commands.climber.lowerRobot import LowerRobot
from commands.climber.setSpeedWheel import SetSpeedWheel
# TODO DETERMINE CONVERSION!!!!
TICKS_TO_INCHES = 1.0
MAX_EXTEND = 12.0




class Climber(Subsystem):
    def __init__(self, Robot):
        """ Create all physical parts used by subsystem. """
        super().__init__('Climber')
        self.robot = Robot
        self.debug = True
        self.backLift = ctre.WPI_TalonSRX(40)
        self.frontLift = ctre.WPI_TalonSRX(41)
        """ self.backWheel1 = ctre.WPI_VictorSPX(2)"""
        self.backWheel2 = ctre.WPI_VictorSPX(3)
#        self.backWheel1.follow(self.backWheel2)
        self.encoder1 = wpilib.Encoder(4,5)
        self.encoder2 = wpilib.Encoder(6,7) 
        self.backLift.setName("Climber" , "BackLift")
        self.frontLift.setName("Climber" , "FrontLift")
        self.backWheel2.setName("Climber" , "Wheels")


    def dashboardInit(self):
        #if self.debug == True:
        #    SmartDashboard.putData(self)
        SmartDashboard.putData("Lift Robot", LiftRobot())
        r = self.robot
        climberWheelsForward : wpilib.buttons.JoystickButton = r.driverLeftButton(7)
        climberWheelsForward.whileHeld(SetSpeedWheel(1))


        climberWheelsBackward : wpilib.buttons.JoystickButton = r.driverLeftButton(8)
        climberWheelsBackward.whileHeld(SetSpeedWheel(-1))


        liftButton : wpilib.buttons.JoystickButton = r.driverLeftButton(9)
        liftButton.whileHeld(LiftRobot())

        
        liftButton : wpilib.buttons.JoystickButton = r.driverLeftButton(10)
        liftButton.whileHeld(LowerRobot())

     



    #gets height
    def getHeightFront(self):
        """this will return the height in inches from encoder
            Pass height to SD
        """
        ticks = self.frontLift.getQuadraturePosition()
        return ticks * TICKS_TO_INCHES
    def getHeightBack(self):
        """this will return the height in inches from encoder
            Pass height to SD
        """
        ticks = self.backLift.getQuadraturePosition()
        return ticks * TICKS_TO_INCHES


    def isFullyExtendedFront(self):
        """ tells us if the front is fully extended"""

        return self.getHeightFront() >= MAX_EXTEND


    def isFullyExtendedBack(self):
        """tells us if the back is fully extended, so it can stop"""
        return self.getHeightBack() >= MAX_EXTEND

    def isFullyExtendedBoth(self):
        """tells us if both front and back are fully extended, so it can stop"""
        return self.isFullyExtendedFront() and self.isFullyExtendedBack() 

    #functions for lift
    def liftFront(self,lift):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down(extend)
        """
        if lift > 0 and self.getHeightFront()>=MAX_EXTEND:
            self.frontLift.set(0)
        elif lift < 0 and self.getHeightFront() < 0:
            self.frontLift.set(0)
        else:
            self.frontLift.set(lift)

    def liftBack(self,lift):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down
        """
        if  lift > 0 and self.getHeightBack()>=MAX_EXTEND:
            self.backLift.set(0)
           
        elif lift < 0 and self.getHeightBack()<0:
            self.backLift.set(0)
        else:
            self.backLift.set(lift)


    #wheel speed
    def wheelForward(self):
        self.backWheel2.set(0.75)
    def wheelBack(self):
        self.backWheel2.set(-0.75)

    #stopping and disable
    def stopFront(self):
        self.frontLift.set(0)
    def stopBack(self):
        self.backLift.set(0)
    def stopDrive(self):
        self.backWheel2.set(0)
    def disable(self):
        self.stopFront()
        self.stopBack()
        self.stopDrive()

    
    def dashboardPeriodic(self):
          if self.debug == True:
            SmartDashboard.putNumber("Ticks on front", self.getHeightFront())
            SmartDashboard.putNumber("Ticks on back", self.getHeightBack())
