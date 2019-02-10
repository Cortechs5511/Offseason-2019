from wpilib.command import Command

class LockLift(Command):
    def __init__(self):
        super().__init__('LockLift')
        robot = self.getRobot()
        self.climber = robot.climber
        self.requires(self.climber)
    def initialize(self):
        self.climber.lockLift()

    def execute(self):
        pass

    def interrupted(self):
        pass

    def end(self):
        pass


    def isFinished(self):

        if self.timeSinceInitialized() >= 0.25:
            return True
        else:
            return False

        