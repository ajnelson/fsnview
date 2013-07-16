# Installing FSNView

First, run the package installation script under `deps` appropriate for your operating system.  These scripts require `sudo` to install packages.

Then, build the dependent modules:

    deps/build_submodules.sh

(Pass `local` to that build script if your PATH variables are configured to let you install to the prefix `~/local`.)

Last, run the normal installation calls:

    ./bootstrap.sh
    ./configure
    make
    make install

`./configure` respects `--prefix`.
