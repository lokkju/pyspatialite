#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.61)
AC_INIT(libspatialite-amalgamation, 3.0.1, a.furieri@lqt.it)
AC_LANG(C)
AC_CONFIG_AUX_DIR([.])
AC_CONFIG_MACRO_DIR([m4])

AM_INIT_AUTOMAKE
AM_MAINTAINER_MODE

# Checks for header files.
AC_CHECK_HEADERS(stdlib.h,, [AC_MSG_ERROR([cannot find stdlib.h, bailing out])])
AC_CHECK_HEADERS(stdio.h,, [AC_MSG_ERROR([cannot find stdio.h, bailing out])])
AC_CHECK_HEADERS(string.h,, [AC_MSG_ERROR([cannot find string.h, bailing out])])
AC_CHECK_HEADERS(memory.h,, [AC_MSG_ERROR([cannot find memory.h, bailing out])])
AC_CHECK_HEADERS(math.h,, [AC_MSG_ERROR([cannot find math.h, bailing out])])
AC_CHECK_HEADERS(float.h,, [AC_MSG_ERROR([cannot find float.h, bailing out])])
AC_CHECK_HEADERS(fcntl.h,, [AC_MSG_ERROR([cannot find fcntl.h, bailing out])])
AC_CHECK_HEADERS(inttypes.h,, [AC_MSG_ERROR([cannot find inttypes.h, bailing out])])
AC_CHECK_HEADERS(stddef.h,, [AC_MSG_ERROR([cannot find stddef.h, bailing out])])
AC_CHECK_HEADERS(stdint.h,, [AC_MSG_ERROR([cannot find stdint.h, bailing out])])
AC_CHECK_HEADERS(sys/time.h,, [AC_MSG_ERROR([cannot find sys/time.h, bailing out])])
AC_CHECK_HEADERS(unistd.h,, [AC_MSG_ERROR([cannot find unistd.h, bailing out])])


# Checks for programs.
AC_PROG_CXX
AC_PROG_CC
AC_PROG_CPP
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_MAKE_SET
AC_LIBTOOL_WIN32_DLL
AC_PROG_LIBTOOL

# Checks for typedefs, structures, and compiler characteristics.
AC_C_CONST
AC_TYPE_OFF_T
AC_TYPE_SIZE_T
AC_HEADER_TIME
AC_STRUCT_TM
AC_C_VOLATILE

# Checks for library functions.
AC_FUNC_LSTAT
AC_FUNC_LSTAT_FOLLOWS_SLASHED_SYMLINK
AC_FUNC_MEMCMP
AC_FUNC_STAT
AC_FUNC_STRFTIME
AC_CHECK_FUNCS([memset sqrt strcasecmp strerror strncasecmp strstr fdatasync ftruncate getcwd gettimeofday localtime_r memmove strerror])

AC_CONFIG_FILES([Makefile \
		headers/Makefile \
		spatialite.pc])

#-----------------------------------------------------------------------
#   --enable-mathsql
#
AC_ARG_ENABLE(mathsql, [AS_HELP_STRING(
  [--enable-mathsql], [enables SQL math functions [default=yes]])],
  [], [mathsql=yes])
if test x"$enable_mathsql" != "xno"; then
  OMIT_MATHSQL_FLAGS=
else
  OMIT_MATHSQL_FLAGS=-DOMIT_MATHSQL
fi
AC_SUBST(OMIT_MATHSQL_FLAGS)
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
#   --enable-geocallbacks
#
AC_ARG_ENABLE(geocallbacks, [AS_HELP_STRING(
  [--enable-geocallbacks], [enables geometry callbacks [default=yes]])],
  [], [geocallbacks=yes])
if test x"$enable_geocallbacks" != "xno"; then
  OMIT_GEOCALLBACKS_FLAGS=
else
  OMIT_GEOCALLBACKS_FLAGS=-DOMIT_GEOCALLBACKS
fi
AC_SUBST(OMIT_GEOCALLBACKS_FLAGS)
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
#   --enable-proj
#
AC_ARG_ENABLE(proj, [AS_HELP_STRING(
  [--enable-proj], [enables PROJ.4 inclusion [default=yes]])],
  [], [proj=yes])
