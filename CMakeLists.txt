cmake_minimum_required(VERSION 3.15...3.27)
project(pxblat LANGUAGES C CXX)

# Find Python
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

# Find pybind11 - try multiple methods
find_package(pybind11 CONFIG QUIET)
if(NOT pybind11_FOUND)
    # Try to find it via Python
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -c "import pybind11; print(pybind11.get_cmake_dir())"
        OUTPUT_VARIABLE pybind11_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ERROR_QUIET
    )
    if(pybind11_DIR)
        list(APPEND CMAKE_PREFIX_PATH "${pybind11_DIR}")
        find_package(pybind11 CONFIG REQUIRED)
    else()
        message(FATAL_ERROR "pybind11 not found. Please install: pip install pybind11")
    endif()
endif()

# Platform-specific settings
if(APPLE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -D_LIBCPP_DISABLE_AVAILABILITY")
endif()

# Find OpenSSL
find_package(OpenSSL REQUIRED)

# Common compile flags
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -pthread")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Source file collection
file(GLOB_RECURSE LIBPXBLAT_CORE_SOURCES "src/pxblat/extc/src/core/*.c")
file(GLOB_RECURSE LIBPXBLAT_AUX_SOURCES "src/pxblat/extc/src/aux/*.c")
file(GLOB_RECURSE LIBPXBLAT_NET_SOURCES "src/pxblat/extc/src/net/*.c")

# Exclude ONLY aux/net.c (not netlib.c or internet.c)
list(FILTER LIBPXBLAT_AUX_SOURCES EXCLUDE REGEX "/aux/net\\.c$")

set(LIBPXBLAT_SOURCES
    ${LIBPXBLAT_CORE_SOURCES}
    ${LIBPXBLAT_AUX_SOURCES}
    ${LIBPXBLAT_NET_SOURCES}
)

# Python binding sources
set(PXBLAT_PYTHON_SOURCES
    src/pxblat/extc/bindings/faToTwoBit.cpp
    src/pxblat/extc/bindings/twoBitToFa.cpp
    src/pxblat/extc/bindings/gfServer.cpp
    src/pxblat/extc/bindings/pygfServer.cpp
    src/pxblat/extc/bindings/gfClient.cpp
)

file(GLOB PXBLAT_BINDER_SOURCES "src/pxblat/extc/bindings/binder/*.cpp")
list(APPEND PXBLAT_PYTHON_SOURCES ${PXBLAT_BINDER_SOURCES})

# Build libpxblat as a shared library
add_library(libpxblat SHARED ${LIBPXBLAT_SOURCES})

target_include_directories(libpxblat PRIVATE
    src/pxblat/extc/include/core
    src/pxblat/extc/include/aux
    src/pxblat/extc/include/net
    ${OPENSSL_INCLUDE_DIR}
)

target_compile_definitions(libpxblat PRIVATE
    _FILE_OFFSET_BITS=64
    _LARGEFILE_SOURCE
    _GNU_SOURCE
    PXBLATLIB
)

# Link libraries
target_link_libraries(libpxblat PUBLIC
    ${OPENSSL_SSL_LIBRARY}
    ${OPENSSL_CRYPTO_LIBRARY}
)

# Link libm on Unix-like systems
if(UNIX)
    target_link_libraries(libpxblat PUBLIC m)
endif()

# Set output name and properties
set_target_properties(libpxblat PROPERTIES
    PREFIX ""
    OUTPUT_NAME "libpxblat"
)

if(APPLE)
    set_target_properties(libpxblat PROPERTIES
        SUFFIX ".dylib"
        INSTALL_NAME_DIR "@loader_path"
    )
else()
    set_target_properties(libpxblat PROPERTIES
        SUFFIX ".so"
    )
endif()

# Build _extc Python extension
pybind11_add_module(_extc ${PXBLAT_PYTHON_SOURCES})

target_include_directories(_extc PRIVATE
    src/pxblat/extc/include/core
    src/pxblat/extc/include/aux
    src/pxblat/extc/include/net
    src/pxblat/extc/bindings
    ${OPENSSL_INCLUDE_DIR}
)

target_compile_definitions(_extc PRIVATE
    VERSION_INFO=${PROJECT_VERSION}
)

if(NOT CMAKE_BUILD_TYPE MATCHES Debug)
    target_compile_definitions(_extc PRIVATE
        DBG_MACRO_DISABLE
    )
endif()

target_link_libraries(_extc PRIVATE
    libpxblat
    ${OPENSSL_SSL_LIBRARY}
    ${OPENSSL_CRYPTO_LIBRARY}
)

if(UNIX)
    target_link_libraries(_extc PRIVATE m)
endif()

# Set visibility
set_target_properties(_extc PROPERTIES
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN ON
)
