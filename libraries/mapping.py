def map_coordinates(destination):
    phys_coords = [int(destination[1]), ord(destination[0].capitalize()) - 64]
    computer_row = 8 - phys_coords[0]
    computer_col = phys_coords[1] - 1
    return [computer_row, computer_col]
