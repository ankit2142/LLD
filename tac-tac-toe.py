from collections import deque
from enum import Enum

# for player
class PieceType(Enum):
    X = "X"
    O = "O"

class PlayingPiece:
    def __init__(self, piece_type):
        self.piece_type = piece_type


class PlayingPieceO(PlayingPiece):
    def __init__(self):
        super().__init__(PieceType.O)

class PlayingPieceX(PlayingPiece):
    def __init__(self):
        super().__init__(PieceType.X)

class Player:
    def __init__(self, name, playing_piece):
        self.name = name
        self.playing_piece = playing_piece


# for tic-tac-toe-board
class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]

    def add_piece(self, row, column, playing_piece):
        if self.board[row][column] is not None:
            return False
        self.board[row][column] = playing_piece
        return True

    def get_free_cells(self):
        free_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] is None]
        return free_cells

    def print_board(self):
        for row in self.board:
            for cell in row:
                if cell:
                    print(cell.piece_type.name, end="   ")
                else:
                    print("    ", end="")
                print("|", end=" ")
            print("\n" + "-" * 20)


# my game class
class TicTacToeGame:
    def __init__(self):
        self.players = deque()
        self.game_board = None

    def initialize_game(self):
        # Create players
        cross_piece = PlayingPieceX()
        player1 = Player("Player1", cross_piece)

        noughts_piece = PlayingPieceO()
        player2 = Player("Player2", noughts_piece)

        self.players.append(player1)
        self.players.append(player2)

        # Initialize the board
        self.game_board = Board(3)

    def start_game(self):
        no_winner = True
        while no_winner:
            player_turn = self.players.popleft()
            self.game_board.print_board()
            free_spaces = self.game_board.get_free_cells()

            if not free_spaces:
                no_winner = False
                continue

            # Get user input
            print(f"Player: {player_turn.name}, Enter row,column: ")
            s = input().strip()
            values = s.split(',')
            input_row = int(values[0])
            input_column = int(values[1])

            # Place the piece
            if not self.game_board.add_piece(input_row, input_column, player_turn.playing_piece):
                print("Incorrect position chosen, try again")
                self.players.appendleft(player_turn)
                continue

            self.players.append(player_turn)

            if self.is_there_winner(input_row, input_column, player_turn.playing_piece.piece_type):
                return player_turn.name

        return "tie"

    def is_there_winner(self, row, column, piece_type):
        row_match = all(self.game_board.board[row][i] is not None and self.game_board.board[row][i].piece_type == piece_type for i in range(self.game_board.size))
        column_match = all(self.game_board.board[i][column] is not None and self.game_board.board[i][column].piece_type == piece_type for i in range(self.game_board.size))
        diagonal_match = all(self.game_board.board[i][i] is not None and self.game_board.board[i][i].piece_type == piece_type for i in range(self.game_board.size))
        anti_diagonal_match = all(self.game_board.board[i][self.game_board.size - i - 1] is not None and self.game_board.board[i][self.game_board.size - i - 1].piece_type == piece_type for i in range(self.game_board.size))
        
        return row_match or column_match or diagonal_match or anti_diagonal_match

if __name__ == "__main__":
    game = TicTacToeGame()
    game.initialize_game()
    print("Game winner is:", game.start_game())
