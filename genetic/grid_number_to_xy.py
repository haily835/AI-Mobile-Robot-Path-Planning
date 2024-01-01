def grid_number_to_xy(position, n):
    
    if position % n == 0:
        c = 0
    else:
        c = position % n
    r = position // n
    return int(r), int(c)

# position_value = 25

# result = grid_number_to_xy(position_value)
# print(result)
