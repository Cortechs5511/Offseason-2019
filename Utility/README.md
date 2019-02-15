# Utility Scripts

This folder contains utility scripts related to updating the robotpy
installation on laptops and the roboRIO.

## Quick Reference

The following should work for the 2019.1.0 release. This README.md and the scripts will need to be updated for new releases.

### Initial Setup

* Create a folder named "frc-2019" on your Desktop.
* Download robotpy-2019.1.0.zip from https://github.com/robotpy/robotpy-wpilib/releases
* Unzip the robotpy-2019.1.0.zip file into the "frc-2019" folder on your desktop.
* Verify that the folder C:\Users\YOUR_LOGIN\Desktop\frc-2019\roborio-2019.1.0 exists.
* Run the following commands. 

```
cd %HOMEPATH\Desktop\frc-2019\robotpy-2019.1.0
py -3 installer.py install-robotpy
```

NOTE: The above command may prompt you for your team number and you will need to enter it. The above command will also FAIL to connect to the roboRIO, but that is expected for now.

Verify that the robotpy-installer is installed by running the following:

```
robotpy-installer -h
```

### Update Software on Laptop

Connect to the Internet and run the following command found in this directory in a COMMAND shell prompt (not PowerShell):

```
robotpy-update.bat
```

NOTE: This updates packages on your laptop and downloads packages to install onto the roboRIO.

### Update Software on roboRIO

After updating your laptop and downloading files for the roboRIO, connect to the robot and run the following command in a COMMAND shell (not PowerShell):

```
robotpy-update-roborio.bat
```

## New Releases

When new releases come out, this README.md file and the batch files will need to be updated with the new version numbers.
