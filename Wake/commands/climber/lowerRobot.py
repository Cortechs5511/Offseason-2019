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
        #lift climber legs to lower the robot
        lean = self.climber.getLean()
        if self.mode == "front":
            self.climber.lift("front")
        elif self.mode == "back":
            self.climber.lift("back")
        elif self.mode == "both":
            self.climber.lift("both")
        else:
            self.climber.stopBack()
            self.climber.stopFront()

    def interrupted(self): self.climber.stop()

    def end(self): self.interrupted()

    def isFinished(self):
        if self.mode == "both" : return self.climber.isFullyRetractedBoth()
        elif self.mode == "front" : return self.climber.isFullyRetractedFront()
        elif self.mode == "back" : return self.climber.isFullyRetractedBack()
        else: return False
