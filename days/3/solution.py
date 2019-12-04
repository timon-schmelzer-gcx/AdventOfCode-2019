class Point:
    def __init__(self, x, y, step):
        self.x = x
        self.y = y
        self.step = step

    def __hash__(self):
        return hash(str(self.x) + ' ' + str(self.y))

    def __eq__(self, other):
        return (
            self.x == other.x and self.y == other.y
        )

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y}, step={self.step})'

    def __lt__(self, other):
        if self.x == other.x and self.y == other.y:
            return self.step < other.step
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x


def read_input(path='data.txt'):
    with open(path, 'r') as infile:
        wirepaths = infile.readlines()
    wirepaths = [
        wirepath.replace('\n', '').split(',') for wirepath in wirepaths
    ]
    return wirepaths


def sort_points(point_one, point_two):
    if point_one.x > point_two.x:
        return point_one
    if point_one.x < point_two.x:
        return point_two

    # Now, x are equal
    if point_one.y > point_two.y:
        return point_one
    if point_one.y < point_two.y:
        return point_two

    # Now, x and y are equal
    if point_one.step > point_two.step:
        return point_one
    if point_one.step < point_two.step:
        return point_two

    # Now, everything is equal
    return point_one


def walk_single_step(cur_point, direction):
    if direction == 'U':
        new_point = Point(
            cur_point.x,
            cur_point.y + 1,
            cur_point.step + 1
        )
    elif direction == 'D':
        new_point = Point(
            cur_point.x,
            cur_point.y - 1,
            cur_point.step + 1
        )
    elif direction == 'R':
        new_point = Point(
            cur_point.x + 1,
            cur_point.y,
            cur_point.step + 1
        )
    elif direction == 'L':
        new_point = Point(
            cur_point.x - 1,
            cur_point.y,
            cur_point.step + 1
        )
    else:
        raise NotImplementedError('Direction not implemented.')

    return new_point


def walk_path(wirepath):
    all_positions = []
    start_position = Point(x=0, y=0, step=0)

    cur_position = start_position

    for instruction in wirepath:
        direction, n_steps = instruction[0], int(instruction[1:])
        for _ in range(n_steps):
            new_position = walk_single_step(cur_position, direction)
            all_positions.append(new_position)
            cur_position = new_position

    return all_positions


def find_interceptions(positions_one, positions_two):
    # The naive implementation below takes several minutes (or even longer)?
    # Use the function 'find_interceptions_fast' instead
    interceptions = []

    print(len(positions_one), len(positions_two))
    for element_one in positions_one:
        for element_two in positions_two:
            if element_one == element_two:
                interceptions.append(element_one)

    return interceptions


def find_interceptions_fast(positions_one, positions_two):
    return list(set(positions_one).intersection(positions_two))


def find_interceptions_and_return_both_fast(positions_one, positions_two):
    interceptions_one = list(set(positions_one).intersection(positions_two))
    interceptions_two = list(set(positions_two).intersection(positions_one))

    # WARNING: Not sorting the interception lists will cause
    # arbitrary behaviour! You can test it by commenting out
    # one of the next two lines and runing the script multiple times.
    interceptions_one = sorted(interceptions_one)
    interceptions_two = sorted(interceptions_two)

    return [
        point_pair for point_pair in zip(
            interceptions_one, interceptions_two
        )
    ]


def find_shortest_distance(inteceptions):
    distances = [abs(point.x) + abs(point.y) for point in inteceptions]
    return min(distances)


def find_minimal_steps(inteceptions):
    all_steps = [
        point_pair[0].step + point_pair[1].step
        for point_pair in inteceptions
    ]
    return min(all_steps)


def solve(wirepath_one, wirepath_two, part=1):
    all_positions_one = walk_path(wirepath_one)
    all_positions_two = walk_path(wirepath_two)

    # The following is too slow for this riddle:
    # interceptions = find_interceptions(all_positions_one, all_positions_two)
    interceptions = find_interceptions_fast(
        all_positions_one, all_positions_two
    )

    if part == 1:
        interceptions = find_interceptions_fast(
            all_positions_one, all_positions_two
        )
        result = find_shortest_distance(interceptions)
    elif part == 2:
        interceptions = find_interceptions_and_return_both_fast(
            all_positions_one, all_positions_two
        )
        result = find_minimal_steps(interceptions)
    else:
        raise NotImplementedError('Part not implemented.')
    return result


def test_solve_part_one():
    examples_and_solutions = [
        [
            'R8,U5,L5,D3'.split(','),
            'U7,R6,D4,L4'.split(','),
            6
        ],
        [
            'R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(','),
            'U62,R66,U55,R34,D71,R55,D58,R83'.split(','),
            159
        ],
        [
            'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(','),
            'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(','),
            135
        ]
    ]
    for wirepath_one, wirepath_two, result in examples_and_solutions:
        assert solve(wirepath_one, wirepath_two, part=1) == result


def test_solve_part_two():
    examples_and_solutions = [
        [
            'R8,U5,L5,D3'.split(','),
            'U7,R6,D4,L4'.split(','),
            30
        ],
        [
            'R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(','),
            'U62,R66,U55,R34,D71,R55,D58,R83'.split(','),
            610
        ],
        [
            'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(','),
            'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(','),
            410
        ]
    ]
    for wirepath_one, wirepath_two, result in examples_and_solutions:
        assert solve(wirepath_one, wirepath_two, part=2) == result


if __name__ == "__main__":
    test_solve_part_one()
    test_solve_part_two()

    wirepath_one, wirepath_two = read_input()

    print('Solution part 1:', solve(wirepath_one, wirepath_two, part=1))
    print('Solution part 2:', solve(wirepath_one, wirepath_two, part=2))
