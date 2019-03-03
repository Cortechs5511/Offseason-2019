import math

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

import navx

import wpilib
from wpilib import SmartDashboard

from CRLibrary.physics import DCMotorTransmission as DCMotor
from CRLibrary.physics import DifferentialDrive as dDrive
from CRLibrary.path import odometry as od
from CRLibrary.path import Path
from CRLibrary.util import units
from sim import simComms

import map

#class Drive(Subsystem):
