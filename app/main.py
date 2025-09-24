from typing import List, Tuple, Optional, Dict


class Deck:
    def __init__(self, row_index: int, col_index: int, is_alive: bool = True) -> None:
        self.row_index = row_index
        self.col_index = col_index
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
    ) -> None:
        self.is_drowned: bool = False
        self.decks: List[Deck] = self.create_decks(start, end)

    @staticmethod
    def create_decks(start: Tuple[int, int], end: Tuple[int, int]) -> List[Deck]:
        decks: List[Deck] = []
        row_start, row_end = sorted([start[0], end[0]])
        col_start, col_end = sorted([start[1], end[1]])

        if row_start != row_end and col_start != col_end:
            # диагональный корабль запрещен
            return []

        for row_index in range(row_start, row_end + 1):
            for col_index in range(col_start, col_end + 1):
                decks.append(Deck(row_index, col_index))
        return decks

    def get_deck(self, row_index: int, col_index: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row_index == row_index and deck.col_index == col_index:
                return deck
        return None

    def fire(self, row_index: int, col_index: int) -> Optional[str]:
        deck = self.get_deck(row_index, col_index)
        if deck and deck.is_alive:
            deck.fire()
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return None


class Battleship:
    def __init__(
        self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    ) -> None:
        self.ships: List[Ship] = []
        self.field: Dict[Tuple[int, int], Deck] = {}

        for start, end in ships:
            ship = Ship(start, end)
            if not ship.decks:
                raise ValueError(
                    f"Invalid ship coordinates: {start}-{end}"
                )
            self.ships.append(ship)
            for deck in ship.decks:
                if (deck.row_index, deck.col_index) in self.field:
                    raise ValueError(
                        f"Overlapping ships at: {deck.row_index},{deck.col_index}"
                    )
                self.field[(deck.row_index, deck.col_index)] = deck

    def fire(self, location: Tuple[int, int]) -> str:
        row_index, col_index = location
        deck = self.field.get((row_index, col_index))
        if not deck or not deck.is_alive:
            return "Miss!"
        deck.fire()
        ship = next(s for s in self.ships if deck in s.decks)
        if all(not d.is_alive for d in ship.decks):
            ship.is_drowned = True
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        field_grid = [["~"] * 10 for _ in range(10)]
        for (row_index, col_index), deck in self.field.items():
            if deck.is_alive:
                field_grid[row_index][col_index] = "□"
            else:
                ship = next(s for s in self.ships if deck in s.decks)
                field_grid[row_index][col_index] = "x" if ship.is_drowned else "*"

        for row in field_grid:
            print(" ".join(row))

    def _validate_field(self) -> None:
        """Проверяет все условия по ТЗ: количество кораблей и соседство"""
        # Проверка количества кораблей по размерам
        count_by_size = {}
        for ship in self.ships:
            size = len(ship.decks)
            count_by_size[size] = count_by_size.get(size, 0) + 1

        if count_by_size.get(1, 0) != 4 or \
           count_by_size.get(2, 0) != 3 or \
           count_by_size.get(3, 0) != 2 or \
           count_by_size.get(4, 0) != 1:
            raise ValueError("Invalid ship distribution")

        # Проверка соседних клеток
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        occupied = set(self.field.keys())
        for row_index, col_index in occupied:
            for d_row, d_col in directions:
                neighbor = (row_index + d_row, col_index + d_col)
                if neighbor in occupied and neighbor != (row_index, col_index):
                    raise ValueError(
                        f"Ships too close at {row_index},{col_index} and {neighbor[0]},{neighbor[1]}"
                    )
