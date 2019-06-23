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

class CargoMech():
    kSlotIdx = 0
    kPIDLoopIdx = 0
    kTimeoutMs = 10

    def initialize(self):
        timeout = 15
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
        self.motor = Talon(map.intake)

        self.gPower = 0
        self.input = 0

        self.motor.configContinuousCurrentLimit(20,timeout) #15 Amps per motor
        self.motor.configPeakCurrentLimit(30,timeout) #20 Amps during Peak Duration
        self.motor.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
        self.motor.enableCurrentLimit(True)

        #Talon motor object created
        self.wrist = Talon(map.wrist)
        if not wpilib.RobotBase.isSimulation():
            self.wrist.configFactoryDefault()
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

    def moveWrist(self,mode):
        #move wrist in and out of robot
        '''replace modes up and down with pid and set angles'''
        if mode == "up":
            self.input = (self.getPowerSimple("up")) + self.getGravity()
            self.wrist.set(self.getPowerSimple("up") + self.getGravity())
        elif mode == "down":
            self.input = (-1 * self.getPowerSimple("down")) + self.getGravity()
            self.wrist.set((-1 * self.getPowerSimple("down")) + self.getGravity())
        elif mode == "upVolts":
            self.input = (self.wristUpVolts/self.maxVolts) + self.getGravity()
            self.wrist.set((self.wristUpVolts/self.maxVolts) + self.getGravity())
        elif mode == "downVolts":
            self.input = (-1 * self.wristDownVolts / self.maxVolts) + self.getGravity()
            self.wrist.set((-1 * self.wristDownVolts/ self.maxVolts) + self.getGravity())
        elif mode == "stop":
            self.input = 0
            self.wrist.set(0)
        else:
            self.input = self.getGravity()
            self.wrist.set(self.getGravity())
            #self.cargoController.setSetpoint(self.getAngle())
            #self.cargoController.enable()
            #self.wrist.set(self.gPower)
            '''replace pid here with kF'''

    def periodic(self):
        #0.4 as a deadband
        if self.xbox.getRawAxis(map.intakeCargo)>0.4: self.intake("intake")
        elif self.xbox.getRawAxis(map.outtakeCargo)>0.4: self.intake("outtake")
        else: self.intake("stop")

        if self.xbox.getRawButton(map.wristUp): self.moveWrist("up")
        elif self.xbox.getRawButton(map.wristDown): self.moveWrist("down")
        elif self.joystick0.getRawButton(map.wristUpVolts): self.moveWrist("upVolts")
        elif self.joystick0.getRawButton(map.wristDownVolts): self.moveWrist("downVolts")
        else: self.moveWrist("gravity")
    #disables intake
    def disable(self): self.intake("stop")

    #gets the angle, used in other support functions
    def getAngle(self):
        pos = self.getPosition()
        angle = abs(pos * 115/self.targetPosDown)
        angle -= 25
        return (angle - 25)
        '''cargo mech vertical is 0 degrees'''
        '''cargo mech down completely is 90 degrees'''
        '''cargo mech has range of -25 to 85 degrees'''

    def getGravity(self):
        angle = self.getAngle()
        power = 0
        if angle < -20:
            power = 0
        elif angle > 80:
            power = 0
        else:
            power = math.sin(math.radians(angle)) / 2
        return power

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
