from enum import Enum


class States(Enum):
    BUSY = "busy"
    ONLINE = "online"
    OFFLINE = "offline"
    ROAMING = "roaming"