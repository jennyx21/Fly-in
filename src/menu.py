from error import NumberError
from typing import Any
import time


class Menu:

    def show(self) -> None:
        print("========================")
        print("Fly-In - Drone simulator")
        print("========================")
        print()
        print("Decide Map difficulty:")
        print("(1) Easy")
        print("(2) Medium")
        print("(3) Hard")
        print("(4) Challenger")
        print("(0) Exit")
        print()
        print("Select a Number:")

    def easy_map(self) -> None:
        print("========================")
        print("Fly-In - Drone simulator")
        print("========================")
        print()
        print("Map selctor - Easy:")
        print("(1) Linear Path")
        print("(2) Simple Fork")
        print("(3) Basic Capacity")
        print("(4) Go back")
        print("(0) Exit")
        print()
        print("Select a Number:")

    def medium_map(self) -> None:
        print("========================")
        print("Fly-In - Drone simulator")
        print("========================")
        print()
        print("Map selctor - Medium:")
        print("(1) Dead End Trap")
        print("(2) Circular loop")
        print("(3) Priority Puzzle")
        print("(4) Go back")
        print("(0) Exit")
        print()
        print("Select a Number:")

    def hard_map(self) -> None:
        print("========================")
        print("Fly-In - Drone simulator")
        print("========================")
        print()
        print("Map selctor - Hard:")
        print("(1) Maze Nightmare")
        print("(2) Capacity Hell")
        print("(3) Ultimate Challange")
        print("(4) Go back")
        print("(0) Exit")
        print()
        print("Select a Number:")

    def challenger_map(self) -> None:
        print("========================")
        print("Fly-In - Drone simulator")
        print("========================")
        print()
        print("Map selctor - Easy:")
        print("(1) The Impossible Dream")
        print("(2) Go back")
        print("(0) Exit")
        print()
        print("Select a Number:")


def map_selctor(menu: Menu) -> Any | tuple[str, str]:
    """ creates a map selector for better user experience"""
    menu.show()
    validator = NumberError()
    try:
        user_input = int(input("> "))
    except ValueError as e:
        print(f"{e}")
        time.sleep(1)
        return map_selctor(menu)

    try:
        validator.main_selector(user_input)
    except NumberError as e:
        print(f"{e}")
        time.sleep(1)
        return map_selctor(menu)

    if user_input == 1:
        menu.easy_map()
        try:
            second_input = int(input("> "))
        except ValueError as e:
            print(f"{e}")
            time.sleep(1)
            return map_selctor(menu)

        try:
            validator.map_selector(second_input)
        except NumberError as e:
            print(f"{e}")
            time.sleep(1)
            return map_selctor(menu)
        if second_input == 1:
            return "1", "src/maps/easy/01_linear_path.txt"
        elif second_input == 2:
            return "2", "src/maps/easy/02_simple_fork.txt"
        elif second_input == 3:
            return "3", "src/maps/easy/03_basic_capacity.txt"
        elif second_input == 4:
            return map_selctor(menu)
        elif second_input == 0:
            return "0", "good bye :)"

    elif user_input == 2:
        menu.medium_map()
        try:
            second_input = int(input("> "))
        except ValueError as e:
            print(f"{e}")
            time.sleep(1)
            return map_selctor(menu)

        try:
            validator.map_selector(second_input)
        except NumberError as e:
            print(f"{e}")
            time.sleep(1)
            return map_selctor(menu)
        if second_input == 1:
            return "4", "src/maps/medium/01_dead_end_trap.txt"
        elif second_input == 2:
            return "5", "src/maps/medium/02_circular_loop.txt"
        elif second_input == 3:
            return "6", "src/maps/medium/03_priority_puzzle.txt"
        elif second_input == 4:
            return map_selctor(menu)
        elif second_input == 0:
            return "0", "good bye :)"
    elif user_input == 3:
        menu.hard_map()
        try:
            second_input = int(input("> "))
        except ValueError as e:
            print(f"{e}")
            time.sleep(1)
            return map_selctor(menu)

        try:
            validator.map_selector(second_input)
        except NumberError as e:
            print(f"{e}")
            time.sleep(1)
            return map_selctor(menu)
        if second_input == 1:
            return "7", "src/maps/hard/01_maze_nightmare.txt"
        elif second_input == 2:
            return "8", "src/maps/hard/02_capacity_hell.txt"
        elif second_input == 3:
            return "9", "src/maps/hard/03_ultimate_challenge.txt"
        elif second_input == 4:
            return map_selctor(menu)
        elif second_input == 0:
            return "0", "good bye :)"
    elif user_input == 4:
        menu.challenger_map()
        try:
            second_input = int(input("> "))
        except ValueError as e:
            print(f"{e}")
            time.sleep(1)
            return map_selctor(menu)

        try:
            validator.challenger_selector(second_input)
        except NumberError as e:
            print(f"{e}")
            time.sleep(1)
            return map_selctor(menu)
        if second_input == 1:
            return "10", "src/maps/challenger/01_the_impossible_dream.txt"
        elif second_input == 2:
            return map_selctor(menu)
        elif second_input == 0:
            return "0", "good bye :)"

    elif user_input == 0:
        return "0", "good bye :)"
    return "invalid"
