from wpilib.command import Command

class LowerRobot(Command):
    def __init__(self):
        super().__init__('lowerRobot')
        robot = self.getRobot()
        self.climber = robot.climber

    def initialize(self):
        pass

    def execute(self):
        self.climber.liftFront(-0.25)
        self.climber.liftBack(-0.25)

    def interrupted(self):
        self.climber.stopFront()
        self.climber.stopBack()

    def end(self):
      
        self.interrupted()
    def isFinished(self):
        return self.climber.isFullyExtendedBoth()