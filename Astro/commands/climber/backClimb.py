from wpilib.command import Command

class BackClimb(Command):
    def __init__(self):
        super().__init__('setSpeedWheel')
        self.robot = self.getRobot()
        self.climber = self.robot.climber

    def initialize(self):
        pass

    def execute(self):
        if self.robot.readDriverLeftButton(14):
            self.climber.liftBack(self.climber.returnClimbSpeed())
        elif self.robot.readDriverLeftButton(15):
            self.climber.liftBack(-1 * self.climber.returnClimbSpeed())

    def interrupted(self):
        self.climber.stopBack()

    def end(self):
        self.climber.stopBack()

    def isFinished(self):
        return True
