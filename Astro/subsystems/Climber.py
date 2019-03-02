import wpilib
from wpilib import SmartDashboard
from wpilib.command.subsystem import Subsystem
from wpilib.command import Command
import wpilib.encoder

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

from commands.climber.liftRobot import LiftRobot
from commands.climber.lowerRobot import LowerRobot
from commands.climber.setSpeedWheel import SetSpeedWheel
from commands.climber.autoClimb import AutoClimb
from subsystems.disableAll import DisableAll
from commands.climber.driveToEdge import DriveToEdge

import math

import map

class Climber(Subsystem):

    # TODO DETERMINE CONVERSION!!!!
    TICKS_TO_INCHES = 1.0 #inches/tick
    MAX_EXTEND = 12.0 #inches

    MAX_ANGLE = 3 #degrees

    climbSpeed = 0.9
    wheelSpeed = 0.7

    def __init__(self, robot):
        super().__init__('Climber')


        self.robot = robot
        self.debug = True
        self.DriveToEdge = DriveToEdge

        timeout = 0
        self.frontsensor = wpilib.AnalogInput(0)
        self.backsensor = wpilib.AnalogInput(1)
        self.backLift = Talon(map.backLift)
        self.frontLift = Talon(map.frontLift)
        self.backLift.setName("Climber", "Back Lift")
        self.frontLift.setName("Climber", "Front Lift")

        if map.robotId == map.astroV1:
            self.frontLift.setInverted(True)
            self.backLift.setInverted(True)
        else:
            self.frontLift.setInverted(True)
            self.backLift.setInverted(True)
        if map.robotId == map.astroV1:
            self.wheelLeft = Victor(map.wheelLeft)
            self.wheelRight = Victor(map.wheelRight)
        elif map.robotId == map.astroV2:
            self.wheelLeft = Talon(map.wheelLeft)
            self.wheelRight = Talon(map.wheelRight)
        self.wheelLeft.setName("Climber", "Wheel Left")
        self.wheelRight.setName("Climber", "Wheel Right")
        if map.robotId == map.astroV1:
            self.wheelRight.setInverted(True)
            self.wheelLeft.setInverted(True)
        elif map.robotId == map.astroV2:
            self.wheelRight.setInverted(True)
            self.wheelLeft.setInverted(False)
        self.switchBottomBack = wpilib.DigitalInput(8)
        self.switchTopFront = wpilib.DigitalInput(7)
        self.switchBottomFront = wpilib.DigitalInput(6)
        self.switchTopBack = wpilib.DigitalInput(9)


        #self.wheels = self.wheelLeft

        self.backLift.setNeutralMode(2)
        self.frontLift.setNeutralMode(2)
        self.wheelLeft.setNeutralMode(2)
        self.wheelRight.setNeutralMode(2)

        for motor in [self.backLift, self.frontLift, self.wheelLeft, self.wheelRight]:
            motor.clearStickyFaults(timeout)
            motor.setSafetyEnabled(False)
            #motor.setExpiration(2 * self.robot.period)

        for motor in [self.backLift, self.frontLift]:
            motor.configContinuousCurrentLimit(20,timeout) #15 Amps per motor
            motor.enableCurrentLimit(True)

            motor.configVoltageCompSaturation(9,timeout) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages

        self.MAX_ROLL = self.returnTolerance()

    def subsystemInit(self):
        r = self.robot

        #SmartDashboard.putData("Drive to Front", self.DriveToEdge("front"))
        #SmartDashboard.putData("Drive to Back", self.DriveToEdge("back"))
        #wheels
        climberWheelsForward : wpilib.buttons.JoystickButton = r.driverLeftButton(7)
        climberWheelsForward.whileHeld(SetSpeedWheel(1))

        climberWheelsBackward : wpilib.buttons.JoystickButton = r.driverLeftButton(8)
        climberWheelsBackward.whileHeld(SetSpeedWheel(-1))

        liftButton : wpilib.buttons.JoystickButton = r.driverLeftButton(9)
        liftButton.whileHeld(LiftRobot("both"))

        liftButton : wpilib.buttons.JoystickButton = r.driverLeftButton(10)
        liftButton.whileHeld(LowerRobot("both"))

        disableAll : wpilib.buttons.JoystickButton = r.operatorButton(9)
        disableAll.whenPressed(DisableAll())

        climberFrontUp : wpilib.buttons.JoystickButton = r.driverLeftButton(13)
        climberFrontUp.whileHeld(LiftRobot("front"))

        climberFrontDown : wpilib.buttons.JoystickButton = r.driverLeftButton(14)
        climberFrontDown.whileHeld(LowerRobot("front"))

        climberBackUp : wpilib.buttons.JoystickButton = r.driverLeftButton(12)
        climberBackUp.whileHeld(LiftRobot("back"))

        climberBackDown : wpilib.buttons.JoystickButton = r.driverLeftButton(15)
        climberBackDown.whileHeld(LowerRobot("back"))

        autoClimbButton : wpilib.buttons.JoystickButton = r.operatorButton(7)
        autoClimbButton.whenPressed(AutoClimb())

        killautoClimbButton : wpilib.buttons.JoystickButton = r.operatorButton(8)
        killautoClimbButton.whenPressed(self.disable())

    def getPitch(self):
        '''negative is leaning forward on V2'''
        return self.robot.drive.pitch

    def getRoll(self):
        return self.robot.drive.roll

    def getHeightFront(self):
        """ this will return the height in inches from encoder """
        #ticks = self.frontLift.getQuadraturePosition()
        #return ticks * self.TICKS_TO_INCHES
        return 0 #temp

    def getHeightBack(self):
        """ this will return the height in inches from encoder """
        #ticks = self.backLift.getQuadraturePosition()
        #return ticks * self.TICKS_TO_INCHES
        return 0 #temp

    def isFullyExtendedFront(self):
        """ tells us if the front is fully extended """
        #return self.getHeightFront() >= self.MAX_EXTEND
        return not self.switchTopFront.get()

    def isFullyExtendedBack(self):
        """ tells us if the back is fully extended, so it can stop """
        #return self.getHeightBack() >= self.MAX_EXTEND
        return not self.switchTopBack.get()

    def isFullyRetractedFront(self):
        return not self.switchBottomFront.get()

    def isFullyRetractedBack(self):
        return not self.switchBottomBack.get()


    def isFullyExtendedBoth(self):
        """ tells us if both front and back are fully extended, so it can stop """
        return self.isFullyExtendedFront() and self.isFullyExtendedBack()

    def isFullyRetractedBoth(self):
        """ tells us if both front and back are fully extended, so it can stop """
        return self.isFullyRetractedFront() and self.isFullyRetractedBack()

    def isLeaning(self, direction):
        '''true checking tip forward'''
        if direction == True and self.getLean()+1 < -self.MAX_ANGLE :
            return True
        elif direction == False and self.getLean()-1 > self.MAX_ANGLE :
            return True
        else:
            return False

    def getLean(self):
        if map.robotId == map.astroV1:
            return self.getRoll()
        else:
            return self.getPitch()

    def isFrontOverGround(self):
        if self.frontsensor.getVoltage() < 1.5:
            return True
        else:
            return False

    def isBackOverGround(self):
        if self.backsensor.getVoltage() < 1.5:
            return True
        else:
            return False

    #wheel speed
    def wheelForward(self):
        self.wheelLeft.set(self.returnWheelSpeed())
        self.wheelRight.set(self.returnWheelSpeed())

    def wheelBack(self):
        self.wheelLeft.set(-1 * self.returnWheelSpeed())
        self.wheelRight.set(-1 * self.returnWheelSpeed())

    def stopFront(self): self.frontLift.set(0)
    def stopBack(self): self.backLift.set(0)

    def stop(self):
        self.stopFront()
        self.stopBack()

    def stopDrive(self):
        self.wheelLeft.set(0)
        self.wheelRight.set(0)

    def disable(self):
        self.stopFront()
        self.stopBack()
        self.stopDrive()

    def dashboardInit(self):
        SmartDashboard.putNumber("ClimberSpeed", 0.9)
        SmartDashboard.putNumber("WheelSpeed", 0.7)

        SmartDashboard.putNumber("Tolerance", 2)

        SmartDashboard.putData("Lift Robot", LiftRobot("both"))
        SmartDashboard.putData("Drive To Edge, Front", DriveToEdge("front"))
        SmartDashboard.putData("Drive To Edge, Back", DriveToEdge("back"))
        SmartDashboard.putData("Lift Robot, Front", LiftRobot("front"))
        SmartDashboard.putData("Lift Robot, Back", LiftRobot("back"))

        #SmartDashboard.putData("Lower Robot", LowerRobot("both"))

    def dashboardPeriodic(self):
        self.MAX_ANGLE = self.returnTolerance()
        self.returnWheelSpeed()
        self.returnClimbSpeed()
        SmartDashboard.putNumber("Lean", self.getLean())

        if self.debug == True:
            SmartDashboard.putBoolean("Fully Extended Front",self.isFullyExtendedFront())
            SmartDashboard.putBoolean("Fully Extended Back",self.isFullyExtendedBack())
            SmartDashboard.putBoolean("Fully Retracted Front",self.isFullyRetractedFront())
            SmartDashboard.putBoolean("Fully Retracted Back",self.isFullyRetractedBack())
            #SmartDashboard.putNumber("FrontTicks", self.getHeightFront())
            #SmartDashboard.putNumber("BackTicks", self.getHeightBack())
            #SmartDashboard.putData("Lean", self.isLeaning())

    def returnCorrectionSpeed(self):
        #proportional speed based on angle
        lean = self.getLean()
        targetAngle = 1
        lean += targetAngle
        error = math.fabs(lean)
        pGain = 0.5
        if lean < -self.MAX_ANGLE:
            return error * pGain
        elif lean > self.MAX_ANGLE:
            return error * -pGain
        else:
            return self.returnClimbSpeed()

    def returnClimbSpeed(self):
        self.climbSpeed = SmartDashboard.getNumber("ClimberSpeed", 0.9)
        return self.climbSpeed

    def returnWheelSpeed(self):
        self.wheelSpeed = SmartDashboard.getNumber("WheelSpeed", 0.7)
        return self.wheelSpeed

    def returnTolerance(self):
        self.tolerance = SmartDashboard.getNumber("Tolerance", 2)
        return self.tolerance
