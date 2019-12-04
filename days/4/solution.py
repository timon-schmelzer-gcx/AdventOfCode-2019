from collections import Counter


def check_for_validity(number):
    digits = str(number)

    adjacent_counter = 0
    last_digit = digits[0]
    for digit in digits[1:]:
        if digit < last_digit:
            return False

        if digit == last_digit:
            adjacent_counter += 1

        last_digit = digit

    return adjacent_counter > 0


def check_for_validity_part_two(number):
    digits = str(number)

    digit_counts = Counter(digits)

    if 2 not in digit_counts.values():
        return False

    return check_for_validity(number)


def check_range(min_code, max_code, part=1):
    total_passwords = 0
    for code in range(min_code, max_code + 1):
        if part == 1:
            if check_for_validity(code):
                total_passwords += 1
        elif part == 2:
            if check_for_validity_part_two(code):
                total_passwords += 1
        else:
            raise NotImplementedError('Part not implemented.')
    return total_passwords


def test_check_for_validity():
    assert check_for_validity(111111) is True
    assert check_for_validity(111123) is True
    assert check_for_validity(122345) is True
    assert check_for_validity(223450) is False
    assert check_for_validity(123789) is False


def test_check_for_validity_part_two():
    assert check_for_validity_part_two(112233) is True
    assert check_for_validity_part_two(123444) is False
    assert check_for_validity_part_two(111122) is True


if __name__ == "__main__":
    test_check_for_validity()
    test_check_for_validity_part_two()

    check_for_validity_part_two(112455)
    total_passwords = check_range(137683, 596253)

    print('Solution part 1:', total_passwords)

    total_passwords_part_two = check_range(137683, 596253, part=2)

    print('Solution part 2:', total_passwords_part_two)
