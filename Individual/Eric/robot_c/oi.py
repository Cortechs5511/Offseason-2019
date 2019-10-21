from wpilib.joystick import Joystick
import map

def getLeftStick():
    return Joystick(0).getY()

def getRightStick():
    return Joystick(1).getY()

def halfSpeedButton():
    return Joystick(0).getButton(1) # must figure out button placement

def flipButton():
    return Joystick(1).getButton(1) # must figure out button placement
