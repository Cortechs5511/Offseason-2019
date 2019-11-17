from wpilib.command import Command
from subsystems import Drive
import oi


class DriveDistance(Command):
    def __init__(self, distance, power):
        super().__init__("Set Distance %d" % distance, power)
        self.power = power ** 0.5
        self.target = distance
        self.requires(self.getRobot().drivetrain)

    def initialize(self):
        Drive.Drive.setSpeed(self.pageDrive(), 0, 0)

    def execute(self):
        self.left = Drive.Drive.getLeftEncoder(self.pageDrive())
        self.right = Drive.Drive.getRightEncoder(self.pageDrive())

        #self.left = float(input("ENTER LEFT ENCODER VALUE\n\n")) # for testing  as physics file dead
        #self.right = float(input("ENTER RIGHT ENCODER VALUE\n\n"))

        leftPower = (self.power / (1 + (2 ** (self.left - (self.target - 4)))))
        rightPower = (self.power / (1 + (2 ** (self.right - (self.target - 4)))))

        if self.left > self.right:
            leftPower -= abs(self.left - self.right) / 30
        elif self.right > self.left:
            rightPower -= abs(self.right - self.left) / 30



        Drive.Drive.setSpeed(self.pageDrive(), leftPower, rightPower)

    def isFinished(self):
        if oi.halfSpeedButton() == True or oi.flipButton() == True:
            return True
        if self.left > self.target and self.right > self.target:
            return True
        else:
            return False

    def end(self):
        Drive.Drive.setSpeed(self.pageDrive(), 0, 0)
