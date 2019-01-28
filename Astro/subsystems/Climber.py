import wpilib
from wpilib import SmartDashboard

from wpilib.command.subsystem import Subsystem
from wpilib.command import Command

import ctre


class thirdLevelFront(Command):
    def __init__(self):
        super().__init__('thirdLevel')
        self.robot = self.getRobot()
        self.thirdLevel = self.robot.thirdLevel
    
    def initialize(self):
        pass

    def execute(self):
        #read encoder values to check
        liftFront()
    
    def interrupted(self):
        stopFront()

    def end(self):
        stopFront()
    

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
        self.encoder1 = wpilib.Encoder(0,1)
        self.encoder2 = wpilib.Encoder(2,3)

    
    def getHeight(self):
        #this will return the height in inches from encoder
        pass

    def wheelSpeed(self):
        #basic drive function for extended wheels
        self.backWheel1.set(0.5)
        self.backWheel2.set(0.5)

    def liftFront(self):
        self.frontLift.set(0.5)

    def lowerFront(self):
        self.frontLift.set(-0.5)

    def stopFront(self):
        self.frontLift.set(0)

    def liftBack(self):
        self.backLift.set(0.5)

    def lowerBack(self):
        self.backLift.set(-0.5)

    def stopBack(self):
        self.backLift.set(0)

    def disable(self):
        pass

    def dashboardInit(self):
        pass

    def dashboardPeriodic(self):
        pass
