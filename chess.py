import libraries.pieces as pieces
import libraries.rules as rules
import libraries.terminal_colors as colors
from libraries.mapping import map_coordinates

class Piece:
    def __init__(self, piece_id, color, coordinates):
        self.id = piece_id
        self.rank = piece_id[0:-1]
        self.color = color
        self.coordinates = coordinates
        self.unmoved = True

    def is_unmoved(self):
        return self.unmoved

    def set_moved(self):
        self.unmoved = False

    def icon(self):
        if self.rank == "rook":
            string_list = pieces.rook.strip("\n").split("\n")
        elif self.rank == "knight":
            string_list = pieces.knight.strip("\n").split("\n")
        elif self.rank == "bishop":
            string_list = pieces.bishop.strip("\n").split("\n")
        elif self.rank == "queen":
            string_list = pieces.queen.strip("\n").split("\n")
        elif self.rank == "king":
            string_list = pieces.king.strip("\n").split("\n")
        else:
            string_list = pieces.pawn.strip("\n").split("\n")
        return self.color + string_list[0] + "\n" + self.color + string_list[1] + "\n" + self.color + string_list[2] + "\n"

    def update_coordinates(self, row, column):
        self.coordinates[0] = row
        self.coordinates[1] = column

    def get_id(self):
        return self.id

    def get_rank(self):
        return self.rank

    def get_color(self):
        return self.color

    def get_coordinates(self):
        return self.coordinates

    def row(self):
        return self.coordinates[0]

    def column(self):
        return self.coordinates[1]

class Player:
    def __init__(self, color, turn):
        self.color = color
        self.turn = turn
        if turn == "first":
            self.pieces = {
                "rook1": Piece("rook1", self.color, [7,0]),
                "knight1": Piece("knight1", self.color, [7,1]),
                "bishop1": Piece("bishop1", self.color, [7,2]),
                "queen1": Piece("queen1", self.color, [7,3]),
                "king1": Piece("king1", self.color, [7,4]),
                "bishop2": Piece("bishop2", self.color, [7,5]),
                "knight2": Piece("knight2", self.color, [7,6]),
                "rook2": Piece("rook2", self.color, [7,7]),
                "pawn1": Piece("pawn1", self.color, [6,0]),
                "pawn2": Piece("pawn2", self.color, [6,1]),
                "pawn3": Piece("pawn3", self.color, [6,2]),
                "pawn4": Piece("pawn4", self.color, [6,3]),
                "pawn5": Piece("pawn5", self.color, [6,4]),
                "pawn6": Piece("pawn6", self.color, [6,5]),
                "pawn7": Piece("pawn7", self.color, [6,6]),
                "pawn8": Piece("pawn8", self.color, [6,7])
            }
        else:
            self.pieces = {
                "rook1": Piece("rook1", self.color, [0,0]),
                "knight1": Piece("knight1", self.color, [0,1]),
                "bishop1": Piece("bishop1", self.color, [0,2]),
                "queen1": Piece("queen1", self.color, [0,3]),
                "king1": Piece("king1", self.color, [0,4]),
                "bishop2": Piece("bishop2", self.color, [0,5]),
                "knight2": Piece("knight2", self.color, [0,6]),
                "rook2": Piece("rook2", self.color, [0,7]),
                "pawn1": Piece("pawn1", self.color, [1,0]),
                "pawn2": Piece("pawn2", self.color, [1,1]),
                "pawn3": Piece("pawn3", self.color, [1,2]),
                "pawn4": Piece("pawn4", self.color, [1,3]),
                "pawn5": Piece("pawn5", self.color, [1,4]),
                "pawn6": Piece("pawn6", self.color, [1,5]),
                "pawn7": Piece("pawn7", self.color, [1,6]),
                "pawn8": Piece("pawn8", self.color, [1,7])
            }

    def get_id(self):
        return "player_one" if self.turn == "first" else "player_two"

    def remove_piece(self, piece_id):
        del self.pieces[piece_id]

    def promote_piece(self, old_piece, new_piece_name):
        if new_piece_name == "pawn":
            return
        old_id = old_piece.get_id()
        new_id = new_piece_name + "3"
        coordinates = old_piece.get_coordinates()
        self.remove_piece(old_id)
        self.pieces[new_id] = Piece(new_id, self.color, coordinates)

    def move_piece(self, piece_id, destination):
        computer_coords = map_coordinates(destination)
        piece = self.pieces[piece_id]
        piece.update_coordinates(computer_coords[0], computer_coords[1])
        piece.set_moved()
        promotion_possible = piece.get_rank() == "pawn" and (computer_coords[0] == 0 if self.turn == "first" else computer_coords[0] == 7)
        if promotion_possible:
            chosen_piece = ""
            while chosen_piece not in ["queen", "bishop", "rook", "knight", "pawn"]:
                chosen_piece = input("What will you promote your pawn to? ")
                if chosen_piece not in ["queen", "bishop", "rook", "knight", "pawn"]:
                    print(colors.MAGENTA + "PROMOTION ERROR" + chosen_piece + colors.GREEN)
            self.promote_piece(piece, chosen_piece)

    def get_all_pieces(self):
        return list(self.pieces.values())

    def get_piece(self, piece_id):
        return self.pieces[piece_id]

    def get_color(self):
        return self.color

