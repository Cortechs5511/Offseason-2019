from wpilib.command import Command

class LowerRobot(Command):
    def __init__(self):
        super().__init__('lowerRobot')
        robot = self.getRobot()
        self.climber = robot.climber

    def initialize(self): pass

    def execute(self): self.climber.lift(-1 * self.climber.returnClimbSpeed())

    def interrupted(self): self.climber.stop()

    def end(self): self.interrupted()

    def isFinished(self): return self.climber.isFullyExtendedBoth()
