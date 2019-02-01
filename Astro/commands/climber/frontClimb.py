from wpilib.command import Command

class setSpeedWheel(Command):
    def __init__(self):
        super().__init__('setSpeedWheel')
        robot = self.getRobot()
        self.Climber = robot.Climber

    def initialize(self):
        pass

    def execute(self):
        pass

    def interrupted(self):
        self.Climber.stopFront()

    def end(self):
        self.Climber.stopFront()

    def isFinished(self):
        return True