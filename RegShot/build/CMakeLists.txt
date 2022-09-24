###
### CMake settings
###
# see http://www.cmake.org/Wiki/CMake_Policies
cmake_minimum_required(VERSION 2.8)


###
### Project settings
###
project(RegShot)

set(EXE_SUFFIX "-alpha")


###
### Project options
###

## Build options
# --> Microsoft Visual C++
# see http://msdn.microsoft.com/en-us/library/aa278396(v=VS.60).aspx
#     http://msdn.microsoft.com/en-us/library/2kzt1wy3(v=VS.71).aspx
option(MSVC_SHARED_RT "MSVC: Build with shared runtime libs (/MD)" OFF)
option(MSVC_STHREADED_RT "MSVC: Build with single-threaded static runtime libs (/ML until VS .NET 2003)" OFF)


###
### Sources, headers, directories and libs
###
file(GLOB sources "../src/[a-zA-Z]*.c")
file(GLOB private_headers "../src/[a-zA-Z]*.h")
file(GLOB resources "../src/[a-zA-Z]*.rc")
file(GLOB manifests "../src/res/[a-zA-Z]*.manifest")


###
### General compilation settings
###
if(WIN32)
	if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
		set(CMAKE_INSTALL_PREFIX "C:/")
	endif()
endif()

# GCC specialities
if(CMAKE_COMPILER_IS_GNUC)
	message(FATAL_ERROR "GNU compiler not supported. Patch submissions welcome.")
endif()

# Microsoft VisualC++ specialities
if(MSVC)
	### General stuff
	# a) Change MSVC runtime library settings (/MD[d], /MT[d], /ML[d] (single-threaded until VS 2003))
	#    plus set lib suffix for later use and project label accordingly
	# see http://msdn.microsoft.com/en-us/library/aa278396(v=VS.60).aspx
	#     http://msdn.microsoft.com/en-us/library/2kzt1wy3(v=VS.71).aspx
	set(LIB_RT_SUFFIX "md")	# CMake defaults to /MD for MSVC
	set(LIB_RT_OPTION "/MD")
	#
	if(NOT MSVC_SHARED_RT)	# User wants to have static runtime libraries (/MT, /ML)
		if(MSVC_STHREADED_RT)	# User wants to have old single-threaded static runtime libraries
			set(LIB_RT_SUFFIX "ml")
			set(LIB_RT_OPTION "/ML")
			if(NOT ${MSVC_VERSION} LESS 1400)
				message(FATAL_ERROR "Single-threaded static runtime libraries (/ML) only available until VS .NET 2003 (7.1).")
			endif()
		else()
			set(LIB_RT_SUFFIX "mt")
			set(LIB_RT_OPTION "/MT")
		endif()

		# correct linker options
		foreach(flag_var  CMAKE_C_FLAGS  CMAKE_CXX_FLAGS)
			foreach(config_name  ""  DEBUG  RELEASE  MINSIZEREL  RELWITHDEBINFO)
				set(var_name "${flag_var}")
				if(NOT "${config_name}" STREQUAL "")
					set(var_name "${var_name}_${config_name}")
				endif()
				string(REPLACE "/MD" "${LIB_RT_OPTION}" ${var_name} "${${var_name}}")
			endforeach()
		endforeach()
	endif()
	#
	set(LABEL_SUFFIX "${LABEL_SUFFIX} ${LIB_RT_SUFFIX}")

	### Project stuff
	if(NOT ${MSVC_VERSION} LESS 1400)
		add_definitions(-D_CRT_SECURE_NO_WARNINGS)
	endif()

	if(CMAKE_CL_64)
		set(PLATFORM_SUFFIX "-x64")
	else()
		set(PLATFORM_SUFFIX "")
	endif()
endif()


###
### Executable
###
add_executable(${PROJECT_NAME}${PLATFORM_SUFFIX}${EXE_SUFFIX}
	WIN32
	${sources}
	${private_headers}
	${resources}
	${manifests}
)

set_target_properties(${PROJECT_NAME}${PLATFORM_SUFFIX}${EXE_SUFFIX}
	PROPERTIES
		PROJECT_LABEL "${PROJECT_NAME}${PLATFORM_SUFFIX}${EXE_SUFFIX}${LABEL_SUFFIX}"
)
