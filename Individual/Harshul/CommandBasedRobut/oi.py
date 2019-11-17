import wpilib
from wpilib.joystick import Joystick
import robotmap

lJs = Joystick(robotmap.joystick["leftJs"])
rJs = Joystick(robotmap.joystick["rightJs"])
def getLeftJs():
    global lJs
    return lJs.getY()

def getRightJs():
    global rJs
    return rJs.getY()

#leftEncoderA = wpilib.Encoder(aSource, )
