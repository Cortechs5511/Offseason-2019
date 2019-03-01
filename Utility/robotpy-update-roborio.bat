@echo off
rem You need to be connected to the robot to run this script
rem
rem Requires that you have already run the robotpy-update.bat script
rem and want to update the roboRIO with the downloaded packages
rem
rem Change following according to your system
if "%PYTHON%" == "" set PYTHON=py -3
set ROBOTPY_VER=2019.2.0
set ROBOTPY=%HOMEPATH%\Desktop\frc-2019\robotpy-%ROBOTPY_VER%

rem Search for installation of python
for %%X in (python py) do (
  where /q %%X && set PYTHON=%%X
)

rem Force -3 if Windows install running via old py command
if %PYTHON% == py set PYTHON=py -3

if defined PYTHON goto foundPython
echo "***ERROR*** Failed to find a Python interpreter in your PATH"
exit /b 1

:foundPython

cd %ROBOTPY%
rem Install/update robotpy on roboRIO
%PYTHON% installer.py install-robotpy
if %errorlevel% neq 0 exit /b %errorlevel%

rem Install robotpy modules for roboRIO
%PYTHON% installer.py install-opkg python37-robotpy-cscore
%PYTHON% installer.py install-opkg python37-robotpy-ctre
%PYTHON% installer.py install-opkg robotpy-rev
%PYTHON% installer.py install-opkg robotpy-pathfinder
%PYTHON% installer.py install-pip robotpy-navx

