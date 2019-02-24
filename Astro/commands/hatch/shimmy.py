import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand

class Shimmy(TimedCommand):
    def __init__(self, timeout=0):
        super().__init__('Shimmy', timeoutInSeconds=timeout)
        self.endTime = timeout
        self.drive = self.getRobot().drive
        self.requires(self.drive)
        self.mode = 0

    def initialize(self):
        self.drive.setMode("Direct")

    def execute(self):
        print(self.timeSinceInitialized(), self.mode)
        if (self.timeSinceInitialized()//0.5) % 2 == 1:
            self.drive.tankDrive(0.5,0)
            self.mode = 1
        elif (self.timeSinceInitialized()//0.5) % 2 == 0:
            self.drive.tankDrive(0,0.5)
            self.mode = 2

    def isFinished(self):
        if self.timeSinceInitialized() > self.endTime:
            return True
        else: return False

    def end(self):
        self.drive.left.set(0)
        self.drive.right.set(0)

    def interrupted(self):
        self.end()
