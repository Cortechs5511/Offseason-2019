import math
import ctre
import wpilib
from wpilib import SmartDashboard
from wpilib.command.subsystem import Subsystem
from wpilib.command import Command
from wpilib import SmartDashboard as sd

class FlipButton(Command):
    def __init__(self):
        super().__init__('Flip')
        robot = self.getRobot()
        self.driveMech = robot.driveMech

    def initialize(self):
        pass

    def execute(self):

        if self.driveMech.flipped:
            self.driveMech.flipped = False
        else:
            self.driveMech.flipped = True

    def interrupted(self):
        self.end()

    def end(self):
        pass
      #  self.driveMechanism.stopDrive()

    def isFinished(self):
        return True

class DriveMode(Command):
    def __init__(self):
        super().__init__('Drivemode')
        robot = self.getRobot()
        self.driveMech = robot.driveMech

    def initialize(self):
        pass

    def execute(self):

        if self.driveMech.tankMode:
            self.driveMech.tankMode = False
        else:
            self.driveMech.tankMode = True
    def interrupted(self):
        self.end()

    def end(self):
        pass
      #  self.driveMechanism.stopDrive()

    def isFinished(self):
        return True
class HumanDrive(Command):

    def __init__(self):
        super().__init__('driveMech')
        self.robot = self.getRobot()
        self.driveMech = self.robot.driveMech
        self.requires(self.driveMech)

    def initialize(self):
        pass

    def execute(self):

        leftSpeed, rightSpeed = self.robot.getTankValues()
        if self.driveMech.flipped:
            oldLeft = leftSpeed
            leftSpeed = -rightSpeed
            rightSpeed = -oldLeft
        self.driveMech.drive(leftSpeed, rightSpeed)

    def interrupted(self):
        self.end()

    def end(self):
        self.driveMech.stopDrive()

    def isFinished(self):
        return False

class DriveMech(Subsystem):

    def __init__(self, robot):

        """ Create all physical parts used by subsystem. """
        super().__init__('Drive')
        # Set to true for extra info to smart dashboard
        self.debug = True
        self.woodrow = True
        self.flipped = False
        self.tankMode = True
        self.robot = robot

        if self.woodrow:
            L1 = wpilib.VictorSP(0)
            L2 = wpilib.VictorSP(1)
            R1 = wpilib.VictorSP(2)
            R2 = wpilib.VictorSP(3)
            self.driveLeft1 = wpilib.SpeedControllerGroup(L1, L2)
            self.driveRight1 = wpilib.SpeedControllerGroup(R1, R2)


        else:
            self.driveLeft1 = ctre.WPI_TalonSRX(10)
            self.driveLeft2 = ctre.WPI_VictorSPX(11)
            self.driveLeft3 = ctre.WPI_VictorSPX(12)
            self.leftEncoder = wpilib.Encoder(0,1)
            self.rightEncoder = wpilib.Encoder(2,3)
            self.driveRight1 = ctre.WPI_TalonSRX(20)
            self.driveRight2 = ctre.WPI_VictorSPX(21)
            self.driveRight3 = ctre.WPI_VictorSPX(22)
            self.driveLeft2.follow(self.driveLeft1)
            self.driveLeft3.follow(self.driveLeft1)
            self.driveRight2.follow(self.driveRight1)
            self.driveRight3.follow(self.driveRight1)
    #   self.driveLeft1.setInverted(True)
     #   self.driveRight1.setInverted(True)


    def drive(self, leftSpeed, rightSpeed):

        if self.woodrow:
            self.driveLeft1.set(-leftSpeed)
            self.driveRight1.set(rightSpeed)
        else:
            self.driveLeft1.set(-leftSpeed)
            self.driveRight1.set(-rightSpeed)



    def stopDrive(self):
        self.drive(0,0)

    def disable(self):
        """ Disables subsystem and puts everything back to starting position. """
        self.stopDrive()

    def updateDashboard(self):
        """ Put diagnostics out to smart dashboard. """
        SmartDashboard.putBoolean("Driving Reverse", self.flipped)
        SmartDashboard.putBoolean("Tank Mode", self.tankMode)
        if self.debug:
           #   SmartDashboard.putNumber("leftEncoder", self.leftEncoder.getRaw())
            #  SmartDashboard.putNumber("rightEncoder", self.rightEncoder.getRaw())
             # SmartDashboard.putNumber("leftEncoderdistance", self.leftEncoder.getDistance())
              #SmartDashboard.putNumber("rightEncoderdistacne", self.rightEncoder.getDistance())
              if not self.woodrow:
                SmartDashboard.putNumber("talonEncoder", self.driveLeft1.getQuadraturePosition())

    def subsystemInit(self):
        """ Adds subsystem specific commands. """
        if self.debug:
            SmartDashboard.putData("Flipped drive", FlipButton())
        b = self.robot.driverRightButton(2)
        b.whenPressed(FlipButton())
        self.setDefaultCommand(HumanDrive())
        SmartDashboard.putData("Tank Mode", DriveMode())
