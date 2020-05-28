import setup_path
import airsim
import pprint
import cv2

pp = pprint.PrettyPrinter(indent=4)

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)


cameraType = "depth"

cameraTypeMap = {
    "depth": airsim.ImageType.DepthVis,
    "segmentation": airsim.ImageType.Segmentation,
    "seg": airsim.ImageType.Segmentation,
    "scene": airsim.ImageType.Scene,
    "disparity": airsim.ImageType.DisparityNormalized,
    "normals": airsim.ImageType.SurfaceNormals
}
