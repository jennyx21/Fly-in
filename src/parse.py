from dataclasses import dataclass, field
from typing import Optional
from error import ParserErorr


ZONES = ["priority", "restricted", "blocked", "normal"]

COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),

    "purple": (128, 0, 128),
    "brown": (139, 69, 19),
    "orange": (255, 165, 0),
    "maroon": (128, 0, 0),
    "gold": (255, 215, 0),
    "darkred": (139, 0, 0),
    "violet": (238, 130, 238),
    "crimson": (220, 20, 60),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "lime": (0, 255, 0),
    "magenta": (255, 0, 255),
    "rainbow": (123, 213, 231)
    }


@dataclass
class Hub:
    name: str | None = None
    x: int | None = None
    y: int | None = None
    color: str = "white"
    zone: str = "normal"
    cost: int = 1
    blocked: bool = False
    max_drones: int = 1


@dataclass
class Connection:
    start_name: str | None = None
    end_name: str | None = None
    start: Optional[Hub] = None
    end: Optional[Hub] = None
    max_link: int = 1


@dataclass
class Map:
    nb_drones: int | None = None
    start: Optional[Hub] = None
    end: Optional[Hub] = None
    hubs: list[Hub] = field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)


class ParseFile:
    """Parses map configuration files and validates map data."""
    
    def read_file(self, filename: str) -> list[str]:
        """
        Read lines from a map configuration file.
        """
        lines = []
        try:
            with open(filename) as f:
                lines = f.readlines()
        except FileNotFoundError as e:
            raise ParserErorr(f"No file found: {e}")

        for line in lines:
            line.strip()

            if not line:
                continue
        return lines

    def take_values(self, lines: list[str]) -> Map:
        drone_map = Map()
        for line in lines:
            conection = Connection()
            hub = Hub()

            if line.startswith("nb_drones"):
                try:
                    drone_map.nb_drones = int(line.split(":")[1].strip())
                except ValueError as e:
                    raise ParserErorr(f"nb_drones schould be an int: {e}")
                if drone_map.nb_drones <= 0:
                    raise ParserErorr("number of drones should be > 0")

            elif line.startswith("start_hub"):
                infos_start: str = line.split(":")[1]
                part, _, options = infos_start.partition("[")
                options = options.replace("]", "").strip()
                parts = part.split()
                if len(parts) > 3 or len(parts) < 3:
                    raise ParserErorr("Invalid hub/coordinate format")
                hub.name = parts[0]
                if "-" in hub.name:
                    raise ParserErorr(f"hub names schould not contain '-':"
                                      f" {hub.name}")
                try:
                    hub.x = int(parts[1])
                    hub.y = int(parts[2])
                except ValueError as e:
                    raise ParserErorr(f"Invalid coordinates: {e}")
                settings = {}
                for option in options.split():
                    if "=" not in option:
                        raise ParserErorr(f"{option} wrong structured")
                    key, value = option.split("=")
                    settings[key] = value
                hub.color = settings.get("color", "white")
                try:
                    hub.max_drones = int(settings.get("max_drones", 1))
                except ValueError as e:
                    raise ParserErorr(f"{hub.name} invalid max "
                                      f"drones value: {e}")
                if hub.max_drones <= 0:
                    raise ParserErorr(f"number of max drones in {hub.name} "
                                      "should be > 0")
                if drone_map.start is not None:
                    raise ParserErorr(f"Error: multiple {hub.name} found")
                hub.cost = 0
                drone_map.start = hub

            elif line.startswith("end_hub"):
                infos_end: str = line.split(":")[1]
                part, _, options = infos_end.partition("[")
                options = options.replace("]", "").strip()
                parts = part.split()
                if len(parts) > 3 or len(parts) < 3:
                    raise ParserErorr("Invalid hub/coordinate format")
                hub.name = parts[0]
                if "-" in hub.name:
                    raise ParserErorr(f"hub names schould not contain '-':"
                                      f" {hub.name}")
                try:
                    hub.x = int(parts[1])
                    hub.y = int(parts[2])
                except ValueError as e:
                    raise ParserErorr(f"Invalid coordinates: {e}")
                settings = {}
                for option in options.split():
                    if "=" not in option:
                        raise ParserErorr(f"{option} wrong structured")
                    key, value = option.split("=")
                    settings[key] = value
                hub.color = settings.get("color", "white")
                try:
                    hub.max_drones = int(settings.get("max_drones", 1))
                except ValueError as e:
                    raise ParserErorr(f"{hub.name} invalid max"
                                      f" drones value: {e}")
                if hub.max_drones <= 0:
                    raise ParserErorr(f"number of max drones in {hub.name} "
                                      "should be > 0")
                if drone_map.end is not None:
                    raise ParserErorr(f"Error: multiple {hub.name} found")
                hub.cost = 0
                drone_map.end = hub

            elif line.startswith("hub"):
                infos: str = line.split(":")[1]
                part, _, options = infos.partition("[")
                options = options.replace("]", "").strip()
                parts = part.split()
                if len(parts) > 3 or len(parts) < 3:
                    raise ParserErorr("Invalid hub/coordinate format")
                hub.name = parts[0]
                if "-" in hub.name:
                    raise ParserErorr(f"hub names schould not contain '-':"
                                      f" {hub.name}")
                try:
                    hub.x = int(parts[1])
                    hub.y = int(parts[2])
                except ValueError as e:
                    raise ParserErorr(f"Invalid coordinates: {e}")
                settings = {}
                for option in options.split():
                    if "=" not in option:
                        raise ParserErorr(f"{option} wrong structured")
                    key, value = option.split("=")
                    settings[key] = value
                hub.color = settings.get("color", "white")
                try:
                    hub.max_drones = int(settings.get("max_drones", 1))
                except ValueError as e:
                    raise ParserErorr(f"{hub.name} invalid max drones"
                                      f" value: {e}")
                if hub.max_drones <= 0:
                    raise ParserErorr(f"number of max drones in {hub.name} "
                                      "should be > 0")
                hub.zone = settings.get("zone", "normal")
                if hub.zone not in ZONES:
                    raise ParserErorr(f"{hub.zone} is an invalid ZoneType")
                if hub.zone == "blocked":
                    hub.cost = 1000
                elif hub.zone == "restricted":
                    hub.cost = 2
                if drone_map.hubs is not None:
                    for h in drone_map.hubs:
                        if h.name == hub.name:
                            raise ParserErorr(f"Error: multiple"
                                              f"{hub.name} found")
                drone_map.hubs.append(hub)

            elif line.startswith("connection"):
                li = line.split(":")[1].strip()
                part, _, options = li.partition("[")
                options = options.replace("]", "").strip()
                if "-" not in part:
                    raise ParserErorr("the connections need to be"
                                      " seperated by '-'")
                parts = part.split("-")
                if len(parts) != 2:
                    raise ParserErorr(f"{line}this connection"
                                      " is missing one argument")
                conection.start_name = parts[0].strip()
                conection.end_name = parts[1].strip()
                if options != "":
                    if "=" not in option:
                        raise ParserErorr(f"{options} wrong structured")
                    try:
                        conection.max_link = int(options.split("=")[1])
                    except ValueError as e:
                        raise ParserErorr(f"invalid max_link_capacity {e}")
                if conection.max_link <= 0:
                    raise ParserErorr("number of max link capacity"
                                      " should be > 0")
                drone_map.connections.append(conection)
            elif line.strip() == "" or line.startswith("#"):
                continue
            else:
                raise ParserErorr(f"Unknowen line {line}")
        return drone_map

    def validate_deeper(self, map: Map) -> Map:
        connections = map.connections
        start_hub = map.start
        end_hub = map.end
        hubs = map.hubs
        for hub in hubs:
            if start_hub is not None and hub.name == start_hub.name:
                raise ParserErorr(f"Multiple {start_hub.name}")
            if end_hub is not None and hub.name == end_hub.name:
                raise ParserErorr(f"Multiple {end_hub.name}")

        valid: int = 1
        for connec in connections:
            if start_hub is None:
                raise ParserErorr("Missing start_hub")
            if end_hub is None:
                raise ParserErorr("Missing end_hub")
            if connec.start_name is None:
                raise ParserErorr("in one connection a start point is missing")
            if connec.end_name is None:
                raise ParserErorr("in one connection a end point is missing")
            if connec.start_name != start_hub.name:
                valid = 0
                for hub in hubs:
                    if connec.start_name == hub.name:
                        valid = 1
            if valid != 1:
                raise ParserErorr(f"{connec} start_name hub is incorrect")

            if connec.end_name != end_hub.name:
                valid = 0
                for hub in hubs:
                    if connec.end_name == hub.name:
                        valid = 1
            if valid != 1:
                raise ParserErorr(f"{connec} end_name hub is incorrect")

            if connec.start_name == connec.end_name:
                raise ParserErorr(f"path {connec.start_name} - "
                                  f"{connec.end_name} invalid path"
                                  " can't connect to itself")
            for h_conec in map.connections:
                if h_conec.end_name is None or h_conec.start_name is None:
                    raise ParserErorr("Connection has missing hub")
                if (connec.start_name + connec.end_name ==
                   h_conec.end_name + h_conec.start_name):
                    raise ParserErorr("a connection A-B == B-A is found")

            for con in connections:
                if start_hub is None:
                    raise ParserErorr("Missing start_hub")
                if end_hub is None:
                    raise ParserErorr("Missing end_hub")
                if con.start_name == start_hub.name:
                    con.start = start_hub
                else:
                    for hub in hubs:
                        if con.start_name == hub.name:
                            con.start = hub
                if con.end_name == end_hub.name:
                    con.end = end_hub
                else:
                    for hub in hubs:
                        if con.end_name == hub.name:
                            con.end = hub
        map.connections = connections
        return map
