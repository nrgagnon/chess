def contains_piece(piece_type, coordinates, player, state):
    row = coordinates[0]
    column = coordinates[1]
    piece = state[row][column]
    if piece_type == "enemy":
        if piece is not None and player.get_color() != piece.get_color():
            return True
    else:
        if piece is not None and player.get_color() == piece.get_color():
            return True
    return False

def check_achieved():
    pass

def checkmate_achieved():
    pass

def get_pawn_moves(piece, player, state):
    legal_destinations = []
    coordinates = piece.get_coordinates()
    player_id = player.get_id()
    # ----------------------------------------
    # Get all possible destinations for a pawn
    # ----------------------------------------
    d1 = [coordinates[0] + (1 if player_id == "player_two" else -1), coordinates[1]]
    d2 = [coordinates[0] + (2 if player_id == "player_two" else -2), coordinates[1]]
    d3 = [coordinates[0] + (1 if player_id == "player_two" else -1), coordinates[1] - 1]
    d4 = [coordinates[0] + (1 if player_id == "player_two" else -1), coordinates[1] + 1]

    if state[d1[0]][d1[1]] == None:
        legal_destinations.append(d1)
    if piece.is_unmoved() and state[d1[0]][d1[1]] == None and state[d2[0]][d2[1]] == None:
        legal_destinations.append(d2)
    if is_legit_square(d3) and contains_piece("enemy", d3, player, state):
        legal_destinations.append(d3)
    if is_legit_square(d4) and contains_piece("enemy", d4, player, state):
        legal_destinations.append(d4)

    return legal_destinations

def is_legit_square(coordinates):
    if coordinates[0] >= 0 and coordinates[0] <= 7:
        if coordinates[1] >= 0 and coordinates[1] <= 7:
            return True
    return False

def get_rook_moves(piece, player, state):
    legal_destinations = []
    coordinates = piece.get_coordinates()
    # ----------------------------------------
    # Get all possible destinations for a rook 
    # ----------------------------------------
    directions = ["up", "down", "right", "left"]
    for direction in directions:
        i = 1 if direction in ["up", "down"] else 0
        j = 1 if direction in ["left", "right"] else 0
        destination = [coordinates[0] + (i if direction == "down" else -i), coordinates[1] + (j if direction == "right" else -j)]
        while is_legit_square(destination) and not (contains_piece("enemy", destination, player, state) or contains_piece("friend", destination, player, state)):
            legal_destinations.append(destination)
            i += 1 if direction in ["up", "down"] else 0
            j += 1 if direction in ["left", "right"] else 0
            destination = [coordinates[0] + (i if direction == "down" else -i), coordinates[1] + (j if direction == "right" else -j)]
        if is_legit_square(destination) and contains_piece("enemy", destination, player, state):
            legal_destinations.append(destination)
    return legal_destinations

def get_bishop_moves(piece, player, state):
    legal_destinations = []
    coordinates = piece.get_coordinates()
    # ------------------------------------------
    # Get all possible destinations for a bishop 
    # ------------------------------------------
    directions = ["northeast", "northwest", "southeast", "southwest"]
    for direction in directions:
        i, j = 1, 1
        destination = [coordinates[0] + (i if "south" in direction else -i), coordinates[1] + (j if "east" in direction else -j)]
        while is_legit_square(destination) and not (contains_piece("enemy", destination, player, state) or contains_piece("friend", destination, player, state)):
            legal_destinations.append(destination)
            i += 1
            j += 1
            destination = [coordinates[0] + (i if "south" in direction else -i), coordinates[1] + (j if "east" in direction else -j)]
        if is_legit_square(destination) and contains_piece("enemy", destination, player, state):
            legal_destinations.append(destination)
    return legal_destinations

def get_knight_moves(piece, player, state):
    legal_destinations = []
    coordinates = piece.get_coordinates()
    # ------------------------------------------
    # Get all possible destinations for a knight
    # ------------------------------------------
    possible_destinations = []
    possible_destinations.append([coordinates[0] + 1, coordinates[1] + 2])
    possible_destinations.append([coordinates[0] + 1, coordinates[1] - 2])
    possible_destinations.append([coordinates[0] - 1, coordinates[1] + 2])
    possible_destinations.append([coordinates[0] - 1, coordinates[1] - 2])
    possible_destinations.append([coordinates[0] + 2, coordinates[1] + 1])
    possible_destinations.append([coordinates[0] + 2, coordinates[1] - 1])
    possible_destinations.append([coordinates[0] - 2, coordinates[1] + 1])
    possible_destinations.append([coordinates[0] - 2, coordinates[1] - 1])
    for pd in possible_destinations:
        if is_legit_square(pd):
            if state[pd[0]][pd[1]] == None or contains_piece("enemy", pd, player, state):
                legal_destinations.append(pd)
    return legal_destinations

def get_king_moves(piece, player, state):
    legal_destinations = [] 
    coordinates = piece.get_coordinates()

    possible_destinations = []
    possible_destinations.append([coordinates[0] + 1, coordinates[1]])
    possible_destinations.append([coordinates[0] - 1, coordinates[1]]) 
    possible_destinations.append([coordinates[0], coordinates[1] + 1])
    possible_destinations.append([coordinates[0], coordinates[1] - 1])
    possible_destinations.append([coordinates[0] + 1, coordinates[1] + 1])
    possible_destinations.append([coordinates[0] + 1, coordinates[1] - 1])
    possible_destinations.append([coordinates[0] - 1, coordinates[1] + 1])
    possible_destinations.append([coordinates[0] - 1, coordinates[1] - 1])

    for destination in possible_destinations:
        if is_legit_square(destination) and (state[destination[0]][destination[1]] == None or contains_piece("enemy", destination, player, state)):
            legal_destinations.append(destination)
    
    return legal_destinations

def get_queen_moves(piece, player, state):
    return get_rook_moves(piece, player, state) + get_bishop_moves(piece, player, state)

def queen_side_castling_possible(player, board):
    try:
        king = player.get_piece("king1")
        rook = player.get_piece("rook1")
    except KeyError:
        return False
    player_id = player.get_id()
    sq1, sq2, sq3 = board.get_squares("b1", "c1", "d1") if player_id == "player_one" else board.get_squares("b8", "c8", "d8")
    if sq1.get_piece() == None and sq2.get_piece() == None and sq3.get_piece() == None:
        if king.is_unmoved() and rook.is_unmoved():
            return True
    return False

def king_side_castling_possible(player, board):
    try:
        king = player.get_piece("king1")
        rook = player.get_piece("rook2")
    except KeyError:
        return False
    player_id = player.get_id()
    sq1, sq2 = board.get_squares("f1", "g1") if player_id == "player_one" else board.get_squares("f8", "g8")
    if sq1.get_piece() == None and sq2.get_piece() == None:
        if king.is_unmoved() and rook.is_unmoved():
            return True
    return False

def en_passant_possible():
    return False
