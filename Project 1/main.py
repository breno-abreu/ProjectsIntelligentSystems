from environment import Environment
from file_reader import FileReader

def main():
    reader = FileReader()
    environment = Environment(reader.get_environment_data(), reader.get_vital_signs_data())
    environment.print_map()

if __name__ == "__main__":
    main()