class Board:
    def __init__(self, square_height, color_one, color_two, label_color, configuration):
        self.square_height = square_height
        self.pad_length = 70
        self.color_one = color_one
        self.color_two = color_two
        self.label_color = label_color
        self.configuration = configuration
        self.rows = []
        self.selected_row = None
        self.selected_column = None
        self.set_rows()

    def get_squares(self, *args):
        squares = []
        for destination in args:
            computer_coords = map_coordinates(destination)
            squares.append(self.rows[computer_coords[0]].get_square(computer_coords[1]))
        if len(squares) == 1:
            return squares[0]
        else:
            return tuple(squares)

    def update_configuration(self, config):
        self.configuration = config
        self.rows = []
        self.set_rows()

    def highlight_piece(self, selected_row, square_num):
        self.rows[selected_row].set_selected([square_num], colors.GREEN_BG)

    def highlight_moves(self, coordinates):
        d = {}
        for elem in coordinates:
            try:
                d[elem[0]].append(elem[1])
            except KeyError:
                d[elem[0]] = [elem[1]]
        for key in d.keys():
            self.rows[key].set_selected(d[key], colors.GREEN_BG)

    def set_rows(self):
        for i in range(0, 8):
            self.rows.append(Row(i, self.configuration[i], self.color_one, self.color_two, self.label_color, self.pad_length, self.square_height))

    def get_string(self):
        board_string = 10 * "\n" + self.pad_length * " " + self.label_color
        for letter in "ABCDEFGH":
            board_string += 6 * " " + letter + 6 * " "
        board_string += colors.WHITE + "\n\n"
        for i in range(0, 8):
            board_string += self.rows[i].get_string() 
        board_string += "\n"
        board_string += self.pad_length * " " + self.label_color
        for letter in "ABCDEFGH":
            board_string += 6 * " " + letter + 6 * " "
        board_string += colors.WHITE + 4 * "\n" 
        return board_string 

class Row:
    def __init__(self, number, contents, color1, color2, label_color, pad_length, square_height):
        self.number = number
        self.contents = contents
        self.primary_color = color1
        self.label_color = label_color
        self.secondary_color = color2
        self.pad_length = pad_length
        self.square_height = square_height
        self.squares = []
        for index, piece in enumerate(contents):
            color = (color2 if index % 2 == 0 else color1) if self.number % 2 == 0 else (color1 if index % 2 == 0 else color2)
            self.squares.append(Square(index, piece, color, self.square_height))

    def get_square(self, number):
        return self.squares[number]

    def set_selected(self, square_nums, color):
        if square_nums is not None:
            for index in range(0, 8):
                self.squares[index].set_selected(True if index in square_nums else False, color)

    def get_string(self):
        row_string = ""
        for line_number in range(0, self.square_height):
            for index, square in enumerate(self.squares):
                if line_number == 3:
                    row_string += (((self.pad_length - 3) * " " + self.label_color + str(8 - self.number) + 2 * " ") if index == 0 else "") + square.get_line(line_number) + (colors.BLACK_BG if index == 7 else "") 
                    row_string += "  " + self.label_color + str(8 - self.number) if index == 7 else ""
                else:
                    row_string += (self.pad_length * " " if index == 0 else "") + square.get_line(line_number) + (colors.BLACK_BG if index == 7 else "")
            row_string += "\n"
        return row_string

