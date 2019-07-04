from wpilib import SmartDashboard
from wpilib import Solenoid

from wpilib.command.subsystem import Subsystem
from wpilib.command import Command

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

import map
import oi

class HatchMech(Subsystem):
    def __init__(self, Robot):
        #Create all physical parts used by subsystem.
        super().__init__('Hatch')
        #self.debug = True
        self.robot = Robot

    def initialize(self):
        #makes control objects
        self.xbox = oi.getJoystick(2)
        self.joystick0 = oi.getJoystick(0)
        self.joystick1 = oi.getJoystick(1)

        #makes solenoid objects to be used in kick and slide functions
        self.kicker = Solenoid(map.hatchKick)
        self.slider = Solenoid(map.hatchSlide)

        self.maxVolts = 10
        timeout = 0

        self.wheels = Talon(map.hatchWheels)
        self.wheels.setNeutralMode(2)
        self.wheels.configVoltageCompSaturation(self.maxVolts)

        self.wheels.configContinuousCurrentLimit(20,timeout) #20 Amps per motor
        self.wheels.configPeakCurrentLimit(30,timeout) #30 Amps during Peak Duration
        self.wheels.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
        self.wheels.enableCurrentLimit(True)
        self.wheels.setInverted(True)

        self.powerIn = 0.9
        self.powerOut = -0.9

        #sets kicker and slide solenoids to in
        self.kick("in")
        self.slide("in")

        #starts lastkick/slide booleans
        self.lastKick = False
        self.lastSlide = False

        self.hasHatch = False

        self.outPower = 0

    def periodic(self):
        self.updateHatch()

        self.currKick = self.xbox.getRawButton(map.kickHatch)
        self.currSlide = self.xbox.getRawButton(map.toggleHatch)

        #if the variable is true and it does not equal the lastkick/slide boolean, sets it to the opposite of what it currently is
        if self.currKick and (self.currKick != self.lastKick): self.kick("toggle")
        if self.currSlide and (self.currSlide != self.lastSlide): self.slide("toggle")

        #after the if statement, sets the lastkick/slide to the currkick/slide
        self.lastKick = self.currKick
        self.lastSlide = self.currSlide

        self.setWheels()

    # kick function to activate kicker solenoid
    def kick(self, mode):
        #out mode sets kicker solenoid to true
        if mode == "out": self.setKick(True)
        #in mode sets kicker solenoid to false
        elif mode == "in": self.setKick(False)
        #if neither of them, makes the kicker solenoid to the opposite of what it is
        else: self.setKick(not self.kicker.get())

    # slide function to activate slide solenoid
    def slide(self, mode):
        # out mode sets slider solenoid to true
        if mode == "out": self.slider.set(True)
        # in mode sets slider solenoid to false
        elif mode == "in": self.slider.set(False)
        #if neither of them, makes the slider solenoid to the opposite of what it is
        else: self.slider.set(not self.slider.get())

    def setKick(self, state):
        self.kicker.set(state)
        if state and self.slider.get() and self.hasHatch: self.hasHatch = False

    def setWheels(self):
        if self.kicker.get() and self.slider.get() and self.hasHatch:
            self.wheels.set(self.powerOut)
            self.outPower = self.powerOut
        elif not self.kicker.get() and self.slider.get() and not self.hasHatch:
            self.wheels.set(self.powerIn)
            self.outPower = self.powerIn
        else:
            self.wheels.set(0)
            self.outPower = 0

    def updateHatch(self):
        #only checks current to possibly set false to true for hasHatch
        threshold = 10 #10 amp current separates freely spinning and stalled
        if self.slider.get() and self.wheels.getOutputCurrent()>threshold:
            self.hasHatch = True

        if self.joystick0.getRawButton(3) or self.joystick0.getRawButton(4) or self.joystick1.getRawButton(3) or self.joystick1.getRawButton(4):
            self.hasHatch = True

    #disable function runs kick function on in
    def disable(self): self.kick("in")

    def dashboardInit(self): pass

    def dashboardPeriodic(self):
        #commented out some values. DON'T DELETE THESE VALUES
        #SmartDashboard.putNumber("Hatch Current", self.wheels.getOutputCurrent())
        #SmartDashboard.putNumber("Power", self.outPower)
        SmartDashboard.putBoolean("Has Hatch", self.hasHatch)
        SmartDashboard.putBoolean("Slider Out", self.slider.get())
        SmartDashboard.putBoolean("Kicker Out", self.kicker.get())

#class ommand to eject hatch
class EjectHatch(Command):
    def __init__(self):
        super().__init__('EjectHatch')
        robot = self.getRobot()
        self.hatch = robot.hatch
        self.requires(self.hatch)

    def initialize(self): pass
    #literally just runs kicker function to out
    def execute(self): self.hatch.kick("out")

    def isFinished(self): return self.timeSinceInitialized()>0.25

    def interrupted(self): pass

    def end(self): self.hatch.kick("in")
