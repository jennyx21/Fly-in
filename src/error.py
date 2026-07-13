class NumberError(Exception):
    pass

    def main_selector(self, nb: int):
        if nb > 5 or nb < 0:
            raise NumberError("Number needs to be in range of 0-5")

    def map_selector(self, nb: int):
        if nb > 4 or nb < 0:
            raise NumberError("Number needs to be in range of 0-4")

    def challenger_selector(self, nb: int):
        if nb > 2 or nb < 0:
            raise NumberError("Number needs to be in range of 0-2")
