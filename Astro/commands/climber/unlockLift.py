from wpilib.command import Command

class UnLockLift(Command):
    def __init__(self):
        super().__init__('UnlockLift')
        robot = self.getRobot()
        self.climber = robot.climber
        self.requires(self.climber)
    def initialize(self):
        self.climber.unlockLift()

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
