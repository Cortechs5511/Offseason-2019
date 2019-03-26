from wpilib import SmartDashboard
from wpilib import DigitalInput

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

import oi
import map

class Climber():

    def initialize(self, robot):

        self.robot = robot
        self.xbox = oi.getJoystick(2)

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

        self.backLift.setNeutralMode(2)
        self.frontLift.setNeutralMode(2)
        self.wheelLeft.setNeutralMode(2)
        self.wheelRight.setNeutralMode(2)

        for motor in [self.backLift, self.frontLift, self.wheelLeft, self.wheelRight]:
            motor.clearStickyFaults(0)
            motor.setSafetyEnabled(False)

        for motor in [self.backLift, self.frontLift]:
            motor.configContinuousCurrentLimit(30,0) #Amps per motor
            motor.enableCurrentLimit(True)

            motor.configVoltageCompSaturation(10,0) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages

        self.backSwitch = DigitalInput(map.backBottomSensor)
        self.frontSwitch = DigitalInput(map.frontBottomSensor)

        self.MAX_ANGLE = 2 #degrees
        self.TARGET_ANGLE = 0 #degrees
        self.climbSpeed = 0.7 #90%
        self.wheelSpeed = 0.9 #90%

        self.backHold = -0.1 #holds back stationary if extended
        self.frontHold = -0.1 #holds front stationary if extended

        self.kP = 0.1 #proportional gain for angle to power

        self.test = True
        self.state = -1

        '''
        NEGATIVE POWER TO ELEVATOR LIFTS ROBOT, LOWERS LEGS
        POSITIVE POWER TO ELEVATOR LOWERS ROBOT, LIFTS LEGS

        NEGATIVE POWER TO WHEELS MOVES ROBOT BACKWARDS
        POSITIVE POWER TO WHEELS MOVES ROBOT FORWARD
        '''

    def lower(self, mode):
      self.retract(mode)

    def lift(self, mode):
      self.extend(mode)

    def periodic(self):
        '''TODO DOUBLE CHECK AND CHANGE AXES/BUTTONS IF NECESSARY'''
        deadband = 0.50

        if self.xbox.getRawAxis(map.lowerFrontClimber) < -deadband: self.lower("front")
        elif self.xbox.getRawAxis(map.lowerBackClimber) < -deadband: self.lower("back")
        elif self.xbox.getRawButton(map.lowerClimber) == True: self.lower("both")
        elif self.xbox.getRawAxis(map.liftFrontClimber) > deadband: self.lift("front")
        elif self.xbox.getRawAxis(map.liftBackClimber) > deadband: self.lift("back")
        elif self.xbox.getRawButton(map.liftClimber) == True: self.lift("both")
        else: self.extend("hold")

        if self.xbox.getRawButton(map.driveForwardClimber): self.wheel("forward")
        elif self.xbox.getRawButton(map.driveBackwardClimber): self.wheel("backward")
        else: self.stopDrive()

        if self.xbox.getRawButton(map.resetAutoClimb):
            self.startState()
        if(self.test): state = self.getStateTest()
        else: state = self.getState()

        if state == 0: self.lift("both")
        elif state == 1: self.wheel("forward")
        elif state == 2: self.lift("front")
        elif state == 3: self.wheel("forward")
        elif state == 4: self.lift("back")

        self.climbSpeed = SmartDashboard.getNumber("ClimbSpeed", 0.9)

    def isFullyExtendedFrontTest(self):
        """ tells us if the front is fully extended """
        return self.fullyExtendedFront

    def isFullyExtendedBackTest(self):
        """ tells us if the back is fully extended, so it can stop """
        return self.fullyExtendedBack

    def isFullyRetractedFrontTest(self):
        """ tells us if the front is fully retracted """
        return self.fullyRetractedFront

    def isFullyRetractedBackTest(self):
        """ tells us if the back is fully retracted, so it can stop """
        return self.fullyRetractedBack

    def isFullyExtendedBothTest(self):
        """ tells us if both front and back are fully extended, so it can stop """
        return self.isFullyExtendedFrontTest() and self.isFullyExtendedBackTest()

    def isFullyRetractedBothTest(self):
        """ tells us if both front and back are fully extended, so it can stop """
        return self.isFullyRetractedFrontTest() and self.isFullyRetractedBackTest()

    def isFrontOverGroundTest(self):
        return self.frontOverGround

    def isBackOverGroundTest(self):
        return self.backOverGround

    def startState(self):
        self.state = 0
        self.dashboardInit()

    def getState(self):

        '''state 0 is robot elevating itself until top sensors trigger
        state 1 is robot driving forward until front sensor triggers
        state 2 is robot lifting front leg until bottom front sensor triggers
        state 3 is robot driving forward until back sensor triggers
        state 4 is robot lifting back leg until bottom back sensor triggers
        state 5 is robot driving forward until drivers disable method'''

        #checking any illogical scenarios, if they occur end autoclimb

        if self.state==1 and (not self.isFullyExtendedBoth() or self.isBackOverGround()):
            self.state = -1

        if self.state==2 and (not self.isFullyExtendedBack() or self.isBackOverGround() or not self.isFrontOverGround()):
            self.state = -1

        if self.state==3 and (not self.isFrontOverGround() or not self.isFullyExtendedBack() or not self.isFullyRetractedFront()):
            self.state = -1

        if self.state==4 and (not self.isFrontOverGround() or not self.isBackOverGround() or not self.isFullyRetractedFront()):
            self.state = -1

        if self.state==5 and (not self.isFrontOverGround() or not self.isBackOverGround() or not self.isFullyRetractedBoth()):
            self.state=-1

        if self.state==0 and self.isFullyExtendedBoth() and not self.isFrontOverGround() and not self.isBackOverGround():
            self.state = -1

        '''checking milestones to transition to next steps'''

        if self.state==1 and self.isFrontOverGround():
            self.state = 2

        if self.state==2 and self.isFullyRetractedFront():
            self.state = 3

        if self.state==3 and self.isBackOverGround():
            self.state = 4

        if self.state==4 and self.isFullyRetractedBack():
            self.state = 5

        return self.state


    def getStateTest(self):
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

    def getLean(self):
        if map.robotId == map.astroV1: return -1* self.robot.drive.getRoll()
        else: return -1* self.robot.drive.getPitch()

    def isLeaning(self, direction):
        '''TRUE TESTS TIPPING FORWARD, FORWARD TIP HAS NEGATIVE ANGLE'''
        maxTarget = self.MAX_ANGLE + self.TARGET_ANGLE
        minTarget = -self.MAX_ANGLE + self.TARGET_ANGLE

        if direction==True and self.getLean() > maxTarget: return True
        elif direction==False and self.getLean() < minTarget: return True
        else: return False

    def backRetracted(self): return not self.frontSwitch.get()
    def frontRetracted(self): return not self.backSwitch.get()

    def getCorrection(self):
        '''CORRECTION IS POSITIVE'''
        multiplier = (self.kP * abs(self.getLean()))
        return (multiplier * self.climbSpeed)

    def retract(self, mode):
        cSpeed = self.getCorrection()

        if mode == "front":
            if self.isLeaning(False):
                self.backLift.set(-1 * cSpeed)
                self.frontLift.set(self.climbSpeed)
            elif self.isLeaning(True):
                self.backLift.set(1 * cSpeed)
                self.frontLift.set(self.climbSpeed)
            else:
                self.stopBack()
                self.frontLift.set(self.climbSpeed)

        elif mode == "back":
            #if self.isLeaning(False): self.frontLift.set(cSpeed) , don't correct front
            self.stopFront()
            self.backLift.set(self.climbSpeed)

        elif mode == "both":
            if self.isLeaning(True):
                self.backLift.set(1 * cSpeed)
                self.frontLift.set(self.climbSpeed)
            elif self.isLeaning(False):
                self.backLift.set(self.climbSpeed)
                self.frontLift.set(cSpeed)
            else:
                self.backLift.set(self.climbSpeed)
                self.frontLift.set(self.climbSpeed)

    def extend(self, mode):
        cSpeed = self.getCorrection()

        if mode == "front":
            if self.isLeaning(False):
                self.backLift.set(-1 * cSpeed)
                self.frontLift.set(self.climbSpeed)
            elif self.isLeaning(True):
                self.backLift.set(1 * cSpeed)
                self.frontLift.set(self.climbSpeed)
            else:
                self.stopBack()
                self.frontLift.set(self.climbSpeed)

        elif mode == "back":
            self.stopFront()
            self.backLift.set(-1 * self.climbSpeed)

        elif mode == "both":
            if self.isLeaning(True):
                self.backLift.set(-1 * self.climbSpeed)
                self.frontLift.set(-1 * cSpeed)
            elif self.isLeaning(False):
                self.backLift.set(-1 * cSpeed)
                self.frontLift.set(-1 * self.climbSpeed)
            else:
                self.backLift.set(-1.17 * self.climbSpeed)
                self.frontLift.set(-1 * self.climbSpeed)

        elif mode == "hold":
            #if self.isLeaning(False):
                #self.backLift.set(-0.7 * cSpeed)
                #self.frontLift.set(0)
            #elif self.isLeaning(True):
                #self.frontLift.set(-1 * cSpeed)
                #self.backLift.set(0)

            self.backLift.set(0)
            self.frontLift.set(0)



    def wheel(self, direction):
        '''FORWARD MOVES ROBOT FORWARD, BACKWARD MOVES ROBOT BACKWARD'''
        if direction == "forward":
            self.wheelLeft.set(self.wheelSpeed)
            self.wheelRight.set(self.wheelSpeed)
        elif direction == "backward":
            self.wheelLeft.set(-1 * self.wheelSpeed)
            self.wheelRight.set(-1 * self.wheelSpeed)

        if self.isLeaning(False):
            self.backLift.set(-1 * self.getCorrection())
            self.stopFront()
        elif self.isLeaning(True):
            self.backLift.set(self.getCorrection())
            self.stopFront()

    def wheelForward(self):
        self.wheelLeft.set(self.wheelSpeed)
        self.wheelRight.set(self.wheelSpeed)

    def wheelBack(self):
        self.wheelLeft.set(-1 * self.wheelSpeed)
        self.wheelRight.set(-1 * self.wheelSpeed)

    def stopFront(self):
        if(self.frontRetracted()): self.frontLift.set(0)
        else: self.frontLift.set(self.frontHold)

    def stopBack(self):
        if(self.backRetracted()): self.backLift.set(0)
        else: self.backLift.set(self.backHold)

    def stopClimb(self):
        self.stopFront()
        self.stopBack()

    def stopDrive(self):
        self.wheelLeft.set(0)
        self.wheelRight.set(0)

    def disable(self):
        self.stopClimb()
        self.stopDrive()

    #def initDefaultCommand(self):
    #    self.setDefaultCommand(SetSpeedClimber())

    def dashboardInit(self):
        pass

    def getNumber(self, key, defVal):
        val = SmartDashboard.getNumber(key, None)
        if val == None:
            val = defVal
            SmartDashboard.putNumber(key, val)
        return val

    def dashboardPeriodic(self):
        SmartDashboard.putNumber("Lean", self.getLean())
        SmartDashboard.putBoolean("FullyExtendedFrontTest2", False)
        SmartDashboard.putBoolean("FullyExtendedBackTest2", False)
        SmartDashboard.putBoolean("FullyRetractedFrontTest2", True)
        SmartDashboard.putBoolean("FullyRetractedBackTest2", True)
        SmartDashboard.putBoolean("FrontOverGroundTest2", True)
        SmartDashboard.putBoolean("BackOverGroundTest2", True)
        SmartDashboard.putNumber("ClimbSpeed", self.climbSpeed)
        self.kP = self.getNumber("Climber kP", 0.4)

        self.fullyExtendedFront = SmartDashboard.getBoolean("FullyExtendedFrontTest2", True)
        self.fullyExtendedBack = SmartDashboard.getBoolean("FullyExtendedBackTest2", True)
        self.fullyRetractedFront = SmartDashboard.getBoolean("FullyRetractedFrontTest2", True)
        self.fullyRetractedBack = SmartDashboard.getBoolean("FullyRetractedBackTest2", True)
        self.frontOverGround = SmartDashboard.getBoolean("FrontOverGroundTest2", True)
        self.backOverGround = SmartDashboard.getBoolean("BackOverGroundTest2", True)
