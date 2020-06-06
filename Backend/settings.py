TARGET_BUFFER: float = 3.0  # m
GROUNDSPEED: float = 4.0  # m/s
COLLISION_SPEED: float = 2.0
VELOCITY_BUFFER = 0.08  # m/s
SET_YAW_TIMEOUT = 3  # s
COLLISION_BUFFER = 30  # m


class State:
    IDLE = 'idle'
    FLYING = 'flying'
    COLLISION = 'colission'


route = {
    "route":
    [
        [47.64222341272163, -122.14042018217175, 30],
        [47.64219728499648, -122.14211353552626, 30],
        [47.642584844914175, -122.14204890371899, 30]
    ]
}
