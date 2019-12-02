from operator import add, mul

OPERATIONS = {
    1: add,
    2: mul
}


def read_input(path='data.txt'):
    with open(path, 'r') as infile:
        intcode = infile.read()
    intcode = intcode.split(',')
    intcode = [int(number) for number in intcode]
    return intcode


def apply_operations(intcode):
    cur_index = 0
    cur_opcode = intcode[cur_index]
    modified_intcode = intcode[:]

    while cur_opcode != 99:
        op = OPERATIONS[cur_opcode]

        index_first = modified_intcode[cur_index + 1]
        index_second = modified_intcode[cur_index + 2]
        index_third = modified_intcode[cur_index + 3]

        val_first = modified_intcode[index_first]
        val_second = modified_intcode[index_second]

        val_result = op(val_first, val_second)
        modified_intcode[index_third] = val_result

        cur_index += 4
        cur_opcode = modified_intcode[cur_index]

    return modified_intcode


def test_apply_operations():
    examples_and_solution = [
        [[1, 0, 0, 0, 99], [2, 0, 0, 0, 99]],
        [[2, 3, 0, 3, 99], [2, 3, 0, 6, 99]],
        [[2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]],
        [[1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]],
        [
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
        ]
    ]
    for example, solution in examples_and_solution:
        assert(apply_operations(example) == solution)


if __name__ == '__main__':
    test_apply_operations()

    intcode = read_input()

    # Modify code according to part one
    intcode_part_one = intcode[:]
    intcode_part_one[1] = 12
    intcode_part_one[2] = 2

    modified_intcode = apply_operations(intcode_part_one)

    print('Solution part 1:', modified_intcode[0])

    for noun in range(100):
        for verb in range(100):
            intcode_part_two = intcode[:]
            intcode_part_two[1] = noun
            intcode_part_two[2] = verb

            modified_intcode = apply_operations(intcode_part_two)

            if modified_intcode[0] == 19690720:
                print('Solution part 2:', 100 * noun + verb)
