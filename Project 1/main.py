from environment import Environment
from file_reader import FileReader
from a_star import AStar

def main():
    reader = FileReader()
    environment = Environment(reader.get_environment_data(), reader.get_vital_signs_data())
    
    a_star = AStar(environment.get_map())
    a_star.run((0, 0), (10, 10))

if __name__ == "__main__":
    main()