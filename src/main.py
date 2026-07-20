from menu import Menu, map_selctor
from parse import ParseFile, Map
from graph import Graph
from visuals import Visualizer
from drone import Create_drones
from simulation import Simulation
from error import ParserErorr, MapError, SimulationError


def main() -> None:
    menu = Menu()
    drone_map = Map()

    parser = ParseFile()
    bfs = ["1", "2", "3", "4"]
    map, filename = map_selctor(menu)
    if map == "0":
        print(filename)
        return
    try:
        lines = parser.read_file(filename)
    except (ParserErorr) as e:
        print(e)
        return

    try:
        drone_map = parser.take_values(lines)
    except (ParserErorr) as e:
        print(e)

    try:
        map_result = parser.validate_deeper(drone_map)
    except (ParserErorr) as e:
        print(e)

    assert map_result.start is not None
    assert map_result.end is not None
    assert map_result.nb_drones is not None
    assert map_result.start.name is not None
    assert map_result.end.name is not None

    nb_drones = map_result.nb_drones
    graph = Graph(map_result)

    try:
        path_bfs = graph.find_path_bfs(map_result.start.name,
                                       map_result.end.name)
    except MapError as e:
        print(e)

    try:
        path_dij = graph.find_path_dijkstra(map_result.start.name,
                                            map_result.end.name)
    except MapError as e:
        print(e)

    if map in bfs:
        drones = Create_drones(nb_drones,
                               path_bfs, path_dij,
                               map_result).init_drones(1)
        try:
            Simulation(drones, map_result, path_bfs).start()
            moves = Simulation(drones, map_result, path_bfs).next_turn()
        except SimulationError as e:
            print(e)
    elif map == "10":
        drones = Create_drones(nb_drones,
                               path_bfs, path_dij,
                               map_result).init_drones(2)
        try:
            Simulation(drones, map_result, path_bfs).start()
            moves = Simulation(drones, map_result, path_bfs).next_turn()
        except SimulationError as e:
            print(e)
    else:
        drones = Create_drones(nb_drones, path_dij,
                               path_bfs, map_result).init_drones(1)
        try:
            Simulation(drones, map_result, path_dij).start()
            moves = Simulation(drones, map_result, path_dij).next_turn()
        except SimulationError as e:
            print(e)

    visuals = Visualizer(moves, map_result, drones)
    visuals.make_window()
    print("Good Bye:)")


if __name__ == "__main__":
    main()
