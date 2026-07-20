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
    def __init__(self, drones: list[Drone], map: Map, path: list[Hub]) -> None:
        self.drones = drones
        self.map = map
        self.turn = 1
        self.counter = 1
        self.start()

    def start(self) -> None:
        for d in self.drones:
            d.position = self.map.start

    def next_turn(self) -> list[list[Move]] | str:
        nb_schedule = 0
        i = 0
        turn: list[str] = []
        moves: list[list[Move]] = []
        turns: list[Move] = []
        while self.check_drones() > 0:
            self.update_map()
            for d in self.drones:
                if d.finished is False:
                    start_pos = d.position
                    if start_pos is None:
                        continue
                    nb_schedule = self.schedule(d)
                    if nb_schedule == 1:
                        current_position = d.position
                        if current_position is None:
                            continue
                        po_index = d.path.index(current_position)
                        next_hub = d.path[po_index + 1]
                        if self.check_next_hub(next_hub):
                            d.position = next_hub
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
                        else:
                            turn.append(f"D{d.id} {TC[start_pos.color]}"
                                        f"{start_pos.name}{TC['reset']}"
                                        "[waiting]")
                            move = Move(
                                turn=self.turn,
                                drone=d,
                                start=start_pos,
                                end=start_pos
                            )
                            turns.append(move)
                    elif nb_schedule == 2:
                        turn.append(f"D{d.id} {TC[start_pos.color]}"
                                    f"{start_pos.name}{TC['reset']}"
                                    " [restricted] ")
                        end_pos = d.position
                        if end_pos is None:
                            end_pos = start_pos
                        move = Move(
                            turn=self.turn,
                            drone=d,
                            start=start_pos,
                            end=end_pos
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
        return "simulation couldn n't be created"

    def check_drones(self) -> int:
        active = 0
        for d in self.drones:
            if d.finished is False:
                active += 1
        return active

    def update_map(self) -> None:
        for hub in self.map.hubs:
            count = 0
            for d in self.drones:
                if d.position == hub:
                    count += 1
            if count >= hub.max_drones:
                hub.blocked = True
            elif count < hub.max_drones:
                hub.blocked = False

    def schedule(self, drone: Drone) -> int:
        if drone.finished:
            return 0

        current_position = drone.position
        if current_position is None:
            return 0

        current_index = drone.path.index(current_position)

        if current_index == len(drone.path) - 1:
            drone.finished = True
            return 0
        elif current_position.zone == "restricted" and drone.waited is False:
            drone.waited = True
            return 2
        elif current_position.zone == "restricted" and drone.waited is True:
            drone.waited = False

        return 1

    def check_next_hub(self, pos_next: Hub) -> bool:
        if pos_next.blocked:
            return False
        return True
