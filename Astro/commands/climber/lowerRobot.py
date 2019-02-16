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
        if self.mode == "front":
            self.climber.liftFront(-1 *self.climber.returnClimbSpeed(), True)
        elif self.mode == "back":
            self.climber.liftBack(-1 *self.climber.returnClimbSpeed(), True)
        elif self.mode == "both":
            self.climber.lift(-1 *self.climber.returnClimbSpeed())


    def interrupted(self): self.climber.stop()

    def end(self): self.interrupted()

    def isFinished(self): return self.climber.isFullyExtendedBoth()
