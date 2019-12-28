from wpilib.joystick import Joystick
import map

def getLeftStick():
    leftStick = Joystick(0).getY()
    return leftStick

def getRightStick():
    rightStick = Joystick(1).getY()
    return rightStick

def halfSpeedButton():
    halfSpeed = Joystick(0).getButton(1) # left trigger
    return halfSpeed

def flipButton():
    flip = Joystick(1).getButton(1) # right trigger
    return flip

def getTurn():
    leftTurn = Joystick(0).getX()
    return leftTurn
