import wpilib

from wpilib import SmartDashboard
from wpilib import SmartDashboard
from wpilib import RobotBase

from ctre import WPI_TalonSRX as Talon

import math

from sim import simComms
import map
import oi

class CargoMech():

    def initialize(self):
        timeout = 15
        SmartDashboard.putNumber("Wrist Power Set", 0)
        SmartDashboard.putNumber("Gravity Power", 0)

        self.F = 0.25
        SmartDashboard.putNumber("F Gain", self.F)

        #self.angle = 0
        #SmartDashboard.putNumber("angle", self.angle)

        self.range = -1200

        self.povPressed = False

        self.maxVolts = 10
        self.wristUpVolts = 4
        self.wristDownVolts = -4
        SmartDashboard.putNumber("Wrist Up Volts", self.wristUpVolts)
        SmartDashboard.putNumber("Wrist Down Volts", self.wristDownVolts)

        self.xbox = oi.getJoystick(2)
        self.joystick0 = oi.getJoystick(0)

        #below is the talon on the intake
        self.intake = Talon(map.intake)
        self.intake.setNeutralMode(2)
        self.intake.configVoltageCompSaturation(self.maxVolts)

        self.intake.configContinuousCurrentLimit(20,timeout) #20 Amps per motor
        self.intake.configPeakCurrentLimit(30,timeout) #30 Amps during Peak Duration
        self.intake.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
        self.intake.enableCurrentLimit(True)

        #Talon motor object created
        self.wrist = Talon(map.wrist)

        if not wpilib.RobotBase.isSimulation():
            self.wrist.configFactoryDefault()

        self.wrist.setInverted(True)

        self.wrist.configVoltageCompSaturation(self.maxVolts)
        self.wrist.setNeutralMode(2)

        self.wrist.configClearPositionOnLimitF(True)

        self.wrist.configContinuousCurrentLimit(20,timeout) #20 Amps per motor
        self.wrist.configPeakCurrentLimit(30,timeout) #30 Amps during Peak Duration
        self.wrist.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
        self.wrist.enableCurrentLimit(True)

    def setIntake(self, mode):
        #Intake/Outtake/Stop, based on the mode it changes the speed of the motor
        if mode == "intake": self.intake.set(0.9)
        elif mode == "outtake": self.intake.set(-0.9)
        else: self.intake.set(0)

    def setWrist(self, mode):
        [setpoint, error] = [10, 5]
        mult = abs(self.getAngle()-50)/100 + 0.5 #increase constant if the arm is not moving enough close to the setpoint
        if mode == "rocket" and self.getAngle() < setpoint-error: self.moveWrist(self.wristDownVolts/ self.maxVolts*mult, mode)
        elif mode == "rocket" and self.getAngle() > setpoint+error: self.moveWrist(self.wristUpVolts/self.maxVolts*mult, mode)
        elif mode == "up": self.moveWrist(self.wristUpVolts/self.maxVolts, mode)
        elif mode == "down": self.moveWrist(self.wristDownVolts/ self.maxVolts, mode)
        elif mode == "rocket" or mode == "gravity": self.moveWrist(0, mode)
        else: self.moveWrist(-self.getGravity(), "stop")

    def moveWrist(self, power, mode):
        self.out = self.wristBounds(power + self.getGravity(), mode)
        self.wrist.set(self.out)

    def wristBounds(self, power, mode):
        angle = self.getAngle()
        if angle > 80 and (mode == "down" or mode == "gravity"): power = 0
        elif angle < -20 and (mode == "up" or mode == "gravity"): power = 0
        elif angle < 10 and mode == "gravity":
            power = self.F #if operator lets go of buttons while at top, arm goes back to upper limit sqitch
        return power

    def getGravity(self):
        return math.sin(math.radians(self.getAngle()))*self.F

    def getAngle(self):
        pos = 0
        if self.wrist.isRevLimitSwitchClosed():
            pos = self.range
            self.wrist.setQuadraturePosition(pos)
        else:
            pos = self.getPosition()
        angle = abs(pos * 115/self.range)
        return (angle-25)

    '''
    def getAngle(self):
        return self.angle
    '''

    def getPosition(self):
        return self.wrist.getQuadraturePosition()

    def periodic(self):
        if self.xbox.getRawAxis(map.intakeCargo)>0.4: self.setIntake("intake")
        elif self.xbox.getRawAxis(map.outtakeCargo)>0.4: self.setIntake("outtake")
        else: self.setIntake("stop")

        if self.xbox.getPOV() > 0 and self.povPressed: self.povPressed = False
        if self.xbox.getPOV() > 0 and not self.povPressed: self.povPressed = True

        if self.povPressed: self.setWrist("rocket")
        elif self.xbox.getRawButton(map.wristUp): self.setWrist("up")
        elif self.xbox.getRawButton(map.wristDown): self.setWrist("down")
        else: self.setWrist("gravity")

    #disables intake
    def disable(self):
        self.setIntake("stop")
        self.setWrist("stop")

    def getNumber(self, key, defVal):
        val = SmartDashboard.getNumber(key, None)
        if val == None:
            val = defVal
            SmartDashboard.putNumber(key, val)
        return val

    def dashboardInit(self): pass

    def dashboardPeriodic(self):
        SmartDashboard.putNumber("Wrist Position", self.wrist.getQuadraturePosition())
        SmartDashboard.putNumber("Wrist Angle" , self.getAngle())
        SmartDashboard.putNumber("Output", self.out)
        self.F = SmartDashboard.getNumber("F Gain", 0)
        self.wristUpVolts = SmartDashboard.getNumber("Wrist Up Volts", 0)
        self.wristDownVolts = SmartDashboard.getNumber("Wrist Down Volts", 0)
        #SmartDashboard.putBoolean("Limit Switch", self.wrist.isFwdLimitSwitchClosed())
        #SmartDashboard.putBoolean("Limit Switch Reverse", self.wrist.isRevLimitSwitchClosed())
        #SmartDashboard.putBoolean("Wrist PinState Quad A", self.wrist.getPinStateQuadA())
        #SmartDashboard.putBoolean("Wrist PinState Quad B", self.wrist.getPinStateQuadB())

        #self.angle = SmartDashboard.getNumber("angle", 0)
