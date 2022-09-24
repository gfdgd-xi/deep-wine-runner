#******************************************************************************
#*  Copyright 2010-2011 XhmikosR
#*
#*  This file is part of Regshot.
#*
#*  Regshot is free software; you can redistribute it and/or modify
#*  it under the terms of the GNU General Public License as published by
#*  the Free Software Foundation; either version 2 of the License, or
#*  (at your option) any later version.
#*
#*  Regshot is distributed in the hope that it will be useful,
#*  but WITHOUT ANY WARRANTY; without even the implied warranty of
#*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#*  GNU General Public License for more details.
#*
#*  You should have received a copy of the GNU General Public License
#*  along with Regshot; if not, write to the Free Software
#*  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#*
#*
#*  makefile.mak
#*    makefile for building Regshot with WDK
#*
#*    Use build_wdk.bat and set there your WDK directory.
#******************************************************************************


# Remove the .SILENT directive in order to display all the commands
.SILENT:


CC = cl.exe
LD = link.exe
RC = rc.exe

!IFDEF x64
BINDIR  = ..\bin\WDK\Release_x64
!ELSE
BINDIR  = ..\bin\WDK\Release_Win32
!ENDIF
OBJDIR  = $(BINDIR)\obj
EXE     = $(BINDIR)\Regshot.exe
SRC     = ..\src
RES     = $(SRC)\res


DEFINES = /D "_WINDOWS" /D "NDEBUG" /D "_CRT_SECURE_NO_WARNINGS" /D "WDK_BUILD"
CFLAGS  = /nologo /c /Fo"$(OBJDIR)/" /W3 /EHsc /MD /O2 /GL /MP $(DEFINES)
LDFLAGS = /NOLOGO /WX /INCREMENTAL:NO /RELEASE /OPT:REF /OPT:ICF /MERGE:.rdata=.text \
          /DYNAMICBASE /NXCOMPAT /LTCG /DEBUG
LIBS    = advapi32.lib comdlg32.lib kernel32.lib shell32.lib user32.lib
RFLAGS  = /l 0x0409


!IFDEF x64
CFLAGS  = $(CFLAGS) /D "_WIN64" /D "_WIN32_WINNT=0x0502"
LIBS    = $(LIBS) msvcrt_win2003.obj
LDFLAGS = $(LDFLAGS) /STACK:67108864 /SUBSYSTEM:WINDOWS,5.02 /MACHINE:X64
RFLAGS  = $(RFLAGS) /d "_WIN64"
!ELSE
CFLAGS  = $(CFLAGS) /D "WIN32" /D "_WIN32_WINNT=0x0500"
LIBS    = $(LIBS) msvcrt_win2000.obj
LDFLAGS = $(LDFLAGS) /STACK:33554432 /LARGEADDRESSAWARE /SUBSYSTEM:WINDOWS,5.0 /MACHINE:X86
RFLAGS  = $(RFLAGS) /d "WIN32"
!ENDIF


###############
##  Targets  ##
###############
BUILD:	CHECKDIRS $(EXE)

CHECKDIRS:
	IF NOT EXIST "$(OBJDIR)" MD "$(OBJDIR)"

CLEAN:
	ECHO Cleaning... & ECHO.
	IF EXIST "$(EXE)"                DEL "$(EXE)"
	IF EXIST "$(OBJDIR)\*.obj"       DEL "$(OBJDIR)\*.obj"
	IF EXIST "$(OBJDIR)\Regshot.res" DEL "$(OBJDIR)\Regshot.res"
	IF EXIST "$(BINDIR)\Regshot.pdb" DEL "$(BINDIR)\Regshot.pdb"
	-IF EXIST "$(OBJDIR)"            RD /Q "$(OBJDIR)"
	-IF EXIST "$(BINDIR)"            RD /Q "$(BINDIR)"

REBUILD:	CLEAN BUILD


####################
##  Object files  ##
####################
OBJECTS= \
    $(OBJDIR)\fileshot.obj \
    $(OBJDIR)\language.obj \
    $(OBJDIR)\misc.obj \
    $(OBJDIR)\output.obj \
    $(OBJDIR)\regshot.obj \
    $(OBJDIR)\regshot.res \
    $(OBJDIR)\setup.obj \
    $(OBJDIR)\ui.obj \
    $(OBJDIR)\winmain.obj


##################
##  Batch rule  ##
##################
{$(SRC)}.c{$(OBJDIR)}.obj::
    $(CC) $(CFLAGS) /Tc $<


################
##  Commands  ##
################
$(EXE): $(OBJECTS)
	$(RC) $(RFLAGS) /fo"$(OBJDIR)\regshot.res" "$(SRC)\regshot.rc" >NUL
	$(LD) $(LDFLAGS) $(LIBS) $(OBJECTS) /OUT:"$(EXE)"


####################
##  Dependencies  ##
####################
$(OBJDIR)\fileshot.obj: \
    $(SRC)\fileshot.c \
    $(SRC)\global.h

$(OBJDIR)\language.obj: \
    $(SRC)\language.c \
    $(SRC)\global.h

$(OBJDIR)\misc.obj: \
    $(SRC)\misc.c \
    $(SRC)\global.h

$(OBJDIR)\output.obj: \
    $(SRC)\output.c \
    $(SRC)\global.h

$(OBJDIR)\regshot.obj: \
    $(SRC)\regshot.c \
    $(SRC)\global.h \
    $(SRC)\version.h

$(OBJDIR)\regshot.res: \
    $(SRC)\regshot.rc \
    $(SRC)\resource.h \
    $(RES)\Regshot.exe.manifest \
    $(RES)\regshot.ico \
    $(SRC)\version.h

$(OBJDIR)\setup.obj: \
    $(SRC)\setup.c \
    $(SRC)\global.h

$(OBJDIR)\ui.obj: \
    $(SRC)\ui.c \
    $(SRC)\global.h

$(OBJDIR)\winmain.obj: \
    $(SRC)\winmain.c \
    $(SRC)\global.h \
    $(SRC)\version.h
