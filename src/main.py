from menu import Menu, map_selctor
from parse import ParseFile, Map
from graph import Graph
from visuals import Visualizer
from drone import Create_drones
from simulation import Simulation


def main():
    menu = Menu()
    lines = []
    drone_map = Map()
    parser = ParseFile()
    bfs = ["1", "2", "3", "4"]
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
    path_bfs = graph.find_path_bfs(result.start.name, result.end.name)
    # path_dij = graph.find_path_dijkstra(result.start.name, result.end.name)
    if path_bfs is False:
        print("No Path found")
    # if map in bfs:
    drones = Create_drones(nb_drones, path_bfs).init_drones()
    Simulation(drones, result, path_bfs).start()
    moves = Simulation(drones, result, path_bfs).next_turn()
    # else:
        # drones = Create_drones(nb_drones, path_dij).init_drones()
        # Simulation(drones, result, path_dij).start()
        # moves = Simulation(drones, result, path_dij).next_turn()
    # visuals = Visualizer(Moves)
    # visuals.make_window()


if __name__ == "__main__":
    main()
