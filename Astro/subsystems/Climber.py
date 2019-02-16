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

import map

class Climber(Subsystem):

    # TODO DETERMINE CONVERSION!!!!
    TICKS_TO_INCHES = 1.0 #inches/tick
    MAX_EXTEND = 12.0 #inches

    #MAX_ROLL = 5 #degrees

    climbSpeed = 0.25

    def __init__(self, robot):
        super().__init__('Climber')

        self.robot = robot
        self.debug = True

        timeout = 0
        self.frontsensor = wpilib.AnalogInput(0)
        self.backsensor = wpilib.AnalogInput(1)
        self.backLift = Talon(map.backLift)
        self.frontLift = Talon(map.frontLift)
        self.frontLift.setInverted(True)
        self.backLift.setInverted(True)
        self.wheelLeft = Victor(map.wheelLeft)
        self.wheelRight = Victor(map.wheelRight)
        self.switchTopFront = wpilib.DigitalInput(7)
        self.switchBottomFront = wpilib.DigitalInput(8)
        self.switchTopBack = wpilib.DigitalInput(9)
        #self.switchBottomBack = wpilib.DigitalInput(3)

        self.wheelRight.follow(self.wheelLeft)
        self.wheels = self.wheelLeft

        self.backLift.setNeutralMode(2)
        self.frontLift.setNeutralMode(2)
        self.wheelLeft.setNeutralMode(2)
        self.wheelRight.setNeutralMode(2)

        for motor in [self.backLift, self.frontLift, self.wheelLeft, self.wheelRight]:
            motor.clearStickyFaults(timeout)
            motor.setSafetyEnabled(False)
            motor.setInverted(False)

        for motor in [self.backLift, self.frontLift]:
            motor.configContinuousCurrentLimit(20,timeout) #15 Amps per motor
            motor.enableCurrentLimit(True)

            motor.configVoltageCompSaturation(9,timeout) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages

        self.MAX_ROLL = self.returnTolerance()

    def subsystemInit(self):
        r = self.robot

        SmartDashboard.putData("Drive to Front", self.DriveToEdge("Front"))
        SmartDashboard.putData("Drive to Back", self.DriveToEdge("Back"))
        #wheels
        climberWheelsForward : wpilib.buttons.JoystickButton = r.driverLeftButton(7)
        climberWheelsForward.whileHeld(SetSpeedWheel(1))

        climberWheelsBackward : wpilib.buttons.JoystickButton = r.driverLeftButton(8)
        climberWheelsBackward.whileHeld(SetSpeedWheel(-1))

        liftButton : wpilib.buttons.JoystickButton = r.driverLeftButton(9)
        liftButton.whileHeld(LiftRobot("both"))

        liftButton : wpilib.buttons.JoystickButton = r.driverLeftButton(10)
        liftButton.whileHeld(LowerRobot("both"))

        climberFrontUp : wpilib.buttons.JoystickButton = r.driverLeftButton(13)
        climberFrontUp.whileHeld(LiftRobot("front"))

        climberFrontDown : wpilib.buttons.JoystickButton = r.driverLeftButton(14)
        climberFrontDown.whileHeld(LowerRobot("front"))

        climberBackUp : wpilib.buttons.JoystickButton = r.driverLeftButton(12)
        climberBackUp.whileHeld(LiftRobot("back"))

        climberBackDown : wpilib.buttons.JoystickButton = r.driverLeftButton(15)
        climberBackDown.whileHeld(LowerRobot("back"))

    def getPitch(self):
        return self.robot.drive.pitch #negate here if pitch is backwards of expected

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
        #return self.switchTopFront.get()
        return False

    def isFullyExtendedBack(self):
        """ tells us if the back is fully extended, so it can stop """
        #return self.getHeightBack() >= self.MAX_EXTEND
        #return self.switchTopBack.get()
        return False

    def isFullyRetractedFront(self):
        #return self.switchBottomFront.get()
        return False

    def isFullyRetractedBack(self):
        #return self.switchBottomBack.get()
        return False

    def isFullyExtendedBoth(self):
        """ tells us if both front and back are fully extended, so it can stop """
        return self.isFullyExtendedFront() and self.isFullyExtendedBack()

    def isLeaning(self, direction):
        '''true checking tip forward'''
        if direction == True and self.getRoll() < -self.MAX_ROLL :
            return True
        elif direction == False and self.getRoll() > self.MAX_ROLL :
            return True
        else:
            return False

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
    #functions for lift
    def liftFront(self, lift, single):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down(extend) """

        if self.isFullyExtendedFront() and lift/abs(lift) == 1 : self.stopFront()
        elif self.isFullyRetractedFront() and lift/abs(lift) == -1 : self.stopFront()
        elif single and self.isLeaning(False): self.backLift.set(0.5)
        elif single and self.isLeaning(True): self.backLift.set(-0.5)
        elif self.isLeaning(False): self.stopFront()
        else: self.frontLift.set(1.1*lift)

    def liftBack(self, lift, single):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down """

        if self.isFullyExtendedBack() and lift/abs(lift) == 1 : self.stopBack()
        elif self.isFullyRetractedBack() and lift/abs(lift) == -1 : self.stopBack()
        elif single and self.isLeaning(False): self.frontLift.set(0.5)
        elif single and self.isLeaning(True): self.frontLift.set(-0.5)
        elif self.isLeaning(True): self.stopBack()
        else: self.backLift.set(lift)

    def lift(self, lift):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down(extend) """
        self.liftFront(lift, False)
        self.liftBack(lift, False)

    #wheel speed
    def wheelForward(self): self.wheels.set(self.returnClimbSpeed())
    def wheelBack(self): self.wheels.set(-1 * self.returnClimbSpeed())

    def stopFront(self): self.frontLift.set(0)
    def stopBack(self): self.backLift.set(0)

    def stop(self):
        self.stopFront()
        self.stopBack()

    def stopDrive(self): self.wheels.set(0)

    def disable(self):
        self.stopFront()
        self.stopBack()
        self.stopDrive()

    def dashboardInit(self):
        SmartDashboard.putNumber("ClimberSpeed", 1)
        SmartDashboard.putNumber("Tolerance", 2)
        SmartDashboard.putData("Lift Robot", LiftRobot("both"))
        SmartDashboard.putData("Lower Robot", LowerRobot("both"))

    def dashboardPeriodic(self):
        if self.debug == True:
            SmartDashboard.putBoolean("Sensor1",self.isFullyExtendedFront())
            SmartDashboard.putBoolean("Sensor2",self.isFullyExtendedBack())
            SmartDashboard.putBoolean("Sensor3",self.isFullyRetractedFront())
            SmartDashboard.putNumber("Pitch", self.getPitch())
            SmartDashboard.putNumber("FrontTicks", self.getHeightFront())
            SmartDashboard.putNumber("BackTicks", self.getHeightBack())

    def returnClimbSpeed(self):
        self.climbSpeed = SmartDashboard.getNumber("ClimberSpeed", 0.9)
        return self.climbSpeed

    def returnTolerance(self):
        self.tolerance = SmartDashboard.getNumber("Tolerance", 2)
        return self.tolerance
