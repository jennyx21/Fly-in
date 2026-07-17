from menu import Menu, map_selctor
from parse import ParseFile, Map
from graph import Graph
from visuals import Visualizer
from drone import Create_drones


def main():
    menu = Menu()
    lines = []
    drone_map = Map()
    parser = ParseFile()
    map, filename = map_selctor(menu)
    state, lines = parser.read_file(filename)
    if state != "succsess":
        print(lines)
        return
    state, drone_map = parser.take_values(lines)
    if state != "succsess":
        print(drone_map)
        return
    state, result = parser.validate_deeper(drone_map)
    if state != "succsess":
        print(result)
        return
    nb_drones = result.nb_drones
    graph = Graph(result)
    path = graph.find_path(result.start.name, result.end.name)
    if path is False:
        print("No Path found")
    else:
        for hub in path:
            print(hub.name)
    drones = Create_drones(nb_drones, path).init_drones()
    visuals = Visualizer(result, drones)
    visuals.make_window()


if __name__ == "__main__":
    main()
