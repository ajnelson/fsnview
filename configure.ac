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
                 src/fsnview
                 src/Makefile])
AC_OUTPUT
