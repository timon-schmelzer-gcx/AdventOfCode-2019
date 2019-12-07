from math import floor


def calculate_fuel(module_mass):
    required_fuel = floor(module_mass / 3) - 2
    return max(required_fuel, 0)


def calculate_fuel_recursive(module_mass):
    total_fuel = 0
    new_fuel = calculate_fuel(module_mass)

    while(new_fuel) > 0:
        total_fuel += new_fuel
        new_fuel = calculate_fuel(new_fuel)

    return total_fuel


def test_calculate_fuel():
    assert calculate_fuel(12) == 2
    assert calculate_fuel(14) == 2
    assert calculate_fuel(1969) == 654
    assert calculate_fuel(100756) == 33583


def test_calculate_fuel_recursive():
    assert calculate_fuel_recursive(14) == 2
    assert calculate_fuel_recursive(1969) == 966
    assert calculate_fuel_recursive(100756) == 50346


if __name__ == '__main__':
    test_calculate_fuel()
    test_calculate_fuel_recursive()

    total_fuel = 0
    total_fuel_recursive = 0

    with open('days/1/data.txt', 'r') as infile:
        for line in infile.readlines():
            module_mass = int(line)
            total_fuel += calculate_fuel(module_mass)
            total_fuel_recursive += calculate_fuel_recursive(module_mass)

    print('Solution part 1:', int(total_fuel))
    print('Solution part 2:', int(total_fuel_recursive))
