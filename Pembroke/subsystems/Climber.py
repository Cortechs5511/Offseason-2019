from wpilib import SmartDashboard
from wpilib import DigitalInput

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

from wpilib import Spark

import oi
import map

class Climber():

    def initialize(self, robot):
        self.usingNeo = True

        self.robot = robot
        self.xbox = oi.getJoystick(2)
        self.joystick0 = oi.getJoystick(0)

        if self.usingNeo:
          # NOTE: If using Spark Max in PWM mode to control Neo brushless
          # motors you MUST configure the speed controllers manually
          # using a USB cable and the Spark Max client software!
          self.frontLift : Spark = Spark(map.frontLiftPwm)
          self.backLift : Spark = Spark(map.backLiftPwm)

        if map.robotId == map.astroV1:
            '''IDS AND DIRECTIONS FOR V1'''
            if not self.usingNeo:
              self.backLift = Talon(map.backLift)
              self.frontLift = Talon(map.frontLift)
              self.frontLift.setInverted(True)
              self.backLift.setInverted(True)

            self.wheelLeft = Victor(map.wheelLeft)
            self.wheelRight = Victor(map.wheelRight)
            self.wheelRight.setInverted(True)
            self.wheelLeft.setInverted(True)

        else:
            '''IDS AND DIRECTIONS FOR V2'''
            if not self.usingNeo:
              self.backLift = Talon(map.frontLift)
              self.frontLift = Talon(map.backLift)
              self.frontSetInverted(True)
              self.backSetInverted(False)

            self.wheelLeft = Talon(map.wheelLeft)
            self.wheelRight = Talon(map.wheelRight)
            self.wheelRight.setInverted(True)
            self.wheelLeft.setInverted(False)

        if not self.usingNeo:
          for motor in [self.backLift, self.frontLift]:
            motor.clearStickyFaults(0)
            motor.setSafetyEnabled(False)
            motor.configContinuousCurrentLimit(30,0) #Amps per motor
            motor.enableCurrentLimit(True)
            motor.configVoltageCompSaturation(10,0) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages

        for motor in [self.wheelLeft, self.wheelRight]:
            motor.clearStickyFaults(0)
            motor.setSafetyEnabled(False)
            motor.setNeutralMode(2)

        self.backSwitch = DigitalInput(map.backBottomSensor)
        self.frontSwitch = DigitalInput(map.frontBottomSensor)

        self.MAX_ANGLE = 2 #degrees
        self.TARGET_ANGLE = 0 #degrees
        self.climbSpeed = 0.85
        self.wheelSpeed = 0.9

        self.backHold = -0.15 #holds back stationary if extended ADJUST**
        self.frontHold = -0.1 #holds front stationary if extended

        self.kP = 0.4 #proportional gain for angle to power

        '''
        NEGATIVE POWER TO ELEVATOR LIFTS ROBOT, LOWERS LEGS
        POSITIVE POWER TO ELEVATOR LOWERS ROBOT, LIFTS LEGS

        NEGATIVE POWER TO WHEELS MOVES ROBOT BACKWARDS
        POSITIVE POWER TO WHEELS MOVES ROBOT FORWARD
        '''

    def periodic(self):
        deadband = 0.50
        frontAxis = self.xbox.getRawAxis(map.liftFrontClimber)
        backAxis = self.xbox.getRawAxis(map.liftBackClimber)

        if abs(frontAxis) > deadband or abs(backAxis):
            if  frontAxis> deadband: self.extend("front")
            elif frontAxis < -deadband: self.retract("front")
            if backAxis > deadband: self.extend("back")
            elif backAxis < -deadband: self.retract("back")
            else: self.extend("hold")
        else:
            if self.xbox.getRawButton(map.lowerClimber) == True: self.retract("both")
            elif self.xbox.getRawButton(map.liftClimber) == True: self.extend("both")
            else: self.extend("hold")

        if self.xbox.getRawButton(map.driveForwardClimber): self.wheel("forward")
        elif self.xbox.getRawButton(map.driveBackwardClimber): self.wheel("backward")
        else: self.stopDrive()

    def isBackOverGround(self):
        return not self.backSwitch.get()

    def getLean(self):
        if map.robotId == map.astroV1: return -1* self.robot.drive.getRoll()
        else: return -1 *  self.robot.drive.getPitch()

    def isLeaning(self, direction):
        '''TRUE TESTS TIPPING FORWARD, FORWARD TIP HAS NEGATIVE ANGLE'''
        maxTarget = self.MAX_ANGLE + self.TARGET_ANGLE
        minTarget = -self.MAX_ANGLE + self.TARGET_ANGLE

        if direction==True and self.getLean() > maxTarget: return True
        elif direction==False and self.getLean() < minTarget: return True
        else: return False

    def backRetracted(self): return not self.isBackOverGround()
    def frontRetracted(self): return not self.isBackOverGround()

    def getCorrection(self):
        '''CORRECTION IS POSITIVE'''
        multiplier = (self.kP * abs(self.getLean()))
        return (multiplier * self.climbSpeed)

    def retract(self, mode):
        cSpeed = self.getCorrection()

        if mode == "front":
            if self.isLeaning(False):
                self.backSet(-1 * cSpeed)
                self.frontSet(self.climbSpeed)
            elif self.isLeaning(True):
                self.backSet(1 * cSpeed)
                self.frontSet(self.climbSpeed)
            else:
                self.stopBack()
                self.frontSet(self.climbSpeed)

        elif mode == "back":
            #if self.isLeaning(False): self.frontSet(cSpeed) , don't correct front
            self.stopFront()
            self.backSet(self.climbSpeed)

        elif mode == "both":
            if self.isLeaning(True):
                self.backSet(1 * cSpeed)
                self.frontSet(self.climbSpeed)
            elif self.isLeaning(False):
                self.backSet(self.climbSpeed)
                self.frontSet(cSpeed)
            else:
                self.backSet(self.climbSpeed)
                self.frontSet(self.climbSpeed)

    def extend(self, mode):
        cSpeed = self.getCorrection()

        if mode == "front":
            if self.isLeaning(False):
                self.backSet(-1 * cSpeed)
                self.frontSet(-self.climbSpeed)
            elif self.isLeaning(True):
                self.backSet(1 * cSpeed)
                self.frontSet(-self.climbSpeed)
            else:
                self.stopBack()
                self.frontSet(-self.climbSpeed)

        elif mode == "back":
            self.stopFront()
            self.backSet(-1 * self.climbSpeed)

        elif mode == "both":
            if self.isLeaning(True):
                self.backSet(-1 * self.climbSpeed)
                self.frontSet(-1 * cSpeed)
            elif self.isLeaning(False):
                self.backSet(-1 * cSpeed)
                self.frontSet(-1 * self.climbSpeed)
            else:
                self.backSet(-1 * self.climbSpeed)
                self.frontSet(-1 * self.climbSpeed)

        elif mode == "hold":
            #if self.isLeaning(False):
                #self.backSet(-0.7 * cSpeed)
                #self.frontSet(0)
            #elif self.isLeaning(True):
                #self.frontSet(-1 * cSpeed)
                #self.backSet(0)

            if self.isBackOverGround():
                self.backSet(0)
                self.frontSet(0)
            else:
                self.stopBack() #sets static speed to hold back up
                self.stopFront()

    def wheel(self, direction):
        '''FORWARD MOVES ROBOT FORWARD, BACKWARD MOVES ROBOT BACKWARD'''
        if direction == "forward":
            self.wheelLeft.set(self.wheelSpeed)
            self.wheelRight.set(self.wheelSpeed)
        elif direction == "backward":
            self.wheelLeft.set(-1 * self.wheelSpeed)
            self.wheelRight.set(-1 * self.wheelSpeed)

        if self.isLeaning(False):
            self.backSet(-1 * self.getCorrection())
            self.stopFront()
        elif self.isLeaning(True):
            self.backSet(self.getCorrection())
            self.stopFront()

    def wheelForward(self):
        self.wheelLeft.set(self.wheelSpeed)
        self.wheelRight.set(self.wheelSpeed)

    def wheelBack(self):
        self.wheelLeft.set(-1 * self.wheelSpeed)
        self.wheelRight.set(-1 * self.wheelSpeed)

    def stopFront(self):
        if(self.frontRetracted()): self.frontSet(0)
        else: self.frontSet(self.frontHold)

    def stopBack(self):
        if(self.backRetracted()): self.backSet(0)
        else: self.backSet(self.backHold)

    def stopClimb(self):
        self.stopFront()
        self.stopBack()

    def stopDrive(self):
        self.wheelLeft.set(0)
        self.wheelRight.set(0)

    def disable(self):
        self.stopClimb()
        self.stopDrive()

    def frontSet(self, power):
        #Negative Power - Legs down
        if self.usingNeo:
            power = -power
        self.frontLift.set(power)

    def backSet(self, power):
        #Negative Power - Legs down
        if self.usingNeo:
            power = -power
        self.backLift.set(power)

    def dashboardInit(self):
        SmartDashboard.putNumber("Climber kP", 0.4)
        SmartDashboard.putNumber("ClimbSpeed", 0.9)

    def dashboardPeriodic(self):
        self.climbSpeed = SmartDashboard.getNumber("ClimbSpeed", 0.9)
        self.kP = SmartDashboard.getNumber("Climber kP", 0.4)
        SmartDashboard.putNumber("Lean", self.getLean())
