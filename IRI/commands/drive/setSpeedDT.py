import math
import wpilib
#from robot import MyRobot
#from subsystems.Drive import Drive
import map
from wpilib.command import Command
from wpilib.command import TimedCommand
from wpilib import SmartDashboard
from wpilib.drive.differentialdrive import DifferentialDrive

class SetSpeedDT(TimedCommand):
    def __init__(self, timeout = 0):
        super().__init__('SetSpeedDT', timeoutInSeconds = timeout)
        self.robot = self.getRobot()
        self.requires(self.robot.drive)
        self.DT = self.robot.drive

        self.Joystick0 = self.robot.joystick0 #this is pretty messed up lol
        self.Joystick1 = self.robot.joystick1

        self.robot.button = False
        self.flip = False

        self.k = self.DT.k

        self.alpha = 0.1 #for quickturn
        self.quickStopAccum = 0
        self.sensitivity = self.DT.sensitivity

    def initialize(self):
        self.DT.setDirect()

    def sign(self, x):
        if x >= 0: return 1
        if x < 0: return -1

    def execute(self):
        input1 = self.Joystick0.getY()
        input2 = self.Joystick1.getX()
        input3 = self.Joystick1.getY()

        if abs(input1)<0.02: input1 = 0
        if abs(input2)<0.02: input2 = 0
        if abs(input3)<0.02: input3 = 0

        input1 = (math.exp(self.k*abs(input1))-1)/(math.exp(self.k)-1)*self.sign(input1)
        input2 = (math.exp(self.k*abs(input2))-1)/(math.exp(self.k)-1)*self.sign(input2)
        input3 = (math.exp(self.k*abs(input3))-1)/(math.exp(self.k)-1)*self.sign(input3)

        if self.DT.driveStyle=="Arcade":
            power = -input1
            turn = input2
            if abs(turn) < 0.1: turn = 0.05 * self.sign(turn)
            if power > 0:
                if turn > 0:
                    [left, right] = [max(power, turn), power-turn]
                else:
                    [left, right] = [power+turn, max(power, -turn)]
            else:
                if turn < 0:
                    [left, right] = [-max(-power, -turn), power-turn]
                else:
                    [left, right] = [power+turn, -max(-power, turn)]

        elif self.DT.driveStyle=="Curvature":
            overPoewr = 0
            angularPower = 0

            power = -input1
            turn = input2
            if abs(power)<0.02: power = 0
            if abs(turn)<0.02: turn = 0
            quickTurn = self.robot.readDriverRightButton(map.halfSpeed) #boolean
            if quickTurn:
                if abs(power)<0.2:
                    self.quickStopAccum = (1-self.alpha)*self.quickStopAccum + self.alpha*turn*2
                overPower = 1
                angularPower = turn
            else:
                overPower = 0
                angularPower = abs(power)*turn*self.sensitivity-self.quickStopAccum
                if self.quickStopAccum>1: self.quickStopAccum -= 1
                elif self.quickStopAccum<-1: self.quickStopAccum += 1
                else: self.quickStopAccum = 0

            right = power - angularPower
            left = power + angularPower
            if left>1:
                right -= overPower * (left - 1)
                left = 1
            elif right>1:
                left -= overPower * (right - 1)
                right = 1
            elif left<-1:
                right += overPower * (-1 - left)
                left = -1
            elif right<-1:
                left += overPower * (-1 - right)
                right = -1


        else: #self.DT.driveStyle=="Tank"
            left = -input1
            right = -input3

            if self.robot.readDriverRightButton(map.halfSpeed) or self.robot.readDriverLeftButton(map.halfSpeed):
                temp = (left+right)/2
                left = temp
                right = temp


        if self.robot.readDriverLeftButton(map.halfSpeed):
            [left, right] = [left * .5, right * .5]

        button = self.robot.readDriverLeftButton(map.flip) or self.robot.readDriverRightButton(map.flip)
        if button and not self.robot.button: self.flip = not self.flip
        self.robot.button = button

        if self.flip: [left, right] = [-right, -left]

        self.DT.tankDrive((left*.85), (right*.85))

    def isFinished(self):
        return False

    def interrupted(self): self.end()

    def end(self): self.DT.tankDrive(0,0)
