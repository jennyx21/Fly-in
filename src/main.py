from menu import Menu, map_selctor
from parse import ParseFile, Map


def main():
    menu = Menu()
    lines = []
    drone_map = Map()
    parser = ParseFile()
    filename = map_selctor(menu)
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


if __name__ == "__main__":
    main()
