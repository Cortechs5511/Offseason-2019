import wpilib


#Can ID
driveLeft1 = 10
driveLeft2 = 11
driveLeft3 = 12
driveRight1 = 20
driveRight2 = 21
driveRight3 = 22

intake = 30
wrist = 31


frontLift = 40
backLift = 41

wheelLeft = 50
wheelRight = 51

#Solenoids

hatchKick = 0
hatchSlide = 1
climberLock1 = 2
climberLock2 = 3

#DIO

leftEncoder = (0,1)
rightEncoder = (2,3)

#sets the system preferences

"""def getInt(Key , V): 
    preferences = wpilib.Preferences.getInstance()
    V = preferences.getInt(Key, V)
    if preferences.containsKey(Key):
        print ("found")
        return preferences.getInt(Key , V )
    print ("Not Found")
    preferences.putInt(Key , V)
    return V

AstroV1 = 1
AstroV2 = 2
Synapse = 3

robotID = getInt("robotID" , AstroV2)