# Installing FSNView

First, run the package installation script under `deps` appropriate for your operating system.  These scripts require `sudo` to install packages.

(You can configure your PATH variables by appending `deps/bashrc` to your `~/.bashrc` file, followed by reloading your shell or running `source ~/.bashrc`.)

Last, run the normal installation calls:

    ./bootstrap.sh
    ./configure
    make
    make install

(`./configure` respects `--prefix`.)
