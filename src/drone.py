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
    path: list[Hub] = field(default_factory=list)


class Create_drones:
    def __init__(self, nb_drones: int, path: list[Hub]):
        self.nb = nb_drones
        self.path = path

    def init_drones(self):
        drones = []
        i = 1
        while i <= self.nb:
            drone = Drone(
                id=i,
                x=self.path[0].x,
                y=self.path[0].y,
                color=DRONE_COLOR,
                path=self.path.copy()
                        )
            drones.append(drone)
            i += 1

        if len(drones) < 1:
            return "Fail", "No drones"
        return drones
