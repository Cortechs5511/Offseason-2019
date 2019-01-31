import wpilib
from wpilib import SmartDashboard

from wpilib.command.subsystem import Subsystem
from wpilib.command import Command
import wpilib.encoder
import ctre

# TODO DETERMINE CONVERSION!!!!
TICKS_TO_INCHES = 1.0

class thirdLevelFront(Command):
    def __init__(self):
        super().__init__('thirdLevelFront')
        self.robot = self.getRobot()
        self.thirdLevelFront = self.robot.thirdLevelFront

    def initialize(self):
        pass

    def execute(self):
        #read encoder values to check
        self.liftFront()

    def interrupted(self):
        self.stopFront()

    def end(self):
        self.stopFront()


    def isFinished(self):
        #stop if encoder is over the height of the third level
        return True

class lowerFront(Command):
    def __init__(self):
        super().__init__('lowerFront')
        self.robot = self.getRobot()
        self.lowerFront = self.robot.lowerFront

    def initialize(self):
        pass

    def execute(self):
        #read encoder values to check
        lowerFront()

    def interrupted(self):
        stopFront()

    def end(self):
        stopFront()


    def isFinished(self):
        #stop if encoder is over the height of the third level
        return True
class setSpeedWheel(Command):

    def __init__(self):
        super().__init__('setSpeedWheel')
        self.robot = self.getRobot()
        self.setSpeedWheel = self.robot.setSpeedWheel
        #set up joystick axis here

    def initialize(self):
        pass

    def execute(self):
        #read encoder values to check
        #get axis measurements for speed
        #self.wheelSpeed()
        pass

    def interrupted(self):
        wheelSpeed(0)

    def end(self):
        self.wheelSpeed(0)

    def isFinished(self):
        #stop if encoder is over the height of the third level
        return True




class Climber(Subsystem):
    def __init__(self, Robot):
        """ Create all physical parts used by subsystem. """
        super().__init__('Climber')
        self.robot = Robot
        self.debug = True
        self.backLift = ctre.WPI_TalonSRX(0)
        self.frontLift = ctre.WPI_TalonSRX(1)
        self.backWheel1 = ctre.WPI_VictorSPX(2)
        self.backWheel2 = ctre.WPI_VictorSPX(3)
        self.backWheel1.follow(self.backWheel2)
        #self.encoder1 = wpilib.Encoder(0,1)
        #self.encoder2 = wpilib.Encoder(2,3)


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

    def liftFront(self,lift):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down
        """
        if self.getHeightFront()>=19:
            self.frontLift.set(0)
        else:
            self.frontLift.set(lift)
        if self.getHeightFront()<=0:
            self.frontLift.set(0)
        else:
            self.frontLift.set(lift)

    def liftBack(self,lift):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down
        """
        if self.getHeightBack()>=19:
            self.backLift.set(0)
        else:
            self.backLift.set(lift)
        if self.getHeightBack()<=0:
            self.backLift.set(0)
        else:
            self.backLift.set(lift)
    def wheelSpeed(self,speed):
        """ Basic drive function for extended wheels.
            dont' forget breakers
        @param speed - Positive values go true.
         """
        self.backWheel2.set(speed)

        '''stopping functions'''
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

    def dashboardInit(self):
        pass
    def dashboardPeriodic(self):
        pass
