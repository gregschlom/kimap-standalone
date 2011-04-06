project(cyrus-sasl)
cmake_minimum_required(VERSION 2.6.2)
set(PACKAGE "cyrus-sasl")
set(VERSION "2.1.22")
set(PLUGINDESTINATION lib/sasl2)
set(PLUGINDIR ${CMAKE_INSTALL_PREFIX}/${PLUGINDESTINATION})
set(CONFIGDIR ${CMAKE_INSTALL_PREFIX}/${PLUGINDESTINATION})

option(STATIC_PLUGIN "test" ON)
option(STATIC_LIBRARY "test" ON)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules)

if(WINCE)
    find_package(Wcecompat REQUIRED)
    include_directories(${WCECOMPAT_INCLUDE_DIR})
    set(CMAKE_REQUIRED_INCLUDES ${CMAKE_REQUIRED_INCLUDES} ${WCECOMPAT_INCLUDE_DIR})
    set(CMAKE_REQUIRED_LIBRARIES ${CMAKE_REQUIRED_LIBRARIES} ${WCECOMPAT_LIBRARIES})
endif(WINCE)

include(CheckIncludeFiles)
check_include_files(sys/socket.h   HAVE_SYS_SOCKET_H)
check_include_files(syslog.h       HAVE_SYSLOG)
check_include_files(time.h         HAVE_TIME_H)
check_include_files(unistd.h       HAVE_UNISTD_H)

include(CheckFunctionExists)
check_function_exists(getaddrinfo       HAVE_GETADDRINFO)
check_function_exists(getnameinfo       HAVE_GETNAMEINFO)
#check_function_exists(getpid            HAVE_GETPID)
check_function_exists(gettimeofday      HAVE_GETTIMEOFDAY)
check_include_files(snprintf       HAVE_SNPRINTF)
if(WIN32)
  set(HAVE_SNPRINTF 1)
endif(WIN32)

include(CheckSymbolExists)
check_symbol_exists(SOCKLENT_T        "sys/socket.h"               SOCKLENT_T)

# TODO: HAVE_SOCKADDR_SA_LEN

if(WIN32)
  add_definitions(-DWIN32)
  add_definitions(-D_CRT_SECURE_NO_DEPRECATE)
  add_definitions(-D_CRT_NONSTDC_NO_DEPRECATE)
  set(HIER_DELIMITER '\\\\')
else(WIN32)
  set(HIER_DELIMITER '/')
endif(WIN32)

if(CMAKE_COMPILER_IS_GNUCC)
  set(HAVE___ATTRIBUTE__ 1)
endif(CMAKE_COMPILER_IS_GNUCC)

configure_file(${CMAKE_SOURCE_DIR}/config.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/config.h)

if(WIN32 AND NOT WINCE)
set(additional_link_libs ws2_32)
endif(WIN32 AND NOT WINCE)

if(WINCE)
set(additional_link_libs ws2 ${WCECOMPAT_LIBRARIES})
endif(WINCE)

set(plugin_SRCS
  plugins/plugin_common.c
  plugins/plugin_common.h
)

if(STATIC_LIBRARY)
    set(LIBSASL_STATIC 1)
    configure_file(include/prop.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/prop.h)
    add_definitions(-DLIBSASL_STATIC)
endif(STATIC_LIBRARY)

if(STATIC_PLUGIN)
    add_definitions(-DSTATIC_PLUGIN
                    -DSTATIC_ANONYMOUS
                    -DSTATIC_CRAMMD5
                    -DSTATIC_DIGESTMD5
                    -DSTATIC_LOGIN
                    -DSTATIC_PLAIN)

    #
    # ANONYMOUS
    #
    set(anonymous_SRCS
      plugins/anonymous.c
      plugins/anonymous_init.c
    )
    #
    # LOGIN
    #
    set(login_SRCS
      plugins/login.c
      plugins/login_init.c
    )
    #
    # PLAIN
    #
    set(plain_SRCS
      plugins/plain.c
      plugins/plain_init.c
    )
    #
    # CRAMMD5
    #
    set(crammd5_SRCS
      plugins/cram.c
      plugins/crammd5_init.c
    )
    #
    # DIGESTMD5
    #
    set(digestmd5_SRCS
      plugins/digestmd5.c
      plugins/digestmd5_init.c
    )
    set(plugin_SRCS ${plugin_SRCS} ${anonymous_SRCS} ${login_SRCS} ${plain_SRCS} ${crammd5_SRCS} ${digestmd5_SRCS})
endif(STATIC_PLUGIN)

