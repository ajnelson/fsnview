#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT(fsnview, 0.0.0, ajnelson@cs.ucsc.edu)
AC_CONFIG_SRCDIR([src/fsnview.in])
AM_INIT_AUTOMAKE

# Checks for programs.
AC_PROG_INSTALL
AC_PROG_MAKE_SET

dnl Search for Python 2.7.3, which catches the MacPorts version in OS X.  Linuxes should be on 2.7.3 as well.
AM_PATH_PYTHON(2.7.3)

# Checks for libraries.

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.

AC_CONFIG_FILES([Makefile
                 deps/Makefile
                 src/fsnview
                 src/Makefile])
AC_OUTPUT
