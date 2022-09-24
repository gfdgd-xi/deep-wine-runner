/*
    Copyright 2011 XhmikosR

    This file is part of Regshot.

    Regshot is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Regshot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Regshot; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/


#ifndef REGSHOT_VERSION_H
#define REGSHOT_VERSION_H


#define DO_STRINGIFY(x) #x
#define STRINGIFY(x)    DO_STRINGIFY(x)

#define REGSHOT_VERSION_MAJOR     1
#define REGSHOT_VERSION_MINOR     8
#define REGSHOT_VERSION_PATCH     3
#define REGSHOT_VERSION_REV       0

#define REGSHOT_VERSION_COPYRIGHT "Copyright (C) 1999-2012, all contributors"
#define REGSHOT_VERSION_NUM       REGSHOT_VERSION_MAJOR,REGSHOT_VERSION_MINOR,REGSHOT_VERSION_PATCH,REGSHOT_VERSION_REV
#define REGSHOT_VERSION           STRINGIFY(REGSHOT_VERSION_MAJOR) ", " STRINGIFY(REGSHOT_VERSION_MINOR) ", " STRINGIFY(REGSHOT_VERSION_PATCH) ", " STRINGIFY(REGSHOT_VERSION_REV)
#define REGSHOT_VERSION_STRING    STRINGIFY(REGSHOT_VERSION_MAJOR) "." STRINGIFY(REGSHOT_VERSION_MINOR) "." STRINGIFY(REGSHOT_VERSION_PATCH) "-beta1V5"

#ifdef _WIN64
#define REGSHOT_TITLE             "Regshot x64"
#define REGSHOT_RESULT_FILE       "~res-x64"
#define REGSHOT_VERSION_PLATFORM  "x64"
#else
#define REGSHOT_TITLE             "Regshot"
#define REGSHOT_RESULT_FILE       "~res"
#define REGSHOT_VERSION_PLATFORM  "win32"
#endif // _WIN64

#ifdef _DEBUG
#define REGSHOT_VERSION_BUILDTYPE "d"
#else
#define REGSHOT_VERSION_BUILDTYPE "r"
#endif

#define DO_STRINGIFY(x) #x
#define STRINGIFY(x)    DO_STRINGIFY(x)

#if defined(__GNUC__)
    #define REGSHOT_VERSION_COMPILER "GCC "STRINGIFY(__GNUC__)"."STRINGIFY(__GNUC_MINOR__)"."STRINGIFY(__GNUC_PATCHLEVEL__)
#elif defined(__INTEL_COMPILER)
    #if __INTEL_COMPILER >= 1200
        #define REGSHOT_VERSION_COMPILER "Intel Compiler 12"
    #else
        #define REGSHOT_VERSION_COMPILER "Intel Compiler (version unknown)"
    #endif
#elif defined(WDK_BUILD)
    #if _MSC_VER == 1600
        #if (_MSC_FULL_VER >= 160040219)
            #define REGSHOT_VERSION_COMPILER "WDK (MSVC 2010 SP1)"
        #else
            #define REGSHOT_VERSION_COMPILER "WDK (MSVC 2010)"
        #endif
    #elif _MSC_VER == 1500
        #if (_MSC_FULL_VER == 150030729)
            #define REGSHOT_VERSION_COMPILER "WDK"
        #else
            #define REGSHOT_VERSION_COMPILER "WDK (version unknown)"
        #endif
    #endif
#elif defined(_MSC_VER)
    #if _MSC_VER == 1600
        #if (_MSC_FULL_VER >= 160040219)
            #define REGSHOT_VERSION_COMPILER "MSVC 2010 SP1"
        #else
            #define REGSHOT_VERSION_COMPILER "MSVC 2010"
        #endif
    #elif _MSC_VER == 1500
        #if (_MSC_FULL_VER >= 150030729)
            #define REGSHOT_VERSION_COMPILER "MSVC 2008 SP1"
        #else
            #define REGSHOT_VERSION_COMPILER "MSVC 2008"
        #endif
    #else
        #define REGSHOT_VERSION_COMPILER "MSVC (version unknown)"
    #endif
#else
    #define REGSHOT_VERSION_COMPILER "(Unknown compiler)"
#endif

#define REGSHOT_VERSION_DESCRIPTION   REGSHOT_VERSION_STRING ", " REGSHOT_VERSION_PLATFORM ", " REGSHOT_VERSION_BUILDTYPE ", " REGSHOT_VERSION_COMPILER


#endif // REGSHOT_VERSION_H
