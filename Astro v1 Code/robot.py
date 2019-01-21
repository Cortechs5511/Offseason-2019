import math
import wpilib
import oi

from wpilib import SmartDashboard
import wpilib.buttons

from wpilib.command import Command
from commandbased import CommandBasedRobot

from commands.setFixedDT import setFixedDT
from commands.setSpeedDT import setSpeedDT
from commands.DriveStraightTime import DriveStraightTime
from commands.DriveStraightDistance import DriveStraightDistance
from commands.DriveStraightCombined import DriveStraightCombined
from commands.DrivePath import DrivePath
from commands.TurnAngle import TurnAngle

from commands.getLimelightData import getLimelightData
from commands.driveVision import driveVision

from commands.Zero import Zero

from commands import Sequences

from commands import autonomous

from commands.autonomous import TestPath
from commands.autonomous import DriveStraight

from subsystems import Drive, Limelight

from CRLibrary.path import odometry as od

import pathfinder as pf

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

#from navx import AHRS as navx

class DebugRate(Command):
    def initialize(self):
        self.curr = 0
        self.print = 10

    def execute(self):
        self.curr += 1
        if(self.curr%self.print==0):
            time = self.timeSinceInitialized()
            #od.display() #displays odometry results
            SmartDashboard.putNumber("Iterations:", self.curr)
            SmartDashboard.putNumber("Time", time)
            if time > 0:
                SmartDashboard.putNumber("Rate", self.curr/time)

class MyRobot(CommandBasedRobot):

    dashboard = True

    def robotInit(self):

        '''
        This is a good place to set up your subsystems and anything else that
        you will need to access later.
        '''
        self.dashboard = True
        #self.setPeriod(0.025) #40 runs per second instead of 50
        #self.setPeriod(0.0333) #30 runs per second

        Command.getRobot = lambda x=0: self

        self.drive = Drive.Drive(self)
        self.limelight = Limelight.Limelight(self)
        self.pistons = HatchMech.HatchMech(self)

        self.timer = wpilib.Timer()
        self.timer.start()

        '''
        Since OI instantiates commands and commands need access to subsystems,
        OI must be initialized after subsystems.
        '''

        self.joystick0 = oi.getJoystick(0)
        self.joystick1 = oi.getJoystick(1)
        self.xbox = oi.getJoystick(2)

        if(self.dashboard): self.updateDashboardInit()

        follower = "Ramsetes"

        self.TestPath = TestPath(follower)

        self.DriveStraight = DriveStraight()

        oi.commands()
        SmartDashboard.putData("CPU Load", DebugRate())

        SmartDashboard.putString("position", "L")

        self.curr = 0
        self.print = 10

    def robotPeriodic(self):
        if(self.dashboard):
            self.updateDashboardPeriodic()
        else:
            pass

    def autonomousInit(self):
        self.drive.zero()
        self.timer.reset()
        self.timer.start()
        self.curr = 0

        gameData = "LLL" #wpilib.DriverStation.getInstance().getGameSpecificMessage()
        position = "M" #SmartDashboard.getString("position", "M")

        self.autoMode = self.autoLogic(gameData, position)
        if self.autoMode == "DriveStraight": self.DriveStraight.start()
        elif self.autoMode == "TestPath": self.TestPath.start()

    def autoLogic(self, gameData, auto):
        return "RightSwitchMiddle"

        '''
        if(auto=="L"):
            if(gameData[0]=="L"): return "LeftSwitchSide"
            else: return "DriveStraight"
        elif(auto=="M"):
            if(gameData[0]=="L"): return "LeftSwitchMiddle"
            else: return "RightSwitchMiddle"
        elif(auto=="R"):
            if(gameData[0]=="L"): return "DriveStraight"
            else: return "RightSwitchSide"
        return "Nothing"
        '''

    def updateDashboardInit(self):
        #'''Subsystems'''
        #SmartDashboard.putData("Drive", self.drive)

        #'''Commands'''
        #SmartDashboard.putData("setFixedDT", setFixedDT())
        #SmartDashboard.putData("setSpeedDT", setSpeedDT())

        #SmartDashboard.putData("DriveStraightDistance", DriveStraightDistance())
        #SmartDashboard.putData("DriveStraightTime", DriveStraightTime())
        #SmartDashboard.putData("DriveStraightCombined", DriveStraightCombined())
        #SmartDashboard.putData("DrivePath", DrivePath())
        #SmartDashboard.putData("TurnAngle", TurnAngle())
        #SmartDashboard.putData("driveVision", driveVision())

        #SmartDashboard.putData("Zero", Zero())

        #'''Additional UpdateDashboard Functions'''
        #Sequences.UpdateDashboard()
        #autonomous.UpdateDashboard()
        pass

    def updateDashboardPeriodic(self):
        #current = self.drive.getOutputCurrent()
        #SmartDashboard.putNumber("Total_Amps",current)


        '''Additional UpdateDashboard Functions'''
        #self.drive.UpdateDashboard()
        self.limelight.UpdateDashboard()

        SmartDashboard.putNumber("DT_DistanceAvg", self.drive.getAvgDistance())

if __name__ == "__main__":
    wpilib.run(MyRobot)
