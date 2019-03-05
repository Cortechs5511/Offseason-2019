from wpilib.command import Command
import map

class SetSpeedClimber(Command):
    def __init__(self):
        super().__init__('setSpeedClimber')
        robot = self.getRobot()
        self.climber = robot.climber
        self.requires(self.climber)
        self.joystick = robot.joystick0

    def initialize(self): pass

    def execute(self):
        if self.joystick.getRawButton(map.lowerFrontClimber) == True:
            self.climber.lower("front")
        elif self.joystick.getRawButton(map.lowerBackClimber) == True:
            self.climber.lower("back")
        elif self.joystick.getRawButton(map.lowerClimber) == True:
            self.climber.lower("both")
        elif self.joystick.getRawButton(map.liftFrontClimber) == True:
            self.climber.lift("front")
        elif self.joystick.getRawButton(map.liftBackClimber) == True:
            self.climber.lift("back")
        elif self.joystick.getRawButton(map.liftClimber) == True:
            self.climber.lift("both")
        else:
            self.climber.stopFront()
            self.climber.stopBack()

    def interrupted(self): self.climber.stop()

    def end(self): self.interrupted()

    def isFinished(self):
        return False
