from environment import Environment
from file_reader import FileReader
from a_star import AStar

def main():
    reader = FileReader()
    environment = Environment(reader.get_environment_data(), reader.get_vital_signs_data())

    environment.print_map()
    
    a_star = AStar(environment.get_map())
    path = a_star.run((0, 0), (4, 3))
    positions = a_star.get_path_only_positions(path['path'])

    environment.print_map_with_path(positions)
    print('cost: ' + str(path['cost']))

    print(positions)


if __name__ == "__main__":
    main()