class Square:
    def __init__(self, number, piece, color, height):
        self.selected = False
        self.selection_color = colors.GREEN_BG
        self.number = number
        self.piece = piece
        self.color = color
        self.height = height
        self.lines = [None] * self.height 
        self.set_lines()

    def can_be_attacked(self, enemy_player, state):
        all_moves = []
        enemy_pieces = enemy_player.get_all_pieces()
        for piece in enemy_pieces:
            pass

    def get_piece(self):
        return self.piece

    def set_selected(self, value, selection_color=colors.GREEN_BG):
        self.selected = value 
        self.selection_color = selection_color

    def set_lines(self):
        self.lines[0] = (self.color if not self.selected else self.selection_color) + 13 * " "
        self.lines[1] = (self.color if not self.selected else self.selection_color) + 13 * " "
        if self.piece is not None:
            icon = self.piece.icon().split("\n")
            for index in range(0, 3):
                self.lines[index + 2] = (self.color if not self.selected else self.selection_color) + 4 * " " + icon[index] + 4 * " "
        else:
            for index in range(2, 5):
                self.lines[index] = (self.color if not self.selected else self.selection_color) + 13 * " "
        self.lines[5] = (self.color if not self.selected else self.selection_color) + 13 * " "

    def get_line(self, number):
        self.set_lines()
        return self.lines[number]

