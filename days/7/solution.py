from operator import add, mul
from itertools import permutations


class Computer():

    OPERATIONS = {
        1: add,
        2: mul
    }

    def __init__(self, intcode, input_codes):
        self.intcode = intcode[:]
        self.cur_index = 0
        self.finished = False

        if len(input_codes) != 5:
            raise AttributeError('Input codes must have length of five.')
        self.input_codes = input_codes
        self.second_inputs = [0] + [None]*5

    def rerun(self):
        for iteration in range(5):
            self.finished = False
            self.cur_index = 0
            output = self.operate(iteration)
        return output

    def operate(self, iteration):
        ith_input_iteration = 0
        while(self.finished is not True):
            instruction = self.intcode[self.cur_index]
            # print('iteration is:', iteration)
            # print('instruction is:', instruction)
            # print('index is:', self.cur_index)
            # print(self.intcode)

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
                if ith_input_iteration == 0:
                    value = self.input_codes[iteration]
                elif ith_input_iteration == 1:
                    value = self.second_inputs[iteration]
                else:
                    raise ValueError(
                        'ith_input_iteration too high:', ith_input_iteration
                    )
                ith_input_iteration += 1
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

                self.second_inputs[iteration + 1] = value
                if iteration == 4:
                    # print('Output:', value)
                    return value
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

            elif instruction == 99:
                iteration += 1
                ith_input_iteration = 0
                self.finished = True

            else:
                raise NotImplementedError(
                    'Instruction not understood,', instruction
                )


def read_input(path='days/7/data.txt'):
    with open(path, 'r') as infile:
        intcode = infile.read()
    intcode = intcode.split(',')
    intcode = [int(number) for number in intcode]
    return intcode


def test_computer():
    # Format: [(intcode, input, max_signal),...]
    examples_and_solutions = [
        (
            [
                3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0
            ], (4, 3, 2, 1, 0), 43210
        ), (
            [
                3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
                101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0
            ], (0, 1, 2, 3, 4), 54321
        ), (
            [
                3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0,
                33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99,
                0, 0, 0
            ], (1, 0, 4, 3, 2), 65210
        )
    ]
    for intcode, input_, max_signal in examples_and_solutions:
        max_signal, best_config = get_max_signal(intcode)

        assert input_ == best_config
        assert max_signal == max_signal


def get_max_signal(intcode):
    all_configurations = permutations(range(5))
    calculated_max_signal = 0
    calculated_best_config = 0

    for configuration in all_configurations:
        computer = Computer(intcode, input_codes=configuration)
        cur_signal = computer.rerun()

        if cur_signal > calculated_max_signal:
            calculated_max_signal = cur_signal
            calculated_best_config = configuration

    return calculated_max_signal, calculated_best_config


if __name__ == "__main__":
    test_computer()

    intcode = read_input()

    print('No solution yet :(')

    # Does not work yet!
    # max_signal, _ = get_max_signal(intcode)

    # print('Solution part 1:', max_signal)
