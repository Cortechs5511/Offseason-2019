from wpilib.command import Command

class LiftRobot(Command):
    def __init__(self, Mode):
        super().__init__('liftRobot')
        robot = self.getRobot()
        self.climber = robot.climber
        self.requires(self.climber)
        self.mode = Mode

    def initialize(self): pass

    def execute(self):
        if self.mode == "front":
            self.climber.backLift.set(0)
            self.climber.frontLift.set(-1 * self.climber.returnClimbSpeed())
        elif self.mode == "back":
            self.climber.frontLift.set(0)
            self.climber.backLift.set(-1* self.climber.returnClimbSpeed())
        elif self.mode == "both":
            if self.climber.isLeaning(True):
                self.climber.backLift.set(self.climber.returnCorrectionSpeed())
            elif self.climber.isLeaning(False):
                self.climber.backLift.set(self.climber.returnCorrectionSpeed())
            else:
                self.climber.backLift.set(-1 * self.climber.returnClimbSpeed())
            self.climber.frontLift.set(-1 * self.climber.returnClimbSpeed())

    def interrupted(self): self.climber.stop()

    def end(self): self.interrupted()

    def isFinished(self):
        if self.mode == "both" : return self.climber.isFullyExtendedBoth()
        elif self.mode == "front" : return self.climber.isFullyExtendedFront()
        elif self.mode == "back" : return self.climber.isFullyExtendedBack()
        else: return False
