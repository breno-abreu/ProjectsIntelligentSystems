from environment import Environment
from file_reader import FileReader
from a_star import AStar
from agent_explorer import AgentExplorer

def main():
    reader = FileReader()
    environment = Environment(reader.get_environment_data(), reader.get_vital_signs_data())
    environment.print_map()
    
    explorer = AgentExplorer(environment, (10, 9))
    explorer.explore()
    

if __name__ == "__main__":
    main()