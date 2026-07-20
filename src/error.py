class ParserErorr(Exception):
    pass


class SimulationError(Exception):
    pass


class MapError(Exception):
    pass


class NumberError(Exception):
    pass

    def main_selector(self, nb: int) -> None:
        if nb > 4 or nb < 0:
            raise NumberError("Number needs to be in range of 0-4")

    def map_selector(self, nb: int) -> None:
        if nb > 4 or nb < 0:
            raise NumberError("Number needs to be in range of 0-4")

    def challenger_selector(self, nb: int) -> None:
        if nb > 2 or nb < 0:
            raise NumberError("Number needs to be in range of 0-2")
