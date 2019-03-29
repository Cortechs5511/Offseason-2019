from wpilib import SmartDashboard
from wpilib import DigitalInput

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

from wpilib import Spark

import oi
import map

class Climber():

    def initialize(self, robot):
        self.robot = robot
        self.xbox = oi.getJoystick(2)
        self.joystick0 = oi.getJoystick(0)

        if map.robotId == map.astroV1:
            '''IDS AND DIRECTIONS FOR V1'''
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
            self.backLift = Talon(map.frontLift)
            self.frontLift = Talon(map.backLift)
            self.frontLift.setInverted(False)
            self.backLift.setInverted(True)

            self.wheelLeft = Talon(map.wheelLeft)
            self.wheelRight = Talon(map.wheelRight)
            self.wheelRight.setInverted(True)
            self.wheelLeft.setInverted(False)

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

        self.started = False

    def periodic(self):

        if self.xbox.getRawButton(map.liftClimber): self.started = True

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

    def isFrontOverGround(self):
        return not self.frontSwitch.get()

    def getLean(self):
        if map.robotId == map.astroV1: return -1* self.robot.drive.getRoll()
        else: return -1 * self.robot.drive.getPitch()

    def backRetracted(self): return not self.isBackOverGround()

    def getCorrection(self):
        return (self.kP * -self.getLean())

    def setSpeeds(self, back, front):
        self.backLift.set(back * self.climbSpeed)
        self.frontLift.set(front * self.climbSpeed)

    def retract(self):
        correction = getCorrection()
        if mode=="front": self.setSpeeds(self.backHold, 1)
        elif mode=="back": self.setSpeed(1, 0)
        elif mode=="both": self.setSpeeds(1 + correction, 1)
        else: self.setSpeeds(0, 0)

    def extend(self):
        correction = getCorretion()
        if mode=="front": self.setSpeeds(correction, -1)
        elif mode=="back": self.setSpeeds(-1, 0)
        elif mode=="both": self.setSpeeds(-1 + correction, -1)
        else: self.setSpeeds(0, 0)

    def wheel(self, direction):
        '''FORWARD MOVES ROBOT FORWARD, BACKWARD MOVES ROBOT BACKWARD'''
        if direction == "forward":
            self.wheelLeft.set(self.wheelSpeed)
            self.wheelRight.set(self.wheelSpeed)
        elif direction == "backward":
            self.wheelLeft.set(-1 * self.wheelSpeed)
            self.wheelRight.set(-1 * self.wheelSpeed)

        correction = getCorrection()
        self.setSpeeds(self.backHold+correction, 0)

    def stopFront(self):
        if(not self.started): self.frontLift.set(0)
        else: self.frontLift.set(self.frontHold)

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
        SmartDashboard.putNumber("Climber kP", 0.2)
        SmartDashboard.putNumber("ClimbSpeed", 0.5)
        SmartDashboard.putNumber("BackHold", -0.15)
        SmartDashboard.putNumber("FrontHold", -0.15)

    def dashboardPeriodic(self):
        self.climbSpeed = SmartDashboard.getNumber("ClimbSpeed", 0.5)
        self.kP = SmartDashboard.getNumber("Climber kP", 0.2)
        self.backHold = SmartDashboard.getNumber("BackHold", -0.15)
        self.frontHold = SmartDashboard.getNumber("FrontHold", -0.15)
        SmartDashboard.putNumber("Lean", self.getLean())
