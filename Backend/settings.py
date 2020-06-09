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
