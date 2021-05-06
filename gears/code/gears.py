class Gear:
    # 0 indexed gear key
    # teeth number 0-8
    num_teeth = 9

    def __init__(self, key):
        self.key = key

    def rotate(self, clockwise, by):
        _by = by % self.num_teeth
        if clockwise:
            self.key += (self.num_teeth - _by)
        else:
            self.key += _by
        self.key = self.key % self.num_teeth


def rotate(gears, gear_index, clockwise, by):
    print(f'Gear: {gear_index} Rotating clockwise: {clockwise} By: {by}')
    print('--------------------------------------------------')
    curr = gears[gear_index]
    # rotate current by 'by'
    curr.rotate(clockwise, by)

    # move right
    _clockwise = not clockwise
    print("Moving right")
    for i in range(gear_index + 1, len(gears)):
        g = gears[i]
        prevKey = g.key + 1
        g.rotate(_clockwise, by)
        print(f'Gear: {i} Prev Key: {prevKey} Key: {g.key + 1} Rotated clockwise: {_clockwise} By: {by}')
        # print_gears(gears, "")
        _clockwise = not _clockwise

    # move left
    _clockwise = not clockwise
    print("Moving left")
    for i in range(gear_index - 1, -1, -1):
        g = gears[i]
        prevKey = g.key + 1
        g.rotate(_clockwise, by)
        print(f'Gear: {i} Prev Key: {prevKey} Key: {g.key + 1} Rotated clockwise: {_clockwise} By: {by}')
        # print_gears(gears, "")
        _clockwise = not _clockwise
    print('--------------------------------------------------')


def print_gears(gears, msg):
    print()
    print(msg)
    for i in range(len(gears)):
        print(f'Gear: {i} key: {gears[i].key + 1}')
    print()


def test():
    # 0 indexed gear keys
    gears = [Gear(2), Gear(6), Gear(2), Gear(5)]
    print_gears(gears, "before rotation")
    rotate(gears, 0, False, 2)
    rotate(gears, 1, True, 3)
    rotate(gears, 2, False, 5)
    rotate(gears, 3, True, 4)
    print_gears(gears, "after rotation of gear 3")


if __name__ == '__main__':
    test()
