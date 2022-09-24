@ECHO OFF
rem ******************************************************************************
rem *  Copyright 2010-2011 XhmikosR
rem *
rem *  This file is part of Regshot.
rem *
rem *  Regshot is free software; you can redistribute it and/or modify
rem *  it under the terms of the GNU General Public License as published by
rem *  the Free Software Foundation; either version 2 of the License, or
rem *  (at your option) any later version.
rem *
rem *  Regshot is distributed in the hope that it will be useful,
rem *  but WITHOUT ANY WARRANTY; without even the implied warranty of
rem *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
rem *  GNU General Public License for more details.
rem *
rem *  You should have received a copy of the GNU General Public License
rem *  along with Regshot; if not, write to the Free Software
rem *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
rem *
rem *
rem *  make_packages.bat
rem *    Batch file for building Regshot with WDK and creating the zip packages
rem ******************************************************************************


SETLOCAL
CD /D %~dp0


rem Check for the help switches
IF /I "%~1" == "help"   GOTO SHOWHELP
IF /I "%~1" == "/help"  GOTO SHOWHELP
IF /I "%~1" == "-help"  GOTO SHOWHELP
IF /I "%~1" == "--help" GOTO SHOWHELP
IF /I "%~1" == "/?"     GOTO SHOWHELP


rem Check for the first switch
IF "%~1" == "" (
  SET INPUTDIRx86=bin\WDK\Release_Win32
  SET INPUTDIRx64=bin\WDK\Release_x64
  SET SUFFIX=_WDK
) ELSE (
  IF /I "%~1" == "WDK" (
    SET INPUTDIRx86=bin\WDK\Release_Win32
    SET INPUTDIRx64=bin\WDK\Release_x64
    SET SUFFIX=_WDK
    GOTO START
  )
  IF /I "%~1" == "/WDK" (
    SET INPUTDIRx86=bin\WDK\Release_Win32
    SET INPUTDIRx64=bin\WDK\Release_x64
    SET SUFFIX=_WDK
    GOTO START
  )
  IF /I "%~1" == "-WDK" (
    SET INPUTDIRx86=bin\WDK\Release_Win32
    SET INPUTDIRx64=bin\WDK\Release_x64
    SET SUFFIX=_WDK
    GOTO START
  )
  IF /I "%~1" == "--WDK" (
    SET INPUTDIRx86=bin\WDK\Release_Win32
    SET INPUTDIRx64=bin\WDK\Release_x64
    SET SUFFIX=_WDK
    GOTO START
  )
  IF /I "%~1" == "VS2010" (
    SET INPUTDIRx86=bin\VS2010\Release_Win32
    SET INPUTDIRx64=bin\VS2010\Release_x64
    SET SUFFIX=_VS2010
    GOTO START
  )
  IF /I "%~1" == "/VS2010" (
    SET INPUTDIRx86=bin\VS2010\Release_Win32
    SET INPUTDIRx64=bin\VS2010\Release_x64
    SET SUFFIX=_VS2010
    GOTO START
  )
  IF /I "%~1" == "-VS2010" (
    SET INPUTDIRx86=bin\VS2010\Release_Win32
    SET INPUTDIRx64=bin\VS2010\Release_x64
    SET SUFFIX=_VS2010
    GOTO START
  )
  IF /I "%~1" == "--VS2010" (
    SET INPUTDIRx86=bin\VS2010\Release_Win32
    SET INPUTDIRx64=bin\VS2010\Release_x64
    SET SUFFIX=_VS2010
    GOTO START
  )
  IF /I "%~1" == "VS2008" (
    SET INPUTDIRx86=bin\VS2008\Release_Win32
    SET INPUTDIRx64=bin\VS2008\Release_x64
    SET SUFFIX=_VS2008
    GOTO START
  )
  IF /I "%~1" == "/VS2008" (
    SET INPUTDIRx86=bin\VS2008\Release_Win32
    SET INPUTDIRx64=bin\VS2008\Release_x64
    SET SUFFIX=_VS2008
    GOTO START
  )
  IF /I "%~1" == "-VS2008" (
    SET INPUTDIRx86=bin\VS2008\Release_Win32
    SET INPUTDIRx64=bin\VS2008\Release_x64
    SET SUFFIX=_VS2008
    GOTO START
  )
  IF /I "%~1" == "--VS2008" (
    SET INPUTDIRx86=bin\VS2008\Release_Win32
    SET INPUTDIRx64=bin\VS2008\Release_x64
    SET SUFFIX=_VS2008
    GOTO START
  )
  IF /I "%~1" == "ICL12" (
    SET INPUTDIRx86=bin\ICL12\Release_Win32
    SET INPUTDIRx64=bin\ICL12\Release_x64
    SET SUFFIX=_ICL12
    GOTO START
  )
  IF /I "%~1" == "/ICL12" (
    SET INPUTDIRx86=bin\ICL12\Release_Win32
    SET INPUTDIRx64=bin\ICL12\Release_x64
    SET SUFFIX=_ICL12
    GOTO START
  )
  IF /I "%~1" == "-ICL12" (
    SET INPUTDIRx86=bin\ICL12\Release_Win32
    SET INPUTDIRx64=bin\ICL12\Release_x64
    SET SUFFIX=_ICL12
    GOTO START
  )
  IF /I "%~1" == "--ICL12" (
    SET INPUTDIRx86=bin\ICL12\Release_Win32
    SET INPUTDIRx64=bin\ICL12\Release_x64
    SET SUFFIX=_ICL12
    GOTO START
  )
  IF /I "%~1" == "GCC" (
    SET INPUTDIRx86=bin\GCC\Release_Win32
    SET INPUTDIRx64=bin\GCC\Release_x64
    SET SUFFIX=_GCC
    GOTO START
  )
  IF /I "%~1" == "/GCC" (
    SET INPUTDIRx86=bin\GCC\Release_Win32
    SET INPUTDIRx64=bin\GCC\Release_x64
    SET SUFFIX=_GCC
    GOTO START
  )
  IF /I "%~1" == "-GCC" (
    SET INPUTDIRx86=bin\GCC\Release_Win32
    SET INPUTDIRx64=bin\GCC\Release_x64
    SET SUFFIX=_GCC
    GOTO START
  )
  IF /I "%~1" == "--GCC" (
    SET INPUTDIRx86=bin\GCC\Release_Win32
    SET INPUTDIRx64=bin\GCC\Release_x64
    SET SUFFIX=_GCC
    GOTO START
  )

  ECHO.
  ECHO Unsupported commandline switch!
  ECHO Run "%~nx0 help" for details about the commandline switches.
  CALL :SUBMSG "ERROR" "Compilation failed!"
)


