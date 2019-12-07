from collections import defaultdict


class Universe:

    def __init__(self):
        self.graph = defaultdict(set)
        self.planets = set()

    def add_connection(self, orbit):
        planet_one, planet_two = orbit.split(')')[::-1]
        self.graph[planet_one].add(planet_two)

        self.register_planet(planet_one)
        self.register_planet(planet_two)

    def register_planet(self, planet):
        self.planets.add(planet)

    def add_connections(self, orbits):
        for orbit in orbits:
            self.add_connection(orbit)

    def get_planets_list(self):
        return sorted(list(self.planets))

    def get_number_of_orbits(self):
        number_of_orbits = 0

        for planet in self.planets:
            sinle_path_length, _ = self.move_orbits_up(planet)
            number_of_orbits += sinle_path_length

        return number_of_orbits

    def move_orbits_up(self, planet, path=None, number_of_moves=0):
        if path is None:
            path = []
        if planet in self.graph.keys():
            next_planet = next(iter(self.graph[planet]))
            path.append(next_planet)
            return self.move_orbits_up(
                next_planet, path, number_of_moves + 1
            )
        else:
            return number_of_moves, path

    def find_matching_planet(self, path_you, path_san):
        last_planet = path_you[-1]
        for planet_you, planet_san in zip(
            path_you[::-1], path_san[::-1]
        ):
            if planet_you == planet_san:
                last_planet = planet_you
            else:
                break

        return last_planet

    def steps_to_santa(self):
        _, you_path = self.move_orbits_up('YOU')
        _, san_path = self.move_orbits_up('SAN')

        matching_planet = self.find_matching_planet(you_path, san_path)

        steps_you = you_path.index(matching_planet)
        steps_san = san_path.index(matching_planet)

        return steps_you + steps_san


def read_input(path='days/6/data.txt'):
    with open(path, 'r') as infile:
        planet_map = infile.read()
    planet_map = planet_map.split()
    return planet_map


def test_orbits():
    planet_map = [
        'COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H',
        'D)I', 'E)J', 'J)K', 'K)L'
    ]
    universe = Universe()
    universe.add_connections(planet_map)

    assert universe.get_number_of_orbits() == 42


def test_orbits_part_two():
    planet_map_part_two = [
        'COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J',
        'J)K', 'K)L', 'K)YOU', 'I)SAN'
    ]

    universe_part_two = Universe()
    universe_part_two.add_connections(planet_map_part_two)

    assert universe_part_two.steps_to_santa() == 4


if __name__ == "__main__":
    test_orbits()

    planet_map = read_input()

    universe = Universe()
    universe.add_connections(planet_map)

    print('Solution part 1:', universe.get_number_of_orbits())
    print('Solution part 2:', universe.steps_to_santa())
