from wpilib.command import Command

class LiftRobot(Command):
    def __init__(self):
        super().__init__('liftRobot')
        robot = self.getRobot()
        self.climber = robot.climber

    def initialize(self): pass

    def execute(self): self.climber.lift(self.climber.returnClimbSpeed())

    def interrupted(self): self.climber.stop()

    def end(self): self.interrupted()

    def isFinished(self): return self.climber.isFullyExtendedBoth()
