from wpilib import SmartDashboard
from ctre import WPI_TalonSRX as Talon
from wpilib import SmartDashboard
from wpilib import PIDController
from wpilib import RobotBase
import wpilib
import map
import oi
from sim import simComms
import math

#gravity for cargo ship is -.1, angle is -28
#gravity for rocket is .15, angle is 5
#gravity for resting position was .15 , angle is -50
#gravity for intake is .15, angle is 50
class CargoMech():
    kSlotIdx = 0
    kPIDLoopIdx = 0
    kTimeoutMs = 10

    def initialize(self):
        timeout = 15
        SmartDashboard.putNumber("Wrist Power Set", 0)
        self.lastMode = "unknown"
        self.sb = []
        self.targetPosUp = -300 #!!!!!
        self.targetPosDown = -1500 #!!!!!
        self.maxVolts = 10
        self.simpleGain = 0.57
        self.wristUpVolts = 5
        self.wristDownVolts = 2
        self.simpleGainGravity = 0.07
        self.xbox = oi.getJoystick(2)
        self.joystick0 = oi.getJoystick(0)
        #below is the talon on the intake
        self.motor = Talon(map.intake)

        self.gPower = 0
        self.input = 0
        self.lastCargoCommand = "resting"

        self.motor.configContinuousCurrentLimit(20,timeout) #15 Amps per motor
        self.motor.configPeakCurrentLimit(30,timeout) #20 Amps during Peak Duration
        self.motor.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
        self.motor.enableCurrentLimit(True)

        #Talon motor object created
        self.wrist = Talon(map.wrist)
        if not wpilib.RobotBase.isSimulation():
            self.wrist.configFactoryDefault()
        self.wrist.configVoltageCompSaturation(self.maxVolts)
        self.wrist.setInverted(True)
        self.wrist.setNeutralMode(2)
        self.motor.setNeutralMode(2)
        self.motor.configVoltageCompSaturation(self.maxVolts)

        self.wrist.configClearPositionOnLimitF(True)

        #MOTION MAGIC CONFIG
        self.loops = 0
        self.timesInMotionMagic = 0

        #self.wrist.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)

        [self.kP, self.kI, self.kD] = [0, 0, 0]
        cargoController = PIDController(self.kP, self.kI, self.kD, source = self.getAngle, output = self.__setGravity__)
        self.cargoController = cargoController
        self.cargoController.disable()

    def intake(self, mode):
        #Intake/Outtake/Stop, based on the mode it changes the speed of the motor
        if mode == "intake": self.motor.set(0.9)
        elif mode == "outtake": self.motor.set(-0.9)
        elif mode == "stop": self.motor.set(0)

    def moveWrist(self, mode):
        #move wrist in and out of robot
        if mode == "resting":
            self.cargoController.setSetpoint(-50)
            self.cargoController.enable()
            if self.getAngle() <= -50:
                self.cargoController.disable()
                self.wrist.set(0.15)
        elif mode == "cargoship":
            self.cargoController.setSetpoint(-28)
            self.cargoController.enable()
            if self.getAngle() <= -25 and self.getAngle() >= -30:
                self.cargoController.disable()
                self.wrist.set(-0.1)
        elif mode == "intake":
            self.cargoController.setSetpoint(50)
            self.cargoController.enable()
            if self.getAngle() >= 45:
                self.cargoController.disable()
                self.wrist.set(0.15)
        elif mode == "rocket":
            #self.wrist.set(-0.3)
            self.cargoController.setSetpoint(5)
            self.cargoController.enable()
            if self.getAngle() <= 10 and self.getAngle() >= 0:
                self.cargoController.disable()
                self.wrist.set(0.15)
        else:
            pass
        '''replace modes up and down with pid and set angles'''

    def periodic(self):
        #0.4 as a deadband
        if self.xbox.getRawAxis(map.intakeCargo)>0.4: self.intake("intake")
        elif self.xbox.getRawAxis(map.outtakeCargo)>0.4: self.intake("outtake")
        else: self.intake("stop")

        if self.xbox.getPOV() == 0:
            self.moveWrist("resting")
            self.lastCargoCommand = "resting"
        elif self.xbox.getPOV() == 90:
            self.moveWrist("cargoship")
            self.lastCargoCommand = "cargoship"
        elif self.xbox.getPOV() == 180:
            self.moveWrist("intake")
            self.lastCargoCommand = "intake"
        elif self.xbox.getPOV() == 270:
            self.moveWrist("rocket")
            self.lastCargoCommand = "rocket"
        else:
            self.moveWrist(self.lastCargoCommand)
        '''replace with callling movewrist based on buttons'''

    #disables intake
    def disable(self): self.intake("stop")

    #gets the angle, used in other support functions
    def getAngle(self):
        pos = self.getPosition()
        angle = abs(pos * 115/self.targetPosDown)
        angle -= 25
        return (angle - 25)

    def getPosition(self):
        return self.wrist.getQuadraturePosition()

    def getFeedForward(self, gain):
        angle = self.getAngle()
        return angle*gain

    def __setGravity__(self, output): self.gPower = output

    def getPowerSimple(self, direction):
        '''true direction is up into robot
        false direction is down out of robot'''
        angle = self.getAngle()
        power = abs(self.simpleGain)
        if angle > 80:
            if direction == "down":
                power = 0
        if angle < -20:
            if direction == "up":
                power = 0
        return power

    def getNumber(self, key, defVal):
        val = SmartDashboard.getNumber(key, None)
        if val == None:
            val = defVal
            SmartDashboard.putNumber(key, val)
        return val

    def dashboardInit(self): pass

    def dashboardPeriodic(self):
        #self.wristUp = self.getNumber("WristUpSpeed" , 0.5)
        #self.wristDown = self.getNumber("WristDownSpeed" , 0.2)
        #self.wristUpVolts = self.getNumber("WristUpVoltage" , 5)
        #self.wristDownVolts = self.getNumber("WristDownVoltage" , 2)
        #self.simpleGain = self.getNumber("Wrist Simple Gain", self.simpleGain)
        #self.simpleGainGravity = self.getNumber("Wrist Simple Gain Gravity", self.simpleGainGravity)
        self.kP = self.getNumber("Wrist kP", 0)
        self.kI = self.getNumber("Wrist kI", 0)
        self.kD = self.getNumber("Wrist kD", 0)
        SmartDashboard.putNumber("Wrist Position", self.wrist.getQuadraturePosition())
        SmartDashboard.putNumber("Wrist Angle" , self.getAngle())
        SmartDashboard.putNumber("Wrist Power", self.input)
        SmartDashboard.putNumber("Wrist Power Up" , self.getPowerSimple("up"))
        SmartDashboard.putNumber("Wrist Power Down" , self.getPowerSimple("down"))
