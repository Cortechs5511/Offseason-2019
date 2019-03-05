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
        #lift climber legs to lower the robot
        lean = self.climber.getLean()
        if self.mode == "front":
            self.climber.lower("front")
        elif self.mode == "back":
            self.climber.lower("back")
        elif self.mode == "both":
            self.climber.lower("both")
        else:
            self.climber.stopBack()
            self.climber.stopFront()

    def interrupted(self): self.climber.stop()

    def end(self): self.interrupted()

    def isFinished(self):
        return False