set(sasl_SRCS
  lib/auxprop.c
  lib/canonusr.c
  lib/checkpw.c
  lib/client.c
  lib/common.c
  lib/config.c
  lib/external.c
  lib/getaddrinfo.c
  lib/getnameinfo.c
  lib/getsubopt.c
  lib/md5.c
  lib/saslutil.c
  lib/server.c
  lib/seterror.c
)
if(NOT HAVE_SNPRINTF)
  list(APPEND sasl_SRCS lib/snprintf.c)
endif(NOT HAVE_SNPRINTF)
if(WIN32)
  list(APPEND sasl_SRCS lib/windlopen.c)
else(WIN32)
  list(APPEND sasl_SRCS lib/dlopen.c)
endif(WIN32)

set(sasl_HDRS
  lib/saslint.h
  lib/staticopen.h
)
set(sasl_inc_HDRS
  include/exits.h
  include/gai.h
  include/hmac-md5.h
  include/md5.h
  include/md5global.h
  include/sasl.h
  include/saslplug.h
  include/saslutil.h
)

include_directories(
  ${CMAKE_SOURCE_DIR}/include
  ${CMAKE_CURRENT_BINARY_DIR}
)
if(STATIC_LIBRARY)
    add_library(sasl2 STATIC ${sasl_SRCS} ${sasl_HDRS} ${sasl_inc_HDRS} ${plugin_SRCS})
    install(FILES ${CMAKE_CURRENT_BINARY_DIR}/prop.h DESTINATION include/sasl)
else(STATIC_LIBRARY)
    add_library(sasl2 SHARED ${sasl_SRCS} ${sasl_HDRS} ${sasl_inc_HDRS} ${plugin_SRCS})
    set_target_properties(sasl2 PROPERTIES DEFINE_SYMBOL LIBSASL_EXPORTS)
    install(FILES include/prop.h DESTINATION include/sasl)
endif(STATIC_LIBRARY)
target_link_libraries(sasl2 ${additional_link_libs})
install(TARGETS sasl2 RUNTIME DESTINATION bin LIBRARY DESTINATION lib ARCHIVE DESTINATION lib)
install(FILES ${sasl_inc_HDRS} DESTINATION include/sasl)

if(NOT STATIC_PLUGIN)
    #
    # ANONYMOUS
    #
    set(anonymous_SRCS
      plugins/anonymous.c
      plugins/anonymous_init.c
    )
    add_library(saslANONYMOUS MODULE ${anonymous_SRCS} ${plugin_SRCS})
    target_link_libraries(saslANONYMOUS sasl2 ${additional_link_libs})
    install(TARGETS saslANONYMOUS DESTINATION ${PLUGINDESTINATION})

    #
    # LOGIN
    #
    set(login_SRCS
      plugins/login.c
      plugins/login_init.c
    )
    add_library(saslLOGIN MODULE ${login_SRCS} ${plugin_SRCS})
    target_link_libraries(saslLOGIN sasl2 ${additional_link_libs})
    install(TARGETS saslLOGIN DESTINATION ${PLUGINDESTINATION})

    #
    # PLAIN
    #
    set(plain_SRCS
      plugins/plain.c
      plugins/plain_init.c
    )
    add_library(saslPLAIN MODULE ${plain_SRCS} ${plugin_SRCS})
    target_link_libraries(saslPLAIN sasl2 ${additional_link_libs})
    install(TARGETS saslPLAIN DESTINATION ${PLUGINDESTINATION})

    #
    # CRAMMD5
    #
    set(crammd5_SRCS
      plugins/cram.c
      plugins/crammd5_init.c
    )
    add_library(saslCRAMMD5 MODULE ${crammd5_SRCS} ${plugin_SRCS})
    target_link_libraries(saslCRAMMD5 sasl2 ${additional_link_libs})
    install(TARGETS saslCRAMMD5 DESTINATION ${PLUGINDESTINATION})

    #
    # DIGESTMD5
    #
    set(digestmd5_SRCS
      plugins/digestmd5.c
      plugins/digestmd5_init.c
    )
    add_library(saslDIGESTMD5 MODULE ${digestmd5_SRCS} ${plugin_SRCS})
    target_link_libraries(saslDIGESTMD5 sasl2 ${additional_link_libs})
    install(TARGETS saslDIGESTMD5 DESTINATION ${PLUGINDESTINATION})
endif(NOT STATIC_PLUGIN)

#
# Pluginviewer
#
add_executable(sasl2_pluginviewer utils/pluginviewer.c)
target_link_libraries(sasl2_pluginviewer sasl2 ${additional_link_libs})
install(TARGETS sasl2_pluginviewer DESTINATION bin)
