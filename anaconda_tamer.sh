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


ssh -t -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "root@$HOST" "tmux attach-session -d -t anaconda"
