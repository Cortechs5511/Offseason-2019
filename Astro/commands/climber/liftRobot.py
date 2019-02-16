from wpilib.command import Command

class LiftRobot(Command):
    def __init__(self, Mode):
        super().__init__('liftRobot')
        robot = self.getRobot()
        self.climber = robot.climber
        self.requires(self.climber)
        self.mode = Mode

    def initialize(self): pass

    def execute(self):
        if self.mode == "front":
            self.climber.liftFront(self.climber.returnClimbSpeed(), True)
        elif self.mode == "back":
            self.climber.liftBack(self.climber.returnClimbSpeed(), True)
        elif self.mode == "both":
            self.climber.lift(self.climber.returnClimbSpeed())

    def interrupted(self): self.climber.stop()

    def end(self): self.interrupted()

    def isFinished(self): return self.climber.isFullyExtendedBoth()