:START
SET "TEMP_NAME=temp_zip%SUFFIX%"

IF NOT EXIST "..\%INPUTDIRx86%\Regshot.exe" CALL :SUBMSG "ERROR" "Compile Regshot Win32 first!"
IF NOT EXIST "..\%INPUTDIRx64%\Regshot.exe" CALL :SUBMSG "ERROR" "Compile Regshot x64 first!"

CALL :SubGetVersion
CALL :SubZipFiles %INPUTDIRx86% Win32
CALL :SubZipFiles %INPUTDIRx64% x64


:END
TITLE Finished!
ECHO.
ENDLOCAL
PAUSE
EXIT /B


:SubZipFiles
TITLE Creating the %2 ZIP file...
CALL :SUBMSG "INFO" "Creating the %2 ZIP file..."

IF EXIST "%TEMP_NAME%"     RD /S /Q "%TEMP_NAME%"
IF NOT EXIST "%TEMP_NAME%" MD "%TEMP_NAME%"

COPY /Y /V "..\gpl.txt"            "%TEMP_NAME%\GPL.txt"
COPY /Y /V "..\files\history.txt"  "%TEMP_NAME%\History.txt"
COPY /Y /V "..\files\language.ini" "%TEMP_NAME%\"
COPY /Y /V "..\files\readme.txt"   "%TEMP_NAME%\Readme.txt"
COPY /Y /V "..\files\regshot.ini"  "%TEMP_NAME%\"
COPY /Y /V "..\%1\Regshot.exe"     "%TEMP_NAME%\"

PUSHD "%TEMP_NAME%"
START "" /B /WAIT "..\..\files\7za.exe" a -tzip -mx=9 "Regshot_%REGSHOTVER%_%2%SUFFIX%.zip" >NUL
IF %ERRORLEVEL% NEQ 0 CALL :SUBMSG "ERROR" "Compilation failed!"

CALL :SUBMSG "INFO" "Regshot_%REGSHOTVER%_%2%SUFFIX%.zip created successfully!"

MOVE /Y "Regshot_%REGSHOTVER%_%2%SUFFIX%.zip" "..\" >NUL
POPD
IF EXIST "%TEMP_NAME%" RD /S /Q "%TEMP_NAME%"
EXIT /B


:SubGetVersion
rem Get the version
FOR /F "tokens=3,4 delims= " %%K IN (
  'FINDSTR /I /L /C:"define REGSHOT_VERSION_MAJOR" "..\src\version.h"') DO (
  SET "VerMajor=%%K"&Call :SubVerMajor %%VerMajor:*Z=%%)
FOR /F "tokens=3,4 delims= " %%L IN (
  'FINDSTR /I /L /C:"define REGSHOT_VERSION_MINOR" "..\src\version.h"') DO (
  SET "VerMinor=%%L"&Call :SubVerMinor %%VerMinor:*Z=%%)
FOR /F "tokens=3,4 delims= " %%M IN (
  'FINDSTR /I /L /C:"define REGSHOT_VERSION_PATCH" "..\src\version.h"') DO (
  SET "VerBuild=%%M"&Call :SubVerBuild %%VerBuild:*Z=%%)
FOR /F "tokens=3,4 delims= " %%N IN (
  'FINDSTR /I /L /C:"define REGSHOT_VERSION_REV" "..\src\version.h"') DO (
  SET "VerRev=%%N"&Call :SubVerRev %%VerRev:*Z=%%)

SET REGSHOTVER=%VerMajor%.%VerMinor%.%VerBuild%
EXIT /B


:SubVerMajor
SET VerMajor=%*
EXIT /B


:SubVerMinor
SET VerMinor=%*
EXIT /B


:SubVerBuild
SET VerBuild=%*
EXIT /B


:SubVerRev
SET VerRev=%*
EXIT /B


:SHOWHELP
TITLE "%~nx0 %1"
ECHO. & ECHO.
ECHO Usage:   %~nx0 [GCC^|ICL12^|VS2008^|VS2010^|WDK]
ECHO.
ECHO Notes:   You can also prefix the commands with "-", "--" or "/".
ECHO          The arguments are not case sensitive.
ECHO. & ECHO.
ECHO Executing "%~nx0" will use the defaults: "%~nx0 WDK"
ECHO.
ENDLOCAL
EXIT /B


:SUBMSG
ECHO. & ECHO ______________________________
ECHO [%~1] %~2
ECHO ______________________________ & ECHO.
IF /I "%~1"=="ERROR" (
  PAUSE
  EXIT
) ELSE (
  EXIT /B
)
