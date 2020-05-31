TARGET_BUFFER: float = 3.0  # m
GROUNDSPEED: float = 5.0  # m/s
VELOCITY_BUFFER = 0.08  # m/s
SET_YAW_TIMEOUT = 1.2  # s


class State:
    IDLE = 'idle'
    FLYING = 'flying'
    COLLISION = 'colission'


route = {
    "route":
    [
        [-122.14042018217175, 47.64222341272163, 30],
        [-122.14211353552626, 47.64219728499648, 30],
        [-122.14204890371899, 47.642584844914175, 30]
    ]
}
