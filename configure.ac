#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.59])
AC_INIT(fsnview, 0.1.0, ajnelson@cs.ucsc.edu)
AC_CONFIG_SRCDIR([src/fsnview.in])
AM_INIT_AUTOMAKE

# Checks for programs.
AC_PROG_CC
AC_PROG_INSTALL
AC_PROG_MAKE_SET

dnl Search for Python 2.7.3, which catches the MacPorts version in OS X.  Linuxes should be on 2.7.3 as well.
m4_define_default([_AM_PYTHON_INTERPRETER_LIST],[python2 python2.7])
AM_PATH_PYTHON(2.7.3)
AC_CHECK_PROGS(PYTHON3, [python3.3 python3.2 python3.1 python3])
if test "x$PYTHON3" == "x"; then
  AC_MSG_ERROR([Python 3 not found.])
fi

# Checks for Python modules: Crypto
AX_PYTHON_MODULE(Crypto)
if test "$HAVE_PYMOD_CRYPTO" != "yes"; then
  # The user should supply the target Python binary.
  # Refs:
  # * http://lists.gnu.org/archive/html/bug-automake/2011-01/msg00108.html
  # * via: http://stackoverflow.com/questions/4619664/autofoo-test-for-maximum-version-of-python#comment5396323_4824135
  AC_MSG_ERROR([Could not find Python module "Crypto", which should have been installed by the "deps/install_dependent_package-....sh" script for your operating system.  If you have not run that script, please do so; if you have, pass as an environment variable the Python *2* (not 3) binary with which Crypto is affiliated. For example, in OS X: PYTHON=/opt/local/bin/python2.7 ./configure ...])
fi
AX_PYTHON_MODULE(fuse)
if test "$HAVE_PYMOD_FUSE" != "yes"; then
  AC_MSG_ERROR([Could not find Python module "fuse", which should have been installed by the "deps/install_dependent_package-....sh" script for your operating system.  If you have not run that script, please do so; if you have, pass as an environment variable the Python *2* (not 3) binary with which fuse is affiliated. For example, in OS X: PYTHON=/opt/local/bin/python2.7 ./configure ...])
fi

# Checks for libraries.

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.

AC_CONFIG_FILES([Makefile
                 deps/Makefile
                 etc/Makefile
                 src/Makefile
                 src/analyze.sh
                 src/analyze_with_fiwalk.sh
                 src/analyze_with_py360.sh
                 src/analyze_with_uxtaf.sh
                 src/compare.sh
                 src/fsnview
                 src/log_and_run_script.sh
                 src/report.sh])
AC_CONFIG_SUBDIRS([deps/sleuthkit
                   deps/uxtaf])
AC_OUTPUT
