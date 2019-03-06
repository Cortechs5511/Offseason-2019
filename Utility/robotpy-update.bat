@echo off
rem You need to be connected to the Internet to run this script
rem
rem Requires that you have already installed python 3.7+ and the robotpy-installer utility
rem via: py -3 installer.py install-robotpy
rem

rem Adjust these each release
set ROBOTPY_VER=2019.2.2
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

rem Install/upgrade pip modules for programming
@echo on
%PYTHON% -m pip install --upgrade --user pip pyfrc coverage pygame pynetworktables robotpy-ctre robotpy-navx robotpy-rev wpilib robotpy-hal-base robotpy-hal-sim robotpy-installer robotpy-pathfinder robotpy-wpilib-utilities
@if %errorlevel% neq 0 exit /b %errorlevel%

@rem Update robotpy installer
cd %ROBOTPY%
@if %errorlevel% neq 0 exit /b %errorlevel%

%PYTHON% installer.py download-robotpy
@if %errorlevel% neq 0 exit /b %errorlevel%

@rem Download robotpy modules for roboRIO
%PYTHON% installer.py download-opkg python37-robotpy-cscore
@if %errorlevel% neq 0 exit /b %errorlevel%
%PYTHON% installer.py download-opkg python37-robotpy-ctre
@if %errorlevel% neq 0 exit /b %errorlevel%
%PYTHON% installer.py download-pip robotpy-navx
@if %errorlevel% neq 0 exit /b %errorlevel%
%PYTHON% installer.py download-opkg robotpy-rev
@if %errorlevel% neq 0 exit /b %errorlevel%
%PYTHON% installer.py download-opkg robotpy-pathfinder
@if %errorlevel% neq 0 exit /b %errorlevel%
%PYTHON% installer.py download-pip pprofile
@if %errorlevel% neq 0 exit /b %errorlevel%
