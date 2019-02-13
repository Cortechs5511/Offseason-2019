from wpilib.command import Command

class FrontClimb(Command):
    def __init__(self):
        super().__init__('setSpeedWheel')
        self.robot = self.getRobot()
        self.climber = self.robot.climber

    def initialize(self): pass

    def execute(self):
        if self.robot.readDriverLeftButton(13): self.climber.liftFront(self.climber.climberSpeed)
        elif self.robot.readDriverLeftButton(12): self.climber.liftFront(-1 * self.climber.climberSpeed)

    def interrupted(self): self.climber.stopFront()

    def end(self): self.climber.stopFront()

    def isFinished(self): return True
