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

# Tips

* The terminal will show QEMU monitor of the VM, allowing some control over it.
  E.g., issue `sendkey ctrl-alt-f1` to switch the VM to the console,
  use `q` to quit, etc.
* If you pass `--append inst.sshd`, a port will be forwarded for you,
  check the output during the `updates` phase.
* This tool can be used to quickly test the installation with different
  kickstarts. You can point the installer to your own server, or
  you can use a built-in one by supplying `--variable-kickstart`
  during the `prime` phase; in the latter case
  you'll have to provide one with `--kickstart` in the `updates` phase.
