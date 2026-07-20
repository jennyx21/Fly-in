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
    if map == "0":
        print(filename)
        return
    state, lines = parser.read_file(filename)

    if state != "succsess":
        print(lines)
        return
    state, drone_map = parser.take_values(lines)

    if state != "succsess":
        print(drone_map)
        return
    state, map_result = parser.validate_deeper(drone_map)

    if state != "succsess":
        print(map_result)
        return
    nb_drones = map_result.nb_drones

    graph = Graph(map_result)
    path_bfs = graph.find_path_bfs(map_result.start.name, map_result.end.name)
    path_dij = graph.find_path_dijkstra(map_result.start.name,
                                        map_result.end.name)
    if map in bfs:
        drones = Create_drones(nb_drones,
                               path_bfs, path_dij,
                               map_result).init_drones(1)
        Simulation(drones, map_result, path_bfs).start()
        moves = Simulation(drones, map_result, path_bfs).next_turn()
    elif map == "10":
        drones = Create_drones(nb_drones,
                               path_bfs, path_dij,
                               map_result).init_drones(2)
        Simulation(drones, map_result, path_bfs).start()
        moves = Simulation(drones, map_result, path_bfs).next_turn()
    else:
        drones = Create_drones(nb_drones, path_dij,
                               path_bfs, map_result).init_drones(1)
        Simulation(drones, map_result, path_dij).start()
        moves = Simulation(drones, map_result, path_dij).next_turn()

    visuals = Visualizer(moves, map_result, drones)
    visuals.make_window()
    print("Good Bye:)")


if __name__ == "__main__":
    main()
