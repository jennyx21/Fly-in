from dataclasses import dataclass, field
from parse import Hub, Map
import random as r

DRONE_COLOR = (r.randint(10, 255), r.randint(10, 255), r.randint(10, 255),)


@dataclass
class Drone:
    id: int
    position: Hub
    color: str = "white"
    finished: bool = False
    waited: bool = False
    path: list[Hub] = field(default_factory=list)


class Create_drones:
    def __init__(self, nb_drones: int, path: list[Hub], map: Map):
        self.nb = nb_drones
        self.path = path
        self.map = map

    def init_drones(self):
        drones = []
        i = 1
        wait = 0
        while i <= self.nb:
            if i > 0:
                for hub in self.path:
                    if hub.zone == "restricted":
                        wait += 1
            drone = Drone(
                id=i,
                position=self.map.start,
                color=DRONE_COLOR,
                path=self.path.copy()
                        )
            drones.append(drone)
            i += 1
            wait += 1

        if len(drones) < 1:
            return "Fail", "No drones"
        return"succsess", drones