if test x"$enable_proj" != "xno"; then
  OMIT_PROJ_FLAGS=
  AC_CHECK_HEADERS(proj_api.h,, [AC_MSG_ERROR([cannot find proj_api.h, bailing out])])
  AC_SEARCH_LIBS(pj_init_plus,proj,,AC_MSG_ERROR(['libproj' is required but it doesn't seem to be installed on this system.]),-lm)
else
  OMIT_PROJ_FLAGS=-DOMIT_PROJ
fi
AC_SUBST(OMIT_PROJ_FLAGS)
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
#   --enable-geos
#
AC_ARG_ENABLE(geos, [AS_HELP_STRING(
  [--enable-geos], [enables GEOS inclusion [default=yes]])],
  [], [geos=yes])
if test x"$enable_geos" != "xno"; then
  OMIT_GEOS_FLAGS=
  AC_CHECK_HEADERS(geos_c.h,, [AC_MSG_ERROR([cannot find geos_c.h, bailing out])])
  AC_SEARCH_LIBS(GEOSTopologyPreserveSimplify,geos_c,,AC_MSG_ERROR(['libgeos_c' is required but it doesn't seem to be installed on this system.]),-lm -lgeos)
  #-----------------------------------------------------------------------
  #   --enable-geosadvanced
  #
  AC_ARG_ENABLE(geosadvanced, [AS_HELP_STRING(
	  [--enable-geosadvanced], [enables GEOS advanced features [default=yes]])],
	  [], [geosadvanced=yes])
  if test x"$enable_geosadvanced" != "xno"; then
	  GEOSADVANCED_FLAGS=-DGEOS_ADVANCED
	  AC_SEARCH_LIBS(GEOSCoveredBy,geos_c,,AC_MSG_ERROR([obsolete 'libgeos_c' (< v.3.3.0). please retry specifying: --disable-geosadvanced.]),-lm -lgeos)
  else
	  GEOSADVANCED_FLAGS=
  fi
	  AC_SUBST(GEOSADVANCED_FLAGS)
else
  OMIT_GEOS_FLAGS=-DOMIT_GEOS
fi
AC_SUBST(OMIT_GEOS_FLAGS)

#-----------------------------------------------------------------------
#   --enable-iconv
#
AC_ARG_ENABLE(iconv, [AS_HELP_STRING(
  [--enable-iconv], [enables ICONV inclusion [default=yes]])],
  [], [geos=yes])
if test x"$enable_iconv" != "xno"; then
  OMIT_ICONV_FLAGS=
  AC_CHECK_HEADERS(iconv.h,, [AC_MSG_ERROR([cannot find iconv.h, bailing out])])
# on some systems "iconv()" lives in libc. On others it lives in libiconv
#  on older systems "libiconv()" lives in libiconv
  AC_SEARCH_LIBS(iconv,iconv,,
    AC_SEARCH_LIBS(libiconv,iconv,,AC_MSG_ERROR(['libiconv' is required but it doesn't seem to be installed on this system.]),))
  AC_SEARCH_LIBS(locale_charset,charset,,
    AC_SEARCH_LIBS(nl_langinfo,c,,AC_MSG_ERROR(['libcharset' is required but it doesn't seem to be installed on this system.]),))
else
  OMIT_ICONV_FLAGS=-DOMIT_ICONV
fi
AC_SUBST(OMIT_ICONV_FLAGS)

#-----------------------------------------------------------------------
#   --enable-freexl
#
AC_ARG_ENABLE(freexl, [AS_HELP_STRING(
  [--enable-freexl], [enables FreeXL inclusion [default=yes]])],
  [], [proj=yes])
if test x"$enable_freexl" != "xno"; then
  OMIT_FREEXL_FLAGS=
  AC_CHECK_HEADERS(freexl.h,, [AC_MSG_ERROR([cannot find freexl.h, bailing out])])
  AC_SEARCH_LIBS(freexl_open,freexl,,AC_MSG_ERROR(['libfreexl' is required but it doesn't seem to be installed on this system.]),-lm)
else
  OMIT_FREEXL_FLAGS=-DOMIT_FREEXL
fi
AC_SUBST(OMIT_FREEXL_FLAGS)
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
#   --enable-epsg
#
AC_ARG_ENABLE(epsg, [AS_HELP_STRING(
  [--enable-epsg], [enables full EPSG dataset support [default=yes]])],
  [], [epsg=yes])
if test x"$enable_epsg" != "xno"; then
  OMIT_EPSG_FLAGS=
else
  OMIT_EPSG_FLAGS=-DOMIT_EPSG
fi
AC_SUBST(OMIT_EPSG_FLAGS)
#-----------------------------------------------------------------------

# Checking for MinGW
AM_CONDITIONAL([MINGW], [test "$target_alias" = "mingw32"])
# Checking for Mac OsX
AM_CONDITIONAL([MACOSX], [test "$target_alias" = "macosx"])

AC_OUTPUT
