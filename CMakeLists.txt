if (POLICY CMP0048)
  cmake_policy(SET CMP0048 NEW)
endif()
#
project( pycompwa.ui
  VERSION 0.0.1
  DESCRIPTION "The common Partial Wave Analysis framework"
  LANGUAGES CXX )

cmake_minimum_required (VERSION 3.4 FATAL_ERROR)

set(DEFAULT_BUILD_TYPE "Release")

# Need to add this to the top level CMakeLists.txt
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/ComPWA/cmake/Modules/")

# Find python3
# unfortunately there is a change in the interface of CMake at version 12
# in which the PythonInterp gets deprecated and FindPython3 should be used
set(Python3_FOUND FALSE)
if (${CMAKE_MAJOR_VERSION} EQUAL 3 AND ${CMAKE_MINOR_VERSION} LESS 12)
  find_package(PythonInterp)
  if(${PYTHONINTERP_FOUND} AND ${PYTHON_VERSION_MAJOR} GREATER 2)
    set(Python3_FOUND TRUE)
    set(Python3_EXECUTABLE ${PYTHON_EXECUTABLE})
  endif()
else()
  set (CMAKE_FIND_FRAMEWORK NEVER)
  find_package(Python3)
endif()

if(NOT ${Python3_FOUND})
  message( FATAL_ERROR "Python3 not found!")
endif()

# # Configure RPATH
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
if (APPLE)
  list(APPEND CMAKE_INSTALL_RPATH "@loader_path/../lib;@loader_path")
else ()
  list(APPEND CMAKE_INSTALL_RPATH "$ORIGIN/:$ORIGIN/../lib")
endif ()

# ComPWA needs to be linked statically since scikit-build
# does not handle the RPATH properly. External libraries as
# boost, ROOT etc may still be linked dynamically
add_subdirectory(ComPWA)

add_subdirectory(pybind11)

# Create python module for ComPWA
pybind11_add_module(ui MODULE PyComPWA.cpp)

target_include_directories(ui PUBLIC ComPWA )

target_link_libraries(ui
  PRIVATE Core FunctionTree Data RootData EvtGenGenerator MinLogLH 
          Minuit2IF HelicityFormalism Tools Plotting 
  )

install(TARGETS ui
  LIBRARY DESTINATION pycompwa
  )
