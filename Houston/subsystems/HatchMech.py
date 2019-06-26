from wpilib import SmartDashboard
from wpilib import Solenoid

from wpilib.command.subsystem import Subsystem
from wpilib.command import Command

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
        #sets kicker and slide solenoids to in
        self.kick("in")
        self.slide("in")
        #starts lastkick/slide booleans
        self.lastKick = False
        self.lastSlide = False
        #boolean object for current kick and current slide
        self.currKick = self.xbox.getRawButton(map.kickHatch)
        self.currSlide = self.xbox.getRawButton(map.toggleHatch)

    def periodic(self):
        #if the variable is true and it does not equal the lastkick/slide boolean, sets it to the opposite of what it currently is
        if self.currKick and (self.currKick != self.lastKick): self.kick("toggle")
        if self.currSlide and (self.currSlide != self.lastSlide): self.slide("toggle")
        #after the if statement, sets the lastkick/slide to the currkick/slide
        self.lastKick = self.currKick
        self.lastSlide = self.currSlide
        #if either button is pressed set the kicker solenoid to true
        if self.joystick0.getRawButton(map.drivehatch) or self.joystick1.getRawButton(map.drivehatch):
            self.kick("out")

    # kick function to activate kicker solenoid
    def kick(self, mode):
        #out mode sets kicker solenoid to true
        if mode == "out": self.kicker.set(True)
        #in mode sets kicker solenoid to false
        elif mode == "in": self.kicker.set(False)
        #if neither of them, makes the kicker solenoid to the opposite of what it is
        else: self.kicker.set(not self.kicker.get())

    # slide function to activate slide solenoid
    def slide(self, mode):
        # out mode sets slider solenoid to true
        if mode == "out": self.slider.set(True)
        # in mode sets slider solenoid to false
        elif mode == "in": self.slider.set(False)
        #if neither of them, makes the slider solenoid to the opposite of what it is
        else: self.slider.set(not self.slider.get())

    #function to check if kicker solenoid is out, gets the boolean state of kicker
    def isEjectorOut(self): return self.kicker.get()

    #function which reads kicker solenoid to return either out/in
    def toggle(self):
        #if kicker is true, run kick function to 'out'
        if self.kicker.get(): self.kick("out")
        #otherwise, run kcik function 'in'
        else: self.kick("in")

    #disable function runs kick function on in
    def disable(self): self.kick("in")

    def dashboardInit(self): pass

    def dashboardPeriodic(self): pass

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
