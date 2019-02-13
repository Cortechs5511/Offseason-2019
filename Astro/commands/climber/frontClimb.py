from wpilib.command import Command

class FrontClimb(Command):
    def __init__(self, up):
        super().__init__('setSpeedWheel')
        self.robot = self.getRobot()
        self.climber = self.robot.climber
        self.up = up

    def initialize(self): pass

    def execute(self):
        if self.up == True: self.climber.liftFront(self.climber.returnClimbSpeed())
        elif self.up == False: self.climber.liftFront(-1 * self.climber.returnClimbSpeed())

    def interrupted(self): self.climber.stopFront()

    def end(self): self.climber.stopFront()

    def isFinished(self): return True
