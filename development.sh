#!/bin/bash

# Stop for current device session && Disable the service so that on the next reboot it won't restart
sudo systemctl stop rbl_upstart && sudo systemctl disable rbl_upstart  > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Upstart serice Stopped and Disable successfully, good to go in development mode..."
else
    echo "Something went wrong..!"
fi
