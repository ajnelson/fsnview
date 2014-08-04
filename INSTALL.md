# Installing FSNView

First, run the package installation script under `deps` appropriate for your operating system.  These scripts require `sudo` to install packages.

(You can configure your PATH variables by appending `deps/bashrc` to your `~/.bashrc` file, followed by reloading your shell or running `source ~/.bashrc`.)

Last, run the normal installation calls:

    ./bootstrap.sh
    ./configure
    make
    make install

`./configure` respects `--prefix`.  A build dependency quirk in UPartsFS means that `./bootstrap.sh` also accepts the environment variable `$prefix`, which should match what you pass to `./configure`.

If it looks like The SleuthKit is building twice, it is.  That's the UPartsFS quirk.  It is not a permanent quirk.
