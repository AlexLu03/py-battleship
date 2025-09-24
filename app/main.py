from typing import List, Tuple, Optional, Dict


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

        for r in range(row_start, row_end + 1):
            for c in range(col_start, col_end + 1):
                decks.append(Deck(r, c))
        return decks

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> Optional[str]:
        deck = self.get_deck(row, column)
        if deck and deck.is_alive:
            deck.fire()
            if all(not d.is_alive for d in self.decks):
                self.is_drowned = True
                return "Sunk!"
            return "Hit!"
        return None


class Battleship:
    def __init__(self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
        self.ships: List[Ship] = []
        self.field: Dict[Tuple[int, int], Deck] = {}

        for start, end in ships:
            ship = Ship(start, end)
            if not ship.decks:
                raise ValueError(f"Invalid ship coordinates: {start}-{end}")
            self.ships.append(ship)
            for deck in ship.decks:
                if (deck.row, deck.column) in self.field:
                    raise ValueError(f"Overlapping ships at: {deck.row},{deck.column}")
                self.field[(deck.row, deck.column)] = deck

    def fire(self, location: Tuple[int, int]) -> str:
        row, col = location
        deck = self.field.get((row, col))
        if not deck:
            return "Miss!"
        if not deck.is_alive:
            return "Miss!"  # уже подбито
        deck.fire()
        ship = next(s for s in self.ships if deck in s.decks)
        if all(not d.is_alive for d in ship.decks):
            ship.is_drowned = True
            return "Sunk!"
        return "Hit!"

    def print_field(self) -> None:
        field_grid = [["~"] * 10 for _ in range(10)]
        for (r, c), deck in self.field.items():
            if deck.is_alive:
                field_grid[r][c] = "□"
            else:
                ship = next(s for s in self.ships if deck in s.decks)
                field_grid[r][c] = "x" if ship.is_drowned else "*"

        for row in field_grid:
            print(" ".join(row))

    def _validate_field(self) -> None:
        # Примерная логика:
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
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,0), (0,1), (1,-1), (1,0), (1,1)]
        occupied = set(self.field.keys())
        for r, c in occupied:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (nr, nc) in occupied and (nr, nc) != (r, c):
                    raise ValueError(f"Ships too close at {r},{c} and {nr},{nc}")
