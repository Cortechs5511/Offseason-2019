from wpilib import SmartDashboard
from wpilib import DigitalInput

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

from wpilib import Spark

import oi
import map

class Climber():

    def initialize(self, robot):
        self.state = -1
        self.robot = robot
        self.xbox = oi.getJoystick(2)
        self.joystick0 = oi.getJoystick(0)
        self.usingNeo = True

        if self.usingNeo:
          # NOTE: If using Spark Max in PWM mode to control Neo brushless
          # motors you MUST configure the speed controllers manually
          # using a USB cable and the Spark Max client software!
          self.frontLift : Spark = Spark(map.frontLiftPwm)
          self.backLift : Spark = Spark(map.backLiftPwm)
          self.frontLift.setInverted(False)
          self.backLift.setInverted(False)

        if map.robotId == map.astroV1:
            if not self.usingNeo:
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
            if not self.usingNeo:
                '''IDS AND DIRECTIONS FOR V2'''
                self.backLift = Talon(map.frontLift)
                self.frontLift = Talon(map.backLift)
                self.frontLift.setInverted(False)
                self.backLift.setInverted(False)
                self.backLift.setNeutralMode(2)
                self.frontLift.setNeutralMode(2)

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

        self.backSwitch = DigitalInput(map.backFloor)
        self.frontSwitch = DigitalInput(map.frontFloor)

        self.switchTopBack = DigitalInput(map.backTopSensor)
        self.switchTopFront = DigitalInput(map.frontTopSensor)

        self.switchBottomBack = DigitalInput(map.backBottomSensor)
        self.switchBottomFront = DigitalInput(map.frontBottomSensor)

        self.MAX_ANGLE = 2 #degrees
        self.TARGET_ANGLE = -1 #degrees
        self.climbSpeed = 0.9
        self.wheelSpeed = 0.9

        self.backHold = -0.12 #holds back stationary if extended ADJUST**
        self.frontHold = -0.12 #holds front stationary if extended

        self.kP = 0.35 #proportional gain for angle to power

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

        if abs(frontAxis) > deadband or abs(backAxis) > deadband:
            if  frontAxis> deadband: self.extend("front")
            elif frontAxis < -deadband: self.retract("front")

            if backAxis > deadband: self.extend("back")
            elif backAxis < -deadband: self.retract("back")
        else:
            if self.xbox.getRawButton(map.lowerClimber) == True: self.retract("both")
            elif self.xbox.getRawButton(map.liftClimber) == True: self.extend("both")
            else:
                if self.xbox.getRawButton(map.driveForwardClimber): self.wheel("forward")
                elif self.xbox.getRawButton(map.driveBackwardClimber): self.wheel("backward")
                else:
                    self.extend("hold")
                    self.stopDrive()

        if self.xbox.getRawButton(map.resetAutoClimb):
            self.startState()
        else: state = self.getState()


        if state == 0: self.extend("both")
        elif state == 1: self.wheel("forward")
        elif state == 2: self.retract("front")
        elif state == 3: self.wheel("forward")
        elif state == 4: self.retract("back")

    def up(self):
        return self.backSwitch.get()
        #return False

    def getLean(self):
        if map.robotId == map.astroV1: return self.robot.drive.getRoll()
        else: return self.robot.drive.getPitch()

    def getCorrection(self):
        return (self.kP * -self.getLean())

    def setSpeeds(self, back, front):
        if self.usingNeo:
            self.backLift.set(-1 * back * self.climbSpeed)
            self.frontLift.set(-1 * front * self.climbSpeed)
        else:
            self.backLift.set(back * self.climbSpeed)
            self.frontLift.set(front * self.climbSpeed)

    def retract(self, mode):
        correction = self.getCorrection()
        if mode=="front": self.setSpeeds(self.backHold, 1)
        elif mode=="back": self.setSpeeds(0.4, 0)
        elif mode=="both": self.setSpeeds(1 + correction, 1)
        else: self.setSpeeds(0, 0)

    def extend(self, mode):
        correction = self.getCorrection()
        if mode=="front": self.setSpeeds(correction, -1)
        elif mode=="back": self.setSpeeds(-1, 0)
        elif mode=="both": self.setSpeeds(-1 + correction, -1)
        elif self.up() == True: self.setSpeeds(self.backHold, self.frontHold)
        else: self.setSpeeds(0, 0)

    def wheel(self, direction):
        '''FORWARD MOVES ROBOT FORWARD, BACKWARD MOVES ROBOT BACKWARD'''
        if direction == "forward":
            self.wheelLeft.set(self.wheelSpeed)
            self.wheelRight.set(self.wheelSpeed)
        elif direction == "backward":
            self.wheelLeft.set(-1 * self.wheelSpeed)
            self.wheelRight.set(-1 * self.wheelSpeed)

        #correction = self.getCorrection()
        #self.setSpeeds(self.backHold+correction, 0)

    def startClimb(self):
        self.state = 0

    def getState(self):

        '''
        state 0 is robot elevating itself until top sensors trigger
        state 1 is robot driving forward until front sensor triggers
        state 2 is robot lifting front leg until bottom front sensor triggers
        state 3 is robot driving forward until back sensor triggers
        state 4 is robot lifting back leg until bottom back sensor triggers
        state 5 is robot driving forward until drivers disable method
        '''

        '''checking any illogical scenarios, if they occur end autoclimb'''

        if self.state==1 and (not self.isFullyExtendedBothTest() or self.isBackOverGroundTest()):
            print("STATE 1 Error")
            self.state = -1

        if self.state==2 and (not self.isFullyExtendedBackTest() or self.isBackOverGroundTest() or not self.isFrontOverGroundTest()):
            print("STATE 2 Error")
            self.state = -1

        if self.state==3 and (not self.isFrontOverGroundTest() or not self.isFullyExtendedBackTest() or not self.isFullyRetractedFrontTest()):
            print("STATE 3 Error")
            self.state = -1

        if self.state==4 and (not self.isFrontOverGroundTest() or not self.isBackOverGroundTest() or not self.isFullyRetractedFrontTest()):
            print("STATE 4 Error")
            self.state = -1

        if self.state==5 and (not self.isFrontOverGroundTest() or not self.isBackOverGroundTest() or not self.isFullyRetractedBothTest()):
            print("STATE 5 Error")
            self.state=-1


        '''checking milestones to transition to next steps'''

        if self.state==0 and self.isFullyExtendedBothTest() and not self.isFrontOverGroundTest() and not self.isBackOverGroundTest():
            print("Transition to State 1")
            self.state = 1

        if self.state==1 and self.isFrontOverGroundTest():
            print("Transition to State 2")
            self.state = 2

        if self.state==2 and self.isFullyRetractedFrontTest():
            print("Transition to State 3")
            self.state = 3

        if self.state==3 and self.isBackOverGroundTest():
            print("Transition to State 4")
            self.state = 4

        if self.state==4 and self.isFullyRetractedBackTest():
            print("Transition to State 5")
            self.state = 5

            return self.state

    def stopClimb(self):
        self.setSpeeds(0, 0)

    def stopDrive(self):
        self.wheelLeft.set(0)
        self.wheelRight.set(0)

    def disable(self):
        self.stopClimb()
        self.stopDrive()

    def isFullyExtendedFront(self):
        """ tells us if the front is fully extended """
        return not self.switchTopFront.get()

    def isFullyExtendedBack(self):
        """ tells us if the back is fully extended, so it can stop """
        return not self.switchTopBack.get()

    def isFullyRetractedFront(self):
        return not self.switchBottomFront.get()

    def isFullyRetractedBack(self):
        return not self.switchBottomBack.get()

    def isFrontOverGround(self):
        return not self.frontSwitch.get()

    def isBackOverGround(self):
        return not self.backSwitch.get()

    def dashboardInit(self):
        SmartDashboard.putNumber("Climber kP", self.kP)
        SmartDashboard.putNumber("ClimbSpeed", self.climbSpeed)
        SmartDashboard.putNumber("BackHold", self.backHold)
        SmartDashboard.putNumber("FrontHold", self.frontHold)

    def dashboardPeriodic(self):
        SmartDashboard.putBoolean("Fully Extended Front",self.isFullyExtendedFront())
        SmartDashboard.putBoolean("Fully Extended Back",self.isFullyExtendedBack())
        SmartDashboard.putBoolean("Fully Retracted Front",self.isFullyRetractedFront())
        SmartDashboard.putBoolean("Fully Retracted Back",self.isFullyRetractedBack())
        SmartDashboard.putBoolean("Front Over Ground", self.isFrontOverGround())
        SmartDashboard.putBoolean("Back Over Ground", self.isBackOverGround())
        self.climbSpeed = SmartDashboard.getNumber("ClimbSpeed", self.climbSpeed)
        self.kP = SmartDashboard.getNumber("Climber kP", self.kP)
        self.backHold = SmartDashboard.getNumber("BackHold", self.backHold)
        self.frontHold = SmartDashboard.getNumber("FrontHold", self.frontHold)
        SmartDashboard.putNumber("Lean", self.getLean())
        SmartDashboard.putNumber("FloorSensor", self.up())
