from environment import Environment
from file_reader import FileReader
from a_star import AStar
from agent_explorer import AgentExplorer

def main():
    reader = FileReader()
    environment = Environment(reader.get_environment_data(), reader.get_vital_signs_data())
    environment.print_map()
    
    explorer = AgentExplorer(environment, (3, 3))
    explorer.explore()
    new_map = explorer.build_explored_map()

    exp_environment = Environment(new_map, None)
    exp_environment.print_map()

    print(explorer.victims)

if __name__ == "__main__":
    main()