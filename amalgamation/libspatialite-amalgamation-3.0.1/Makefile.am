ACLOCAL_AMFLAGS = -I m4

AM_CFLAGS = -D_LARGE_FILE=1 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE=1 \
        -DSQLITE_ENABLE_RTREE=1 -DNDEBUG=1 -DSPL_AMALGAMATION=1 \
	@OMIT_GEOS_FLAGS@ @GEOSADVANCED_FLAGS@ @OMIT_PROJ_FLAGS@ \
	@OMIT_ICONV_FLAGS@ @OMIT_MATHSQL_FLAGS@ \
	@OMIT_EPSG_FLAGS@ @OMIT_GEOCALLBACKS_FLAGS@ @OMIT_FREEXL_FLAGS@

INCLUDES = @CFLAGS@
INCLUDES += -I$(top_srcdir)/src/headers

lib_LTLIBRARIES = libspatialite.la

libspatialite_la_SOURCES = spatialite.c \
	sqlite3.c

if MINGW
libspatialite_la_LDFLAGS = -version-info 4:0:2 -no-undefined
libspatialite_la_LIBADD = 
else
libspatialite_la_LDFLAGS = -version-info 4:0:2
libspatialite_la_LIBADD = -lpthread -ldl
endif

AUTOMAKE_OPTIONS = dist-zip

EXTRA_DIST = makefile.vc nmake.opt 

SUBDIRS = headers

pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = spatialite.pc
