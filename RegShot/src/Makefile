#******************************************************************************
#*  Copyright 2011 XhmikosR
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
#*  makefile
#*    makefile for building Regshot with GCC
#*
#******************************************************************************


CC=gcc.exe

all:.all
distclean: clean

#DEBUG=yes
#64BIT=yes

ifeq ($(64BIT),yes)
    MY_PREFIX=x86_64-w64-mingw32-
    CFLAGS=-DWIN64 -D_WIN64 -D_WIN32_WINNT=0x0502
    OPTFLAGS=-O3 -m64
    STACK_SIZE=67108864
else
    CFLAGS=-DWIN32 -D_WIN32 -D_WIN32_WINNT=0x0500
    OPTFLAGS=-O3 -march=i686 -msse -mfpmath=sse
    STACK_SIZE=33554432
endif

ifeq ($(DEBUG),yes)
    CFLAGS+=-DDEBUG -D_DEBUG -g
else
    CFLAGS+=-DNDEBUG -UDEBUG
endif

SRCS_C=\
    fileshot.c \
    language.c \
    misc.c \
    output.c \
    regshot.c \
    setup.c \
    ui.c \
    winmain.c

RESSRC=regshot.rc

TARGET_DIR=../bin/GCC/

ifeq ($(DEBUG),yes)
    MY_DIR_PREFIX=Debug
else
    MY_DIR_PREFIX=Release
endif

ifeq ($(64BIT),yes)
    MY_ARCH=x64
else
    MY_ARCH=Win32
endif

OBJ_DIR=$(TARGET_DIR)$(MY_DIR_PREFIX)_$(MY_ARCH)/obj/

OUTFLAGS=-MMD -o\

TARGET_EXE=$(TARGET_DIR)$(MY_DIR_PREFIX)_$(MY_ARCH)/Regshot.exe


# Targets

.all: outdirs $(TARGET_EXE)

.PHONY: outdirs $(OBJ_DIR)
outdirs: $(OBJ_DIR)
$(OBJ_DIR):
	$(shell test -d $(@) || mkdir -p $(@))


.PHONY: clean
clean:
	rm -f $(TARGET_EXE)
	rm -r -f $(OBJ_DIR)


# Commands

OBJS+=$(SRCS_C:%.c=$(OBJ_DIR)%.o) $(RESSRC:%.rc=$(OBJ_DIR)%.res.o)

$(OBJ_DIR)%.o: %.c
	@echo $<
	@$(MY_PREFIX)$(CC) -c $(CFLAGS) $(OPTFLAGS) $(OUTFLAGS) $@ $<

$(OBJ_DIR)%.res.o: %.rc
	@echo $<
	@$(MY_PREFIX)windres -o $@ $<

$(TARGET_EXE): $(OBJS)
	@echo $@
	@$(MY_PREFIX)$(CC) -mwindows -Wl,--stack=$(STACK_SIZE) -o $@ $(OBJS)
ifneq ($(DEBUG),yes)
	@$(MY_PREFIX)strip $@
endif

-include $(SRCS_C:%.c=$(OBJ_DIR)%.d)
