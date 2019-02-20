from wpilib.command import Command

class LowerRobot(Command):
    def __init__(self, mode):
        super().__init__('lowerRobot')
        robot = self.getRobot()
        self.climber = robot.climber
        self.requires(self.climber)
        self.mode = mode

    def initialize(self): pass

    def execute(self):
        lean = self.climber.getPitch()
        if self.mode == "front":
            if lean < -0.5: self.climber.backLift.set(0.5)
            elif lean < -2 : self.climber.backLift.set(-0.5)
            else: self.climber.liftBack(0)
            self.climber.liftFront(-1 *self.climber.returnClimbSpeed(), True)
        elif self.mode == "back":
            self.climber.liftBack(-1 *self.climber.returnClimbSpeed(), True)
        elif self.mode == "both":
            self.climber.lift(-1 *self.climber.returnClimbSpeed())

    def interrupted(self): self.climber.stop()

    def end(self): self.interrupted()

    def isFinished(self):
        if self.mode == "both" : return self.climber.isFullyRetractedBoth()
        elif self.mode == "front" : return self.climber.isFullyRetractedFront()
        elif self.mode == "back" : return self.climber.isFullyRetractedBack()
        else: return False
