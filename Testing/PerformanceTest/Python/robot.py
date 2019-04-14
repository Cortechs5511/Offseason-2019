import math
import wpilib

import pythonTest

from wpilib import SmartDashboard
from commandbased import CommandBasedRobot

class MyRobot(CommandBasedRobot):
    def __init__(self):
        super().__init__()

    def robotInit(self):
        SmartDashboard.putData("Performance Test", pythonTest.PythonTest())

if __name__ == "__main__":
    wpilib.run(MyRobot)
