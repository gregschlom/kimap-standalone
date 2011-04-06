cmake_minimum_required(VERSION 2.6)
project(zlib)

option(ZLIB_INSTALL "install libraries" YES)

set (zlib_sources
    adler32.c
    compress.c
    crc32.c
    deflate.c
    gzio.c
    infback.c
    inffast.c
    inflate.c
    inftrees.c
    trees.c
    uncompr.c
    zutil.c
)

set(ZLIB_STATIC 1)
add_definitions(-DZLIB_STATIC)
set(LIBRARY_TYPE STATIC)

add_library(zlib ${LIBRARY_TYPE} ${zlib_sources})
target_link_libraries(zlib)

if (ZLIB_INSTALL)
      install(TARGETS zlib
          RUNTIME DESTINATION bin
          LIBRARY DESTINATION lib
          ARCHIVE DESTINATION lib
      )
    install( FILES
        zlib.h
        zconf.h
      DESTINATION include
    )
endif (ZLIB_INSTALL)
    