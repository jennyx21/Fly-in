from dataclasses import dataclass, field
from parse import Hub
import random as r

DRONE_COLOR = (r.randint(10, 255), r.randint(10, 255), r.randint(10, 255),)


@dataclass
class Drone:
    id: int
    y: float
    x: float
    color: str = "white"
    current: int = 1
    waiting: int = 0
    finished: bool = False
    moving: bool = False
    path: list[Hub] = field(default_factory=list)


class Create_drones:
    def __init__(self, nb_drones: int, path: list[Hub]):
        self.nb = nb_drones
        self.path = path

    def init_drones(self):
        drones = []
        i = 1
        wait = 0
        while i <= self.nb:
            if i > 0:
                for hub in self.path:
                    if hub.zone == "resticted":
                        wait += 1
            drone = Drone(
                id=i,
                x=self.path[0].x,
                y=self.path[0].y,
                color=DRONE_COLOR,
                waiting=wait,
                path=self.path.copy()
                        )
            drones.append(drone)
            i += 1
            wait += 1

        if len(drones) < 1:
            return "Fail", "No drones"
        return drones
