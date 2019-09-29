from wpilib.joystick import Joystick

def getLeftStick():
    leftStick = Joystick(0)
    return leftStick

def getRightStick():
    rightStick = Joystick(1)
    return rightStick
