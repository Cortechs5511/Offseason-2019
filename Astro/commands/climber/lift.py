from wpilib.command import Command
from wpilib.command import CommandGroup
import subsystems

class LiftCommand(Command):
    """ Base class used for command that manipulate climber legs. """
    def __init__(self, name):
        super().__init__(name)
        robot = self.getRobot()
        self.climber: subsystems.Climber.Climber = robot.climber
        self.requires(self.climber)
        self.extendSpeed: float = self.climber.returnClimbSpeed()
        self.retractSpeed: float = -self.climbSpeed
        # NOTE: We may not use it, but I think we want full control
        # of the drive for all lift operations (we don't want operator
        # messing with drive wheels)
        self.drive: subsystems.Drive.Drive = robot.drive
        self.requires(self.drive)

    def initialize(self):
        # Get climb power to use from dashboard (in case it was changed)
        self.climbSpeed = self.climber.returnClimbSpeed()
        # In case we decide to have different power for extend vs retract
        self.retractSpeed = -self.climbSpeed
        # Stop main drive wheels 
        self.drive.setDirect()
        self.drive.tankDrive(0, 0)

    def end(self):
        """ Stops all leg and wheel motors when any climber command terminates. """
        self.climber.disable()

    def interrupted(self):
      self.end()

    def getLean(self) -> float:
        """
        Returns degrees that robot is leaning forward (-) or backward (+).
        """
        self.climber.getRoll()

    def isLeaningForward(self, lean) -> bool:
        """
        Indicates whether robot lean value is forward or backward.
        : param lean : Signed lean value.
        : return : True if leaning forward, false if leaning backward.
        """
        return lean < 0

    def reducePower(self, power, lean) -> float:
        """
        Returns a reduced power value based on amount of lean.
        : param power : Desired power value if level.
        : return : Reduced power level based on amount of lean.
        """
        # Reduce power by 0.05 per degree of lean, but not more
        # than 25 percent
        reduction = min(0.05 * lean, 0.25)
        return power * (1.0 - reduction)

    def fullyExtendBothLegs(self):
        """
        Tries to apply power values to smoothly
        extend both legs while maintaining a level robot.
        """
        maxLean: float = 2.0
        frontPower: float = self.climbSpeed
        backPower: float = self.climbSpeed
        lean: float = self.getLean()

        if self.isLeaningForward(lean):
          backPower = self.reducePower(backPower, lean)
        else:
          frontPower = self.reducePower(frontPower, lean)

        # Apply computed power
        self.climber.moveFrontLegs(frontPower, maxLean)
        self.climber.moveBackLegs(backPower, maxLean)

    def maintainBackLegs(self):
        """
        Checks to see how out of "level" we are and if necessary will apply power
        to back motors to adjust.
        """
        # Note, I think we prefer leaning forwards slightly when
        # robot is up and moving onto ramp, so desired lean
        # might be better set to something less than 0.
        desiredLean: float = -2.0
        offLean: float = 1.0 # Turn off back motor if in this range
        maxLean: float = 3.0 # Turn on back motor if out of this range
        forwardLeanLimit = desiredLean - maxLean
        backwardLeanLimit = desiredLean + maxLean
        lean: float = self.getLean()

        if lean < -forwardLeanLimit:
          # Leaning too far forward, need to retract back legs
          self.climber.moveBackLegs(self.retractSpeed, -forwardLeanLimit)
        elif lean > backwardLeanLimit:
          # Leaning too far back, need to extend back legs
          self.climber.moveBackLegs(self.extendSpeed, backwardLeanLimit)
        elif lean > (desiredLean - offLean) and lean < (desiredLean + offLean):
          # Back in good range, turn motors off until something changes a lot
          self.climber.stopBack()


class ExtendBothLegs(LiftCommand):
    """ Command that lifts the robot into the air by extending both legs. """
    def __init__(self):
        super().__init__("ExtendBothLegs")

    def execute(self):
        self.fullyExtendBothLegs()

    def isFinished(self):
        return self.climber.isFullyExtendedBoth()


class RetractFrontLegs(LiftCommand):
    """ Command that retracts the front legs once front wheels are on top platform. """
    def __init__(self):
        super().__init__("RetractFrontLegs")

    def execute(self):
        # Keep back legs level
        self.maintainBackLegs()

        # Retract front legs
        maxLean = 5.0
        self.climber.moveFrontLegs(self.retractSpeed, maxLean)

    def isFinished(self):
        # Hmmm, should we stop if sensor is not indicating that front
        # is over ground?
        return self.climber.isFullyRetractedFront() or not self.climber.isFrontOverGround()


class RetractBackLegs(LiftCommand):
    """ Command that retracts the back legs once drive wheels are on top platform. """
    def __init__(self):
        super().__init__("RetractBackLegs")

    def execute(self):
        # Retract both legs (keep them up)
        maxLean = 5.0
        self.climber.moveBackLegs(self.retractSpeed, maxLean)
        self.climber.moveFrontLegs(self.retractSpeed, maxLean)

    def isFinished(self):
        # Hmmm, should we stop if sensor is not indicating that back
        # is over ground?
        return self.climber.isFullyRetractedBack() or not self.climber.isBackOverGround()


class DriveToFrontSensor(LiftCommand):
    """ Command that drives forward until the front sensor is over ground. """
    def __init__(self):
        super().__init__("DriveToFrontSensor")

    def execute(self):
        self.climber.wheelForward()
        # Keep robot level with back legs while driving forward
        self.maintainBackLegs()
        # Should we also be driving main drive wheels?
        # Maybe minimal power so climber wheels don't have to fight
        self.drive.tankDrive(0.15, 0.15)

    def isFinished(self):
        return self.climber.isFrontOverGround()


class DriveToBackSensor(DriveToFrontSensor):
    """ Command that drives forward until the back sensor is over ground. """
    def __init__(self):
        super().__init__()
        self.setName("DriveToBackSensor")

    def isFinished(self):
        return self.climber.isBackOverGround()


class ClimbUp(CommandGroup):
    """
    Command that takes robot from facing podium all the way
    so that it is on top the podium.
    """
    def __init__(self):
        self.addSequential(ExtendBothLegs())
        self.addSequential(DriveToFrontSensor())
        self.addSequential(RetractFrontLegs())
        self.addSequential(DriveToBackSensor())
        self.addSequential(RetractBackLegs())
        # TODO: Determine command to drive rest of way
