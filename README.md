# Diadem Robot V2 — ROS 2 Humble

<div align="center">

![Diadem Logo](https://github.com/rigbetellabs/rbl_docs/blob/main/img/logo.png)

Welcome to the official repository for **Diadem Robot V2** by **RigBetel Labs**.  
A 4-wheel skid-steer robot running ROS 2 Humble with Nav2, SLAM (Cartographer), EKF odometry, YDLidar, and Gazebo simulation.

<a href="https://rigbetellabs.com/">![Website](https://img.shields.io/website?down_color=lightgrey&down_message=offline&label=Rigbetellabs%20Website&style=for-the-badge&up_color=green&up_message=online&url=https%3A%2F%2Frigbetellabs.com%2F)</a>
<a href="https://www.youtube.com/channel/UCfIX89y8OvDIbEFZAAciHEA">![Youtube Subscribers](https://img.shields.io/youtube/channel/subscribers/UCfIX89y8OvDIbEFZAAciHEA?label=YT%20Subscribers&style=for-the-badge)</a>
<a href="https://www.instagram.com/rigbetellabs/">![Instagram](https://img.shields.io/badge/Follow_on-Instagram-pink?style=for-the-badge&logo=appveyor?label=Instagram)</a>

</div>

---

## Table of Contents

- [1. Package Overview](#1-package-overview)
- [2. Prerequisites](#2-prerequisites)
- [3. Installation](#3-installation)
  - [3.1 Clone the Repository](#31-clone-the-repository)
  - [3.2 Install Dependencies](#32-install-dependencies)
  - [3.3 Configure USB Ports (Real Robot Only)](#33-configure-usb-ports-real-robot-only)
  - [3.4 Build the Workspace](#34-build-the-workspace)
- [4. WiFi Setup (Real Robot)](#4-wifi-setup-real-robot)
- [5. Robot Modes](#5-robot-modes)
  - [5.1 Demo Mode (Auto-start on Boot)](#51-demo-mode-auto-start-on-boot)
  - [5.2 Development Mode (Manual Launch)](#52-development-mode-manual-launch)
- [6. Launch Sequence](#6-launch-sequence)
  - [6.1 Real Robot — Firmware Only](#61-real-robot--firmware-only)
  - [6.2 Real Robot — Full Bringup (Nav2 + SLAM)](#62-real-robot--full-bringup-nav2--slam)
  - [6.3 Simulation (Gazebo)](#63-simulation-gazebo)
- [7. SLAM — Mapping](#7-slam--mapping)
- [8. Navigation — Using a Pre-built Map](#8-navigation--using-a-pre-built-map)
- [9. Teleoperation](#9-teleoperation)
- [10. ROS Topics Reference](#10-ros-topics-reference)
- [11. Robot Parameters](#11-robot-parameters)
- [12. Diagnostics](#12-diagnostics)
- [13. Charging Instructions](#13-charging-instructions)
- [14. LED Indicators](#14-led-indicators)

---

## 1. Package Overview

| Package | Description |
|---|---|
| `diadem_description` | URDF/Xacro robot model, meshes, RViz configs |
| `diadem_firmware` | micro-ROS agent, sensor/actuator bringup, Realsense camera |
| `diadem_bringup` | Top-level launch — orchestrates all subsystems for real robot & sim |
| `diadem_gazebo` | Gazebo worlds and robot spawner |
| `diadem_slam` | Cartographer SLAM and slam_toolbox configs |
| `diadem_navigation` | Nav2 config, params, and pre-built maps |
| `diadem_odom` | EKF odometry (robot_localization), RTAB-Map odometry |
| `diadem_gps_uti` | GPS utilities |
| `ydlidar_ros2_driver` | YDLidar ROS 2 driver |
| `YDLidar-SDK` | YDLidar C++ SDK |
| `ros_tcp` | ROS–TCP endpoint for Unity/external tools |

---

## 2. Prerequisites

- **OS:** Ubuntu 22.04 LTS
- **ROS 2:** [Humble Hawksbill](https://docs.ros.org/en/humble/Installation.html)
- **micro-ROS workspace:** `~/uros_ws` built and sourced
- **Colcon** build tool

```bash
# Verify ROS 2 installation
ros2 --version
```

---

## 3. Installation

### 3.1 Clone the Repository

```bash
mkdir -p ~/diadem_ws/src
cd ~/diadem_ws/src
git clone https://github.com/rigbetellabs/diadem.git .
```

### 3.2 Install Dependencies

Install all required apt packages:

```bash
cd ~/diadem_ws/src
cat requirements.txt | xargs sudo apt-get install -y
```

Key dependencies installed:

| Package | Purpose |
|---|---|
| `ros-humble-nav2-bringup` | Navigation2 stack |
| `ros-humble-slam-toolbox` | SLAM Toolbox |
| `ros-humble-cartographer-ros` | Cartographer SLAM |
| `ros-humble-robot-state-publisher` | TF / URDF publishing |
| `ros-humble-teleop-twist-keyboard` | Keyboard teleoperation |
| `ros-humble-v4l2-camera` | USB camera driver |

### 3.3 Configure USB Ports (Real Robot Only)

Run the install script once to set up udev rules (maps physical USB ports to `/dev/esp`, `/dev/lidar`) and add your user to the `dialout` group:

```bash
cd ~/diadem_ws/src
source install.sh
```

> [!IMPORTANT]
> Log out and back in after running `install.sh` for the group changes to take effect.

USB port mapping after setup:

| Symlink | Device | Connected To |
|---|---|---|
| `/dev/esp` | USB port `1-5` | ESP32 micro-ROS MCU |
| `/dev/lidar` | USB port `1-3.2` | YDLidar |

### 3.4 Build the Workspace

```bash
cd ~/diadem_ws
source /opt/ros/humble/setup.bash
source ~/uros_ws/install/setup.bash   # micro-ROS
colcon build --symlink-install
source install/setup.bash
```

> [!TIP]
> Add the following lines to your `~/.bashrc` to source automatically on every new terminal:
> ```bash
> source /opt/ros/humble/setup.bash
> source ~/uros_ws/install/setup.bash
> source ~/diadem_ws/install/setup.bash
> export ROS_DOMAIN_ID=169
> ```

---

## 4. WiFi Setup (Real Robot)

When the robot first powers on it has no WiFi connection. Use a mobile hotspot to configure it.

### Step 1 — Create a mobile hotspot

| Field | Value |
|---|---|
| Hotspot Name | `admin` |
| Hotspot Password | `adminadmin` |

### Step 2 — Power on the robot

Wait for the robot to connect to your hotspot (IP appears on the robot display).

### Step 3 — SSH into the robot

```bash
# By hostname
ssh diadem@rigbetellabs.local
# Password: rbl@2020

# By IP (shown on robot display)
ssh diadem@<robot-ip>
```

### Step 4 — Connect to your WiFi network

```bash
# List available networks
sudo nmcli dev wifi list --rescan yes

# Connect
sudo nmcli device wifi connect "your-wifi-name" password "your-wifi-password"
```

> [!IMPORTANT]
> The SSH session will drop after connecting. Wait ~30 seconds for the robot to reconnect to your WiFi. The new IP will appear on the robot display.

### Step 5 — Reconnect over WiFi

Connect your laptop to the same WiFi network, then SSH using the new IP:

```bash
ssh diadem@<new-robot-ip>
# Password: rbl@2020
```

### Remote PC — Set ROS Domain ID

The robot runs on `ROS_DOMAIN_ID=169`. Run this in every new terminal on your remote PC:

```bash
export ROS_DOMAIN_ID=169
```

---

## 5. Robot Modes

### 5.1 Demo Mode (Auto-start on Boot)

In Demo Mode the robot launches all ROS nodes automatically on boot via a systemd user service. No SSH or manual launching needed.

```bash
cd ~/diadem_ws/src
./demo.sh
```

This enables and starts `rbl_upstart.service`, which runs `start.sh` on every boot.

### 5.2 Development Mode (Manual Launch)

Development Mode stops the auto-start service so you can launch nodes manually for testing.

```bash
cd ~/diadem_ws/src
./development.sh
```

> [!NOTE]
> After switching to Development Mode, no ROS nodes will start on the next boot. You must launch manually using the commands below.

---

## 6. Launch Sequence

All launch commands assume the workspace is sourced and `ROS_DOMAIN_ID=169` is set.

### 6.1 Real Robot — Firmware Only

Starts micro-ROS agent, MAVROS, hubble scripts, and Realsense camera (optional):

```bash
# With Realsense camera (default: True)
ros2 launch diadem_firmware bringup.launch.py

# Without Realsense
ros2 launch diadem_firmware bringup.launch.py realsense:=False
```

Nodes launched:

| Node | Description |
|---|---|
| micro-ROS agent | Bridges ESP32 MCU ↔ ROS 2 |
| MAVROS | MAVLink bridge (optional, for MAVLink devices) |
| hubble_scripts | Network and navigation status publishers |
| Realsense camera | Intel RealSense depth/RGB stream |

### 6.2 Real Robot — Full Bringup (Nav2 + SLAM)

Use `diadem_bringup` for the complete real-robot stack: state publishers, YDLidar, micro-ROS, EKF odometry, SLAM/Nav2.

**Exploration / SLAM mode** (builds a map while navigating):

```bash
ros2 launch diadem_bringup autobringup.launch.py \
  use_sim_time:=False \
  exploration:=True
```

**Navigation mode** (uses a pre-built map):

```bash
ros2 launch diadem_bringup autobringup.launch.py \
  use_sim_time:=False \
  exploration:=False \
  map:=/path/to/your_map.yaml
```

Launch arguments:

| Argument | Default | Description |
|---|---|---|
| `use_sim_time` | `False` | `True` for Gazebo simulation |
| `exploration` | `True` | `True` = SLAM, `False` = Nav with map |
| `map` | `nav2_test_map.yaml` | Path to map YAML (used when `exploration:=False`) |
| `rvizconfig` | nav2 default | Absolute path to custom RViz config |

### 6.3 Simulation (Gazebo)

**Full sim bringup** (SLAM + Nav2 in Gazebo):

```bash
ros2 launch diadem_bringup autobringup.launch.py \
  use_sim_time:=True \
  exploration:=True \
  world:=nav2_test_world.sdf
```

Available simulation worlds:

| World file | Description |
|---|---|
| `nav2_test_world.sdf` | Default indoor test environment |
| `simple_warehouse.sdf` | Warehouse layout |

Sim-only arguments:

| Argument | Default | Description |
|---|---|---|
| `world` | `nav2_test_world.sdf` | World file name (in `diadem_gazebo/worlds/`) |
| `headless` | `False` | Run Gazebo server only (no GUI) |
| `x_pose` | `0.0` | Robot spawn X position |
| `y_pose` | `0.0` | Robot spawn Y position |
| `z_pose` | `0.1` | Robot spawn Z position |
| `yaw_pose` | `0.0` | Robot spawn yaw |

**Spawn robot only** (if Gazebo already running):

```bash
ros2 launch diadem_gazebo spawn_robot.launch.py
```

---

## 7. SLAM — Mapping

SLAM is handled by **Cartographer** (default) or **slam_toolbox**.

**Cartographer:**

```bash
ros2 launch diadem_slam cartographer.launch.py \
  use_sim_time:=False \
  exploration:=True
```

**slam_toolbox:**

```bash
ros2 launch diadem_slam slam_toolbox.launch.py
```

**Save the map** once you're satisfied with it:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/diadem_ws/src/diadem_navigation/maps/my_map
```

This creates `my_map.pgm` and `my_map.yaml`. Pass the YAML path as the `map` argument to use it for navigation.

---

## 8. Navigation — Using a Pre-built Map

```bash
ros2 launch diadem_bringup autobringup.launch.py \
  use_sim_time:=False \
  exploration:=False \
  map:=~/diadem_ws/src/diadem_navigation/maps/my_map.yaml
```

This launches:
- `map_server` — loads the saved map
- `amcl` — AMCL localization
- Nav2 lifecycle manager
- EKF odometry (`robot_localization`)
- YDLidar, micro-ROS, state publishers

Use RViz to set the **2D Pose Estimate** and then send **Nav2 Goals**.

**AMCL navigation (standalone):**

```bash
ros2 launch diadem_navigation amcl_navigation.launch.py
```

---

## 9. Teleoperation

Teleoperate the robot via keyboard after launching firmware or full bringup:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Or publish directly to `/cmd_vel`:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

---

## 10. ROS Topics Reference

### Subscriber Topics (Commands → Robot)

| Topic | Type | Description |
|---|---|---|
| `/cmd_vel` | `geometry_msgs/Twist` | Velocity command (linear + angular) |
| `/motor_control/enable` | `std_msgs/Bool` | Enable individual motor control |
| `/motor_control/right_front` | `std_msgs/Int32` | Right-front motor speed (−255 to 255) |
| `/motor_control/left_front` | `std_msgs/Int32` | Left-front motor speed (−255 to 255) |
| `/motor_control/right_back` | `std_msgs/Int32` | Right-back motor speed (−255 to 255) |
| `/motor_control/left_back` | `std_msgs/Int32` | Left-back motor speed (−255 to 255) |
| `/pid/mode` | `std_msgs/Int32` | PID mode: `0`=stop, `1`=fast, `2`=smooth, `3`=supersmooth |
| `/pid/constants` | `std_msgs/Float32MultiArray` | Custom PID values `[P, I, D]` |
| `/pid/custom/enable` | `std_msgs/Bool` | Enable custom PID mode |
| `/pid/custom/save` | `std_msgs/Float32MultiArray` | Save custom PID values |
| `/hill_hold_control` | `std_msgs/Bool` | Enable hill-hold (slope braking) |
| `/microros_domain_id` | `std_msgs/Int32` | Change firmware ROS domain ID |
| `/buzzer/functions/enable` | `std_msgs/Bool` | Enable/disable buzzer |
| `/buzzer/battery_low/enable` | `std_msgs/Bool` | Enable/disable low-battery buzzer |
| `/ecu/restart` | `std_msgs/Bool` | Restart ESP32 ECU ⚠️ |
| `/diagnostics/test` | `std_msgs/Int32` | Trigger a diagnostics test |

> [!WARNING]
> `/motor_control/enable` allows direct individual motor control. **Lift the robot off the ground** before using this to prevent accidents.

> [!WARNING]
> `/ecu/restart` will reset the ESP32. GPIO pins may enter a floating state momentarily.

### Publisher Topics (Robot → ROS)

| Topic | Type | Description |
|---|---|---|
| `/cmd_vel` | `geometry_msgs/Twist` | Current velocity command echo |
| `/imu/data` | `sensor_msgs/Imu` | IMU orientation, angular velocity, linear acceleration |
| `/battery/percentage` | `std_msgs/Float32` | Remaining battery % |
| `/battery/voltage` | `std_msgs/Float32` | Battery voltage (22.4V–29.4V) |
| `/wheel/ticks` | `std_msgs/Int32MultiArray` | Encoder ticks `[lf, lb, rf, rb]` |
| `/wheel/vel` | `std_msgs/Float32MultiArray` | Wheel velocities `[lf, lb, rf, rb]` |
| `/wheel/rpm` | `std_msgs/Int32MultiArray` | Wheel RPM `[lf, lb, rf, rb]` |
| `/robot/nav_status` | `std_msgs/Int32` | Navigation status |
| `/robot/network_status` | `std_msgs/String` | Network connectivity status |
| `/estop/status` | `std_msgs/Bool` | Emergency stop button state |

#### Battery Beep Reference

| Battery % | Behaviour |
|---|---|
| 100 – 20 | Silent |
| 20 – 15 | Beep every 2 minutes |
| 15 – 10 | Beep every 1 minute |
| Below 10 | Very frequent beeping |
| 0 | Continuous beep |

> [!CAUTION]
> Do not discharge the battery below **10%** — permanent battery damage may result.

---

## 11. Robot Parameters

| Parameter | Value |
|---|---|
| Drive Type | Skid Steer (4-wheel) |
| Wheel Diameter | 0.35 m |
| Wheel Separation (Width) | 0.58 m |
| Wheel Separation (Length) | 0.5 m |
| Motor Type | DC Geared Motor |
| Motor RPM | 110 |
| Encoder Type | Magnetic Encoder |
| PPR (Pulses Per Revolution) | 600 |
| Microcontroller | DOIT ESP32 DevKit V1 |
| Payload Capacity | 200–250 kg |
| Battery Type | Lithium-ion 193 AH 6S 24V |
| Battery Life | ~3 hours |

---

## 12. Diagnostics

SSH into the robot and run:

```bash
cd ~/diadem_ws/src/diadem_firmware/scripts
python3 diadem_diagnostics.py
```

The script checks:
- IMU data consistency
- Battery status
- Motor functionality
- Topic publishing rates

> [!NOTE]
> Ensure the robot is on a flat surface and has sufficient space to move before running motor tests.

---

## 13. Charging Instructions

1. **Switch the robot to charging mode** before plugging in the charger.
2. The charger requires **220V 16A AC** input — verify your power socket supports this.
3. Plug in the charger and wait until the charge indicator shows full.

> [!CAUTION]
> Never plug in the charger without first setting the robot to charging mode.

---

## 14. LED Indicators

| LED Pattern | Meaning |
|---|---|
| All orange fading | ROS/RC not connected |
| White status lights, white headlights, red brake lights | ROS mode connected |
| Purple status lights, white headlights, red brake lights | RC mode active |
| Orange indicator lights, red brake lights | Turning (forward-left or forward-right) |
| Yellow indicator lights, red brake lights | Reversing |
| Red indicator lights, red brake lights | Battery low |
| All lights red | Emergency stop pressed |

---

## Contact

For support and collaboration, reach out to **RigBetel Labs**:  
🌐 [rigbetellabs.com](https://rigbetellabs.com)