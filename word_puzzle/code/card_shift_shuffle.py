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
    print(f'shift   in.p {pos} out.p {new_pos}')
    return new_pos


def shuffle(pos, pile_sz, num_piles):
    row, col = shuffled_row_col(pos, num_piles)
    new_pos = row + ((col - 1) * pile_sz)
    print(f'shuffle in.p {pos} out.p {new_pos} ({row},{col})')
    return new_pos


def shuffled_row_col(pos, num_piles):
    q = math.floor(pos / num_piles)
    r = pos % num_piles
    if r == 0:
        row = q
        col = r + num_piles
    else:
        row = q + 1
        col = r
    return row, col


def test():
    num_piles = 3
    pile_sz = 3
    num_rounds = 3
    for p in range(1, (num_piles * pile_sz + 1)):
        play_round(p, pile_sz, num_piles, num_rounds)

    num_piles = 3
    pile_sz = 7
    num_rounds = 3
    for p in range(1, (num_piles * pile_sz + 1)):
        play_round(p, pile_sz, num_piles, num_rounds)

    num_piles = 3
    pile_sz = 5
    num_rounds = 3
    for p in range(1, (num_piles * pile_sz + 1)):
        play_round(p, pile_sz, num_piles, num_rounds)

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


def play_round(p, pile_sz, num_piles, num_rounds):
    print(f'start.p      {p}')
    for i in range(1, num_rounds + 1):
        p = shift(p, pile_sz, num_piles)
        p = shuffle(p, pile_sz, num_piles)
    print("-----------")


if __name__ == '__main__':
    test()

# 12 => 18
# 14 => 12
# 8 => 10
# 10 => 4
# 11 => 11
#
# p + 7
# p - 7
#
# q = p / 3
# r = p % 3
#
# p = 11, q = 3, r = 2 => (4, 2) => 11
# p = 8, q = 2, r = 2 => (3, 2) => 10
# p = 10, q = 3, r = 1 => (4, 1) => 4
# p = 14, q = 4, r = 2 => (5, 2) => 12
# p = 12, q = 4, r = 0 => (4, 3) = 18
#
# if r == 0 : (row = q, col = r + 3)
#    else   : (row = q + 1, col = r)
#
# row + ((col - 1) * 7)
