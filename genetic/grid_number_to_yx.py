def grid_number_to_yx(position, n):
    if position % n == 0:
        c = 0
    else:
        c = position % n
    r = position // n
    return int(r), int(c)

