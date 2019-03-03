from wpilib.command import Command

class LowerRobot(Command):
    def __init__(self, mode):
        super().__init__('lowerRobot')
        robot = self.getRobot()
        self.climber = robot.climber
        self.requires(self.climber)
        self.mode = mode

    def initialize(self): pass

    def execute(self):
        lean = self.climber.getLean()
        if self.mode == "front":
            self.climber.backLift.set(0)
            self.climber.frontLift.set(self.climber.returnClimbSpeed())
        elif self.mode == "back":
            self.climber.frontLift.set(0)
            self.climber.backLift.set(self.climber.returnClimbSpeed())
        elif self.mode == "both":
            if self.climber.isLeaning(False) or self.climber.isLeaning(True):
                self.climber.backLift.set(self.climber.returnCorrectionSpeed())
                self.climber.frontLift.set(self.climber.returnCorrectionSpeed())
            else:
                self.climber.frontLift.set(self.climber.returnClimbSpeed())
                self.climber.backLift.set(self.climber.returnClimbSpeed())

    def interrupted(self): self.climber.stop()

    def end(self): self.interrupted()

    def isFinished(self):
        if self.mode == "both" : return self.climber.isFullyRetractedBoth()
        elif self.mode == "front" : return self.climber.isFullyRetractedFront()
        elif self.mode == "back" : return self.climber.isFullyRetractedBack()
        else: return False
