import math


def shift(pos, pile_sz, num_piles):
    mid = math.floor(num_piles / 2) + 1
    q = math.floor(pos / pile_sz)
    r = pos % pile_sz
    if r == 0:
        pile = q
    else:
        pile = q + 1
    diff = mid - pile
    new_pos = pos + (diff * pile_sz)
    # print(f'pos {pos} pile {pile} mid {mid} diff {diff} new pos {new_pos}')
    print(f'shift   in.p {pos} out.p {new_pos} {pos_to_point(new_pos, pile_sz)}')
    return new_pos


def shuffle(pos, pile_sz, num_piles):
    q = math.floor(pos / num_piles)
    r = pos % num_piles
    if r == 0:
        row = q
        col = r + num_piles
    else:
        row = q + 1
        col = r
    new_pos = row + ((col - 1) * pile_sz)
    print(f'shuffle in.p {pos} out.p {new_pos} ({row}, {col})')
    return new_pos


def pos_to_point(pos, pile_sz):
    q = math.floor(pos / pile_sz)
    r = pos % pile_sz
    if r == 0:
        row = pile_sz
        col = q
    else:
        row = r
        col = q + 1
    return row, col


def play_round(pos, pile_sz, num_piles, num_rounds):
    print(f'start.p      {pos} {pos_to_point(pos, pile_sz)}')
    # midpoint
    expected = math.floor((pile_sz * num_piles) / 2) + 1
    for i in range(1, num_rounds + 1):
        pos = shift(pos, pile_sz, num_piles)
        pos = shuffle(pos, pile_sz, num_piles)
    assert pos == expected
    print("-----------")


def test():
    # num_piles = 3
    # pile_sz = 7
    # num_rounds = 3
    # for p in range(1, (num_piles * pile_sz + 1)):
    #     play_round(p, pile_sz, num_piles, num_rounds)
    #
    # num_piles = 3
    # pile_sz = 5
    # num_rounds = 3
    # for p in range(1, (num_piles * pile_sz + 1)):
    #     play_round(p, pile_sz, num_piles, num_rounds)

    num_piles = 3
    pile_sz = 9
    num_rounds = 5
    for p in range(1, (num_piles * pile_sz + 1)):
        play_round(p, pile_sz, num_piles, num_rounds)

    num_piles = 5
    pile_sz = 7
    num_rounds = 3
    for p in range(1, (num_piles * pile_sz + 1)):
        play_round(p, pile_sz, num_piles, num_rounds)


if __name__ == '__main__':
    test()

# 1 8  15
# 2 9  16
# 3 10 17
# 4 11 18
# 5 12 19
# 6 13 20
# 7 14 21


# 8, 10, 11
# 9, 10, 11
# 10, 11
# 11
# 12, 11
# 13, 12, 11
# 14, 12, 11

