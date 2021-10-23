# cspell:ignore RPATH
if(POLICY CMP0048)
  cmake_policy(SET CMP0048 NEW)
endif()
#
project(
  pycompwa.ui
  VERSION 0.0.1
  DESCRIPTION "The common Partial Wave Analysis framework"
  LANGUAGES CXX)

cmake_minimum_required(VERSION 3.4 FATAL_ERROR)

set(DEFAULT_BUILD_TYPE "Release")
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Need to add this to the top level CMakeLists.txt
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/src/ComPWA/cmake/Modules/")

# # Configure RPATH
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
if(APPLE)
  list(APPEND CMAKE_INSTALL_RPATH "@loader_path/../lib;@loader_path")
else()
  list(APPEND CMAKE_INSTALL_RPATH "$ORIGIN/:$ORIGIN/../lib")
endif()

# ComPWA needs to be linked statically since scikit-build
# does not handle the RPATH properly. External libraries as
# boost, ROOT etc may still be linked dynamically
add_subdirectory(src/ComPWA)

add_subdirectory(src/pybind11)

include_directories(src/ComPWA)
include_directories(src/pybind11)

# Create python module for ComPWA
pybind11_add_module(ui MODULE src/pycompwa/ui.cpp)

target_include_directories(ui PUBLIC ComPWA)

target_link_libraries(
  ui
  PRIVATE Ascii
          Core
          FunctionTree
          Data
          RootData
          EvtGenGenerator
          MinLogLH
          Minuit2IF
          HelicityFormalism
          Tools
          Plotting)

install(TARGETS ui LIBRARY DESTINATION pycompwa)
