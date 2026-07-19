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
    def __init__(self, nb_drones: int, path: list[Hub], path2: list[Hub], map: Map):
        self.nb = nb_drones
        self.path = path
        self.path2 = path2
        self.map = map

    def init_drones(self, n: int):
        drones = []
        i = 1
        if n == 1:
            while i <= self.nb:
                drone = Drone(
                    id=i,
                    position=self.map.start,
                    color=DRONE_COLOR,
                    path=self.path.copy()
                            )
                drones.append(drone)
                i += 1
        else:
            while i <= self.nb:
                if i % 2 == 0:
                    drone = Drone(
                        id=i,
                        position=self.map.start,
                        color=DRONE_COLOR,
                        path=self.path.copy()
                                )
                    drones.append(drone)
                else:
                    drone = Drone(
                        id=i,
                        position=self.map.start,
                        color=DRONE_COLOR,
                        path=self.path2.copy()
                                )
                    drones.append(drone)
                i += 1

        if len(drones) < 1:
            return "Fail", "No drones"
        return "succsess", drones
