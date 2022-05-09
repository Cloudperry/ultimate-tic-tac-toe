from enum import Enum
from collections import namedtuple

Coord = namedtuple("Coord", ["x", "y"])

class CellState(Enum):
    Empty = 0
    Player1 = 1
    Player2 = 2

def check_winner_generic(board: list) -> CellState:
    for n in range(3):
        row_not_empty = board[n][0] != CellState.Empty
        col_not_empty = board[0][n] != CellState.Empty
        if row_not_empty and board[n][0] == board[n][1] == board[n][2]:
            return board[n][0]
        elif col_not_empty and board[0][n] == board[1][n] == board[2][n]:
            return board[0][n]
    diag_1_not_empty = board[0][0] != CellState.Empty # North west to south east diagonal
    diag_2_not_empty = board[0][2] != CellState.Empty # North east to south west diagonal
    if diag_1_not_empty and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    elif diag_2_not_empty and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return CellState.Empty

class LocalBoard:
    def __init__(self) -> None:
        self.local_b = [[CellState.Empty for _ in range(3)] for _ in range(3)]
        self.winner = CellState.Empty

    def place_mark(self, player_n: int, coord: Coord) -> bool:
        if self.local_b[coord.y][coord.x] != CellState.Empty:
            return False
        else:
            self.local_b[coord.y][coord.x] = CellState(player_n)
            return True

    def check_winner(self) -> CellState:
        if self.winner == CellState.Empty:
            self.winner = check_winner_generic(self.local_b)
        return self.winner

class Game:
    def __init__(self, starting_player_n: int) -> None:
        self.turn_of_player = starting_player_n
        self.move_count = 0
        self.board = [[LocalBoard() for _ in range(3)] for _ in range(3)]
        self.board_status = [[CellState.Empty for _ in range(3)] for _ in range(3)]
        self.next_board = None
        self.winner = CellState.Empty
        self.winning_player = None

    def global_pos_to_local(self, pos: Coord) -> tuple:
        return Coord(pos.x // 3, pos.y // 3), Coord(pos.x % 3, pos.y % 3)

    def board_allowed(self, b_pos: Coord) -> bool:
        board_won = self.board[b_pos.y][b_pos.x].winner != CellState.Empty
        return not board_won and (self.next_board is None or b_pos == self.next_board)

    def place_mark(self, player_n: int, b_pos: Coord, pos: Coord):
        if player_n != self.turn_of_player or not self.board_allowed(b_pos):
            return False
        else:
            result = self.board[b_pos.y][b_pos.x].place_mark(player_n, pos)
            if result: # Execute win and turn logic only if mark was actually placed
                self.move_count += 1
                self.turn_of_player = next(iter({1, 2} - {player_n}))
                win_status = self.board[b_pos.y][b_pos.x].check_winner()
                if win_status != CellState.Empty:
                    self.board_status[b_pos.y][b_pos.x] = win_status
                if self.board_status[pos.y][pos.x] == CellState.Empty:
                    self.next_board = pos
                else:
                    self.next_board = None
            return result

    def get_board_n(self, b_pos: Coord) -> int:
        return b_pos.x + 1 + b_pos.y * 3

    def get_cell(self, b_pos: Coord, pos: Coord) -> CellState:
        return self.board[b_pos.y][b_pos.x].local_b[pos.y][pos.x]

    def pos_open(self, board: Coord, pos: Coord) -> bool:
        return self.board_allowed(board) and self.get_cell(board, pos) == CellState.Empty

    def check_winner(self) -> CellState:
        if self.winner == CellState.Empty:
            self.winner = check_winner_generic(self.board_status)
            if self.winner != CellState.Empty:
                self.winning_player = self.winner.value
        return self.winner

    def __str__(self) -> str:
        result = ""
        for row in range(9):
            if row == 0:
                result += "   0   1   2     3   4   5     6   7   8\n\n      LB1           LB2           LB3\n"
            result += f"{row} "
            for col in range(9):
                b_pos, local_pos = self.global_pos_to_local(Coord(col, row))
                cell = self.get_cell(b_pos, local_pos)
                if cell == CellState.Empty:
                    result += "   "
                elif cell == CellState.Player1:
                    result += " X "
                elif cell == CellState.Player2:
                    result += " O "
                if (col + 1) % 3 == 0:
                    result += "   "
                elif col != 8:
                    result += "|"
            if row != 8:
                if (row + 1) % 3 == 0:
                    result += f"\n\n      LB{1 + ((row + 1) // 3) * 3}           LB{2 + ((row + 1) // 3) * 3}           LB{3 + ((row + 1) // 3) * 3}\n"
                else:
                    result += "\n  -----------   -----------   -----------\n"
        return result

class Games:
    def __init__(self) -> None:
        self.active_games = {}

    def new_game_in(self, lobby_id: int, starting_player_n: int):
        self.active_games[lobby_id] = Game(starting_player_n)

    def delete_game_in(self, lobby_id: int):
        del self.active_games[lobby_id]

if __name__ == "__main__":
    g = Game(2)
    g.place_mark(1, Coord(1, 1), Coord(1, 1))
    g.place_mark(2, Coord(1, 1), Coord(2, 1))
    g.place_mark(1, Coord(2, 1), Coord(1, 0))
    g.place_mark(2, Coord(1, 0), Coord(1, 1))
    print(g)
    print(g.check_winner()) # CellState.Empty
    g.place_mark(1, Coord(1, 1), Coord(1, 0))
    g.place_mark(2, Coord(1, 0), Coord(2, 1))
    g.place_mark(1, Coord(2, 1), Coord(1, 1))
    g.place_mark(2, Coord(1, 1), Coord(0, 1))
    g.place_mark(1, Coord(0, 1), Coord(1, 2))
    g.place_mark(2, Coord(1, 2), Coord(2, 1))
    print(g)
    print(g.check_winner()) # CellState.Empty
    print(g.next_board) # Coord(2, 1)
    g.place_mark(1, Coord(2, 1), Coord(1, 2))
    g.place_mark(2, Coord(1, 2), Coord(1, 1))
    g.place_mark(1, Coord(1, 1), Coord(1, 2))
    g.place_mark(2, Coord(1, 2), Coord(0, 1))
    g.place_mark(1, Coord(0, 1), Coord(1, 0))
    g.place_mark(2, Coord(1, 0), Coord(0, 1))
    g.place_mark(1, Coord(0, 1), Coord(1, 1))
    print(g)
    print(g.check_winner()) # CellState.Player1
    print(g.next_board) # None
