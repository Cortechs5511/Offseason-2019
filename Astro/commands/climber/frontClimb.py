from wpilib.command import Command

class FrontClimb(Command):
    def __init__(self, up):
        super().__init__('setSpeedWheel')
        self.robot = self.getRobot()
        self.climber = self.robot.climber
        self.requires(self.climber)
        self.up = up

    def initialize(self): pass

    def execute(self):
        tilt = self.climber.getRoll()
        tol = self.climber.returnTolerance()
        if self.up == True:
            self.climber.liftFront(self.climber.returnClimbSpeed(), False)
        elif self.up == False: self.climber.liftFront(-1 * self.climber.returnClimbSpeed(), False)
        if tilt > tol:
            self.climber.liftBack(self.climber.returnClimbSpeed(), False)
        elif tol < -tilt:
            self.climber.liftBack(-1 * self.climber.returnClimbSpeed(), False)

    def interrupted(self): self.climber.stopFront()

    def end(self): self.climber.stopFront()

    def isFinished(self): return self.climber.isFullyExtendedBoth()
