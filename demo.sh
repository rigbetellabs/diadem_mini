	#!/bin/bash

# Get LAN card
# Get current IP address of the robot, not required but still doing this
current_ip=$(hostname -I | sed -r 's/\s+$//' | grep -oE '^[^[:space:]]+') # Remove trailing whitespaces as well as any other text followed
# current_ip = 192.168.0.96 # If in any case


upstart_status=$(ls /lib/systemd/system/ | grep rbl_upstart)

# Check if service exists if yes start the service

if [ -n "$upstart_status" ]; then
	echo "Found a existing upstart service, enabling it..." 
	sudo systemctl enable rbl_upstart.service > /dev/null 2>&1 && sudo systemctl start rbl_upstart.service 

	if [ $? -eq 0 ]; then
    		echo "Upstart service Enabled and Started successfully, robot in demonstration mode..."
	else
    		echo "Something went wrong..!"
	fi

# If not add a new one
else
	echo "Did not found a upstart service, creating new one.."
	rosrun robot_upstart install diadem_mini_firmware/launch/demo_mode.launch --job rbl_upstart --symlink > /dev/null 2>&1
        if [ $? -eq 0 ]; then
                echo "Upstart service installed successfully..."
        else
                echo "Something went wrong..!"
        fi
	# Below not working, rbl_upstart: No IP address on wlp0s20f3, cannot roslaunch.
	# rosrun robot_upstart install acrux_firmware/launch/demo_mode.launch --job rbl_upstart --master http://192.168.0.96:11311 --interface wlp0s20f3 --symlink

	sudo systemctl daemon-reload && sudo systemctl start rbl_upstart

        if [ $? -eq 0 ]; then
                echo "Upstart service Enabled and Started successfully, robot in demonstration mode..."
        else
                echo "Something went wrong..!"
        fi
fi