class Game:
    def __init__(self, white, black):
        self.help_mode_on = True
        self.complete = False
        self.player_one = white
        self.player_two = black 
        self.current_player = self.player_one
        self.state = [
            [black.get_piece("rook1"), black.get_piece("knight1"), black.get_piece("bishop1"), black.get_piece("queen1"), black.get_piece("king1"), black.get_piece("bishop2"), black.get_piece("knight2"), black.get_piece("rook2")],
            [black.get_piece("pawn1"), black.get_piece("pawn2"), black.get_piece("pawn3"), black.get_piece("pawn4"), black.get_piece("pawn5"), black.get_piece("pawn6"), black.get_piece("pawn7"), black.get_piece("pawn8")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [white.get_piece("pawn1"), white.get_piece("pawn2"), white.get_piece("pawn3"), white.get_piece("pawn4"), white.get_piece("pawn5"), white.get_piece("pawn6"), white.get_piece("pawn7"), white.get_piece("pawn8")],
            [white.get_piece("rook1"), white.get_piece("knight1"), white.get_piece("bishop1"), white.get_piece("queen1"), white.get_piece("king1"), white.get_piece("bishop2"), white.get_piece("knight2"), white.get_piece("rook2")]
        ]
        self.board = Board(6, colors.BLACK_BG, colors.BLUE_BG, colors.CYAN, self.state)

    def is_complete(self):
        return self.complete

    def print_board(self):
        print(self.board.get_string(), flush=True)

    def clear_state(self):
        for i in range(0, 8):
            for j in range(0, 8):
                self.state[i][j] = None

    def get_legal_moves(self, piece):
        rank = piece.get_rank()
        player = self.current_player
        if rank == "pawn":
            legal_destinations = rules.get_pawn_moves(piece, player, self.state)
        elif rank == "bishop":
            legal_destinations = rules.get_bishop_moves(piece, player, self.state)
        elif rank == "knight":
            legal_destinations = rules.get_knight_moves(piece, player, self.state)
        elif rank == "rook":
            legal_destinations = rules.get_rook_moves(piece, player, self.state)
        elif rank == "king":
            legal_destinations = rules.get_king_moves(piece, player, self.state)
        else:
            legal_destinations = rules.get_queen_moves(piece, player, self.state)
        return legal_destinations

    def destination_is_legal(self, destination, piece):
        computer_coords = map_coordinates(destination)
        rank = piece.get_rank()
        player = self.current_player
        if rank == "pawn":
            legal_destinations = rules.get_pawn_moves(piece, player, self.state)
        elif rank == "bishop":
            legal_destinations = rules.get_bishop_moves(piece, player, self.state)
        elif rank == "knight":
            legal_destinations = rules.get_knight_moves(piece, player, self.state)
        elif rank == "rook":
            legal_destinations = rules.get_rook_moves(piece, player, self.state)
        elif rank == "king":
            legal_destinations = rules.get_king_moves(piece, player, self.state)
        else:
            legal_destinations = rules.get_queen_moves(piece, player, self.state)
        if computer_coords in legal_destinations:
            return True
        return False
                 
    def update_state(self):
        self.clear_state() 
        pieces_in_play = self.player_one.get_all_pieces() + self.player_two.get_all_pieces()
        for piece in pieces_in_play:
            row = piece.row()
            column = piece.column()
            self.state[row][column] = piece 

    def switch_players(self):
        self.current_player = self.player_one if self.current_player == self.player_two else self.player_two

    def request_move(self):
        self.print_board()
        q_castling_possible = rules.queen_side_castling_possible(self.current_player, self.board)
        k_castling_possible = rules.king_side_castling_possible(self.current_player, self.board)
        en_passant_possible = rules.en_passant_possible() 
        performed_special_move = False
        if k_castling_possible:
            response = input("KING-SIDE CASTLING POSSIBLE: Execute? " + colors.GREEN).upper()
            if response == "YES":
                performed_special_move = True
                if self.current_player.get_id() == "player_one":
                    self.current_player.move_piece("rook2", "f1")
                    self.current_player.move_piece("king1", "g1")
                else:
                    self.current_player.move_piece("rook2", "f8")
                    self.current_player.move_piece("king1", "g8")
        if not performed_special_move and q_castling_possible:
            response = input("QUEEN-SIDE CASTLING POSSIBLE: Execute? " + colors.GREEN).upper()
            if response == "YES":
                performed_special_move = True
                if self.current_player.get_id() == "player_one":
                    self.current_player.move_piece("rook1", "c1")
                    self.current_player.move_piece("king1", "b1")
                else:
                    self.current_player.move_piece("rook1", "c8")
                    self.current_player.move_piece("king1", "b8")
        if not performed_special_move:
            piece_id = input(self.current_player.get_color() + "Which piece would you like to move? " + colors.GREEN)
            piece = self.current_player.get_piece(piece_id)
            coordinates = piece.get_coordinates()
            self.board.highlight_piece(coordinates[0], coordinates[1])
            self.board.highlight_moves(self.get_legal_moves(piece))
            self.print_board()
            move_is_illegal = True
            while move_is_illegal:
                destination = input(self.current_player.get_color() + "Where do you want to move? " + colors.GREEN)
                move_is_illegal = not self.destination_is_legal(destination, piece)
                if move_is_illegal:
                    print(colors.MAGENTA + "ILLEGAL MOVE ERROR")
            enemy_piece = self.board.get_squares(destination).get_piece()
            if enemy_piece is not None:
                enemy = self.player_one if self.current_player == self.player_two else self.player_two
                enemy_id = enemy_piece.get_id()
                enemy.remove_piece(enemy_id)
            self.current_player.move_piece(piece_id, destination)
        self.update_state()
        self.board.update_configuration(self.state)
        self.switch_players()

if __name__ == "__main__":
    white = Player(colors.WHITE, "first")
    black = Player(colors.RED, "second")
    chess_game = Game(white, black)
    while not chess_game.is_complete():
        chess_game.request_move()
