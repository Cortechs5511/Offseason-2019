from wpilib.command import Command

class FrontClimb(Command):
    def __init__(self):
        super().__init__('setSpeedWheel')
        robot = self.getRobot()
        self.climber = robot.climber

    def initialize(self):
        pass

    def execute(self):
        pass

    def interrupted(self):
        self.climber.stopFront()

    def end(self):
        self.climber.stopFront()

    def isFinished(self):
        return True