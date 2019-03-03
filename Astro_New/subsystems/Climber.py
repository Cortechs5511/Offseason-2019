import wpilib
from wpilib import SmartDashboard
import wpilib.encoder
import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor
import math
import map

class Climber():

    def climberInit(self):

        timeout = 0
        self.xbox = map.getJoystick(2)

        #SENSORS
        self.frontSensor = wpilib.AnalogInput(0)
        self.backSensor = wpilib.AnalogInput(1)
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

        #LIFT MOTORS
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
            motor.setSafetyEnabled(True)

        for motor in [self.backLift, self.frontLift]:
            motor.configContinuousCurrentLimit(20,timeout) #15 Amps per motor
            motor.enableCurrentLimit(True)
            motor.configVoltageCompSaturation(9,timeout) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages

        self.backLift.setName("Climber", "Back Lift")
        self.frontLift.setName("Climber", "Front Lift")
        self.wheelLeft.setName("Climber", "Wheel Left")
        self.wheelRight.setName("Climber", "Wheel Right")

        self.backLift.setNeutralMode(2)
        self.frontLift.setNeutralMode(2)
        self.wheelLeft.setNeutralMode(2)
        self.wheelRight.setNeutralMode(2)



    def climberPeriodic(self):
        lean = self.getLean()
        #BUTTONS
        #lower climber legs
        if self.xbox.getRawButton(map.lowerFrontClimber) == True:
            self.lowerFront()
        elif self.xbox.getRawButton(map.lowerBackClimber) == True:
            self.lowerBack()
        elif self.xbox.getRawButton(map.lowerClimber) == True:
            self.lowerBoth()
        #lift climber legs
        elif self.xbox.getRawButton(map.liftFrontClimber) == True:
            self.liftFront()
        elif self.xbox.getRawButton(map.liftBackClimber) == True:
            self.liftBoth()
        elif self.xbox.getRawButton(map.liftClimber) == True:
            self.liftBoth()
        else:
            stopFront()
            stopBack()

        #AUTOCLIMB
        if self.xbox.getRawButton(map.autoClimb):
            state = self.getState()
            if state == 0:
                self.liftBoth()
            elif state == 1:
                self.wheelForward()
            elif state == 2:
                self.liftFront()
            elif state == 3:
                self.wheelForward()
            elif state == 4:
                self.liftBack()
            else:
                pass
    #LOGIC AND SENSOR FEEDBACK

    # lift and lower are in terms of legs
    def liftFront(self):
        self.backLift.set(0)
        self.frontLift.set(self.returnClimbSpeed())

    def liftBack(self):
        self.frontLift.set(0)
        self.backLift.set(self.returnClimbSpeed())

    def liftBoth(self):
        if self.isLeaning(False) or self.isLeaning(True):
            self.backLift.set(self.returnCorrectionSpeed())
            self.frontLift.set(self.returnCorrectionSpeed())
        else:
            self.frontLift.set(self.returnClimbSpeed())
            self.backLift.set(self.returnClimbSpeed())

    def lowerFront(self):
        self.backLift.set(0)
        self.frontLift.set(-1 * self.returnClimbSpeed())

    def lowerBack(self):
        self.frontLift.set(0)
        self.backLift.set(-1* self.returnClimbSpeed())

    def lowerBoth(self):
        if self.isLeaning(False) or self.isLeaning(True):
            self.backLift.set(self.returnCorrectionSpeed())
            self.frontLift.set(self.returnCorrectionSpeed())
        else:
            self.frontLift.set(-1 * self.returnClimbSpeed())
            self.backLift.set(-1 *self.returnClimbSpeed())

    def getPitch(self):
        '''negative is leaning forward V2'''
        return self.robot.drive.pitch


    def getRoll(self):
        '''negative is leaning forward V1'''
        return self.robot.drive.roll

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
            return self.getRoll()
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

    def wheelForward(self):
        self.wheelLeft.set(self.returnWheelSpeed())
        self.wheelRight.set(self.returnWheelSpeed())

    def wheelBack(self):
        self.wheelLeft.set(-1 * self.returnWheelSpeed())
        self.wheelRight.set(-1 * self.returnWheelSpeed())

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

    #DISABLE FUNCTION

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
        if isFullyRetractedBoth():
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

    def dashboardInit(self):
        SmartDashboard.putNumber("ClimberSpeed", 0.9)
        SmartDashboard.putNumber("WheelSpeed", 0.7)
        SmartDashboard.putNumber("Tolerance", 2)

    def dashboardPeriodic(self):
        self.returnWheelSpeed()
        self.returnClimbSpeed()
        SmartDashboard.putNumber("Lean", self.getLean())

        if self.debug == True:
            SmartDashboard.putBoolean("Fully Extended Front",self.isFullyExtendedFront())
            SmartDashboard.putBoolean("Fully Extended Back",self.isFullyExtendedBack())
            SmartDashboard.putBoolean("Fully Retracted Front",self.isFullyRetractedFront())
            SmartDashboard.putBoolean("Fully Retracted Back",self.isFullyRetractedBack())
