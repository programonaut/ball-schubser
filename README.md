# Ball 🥎 Schubser 🤖

A robot 🤖 that pushes a ball 🥎 (into a goal 🥅).

[<img src="media/ball-schubser_front_side_new_desc.jpg" width="400"/>](media/ball-schubser_front_side_new_desc.jpg)

**Check out the paper we published here: [Development of an Autonomous Robot for Detecting and Collecting Objects](paper/Term-Paper_v1.pdf) and the Demo Video here: [Demo Video - Ball Schubser](https://youtu.be/InvO-HXr4YA)**

## Contributors

- Anton Bracke
- Domenic Gosein
- Jannis Seefeld
- Jan Mayer
- Maximilian Kürschner

## Paper
You can find the paper for this project here

---

## Startup Instructions

1. Clone this repo
2. Inside `.env` add `MASTER_IP=<your-ip>`
3. Run `docker-compose up -d --remove-orphans`
4. Start Turtlebot and connect to via SSH `ssh ubuntu@<your-ip>` with default password: `turtlebot`
5. Set `export ROS_MASTER_URI=<your-ip>`
6. Run `sh ~/launch.sh`
7. Run `sh ~/cam.sh`
 
### Simplified (beta)

1. Clone this repo
2. Execute `export BIP=<your bots ip> && export MIP=<your pc ip>`
3. Execute `start-everything`

## Raspberry Pi 🐢 bot Preparation

To prepare the image for the Raspberry Pi follow these instructions: https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/#sbc-setup

After the micro SD card is ready, boot it from your Turtlebot, connect via SSH: `ssh ubuntu@<TURTLEBOT IP>` (default password: `turtlebot`) and do the following:

1. Run: `sudo usermod -aG root ubuntu` to make the user root (see Lessons Learned).
2. Add your network to the `/etc/netplan/50-cloud-init.yaml` or prepare and copy it via SCP: `scp 50-cloud-init.yaml ubuntu@<TURTLEBOT IP>:/etc/netplan/50-cloud-init.yaml`. Also refer to this [template](turtlebot/50-cloud-init.yaml).
3. Edit: `nano ~/.bashrc` to add the below variables and: `source ~/.bashrc`.
   
   ```bash
   export ROS_MASTER_URI=http://<REMOTE PC IP>:11311
   export ROS_HOSTNAME=<TURTLEBOT IP>
   ```

4. Install Raspberry Pi Cam and dependencies with the following commands:
   
   ```bash
   sudo apt install libraspberrypi-dev libraspberrypi0 libpigpiod-if-dev ros-noetic-compressed-image-transport ros-noetic-camera-info-manager ros-noetic-diagnostic-updater
   cd ~/catkin/src
   git clone https://github.com/UbiquityRobotics/raspicam_node
   catkin_make
   ```

5. Run: `export TURTLEBOT3_MODEL=Burger` to set the Turtlebot model.
6. Start without LIDAR sensor: `roslaunch turtlebot3_bringup turtlebot3_core.launch`.
7. Start the Cam via:
   
   ```bash
   rosparam set cv_camera/device_id 0
   rosrun cv_camera cv_camera_node
   ```

For step 5, 6 and 7 you can also use the provided [Makefile](Makefile) and run `make start-everything`.

## Detection Node

Download weights for yolov4 from: https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights and move the weights into `detect/yolo_node/weights`.

Dependencies:
* tensorflow
* pandas
* opencv-python

## Lessons Learned

* The default user `ubuntu` on the Turtlebot image does not have the proper `tty` permissions. The problem could be solved by adding `ubuntu` to `root` user group, by executing: `sudo usermod -aG root ubuntu`, as the normal group used for that called `dialout` was not set for `tty`.
* ROS machines must have a resolved DNS name as they communicate with each other, see: http://wiki.ros.org/ROS/NetworkSetup.
* Router should not be connected to the internet in order to not disturb the connection
* Running the detection on the Turtlebot causes extrem delays:

```bash
1/1 [==============================] - 6s 6s/step
x1                    250
y1                    256
x2                    354
y2                    360
class_name    sports ball
score            0.693495
w                     104
h                     104
Name: 0, dtype: object
1/1 [==============================] - 6s 6s/step
x1                    250
y1                    255
x2                    354
y2                    360
class_name    sports ball
score            0.756736
w                     104
h                     105
Name: 0, dtype: object
```

## Raspi cam

- ui: `rqt`
- list all packages: `rospack list-names`
- build packages inside `~/catkin_ws`: catkin_make
- start master: `roscore`
