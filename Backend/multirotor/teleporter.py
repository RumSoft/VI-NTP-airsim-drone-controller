import setup_path
import airsim
import time
import cv2
import msvcrt

client = airsim.MultirotorClient()
client.confirmConnection()

change = 1

while True:
    key = msvcrt.getche().decode("utf-8")
    pose = client.simGetVehiclePose()

    if(key == 'w'):
        pose.position.x_val += change
        client.simSetVehiclePose(pose, True, "")

    if(key == 's'):
        pose.position.x_val -= change
        client.simSetVehiclePose(pose, True, "")

    if(key == 'a'):
        pose.position.y_val -= change
        client.simSetVehiclePose(pose, True, "")

    if(key == 'd'):
        pose.position.y_val += change
        client.simSetVehiclePose(pose, True, "")

    if(key == 'p'):
        xd = client.getGpsData().gnss.geo_point
        print(xd.latitude, xd.longitude)

    if (key == 27 or key == 'q' or key == 'x'):
        break
