import setup_path
import airsim
import pprint
pp = pprint.PrettyPrinter(indent=4)

client = airsim.MultirotorClient()
client.confirmConnection()
#client.enableApiControl(false)

xd = client.getGpsData()
pp.pprint(xd)
