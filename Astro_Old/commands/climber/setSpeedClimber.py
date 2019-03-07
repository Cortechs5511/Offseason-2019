from wpilib.command import Command
import map

class SetSpeedClimber(Command):
    def __init__(self):
        super().__init__('setSpeedClimber')
        robot = self.getRobot()
        self.climber = robot.climber
        self.requires(self.climber)
        self.joystick = robot.xbox2

    def initialize(self): pass

    def execute(self):
        deadband = 0.05
        if self.joystick.getRawAxis(map.lowerFrontClimber) < -deadband:
            self.climber.lower("front")
        elif self.joystick.getRawAxis(map.lowerBackClimber) < -deadband:
            self.climber.lower("back")
        elif self.joystick.getRawButton(map.lowerClimber) == True:
            self.climber.lower("both")
        elif self.joystick.getRawAxis(map.liftFrontClimber) > deadband:
            self.climber.lift("front")
        elif self.joystick.getRawAxis(map.liftBackClimber) > deadband:
            self.climber.lift("back")
        elif self.joystick.getRawButton(map.liftClimber) == True:
            self.climber.lift("both")
        elif self.joystick.getRawButton(map.driveForwardClimber):
            self.climber.wheel("forward")
        elif self.joystick.getRawButton(map.driveBackwardClimber):
            self.climber.wheel("backward")
        else:
            self.climber.stopFront()
            self.climber.stopBack()
            self.climber.stopDrive()

    def interrupted(self): self.climber.stop()

    def end(self): self.interrupted()

    def isFinished(self):
        return False
