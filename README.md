# Anaconda Tamer
Tool to help with remote development of the Anaconda installer. This tool will ssh to the running installation and enable you debugging from the local terminal.

Benefits: 

* Your local settings stays the same because ssh will use your settings automatically
* You can easily copy from and to the VM
* You can completely control text and vnc installations

Drawbacks:

* You *can't* control graphical installation


## How to use
This repository contains main script `anaconda_tamer.sh`. The script needs an address (IP or hostname) of the VM running the Anaconda installation. This VM must be started with the inst.sshd parameter. Everything else should be automatically solved by *Anaconda Tamer*.

When the Anaconda tamer ssh to the installation environment it automatically attach running tmux session. The benefit of this is that Anaconda installer is running from there so we can even use PDB debugger easily and in case the connection will be dropped you won't lost any work.

``
./anaconda_tamer.sh <address>
``

## Useful info
If you are using tmux locally then you will end with nested tmux in your local tmux instance. In that case you can control the inner tmux by pressing prefix (Ctrl+b) twice, after that everything will be send to the inner instance. You don't need this if you have other than default prefix.

# Warning!
The ssh have strict host key checking disabled. This is not secure and can be used by the *man-in-the-middle attack*! This behavior is required to adapt to a typical Anaconda development when the installation environment generates an ssh key on boot. See `StrictHostKeyChecking` in `ssh_config(5)` for more info.
