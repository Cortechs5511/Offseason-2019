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
        self.debug = True
        self.test = True
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

        self.state = -1

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
            self.frontLift.setInverted(True)
            self.backLift.setInverted(False)

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
        if self.joystick.getRawButton(map.lowerFrontClimber):
            self.lower("front")
        elif self.joystick.getRawButton(map.lowerBackClimber):
            self.lower("back")
        elif self.joystick.getRawButton(map.lowerClimber):
            self.lower("both")
        elif self.joystick.getRawButton(map.liftFrontClimber):
            self.lift("front")
        elif self.joystick.getRawButton(map.liftBackClimber):
            self.lift("back")
        elif self.joystick.getRawButton(map.liftClimber):
            self.lift("both")
        elif self.joystick.getRawButton(map.driveForwardClimber):
            self.wheel("forward")
        elif self.joystick.getRawButton(map.driveBackwardClimber):
            self.wheel("backward")
        else:
            self.stopFront()
            self.stopBack()
            self.stopDrive()

        self.sensorAnglePeriodic()

        #AUTOCLIMB
        if self.joystick.getRawButton(map.resetAutoClimb):
            self.startState()

        if self.joystick.getRawButton(map.autoClimb):

            if(self.test): state = self.getStateTest()
            else: state = self.getState()

            if state == 0: self.lift("both")
            elif state == 1: self.wheel("forward")
            elif state == 2: self.lift("front")
            elif state == 3: self.wheel("forward")
            elif state == 4: self.lift("back")

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
            self.backLift.set(0.1 * (self.getLean() + 10))
            self.frontLift.set(-1* self.returnClimbSpeed())
            print([-0.1 * (self.getLean()+10), -1*self.returnClimbSpeed()])
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



    def getLean(self):
        if map.robotId == map.astroV1:
            return self.navx.getRoll()
        else:
            return self.getPitch()

    def isLeaning(self, direction):
        '''true checking tip forward'''
        if direction == True and self.getLean()+1 < -self.MAX_ANGLE: return True
        elif direction == False and self.getLean()-1 > self.MAX_ANGLE: return True
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


    def isFrontOverGroundTest(self):
        return self.frontOverGround

    def isBackOverGroundTest(self):
        return self.backOverGround

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
        multiplier = 1 - (0.2 * math.fabs(error))
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

    def startState(self):
        self.state = 0
        self.updateDashboardInit()

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

    #DASHBOARD FUNCTIONS

    def updateDashboardInit(self):
        SmartDashboard.putNumber("ClimberSpeed", 0.9)
        SmartDashboard.putNumber("WheelSpeed", 0.7)
        SmartDashboard.putNumber("Tolerance", 2)

        SmartDashboard.putBoolean("FullyExtendedFrontTest2", False)
        SmartDashboard.putBoolean("FullyExtendedBackTest2", False)
        SmartDashboard.putBoolean("FullyRetractedFrontTest2", True)
        SmartDashboard.putBoolean("FullyRetractedBackTest2", True)
        SmartDashboard.putBoolean("FrontOverGroundTest2", True)
        SmartDashboard.putBoolean("BackOverGroundTest2", True)

    def updateDashboardPeriodic(self):
        self.returnWheelSpeed()
        self.returnClimbSpeed()
        SmartDashboard.putNumber("Lean", self.getLean())

        if self.debug:
            SmartDashboard.putBoolean("Fully Extended Front",self.isFullyExtendedFront())
            SmartDashboard.putBoolean("Fully Extended Back",self.isFullyExtendedBack())
            SmartDashboard.putBoolean("Fully Retracted Front",self.isFullyRetractedFront())
            SmartDashboard.putBoolean("Fully Retracted Back",self.isFullyRetractedBack())
            SmartDashboard.putBoolean("Front Over Ground", self.isFrontOverGround())
            SmartDashboard.putBoolean("Back Over Ground", self.isBackOverGround())
            SmartDashboard.putNumber("State", self.state)

        self.fullyExtendedFront = SmartDashboard.getBoolean("FullyExtendedFrontTest2", True)
        self.fullyExtendedBack = SmartDashboard.getBoolean("FullyExtendedBackTest2", True)
        self.fullyRetractedFront = SmartDashboard.getBoolean("FullyRetractedFrontTest2", True)
        self.fullyRetractedBack = SmartDashboard.getBoolean("FullyRetractedBackTest2", True)
        self.frontOverGround = SmartDashboard.getBoolean("FrontOverGroundTest2", True)
        self.backOverGround = SmartDashboard.getBoolean("BackOverGroundTest2", True)
