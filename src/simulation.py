from drone import Drone
from parse import Map, Hub
from dataclasses import dataclass

TC = {
    "white": "\033[97m",
    "black": "\033[30m",
    "red": "\033[91m",
    "green": "\033[92m",
    "blue": "\033[94m",

    "purple": "\033[95m",
    "brown": "\033[33m",
    "orange": "\033[38;5;208m",
    "maroon": "\033[38;5;88m",
    "gold": "\033[38;5;220m",
    "darkred": "\033[31m",
    "violet": "\033[38;5;177m",
    "crimson": "\033[38;5;161m",
    "yellow": "\033[93m",
    "cyan": "\033[96m",
    "lime": "\033[92m",
    "magenta": "\033[95m",

    "rainbow": "\033[38;5;213m",

    "reset": "\033[0m"
}


@dataclass
class Move:
    turn: int
    drone: Drone
    start: Hub
    end: Hub


class Simulation:
    def __init__(self, drones: list[Drone], map: Map, path: list[Hub]):
        self.drones = drones
        self.map = map
        self.path = path
        self.turn = 1
        self.counter = 1
        self.start()

    def start(self):
        for d in self.drones:
            d.position = self.map.start

    def next_turn(self):
        nb_schedule = 0
        i = 0
        turn = []
        moves = []
        turns = []
        while self.check_drones() > 0:
            self.update_map()
            for d in self.drones:
                if d.finished is False:
                    start_pos = d.position
                    nb_schedule = self.schedule(d)
                    if nb_schedule == 1:
                        po_index = self.path.index(d.position)
                        if self.check_next_hub(self.path[po_index + 1]):
                            d.position = self.path[po_index + 1]
                            turn.append(f"D{d.id} {TC[start_pos.color]}"
                                        f"{start_pos.name} {TC['reset']}-> "
                                        f"{TC[d.position.color]}"
                                        f"{d.position.name}"
                                        f"{TC['reset']} ")
                            move = Move(
                                turn=self.turn,
                                drone=d,
                                start=start_pos,
                                end=d.position
                            )
                            turns.append(move)
                        elif not self.check_next_hub(self.path[po_index + 1]):
                            turn.append(f"D{d.id} {TC[start_pos.color]}"
                                        f"{start_pos.name}{TC['reset']}"
                                        "[waiting]")
                            move = Move(
                                turn=self.turn,
                                drone=d,
                                start=start_pos,
                                end=d.position
                            )
                        turns.append(move)
                    elif nb_schedule == 2:
                        turn.append(f"D{d.id} {TC[start_pos.color]}"
                                    f"{start_pos.name}{TC['reset']}"
                                    " [restricted] ")
                        move = Move(
                            turn=self.turn,
                            drone=d,
                            start=start_pos,
                            end=d.position
                        )
                        turns.append(move)
                    self.update_map()
            if self.check_drones() == 0:
                for d in self.drones: 
                    d.position = self.map.start
                return moves
            print(f"Turn {self.turn}: ", end="")
            while i < len(turn):
                print(turn[i], end="")
                i += 1
            print()
            moves.append(turns.copy())
            turns.clear()
            self.turn += 1

    def check_drones(self):
        aktive = 0
        for d in self.drones:
            if d.finished is False:
                aktive += 1
        return aktive

    def update_map(self):
        for hub in self.map.hubs:
            count = 0
            for d in self.drones:
                if d.position == hub:
                    count += 1
            if count >= hub.max_drones:
                hub.blocked = True
            elif count < hub.max_drones:
                hub.blocked = False

    def schedule(self, drone: Drone):
        if drone.finished:
            return 0

        current_index = drone.path.index(drone.position)

        if current_index == len(drone.path) - 1:
            drone.finished = True
            return 0
        elif drone.position.zone == "restricted" and drone.waited is False:
            drone.waited = True
            return 2
        elif drone.position.zone == "restricted" and drone.waited is True:
            drone.waited = False
        else:
            next_hub = drone.path[current_index + 1]

            if next_hub.blocked:
                return 0

        return 1

    def check_next_hub(self, pos_next: Hub):
        if pos_next.blocked:
            return False
        return True
