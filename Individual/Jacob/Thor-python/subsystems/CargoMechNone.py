'''CARGOMECH NONE'''
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
        self.wristPowerSet = 0
        SmartDashboard.putNumber("Wrist Power Set", self.wristPowerSet)

        self.maxVolts = 10
        self.wristUpVolts = 4
        self.wristDownVolts = -4

        self.xbox = oi.getJoystick(2)
        self.out = 0

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
        if mode == "up":
            self.out = self.wristUpVolts/self.maxVolts
        elif mode == "down":
            self.out = self.wristDownVolts/self.maxVolts
        else:
            self.out = 0
        self.setWristPower(self.out)

    def setWristPower(power):
        self.wrist.set(power)

    def periodic(self):
        if self.xbox.getRawAxis(map.intakeCargo)>0.4: self.setIntake("intake")
        elif self.xbox.getRawAxis(map.outtakeCargo)>0.4: self.setIntake("outtake")
        else: self.setIntake("stop")

        if self.xbox.getRawButton(map.wristUp): self.setWrist("up")
        elif self.xbox.getRawButton(map.wristDown): self.setWrist("down")
        else: self.setWrist("stop")

    #disables intake
    def disable(self):
        self.setIntake("stop")
        self.setWrist("stop")

    def dashboardInit(self): pass

    def dashboardPeriodic(self):
        SmartDashboard.putNumber("Cargomech Wrist Output", self.out)
        self.wristPowerSet = SmartDashboard.getNumber("Wrist Power Set", 0)
