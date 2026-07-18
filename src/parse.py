from dataclasses import dataclass, field

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
    name: str = None
    x: int = None
    y: int = None
    color: str = "white"
    zone: str = "normal"
    cost: int = 1
    blocked: bool = False
    max_drones: int = 1


@dataclass
class Connection:
    start_name: str = None
    end_name: str = None
    start: Hub = None
    end: Hub = None
    max_link: int = 1


@dataclass
class Map:
    nb_drones: int = None
    start: Hub = None
    end: Hub = None
    hubs: list[Hub] = field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)


class ParseFile:

    def read_file(self, filename):
        lines = []
        try:
            with open(filename) as f:
                lines = f.readlines()
        except FileNotFoundError as e:
            return "Fail", f"No file found: {e}"

        for line in lines:
            line.strip()

            if not line:
                continue
        return "succsess", lines

    def take_values(self, lines: list[str]):
        drone_map = Map()
        for line in lines:
            conection = Connection()
            hub = Hub()

            if line.startswith("nb_drones"):
                try:
                    drone_map.nb_drones = int(line.split(":")[1].strip())
                except ValueError as e:
                    return "Fail", f"nb_drones schould be an int: {e}"
                if drone_map.nb_drones <= 0:
                    return "Fail", "number of drones should be > 0"

            elif line.startswith("start_hub"):
                infos: str = line.split(":")[1]
                part, _, options = infos.partition("[")
                options = options.replace("]", "").strip()
                parts = part.split()
                if len(parts) > 3 or len(parts) < 3:
                    return "Fail", "Invalid hub/coordinate format"
                hub.name = parts[0]
                if "-" in hub.name:
                    return "Fail", (f"hub names schould not contain '-':"
                                    f" {hub.name}")
                try:
                    hub.x = int(parts[1])
                    hub.y = int(parts[2])
                except ValueError as e:
                    return "Fail", f"Invalid coordinates: {e}"
                settings = {}
                for option in options.split():
                    if "=" not in option:
                        return "Fail", f"{option} wrong structured"
                    key, value = option.split("=")
                    settings[key] = value
                hub.color = settings.get("color", "white")
                try:
                    hub.max_drones = int(settings.get("max_drones", 1))
                except ValueError as e:
                    return "Fail", f"{hub.name} invalid max drones value: {e}"
                if hub.max_drones <= 0:
                    return "fail", (f"number of max drones in {hub.name} "
                                    "should be > 0")
                if drone_map.start is not None:
                    return "Fail", f"Error: multiple {hub.name} found"
                hub.cost = 0
                drone_map.start = hub

            elif line.startswith("end_hub"):
                infos: str = line.split(":")[1]
                part, _, options = infos.partition("[")
                options = options.replace("]", "").strip()
                parts = part.split()
                if len(parts) > 3 or len(parts) < 3:
                    return "Fail", "Invalid hub/coordinate format"
                hub.name = parts[0]
                if "-" in hub.name:
                    return "Fail", (f"hub names schould not contain '-':"
                                    f" {hub.name}")
                try:
                    hub.x = int(parts[1])
                    hub.y = int(parts[2])
                except ValueError as e:
                    return "Fail", f"Invalid coordinates: {e}"
                settings = {}
                for option in options.split():
                    if "=" not in option:
                        return "Fail", f"{option} wrong structured"
                    key, value = option.split("=")
                    settings[key] = value
                hub.color = settings.get("color", "white")
                try:
                    hub.max_drones = int(settings.get("max_drones", 1))
                except ValueError as e:
                    return "Fail", f"{hub.name} invalid max drones value: {e}"
                if hub.max_drones <= 0:
                    return "fail", (f"number of max drones in {hub.name} "
                                    "should be > 0")
                if drone_map.end is not None:
                    return "Fail", f"Error: multiple {hub.name} found"
                hub.cost = 0
                drone_map.end = hub

            elif line.startswith("hub"):
                infos: str = line.split(":")[1]
                part, _, options = infos.partition("[")
                options = options.replace("]", "").strip()
                parts = part.split()
                if len(parts) > 3 or len(parts) < 3:
                    return "Fail", "Invalid hub/coordinate format"
                hub.name = parts[0]
                if "-" in hub.name:
                    return "Fail", (f"hub names schould not contain '-':"
                                    f" {hub.name}")
                try:
                    hub.x = int(parts[1])
                    hub.y = int(parts[2])
                except ValueError as e:
                    return "Fail", f"Invalid coordinates: {e}"
                settings = {}
                for option in options.split():
                    if "=" not in option:
                        return "Fail", f"{option} wrong structured"
                    key, value = option.split("=")
                    settings[key] = value
                # self.set_colors(settings.get("color", "white"), hub)
                hub.color = settings.get("color", "white")
                try:
                    hub.max_drones = int(settings.get("max_drones", 1))
                except ValueError as e:
                    return "Fail", f"{hub.name} invalid max drones value: {e}"
                if hub.max_drones <= 0:
                    return "fail", (f"number of max drones in {hub.name} "
                                    "should be > 0")
                hub.zone = settings.get("zone", "normal")
                if hub.zone not in ZONES:
                    return "Fail", f"{hub.zone} is an invalid ZoneType"
                if hub.zone == "blocked":
                    hub.cost = float("inf")
                elif hub.zone == "restricted":
                    hub.cost = 2
                if drone_map.hubs is not None:
                    for h in drone_map.hubs:
                        if h.name == hub.name:
                            return "Fail", f"Error: multiple {hub.name} found"
                drone_map.hubs.append(hub)

            elif line.startswith("connection"):
                li = line.split(":")[1].strip()
                part, _, options = li.partition("[")
                options = options.replace("]", "").strip()
                if "-" not in part:
                    return "Fail", ("the connections need to be"
                                    " seperated by '-'")
                parts = part.split("-")
                if len(parts) != 2:
                    return "Fail", (f"{line}this connection"
                                    " is missing one argument")
                conection.start_name = parts[0].strip()
                conection.end_name = parts[1].strip()
                if options != "":
                    if "=" not in option:
                        return "Fail", f"{options} wrong structured"
                    try:
                        conection.max_link = int(options.split("=")[1])
                    except ValueError as e:
                        return "Fail", f"invalid max_link_capacity {e}"
                if conection.max_link <= 0:
                    return "fail", "number of max link capacity should be > 0"
                drone_map.connections.append(conection)
            elif line.strip() == "" or line.startswith("#"):
                continue
            else:
                return "Faile", f"Unknowen line {line}"
        return "succsess", drone_map

    def validate_deeper(self, map: Map):
        connections = map.connections
        start_hub = map.start
        end_hub = map.end
        hubs = map.hubs
        for hub in hubs:
            if hub.name == start_hub.name:
                return "Fail", f"Multiple {start_hub.name}"
            if hub.name == end_hub.name:
                return "Fail", f"Multiple {end_hub.name}"

        valid: int = 1
        for connec in connections:
            if connec.start_name is None:
                return "Fail", "in one connection a start point is missing"
            if connec.end_name is None:
                return "Fail", "in one connection a end point is missing"
            if connec.start_name != start_hub.name:
                valid = 0
                for hub in hubs:
                    if connec.start_name == hub.name:
                        valid = 1
            if valid != 1:
                return "Fail", f"{connec} start_name hub is incorrect"

            if connec.end_name != end_hub.name:
                valid = 0
                for hub in hubs:
                    if connec.end_name == hub.name:
                        valid = 1
            if valid != 1:
                return "Fail", f"{connec} end_name hub is incorrect"

            if connec.start_name == connec.end_name:
                return "Fail", (f"path {connec.start_name} - {connec.end_name}"
                                "invalid path can't connect to itself")
            for h_conec in map.connections:
                if (connec.start_name + connec.end_name ==
                   h_conec.end_name + h_conec.start_name):
                    return "Fail", "a connection A-B == B-A is found"

            for con in connections:
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
        return "succsess", map

    # def set_colors(self, name: str, hub: Hub):
    #     colors = COLORS
    #     hub.color[name] = colors[name]

