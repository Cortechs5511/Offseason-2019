from wpilib.command import Command

class setSpeedWheel(Command):
    def __init__(self,power):
        super().__init__('setSpeedWheel')
        robot = self.getRobot()
        self.Climber = robot.Climber
        self.requires(self.Climber)
        self.power = power

    def initialize(self):
        pass

    def execute(self):
        if self.power == 1:
            self.Climber.wheelFoward()
        if self.power == -1:
            self.Climber.wheelBack()

    def interrupted(self):
        self.Climber.stopDrive()

    def end(self):
        self.Climber.stopDrive()

    def isFinished(self):
        return self.power == 0