import wpilib
from wpilib.command import Command
from commands.climber import setSpeedWheel

class DriveToEdge(Command):
    def __init__(self, Mode):
        super().__init__('DriveToEdge')
        robot = self.getRobot()
        self.climber = robot.climber
        self.requires(self.climber)
        self.mode = Mode

    def initialize(self):
        pass

    def execute(self):
        lean = self.climber.getLean()
        if self.mode == "front":
            self.climber.wheelForward()
            if self.climber.isLeaning(False):
                self.climber.backLift.set(self.climber.returnCorrectionSpeed())
            elif self.climber.isLeaning(True):
                self.climber.backLift.set(self.climber.returnCorrectionSpeed())
            else: self.climber.backLift.set(0)
            self.climber.frontLift.set(0)
            #self.climber.liftFront(-1 *self.climber.returnClimbSpeed(), True)
        elif self.mode == "back":
            self.climber.wheelForward()
            if self.climber.isLeaning(False):
                self.climber.backLift.set(self.climber.returnCorrectionSpeed())
            elif self.climber.isLeaning(True):
                self.climber.backLift.set(self.climber.returnCorrectionSpeed())
            else: self.climber.backLift.set(0)
            self.climber.frontLift.set(0)

    def interrupted(self):
        self.end()

    def end(self):
        self.climber.stopDrive()

    def isFinished(self):
        if self.mode == "front" and self.climber.isFrontOverGround():
            return True
        elif self.mode == "back" and self.climber.isBackOverGround():
            return True

        return False
