from wpilib import SmartDashboard
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

import oi
import map

class Climber(Subsystem):

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

        self.backSwitch = wpilib.DigitalInput(map.backBottomSensor)
        self.frontSwitch = wpilib.DigitalInput(map.frontBottomSensor)

        self.MAX_ANGLE = 3 #degrees
        self.climbSpeed = 0.9 #90%
        self.wheelSpeed = 0.9 #90%

        self.backHold = -0.1 #holds back stationary if extended
        self.frontHold = -0.1 #holds front stationary if extended

        self.kP = 0.1 #proportional gain for angle to power

        '''
        NEGATIVE POWER TO ELEVATOR LIFTS ROBOT, LOWERS LEGS
        POSITIVE POWER TO ELEVATOR LOWERS ROBOT, LIFTS LEGS

        NEGATIVE POWER TO WHEELS MOVES ROBOT BACKWARDS
        POSITIVE POWER TO WHEELS MOVES ROBOT FORWARD
        '''

    def periodic(self):
        '''TODO DOUBLE CHECK AND CHANGE AXES/BUTTONS IF NECESSARY'''
        deadband = 0.50

        if self.joystick.getRawAxis(map.lowerFrontClimber) < -deadband: self.lower("front")
        elif self.joystick.getRawAxis(map.lowerBackClimber) < -deadband: self.lower("back")
        elif self.joystick.getRawButton(map.lowerClimber) == True: self.lower("both")
        elif self.joystick.getRawAxis(map.liftFrontClimber) > deadband: self.climber.lift("front")
        elif self.joystick.getRawAxis(map.liftBackClimber) > deadband: self.climber.lift("back")
        elif self.joystick.getRawButton(map.liftClimber) == True: self.climber.lift("both")
        else: self.stopClimb()

        if self.joystick.getRawButton(map.driveForwardClimber): self.climber.wheel("forward")
        elif self.joystick.getRawButton(map.driveBackwardClimber): self.climber.wheel("backward")
        else: self.climber.stopDrive()

    def getLean(self):
        if map.robotId == map.astroV1: return self.robot.drive.getRoll()
        else: return self.robot.drive.getPitch()

    def isLeaning(self, direction):
        '''TRUE TESTS TIPPING FORWARD, FORWARD TIP HAS NEGATIVE ANGLE'''

        if direction==True and self.getLean()<-self.MAX_ANGLE: return True
        elif direction==False and self.getLean()>self.MAX_ANGLE: return True
        else: return False

    def backRetracted(self): return not self.frontSwitch.get()
    def frontRetracted(self): return not self.backSwitch.get()

    def getCorrection(self):
        '''CORRECTION IS POSITIVE'''
        multiplier = 1 - (self.kP * math.fabs(self.getLean()))
        return (multiplier * self.climbSpeed)

    def retract(self, mode):
        cSpeed = self.getCorrection()

        if mode == "front":
            if self.isLeaning(True): self.backLift.set(cspeed)
            else: self.stopBack()

            self.frontLift.set(self.climbSpeed)

        elif mode == "back":
            if self.isLeaning(False): self.frontLift.set(cspeed)
            else: self.stopFront()

            self.backLift.set(self.climbSpeed)

        elif mode == "both":
            if self.isLeaning(True):
                self.backLift.set(cspeed)
                self.frontLift.set(self.climbSpeed)
            elif self.isLeaning(False):
                self.backLift.set(self.climbSpeed)
                self.frontLift.set(cspeed)
            else:
                self.backLift.set(self.climbSpeed)
                self.frontLift.set(self.climbSpeed)

    def extend(self, mode):
        cSpeed = self.getCorrection()

        if mode == "front":
            if self.isLeaning(False): self.backLift.set(-1 * cspeed)
            else: self.stopBack()

            self.frontLift.set(-1 * self.climbSpeed)

        elif mode == "back":
            if self.isLeaning(True): self.frontLift.set(-1 * cspeed)
            else: self.stopFront()

            self.backLift.set(-1 * self.climbSpeed)

        elif mode == "both":
            if self.isLeaning(True):
                self.backLift.set(-1 * self.climbSpeed)
                self.frontLift.set(-1 * cspeed)
            elif self.isLeaning(False):
                self.backLift.set(-1 * cspeed)
                self.frontLift.set(-1 * self.climbSpeed)
            else:
                self.backLift.set(-1 * self.climbSpeed)
                self.frontLift.set(-1 * self.climbSpeed)

    def wheel(self, direction):
        '''FORWARD MOVES ROBOT FORWARD, BACKWARD MOVES ROBOT BACKWARD'''
        if direction == "forward":
            self.wheelLeft.set(self.wheelSpeed)
            self.wheelRight.set(self.wheelSpeed)
        elif direction == "backward":
            self.wheelLeft.set(-1 * self.wheelSpeed)
            self.wheelRight.set(-1 * self.wheelSpeed)

        if self.isLeaning(False):
            self.backLift.set(-1 * self.returnCorrectionSpeed())
            self.stopFront()
        elif self.isLeaning(True):
            self.backLift.set(self.returnCorrectionSpeed())
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

    def initDefaultCommand(self):
        self.setDefaultCommand(SetSpeedClimber())

    def dashboardInit(self):
        pass

    def dashboardPeriodic(self):
        SmartDashboard.putNumber("Lean", self.getLean())
