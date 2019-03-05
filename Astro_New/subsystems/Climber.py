import wpilib
from wpilib import SmartDashboard
import wpilib.encoder
import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor
import math
import map
from subsystems import Sensors
import navx

class Climber():
    def climberInit(self):
        timeout = 0
        self.debug = False
        self.joystick = map.getJoystick(0)
        self.navx = navx.AHRS.create_spi()
        self.MAX_ANGLE = 3

        self.pitch = 0
        self.roll = 0
        self.frontSensor = wpilib.AnalogInput(map.frontSensor)
        self.backSensor = wpilib.AnalogInput(map.backSensor)
        self.switchBottomBack = wpilib.DigitalInput(map.backBottomSensor)
        self.switchTopFront = wpilib.DigitalInput(map.frontTopSensor)
        self.switchBottomFront = wpilib.DigitalInput(map.frontBottomSensor)
        self.switchTopBack = wpilib.DigitalInput(map.backTopSensor)

        if map.robotId == map.astroV1:
            self.wheelLeft = Victor(map.wheelLeft)
            self.wheelRight = Victor(map.wheelRight)
        elif map.robotId == map.astroV2:
            self.wheelLeft = Talon(map.wheelLeft)
            self.wheelRight = Talon(map.wheelRight)
        self.backLift = Talon(map.backLift)
        self.frontLift = Talon(map.frontLift)
        if map.robotId == map.astroV1:
            self.frontLift.setInverted(True)
            self.backLift.setInverted(True)
        else:
            self.frontLift.setInverted(False)
            self.backLift.setInverted(True)
        if map.robotId == map.astroV1:
            self.wheelRight.setInverted(True)
            self.wheelLeft.setInverted(True)
        elif map.robotId == map.astroV2:
            self.wheelRight.setInverted(True)
            self.wheelLeft.setInverted(False)
        for motor in [self.backLift, self.frontLift, self.wheelLeft, self.wheelRight]:
            motor.clearStickyFaults(timeout)
            #motor.setSafetyEnabled(True)
            motor.setSafetyEnabled(False)
        for motor in [self.backLift, self.frontLift]:
            motor.configContinuousCurrentLimit(20,timeout) #15 Amps per motor
            motor.enableCurrentLimit(True)
            motor.configVoltageCompSaturation(9,timeout) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages
        self.backLift.setNeutralMode(2)
        self.frontLift.setNeutralMode(2)
        self.wheelLeft.setNeutralMode(2)
        self.wheelRight.setNeutralMode(2)

        self.backLift.setName("Climber", "Back Lift")
        self.frontLift.setName("Climber", "Front Lift")
        self.wheelLeft.setName("Climber", "Wheel Left")
        self.wheelRight.setName("Climber", "Wheel Right")

    def climberPeriodic(self):
        lean = self.getLean()
        if self.joystick.getRawButton(map.lowerFrontClimber) == True:
            self.lower("front")
        elif self.joystick.getRawButton(map.lowerBackClimber) == True:
            self.lower("back")
        elif self.joystick.getRawButton(map.lowerClimber) == True:
            self.lower("both")
        elif self.joystick.getRawButton(map.liftFrontClimber) == True:
            self.lift("front")
        elif self.joystick.getRawButton(map.liftBackClimber) == True:
            self.lift("back")
        elif self.joystick.getRawButton(map.liftClimber) == True:
            self.lift("both")
        else:
            self.stopFront()
            self.stopBack()

        self.sensorAnglePeriodic()

        #AUTOCLIMB
        if self.joystick.getRawButton(map.autoClimb):
            state = self.getState()
            if state == 0:
                self.lift("both")
            elif state == 1:
                self.wheel("forward")
            elif state == 2:
                self.lift("front")
            elif state == 3:
                self.wheel("forward")
            elif state == 4:
                self.lift("back")
            else:
                pass
    #LOGIC AND SENSOR FEEDBACK

    # lift and lower are in terms of legs
    def lift(self, mode):
        if mode == "front":
            if self.isLeaning(True):
                self.backLift.set(self.returnCorrectionSpeed())
            else:
                self.stopBack()
            self.frontLift.set(self.returnClimbSpeed())
        elif mode == "back":
            self.frontLift.set(0)
            self.backLift.set(self.returnClimbSpeed())
        elif mode == "both":
            if self.isLeaning(True):
                self.backLift.set(self.returnCorrectionSpeed())
                self.frontLift.set(self.returnClimbSpeed())
            elif self.isLeaning(False):
                self.backLift.set(self.returnClimbSpeed())
                self.frontLift.set(self.returnCorrectionSpeed())
            else:
                self.backLift.set(self.returnClimbSpeed())
                self.frontLift.set(self.returnClimbSpeed())


    def lower(self, mode):
        if mode == "front":
            if self.isLeaning(True):
                self.backLift.set(self.returnCorrectionSpeed())
            else:
                self.stopBack()
            self.frontLift.set(self.returnClimbSpeed())
        elif mode == "back":
            self.frontLift.set(0)
            self.backLift.set(-1* self.returnClimbSpeed())
        elif mode == "both":
            if self.isLeaning(False):
                self.backLift.set(-1 * self.returnCorrectionSpeed())
                self.frontLift.set(-1 * self.returnClimbSpeed())
            elif self.isLeaning(True):
                self.backLift.set(-1 * self.returnClimbSpeed())
                self.frontLift.set(-1 * self.returnCorrectionSpeed())
            else:
                self.backLift.set(-1 * self.returnClimbSpeed())
                self.frontLift.set(-1 * self.returnClimbSpeed())

    def sensorAnglePeriodic(self):
        self.pitch = self.navx.getPitch()
        self.roll = self.navx.getRoll()

    def getPitch(self):
        '''negative is leaning forward V2'''
        return self.pitch
        #return 0

    def getRoll(self):
        '''negative is leaning forward V1'''
        return self.roll
        #return 0

    def isFullyExtendedFront(self):
        """ tells us if the front is fully extended """
        return not self.switchTopFront.get()

    def isFullyExtendedBack(self):
        """ tells us if the back is fully extended, so it can stop """
        return not self.switchTopBack.get()

    def isFullyRetractedFront(self):
        """ tells us if the front is fully retracted """
        return not self.switchBottomFront.get()

    def isFullyRetractedBack(self):
        """ tells us if the back is fully retracted, so it can stop """
        return not self.switchBottomBack.get()

    def isFullyExtendedBoth(self):
        """ tells us if both front and back are fully extended, so it can stop """
        return self.isFullyExtendedFront() and self.isFullyExtendedBack()

    def isFullyRetractedBoth(self):
        """ tells us if both front and back are fully extended, so it can stop """
        return self.isFullyRetractedFront() and self.isFullyRetractedBack()

    def getLean(self):
        if map.robotId == map.astroV1:
            return self.navx.getRoll()
        else:
            return self.getPitch()

    def isLeaning(self, direction):
        '''true checking tip forward'''
        if direction == True and self.getLean()+1 < -self.MAX_ANGLE :
            return True
        elif direction == False and self.getLean()-1 > self.MAX_ANGLE :
            return True
        else:
            return False

    def isFrontOverGround(self):
        if self.frontSensor.getVoltage() < 1.5:
            return True
        else:
            return False

    def isBackOverGround(self):
        if self.backSensor.getVoltage() < 1.5:
            return True
        else:
            return False

    #SET SPEED CLIMBER

    def wheel(self, direction):
        if direction == "forward":
            self.wheelLeft.set(self.returnWheelSpeed())
            self.wheelRight.set(self.returnWheelSpeed())
        elif direction == "backward":
            self.wheelLeft.set(-1 * self.returnWheelSpeed())
            self.wheelRight.set(-1 * self.returnWheelSpeed())

        if self.isLeaning(False):
            self.backLift.set(-1 * self.returnCorrectionSpeed())
            self.stopFront()
        elif self.isLeaning(True):
            self.backLift.set(self.returnCorrectionSpeed())
            self.stopFront()


    def returnCorrectionSpeed(self):
        #proportional speed based on angle
        targetAngle = -1
        lean = self.getLean()
        error = lean - targetAngle
        multiplier = 1 - (0.1 * math.fabs(error))
        return (multiplier * self.returnClimbSpeed())
    #DISABLE FUNCTION

    def stopFront(self):
        self.frontLift.set(0)

    def stopBack(self):
        self.backLift.set(0)

    def stop(self):
        self.stopFront()
        self.stopBack()

    def stopDrive(self):
        self.wheelLeft.set(0)
        self.wheelRight.set(0)

    def disable(self):
        self.stop()
        self.stopDrive()

    #SYSTEM SPEEDS FROM DASHBOARD

    def returnClimbSpeed(self):
        self.climbSpeed = SmartDashboard.getNumber("ClimberSpeed", 0.9)
        return self.climbSpeed

    def returnWheelSpeed(self):
        self.wheelSpeed = SmartDashboard.getNumber("WheelSpeed", 0.7)
        return self.wheelSpeed

    def returnTolerance(self):
        self.tolerance = SmartDashboard.getNumber("Tolerance", 2)
        return self.tolerance

    #AUTO CLIMB HELPERS

    def getState(self):
        """ *state 1 - robot is fully up and legs are Extended
        *state 2 - robot front is over platform
        *state 3 - robot front legs are Retracted
        state 4 - robot back is over platform
        *state 5 - robot back legs are fully retracted
        state 6 - something is wrong"""
        if self.isFullyRetractedBoth():
            state = 0
        if self.isFullyExtendedBoth():
            state = 1
        elif self.isFullyExtendedBoth() and self.isFrontOverGround():
            state = 2
        elif self.isFullyRetractedFront() and self.isFrontOverGround():
            state = 3
        elif self.isFrontOverGround() and self.isBackOverGround() and self.isFullyRetractedBack():
            state = 5
        elif self.isFrontOverGround() and self.isBackOverGround():
            state = 4
        else:
            state = 6

    #DASHBOARD FUNCTIONS

    def updateDashboardInit(self):
        SmartDashboard.putNumber("ClimberSpeed", 0.9)
        SmartDashboard.putNumber("WheelSpeed", 0.7)
        SmartDashboard.putNumber("Tolerance", 2)

    def updateDashboardPeriodic(self):
        self.returnWheelSpeed()
        self.returnClimbSpeed()
        SmartDashboard.putNumber("Lean", self.getLean())

        if self.debug == True:
            SmartDashboard.putBoolean("Fully Extended Front",self.isFullyExtendedFront())
            SmartDashboard.putBoolean("Fully Extended Back",self.isFullyExtendedBack())
            SmartDashboard.putBoolean("Fully Retracted Front",self.isFullyRetractedFront())
            SmartDashboard.putBoolean("Fully Retracted Back",self.isFullyRetractedBack())
