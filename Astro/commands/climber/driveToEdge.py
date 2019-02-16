from wpilib.command import command

class DriveToEdge(Command):
     def __init__(self, Mode):
        super().__init__('liftRobot')
        robot = self.getRobot()
        self.climber = robot.climber
        self.requires(self.climber)
        self.mode = Mode
    def initialize(self): 
        pass 
    def execute(self):
        if self.mode == "front":
            self.climber.setSpeedWheel(1)
        elif self.mode == "back":
            self.climber.setSpeedWheel(1)
    def interrupted(self):
        self.end()
    def end(self):
        self.climber.setSpeedWheel(0)
    def isFinished(self):
        if self.mode == "front" and self.Climber.isFrontOverGround():
            return True
        elif self.mode == "back" and self.Climber.isBackOverGround():
            return True

        return False






















