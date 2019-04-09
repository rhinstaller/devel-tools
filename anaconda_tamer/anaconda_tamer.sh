#!/bin/bash

if [ $# -eq 1 ]; then
    HOST="$1"
else
    echo "Missing parameter!" >&2
    echo "" >&2
    echo "$0 <host_address>" >&2
    echo "" >&2
    echo "<host_address> - Address of the VM where Anaconda is running!" >&2
    exit 1
fi

# connect to a remote server with specific options useful for development
#
# StrictHostKeyChecking -- do not check that ssh public key changed (public key is not persistent between reboots)
# UserKnownHostsFile -- do not store public key of the VM (public key is not persistent between reboots)
# ServerAliveInterval -- make the timeout time smaller (in case you will reboot machine which you are connected to)
ssh -t -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=5 "root@$HOST" "tmux attach-session -d -t anaconda"
