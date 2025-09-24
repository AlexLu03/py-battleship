from typing import List, Tuple, Optional


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def fire(self) -> None:
        self.is_alive = False

    def __repr__(self) -> str:
        return "□" if self.is_alive else "x"


class Ship:
    def __init__(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        is_drowned: bool = False,
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = self.create_decks(start, end)

    @staticmethod
    def create_decks(start: Tuple[int, int],
                     end: Tuple[int, int]) -> List[Deck]:
        decks: List[Deck] = []
        if start[0] == end[0]:  # горизонтальный
            for col in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], col))
        elif start[1] == end[1]:  # вертикальный
            for row in range(start[0], end[0] + 1):
                decks.append(Deck(row, start[1]))
        return decks

    def fire(self, row: int, column: int) -> Optional[str]:
        for deck in self.decks:
            if deck.row == row and deck.column == column and deck.is_alive:
                deck.fire()
                if all(not d.is_alive for d in self.decks):
                    self.is_drowned = True
                    return "Sunk!"
                return "Hit!"
        return None


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
                 ) -> None:
        self.ships: List[Ship] = []
        for start, end in ships:
            self.ships.append(Ship(start, end))

    def fire(self, location: Tuple[int, int]) -> str:
        row, col = location
        for ship in self.ships:
            result = ship.fire(row, col)
            if result:
                return result
        return "Miss!"

    def print_field(self) -> None:
        field = [["~"] * 10 for _ in range(10)]
        for ship in self.ships:
            for deck in ship.decks:
                if deck.is_alive:
                    field[deck.row][deck.column] = "□"
                else:
                    field[deck.row][deck.column] = (
                        "x" if ship.is_drowned else "*"
                    )
        for row in field:
            print(" ".join(row))
