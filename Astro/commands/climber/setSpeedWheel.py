from wpilib.command import Command

class SetSpeedWheel(Command):

    def __init__(self,power):
        super().__init__('SetSpeedWheel')

        self.climber = self.getRobot().climber
        self.requires(self.climber)

        self.power = power

    def initialize(self): pass

    def execute(self):
        if self.climber.isLeaning(False): self.climber.backLift.set(0.5)
        elif self.climber.isLeaning(True): self.climber.backLift.set(-0.5)
        else: self.climber.liftBack(0, True)

        if self.power == 1: self.climber.wheelForward()
        if self.power == -1: self.climber.wheelBack()

    def interrupted(self): self.end()

    def end(self): self.climber.stopDrive()

    def isFinished(self): return self.power == 0
