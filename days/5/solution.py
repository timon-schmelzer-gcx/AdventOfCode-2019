# This code contain a lot of functionality already provided in day 2.
from operator import add, mul


class Computer():
    OPERATIONS = {
        1: add,
        2: mul
    }

    def __init__(
        self, intcode, lazy_input=None, no_zero_output=False,
            output_string='Output: {}'):
        self.intcode = intcode
        self.cur_index = 0
        self.finished = False
        self.lazy_input = lazy_input
        self.no_zero_output = no_zero_output
        self.output_string = output_string

    def operate(self):
        while(not self.finished):
            instruction = self.intcode[self.cur_index]

            if str(instruction).endswith('1') or \
                    str(instruction).endswith('2'):
                # Extend to four digit number. E.g. 102 --> 0102.
                instruction_zfilled = str(instruction).zfill(4)

                # Make sure nothing stange happens, e.g. input of 1012.
                if instruction_zfilled[-2] != '0':
                    raise NotImplementedError(
                        f'Instruction not implemented, {instruction}'
                    )

                # Remove last two digits and reverse
                instruction_short = instruction_zfilled[:2:][::-1]

                # First value
                if instruction_short[0] == '0':
                    value_first = self.intcode[
                        self.intcode[self.cur_index + 1]
                    ]
                elif instruction_short[0] == '1':
                    value_first = self.intcode[self.cur_index + 1]
                else:
                    raise NotImplementedError(
                        f'Instruction not implemented, {instruction}'
                    )

                # Second value
                if instruction_short[1] == '0':
                    value_second = self.intcode[
                        self.intcode[self.cur_index + 2]
                    ]
                elif instruction_short[1] == '1':
                    value_second = self.intcode[self.cur_index + 2]
                else:
                    raise NotImplementedError(
                        f'Instruction not implemented, {instruction}'
                    )

                # Apply operation
                result = self.OPERATIONS[int(str(instruction)[-1])](
                    value_first, value_second
                )

                # Fill result
                self.intcode[self.intcode[self.cur_index + 3]] = result
                self.cur_index += 4

            elif str(instruction).endswith('3'):
                if self.lazy_input:
                    value = self.lazy_input
                else:
                    value = int(input(
                        'Input (Hint: Type 1 for part 1 solution and 5 for '
                        'part 2. Ignore zeros for the first part): '
                    ))
                instruction_zfilled = str(instruction).zfill(3)

                if instruction_zfilled[0] == '0':
                    self.intcode[self.intcode[self.cur_index + 1]] = value
                elif instruction_zfilled[0] == '1':
                    self.intcode[self.cur_index + 1] = value
                else:
                    raise NotImplementedError(
                        f'Instruction not implemented, {instruction}'
                    )
                self.cur_index += 2

            elif str(instruction).endswith('4'):
                instruction_zfilled = str(instruction).zfill(3)

                if instruction_zfilled[0] == '0':
                    value = self.intcode[self.intcode[self.cur_index + 1]]
                elif instruction_zfilled[0] == '1':
                    value = self.intcode[self.cur_index + 1]
                else:
                    raise NotImplementedError(
                        f'Instruction not implemented, {instruction}'
                    )
                if not(value == 0 and self.no_zero_output):
                    print(self.output_string.format(value))
                self.cur_index += 2

            elif str(instruction).endswith('5') or \
                    str(instruction).endswith('6') or \
                    str(instruction).endswith('7') or \
                    str(instruction).endswith('8'):
                instruction_zfilled = str(instruction).zfill(4)

                # Make sure nothing stange happens, e.g. input of 1012.
                if instruction_zfilled[-2] != '0':
                    raise NotImplementedError(
                        f'Instruction not implemented, {instruction}'
                    )

                last_digit = int(instruction_zfilled[-1])

                # Remove last two digits and reverse
                instruction_short = instruction_zfilled[:2:][::-1]

                if instruction_zfilled[0] == '0':
                    value = self.intcode[self.intcode[self.cur_index + 1]]
                elif instruction_zfilled[0] == '1':
                    value = self.intcode[self.cur_index + 1]

                # First value
                if instruction_short[0] == '0':
                    value_first = self.intcode[
                        self.intcode[self.cur_index + 1]
                    ]
                elif instruction_short[0] == '1':
                    value_first = self.intcode[self.cur_index + 1]
                else:
                    raise NotImplementedError(
                        f'Instruction not implemented, {instruction}'
                    )

                # Second value
                if instruction_short[1] == '0':
                    value_second = self.intcode[
                        self.intcode[self.cur_index + 2]
                    ]
                elif instruction_short[1] == '1':
                    value_second = self.intcode[self.cur_index + 2]
                else:
                    raise NotImplementedError(
                        f'Instruction not implemented, {instruction}'
                    )

                # Third value (for 7 and 8 instructions)
                value_third = self.intcode[self.cur_index + 3]

                if last_digit == 5:
                    if value_first != 0:
                        self.intcode[self.cur_index] = value_second
                        self.cur_index = self.intcode[self.cur_index]
                    else:
                        self.cur_index += 3
                elif last_digit == 6:
                    if value_first == 0:
                        self.intcode[self.cur_index] = value_second
                        self.cur_index = self.intcode[self.cur_index]
                    else:
                        self.cur_index += 3
                elif last_digit == 7:
                    if value_first < value_second:
                        self.intcode[value_third] = 1
                    else:
                        self.intcode[value_third] = 0
                    self.cur_index += 4
                elif last_digit == 8:
                    if value_first == value_second:
                        self.intcode[value_third] = 1
                    else:
                        self.intcode[value_third] = 0
                    self.cur_index += 4
                else:
                    # Should never happen
                    raise NotImplementedError(
                        f'Instruction not implemented, {instruction}'
                    )

            elif instruction in [99]:
                self.finished = True
                return self.intcode

            else:
                raise NotImplementedError(
                    'Instruction not understood,', instruction
                )


def read_input(path='data.txt'):
    with open(path, 'r') as infile:
        intcode = infile.read()
    intcode = intcode.split(',')
    intcode = [int(number) for number in intcode]
    return intcode


def test_apply_operations():
    '''Apply tests from day 2.'''
    examples_and_solutions = [
        [[1, 0, 0, 0, 99], [2, 0, 0, 0, 99]],
        [[2, 3, 0, 3, 99], [2, 3, 0, 6, 99]],
        [[2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]],
        [[1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]],
        [
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
        ]
    ]
    for example, solution in examples_and_solutions:
        computer = Computer(example)
        result = computer.operate()
        assert result == solution


def test_apply_operations_improved():
    '''Apply test given from day 5.'''
    computer = Computer([1002, 4, 3, 4, 33])
    result = computer.operate()
    assert result == [1002, 4, 3, 4, 99]


def test_apply_operations_improved_part_two():
    '''Apply test given from day 5, part 2.'''
    computer = Computer([
        3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
        1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
        999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
    ])
    computer.operate()


if __name__ == '__main__':
    test_apply_operations()
    test_apply_operations_improved()

    # Comment out the next line to run the test
    # test_apply_operations_improved_part_two()

    intcode = read_input()

    # Part 1
    computer = Computer(
        intcode[:],
        # Additional flags for same output as the other days
        lazy_input=2,
        no_zero_output=True,
        output_string='Solution part 1: {}'
    )
    computer.operate()

    # Part 2
    computer = Computer(
        intcode[:],
        # Additional flags for same output as the other days
        lazy_input=5,
        no_zero_output=True,
        output_string='Solution part 2: {}'
    )
    computer.operate()
