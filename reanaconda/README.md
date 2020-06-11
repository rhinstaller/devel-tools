# reanaconda

A script to make testing different updates.img in QEMU faster.
This is achieved by separating the installation into two stages,
with a checkpoint before downloading updates.img.

# Requirements

Python 3.6+ (3.7+?), docopt, QEMU, netcat.

# Usage example

```
$ cd $ANACONDA_CHECKOUT
$ ./reanaconda.py prime --sensible --tree http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/32/Everything/x86_64/os
$ # modify smth in an Anaconda, regenerate updates.img with scripts/makeupdates
$ ./reanaconda.py updates path/to/updates.img
$ # or: echo updates.img | entr -r ./scripts/reanaconda updates updates.img
$ ./reanaconda.py cleanup
```
