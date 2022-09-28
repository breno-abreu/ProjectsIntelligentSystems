class Environment:
    def __init__(self, enviroment_data, vital_signs_data):
        self.enviroment_data = enviroment_data
        self.vital_signs_data = vital_signs_data
        self.victim_data = self.get_victim_data()
        self.env_map = self.build_map()
    
    def get_map(self):
        return self.env_map

    def print_victim_data(self):
        for key in self.victim_data:
            data = ""
            for i in range(len(self.victim_data[key])):
                data += "   " + str(self.victim_data[key][i])
            print(key + ":" + data)
    
    def build_map(self):
        env_map = []
        x_pos = 0
        y_pos = 0
        for y in range(self.enviroment_data["YMax"]):
            row = []
            for _ in range(self.enviroment_data["XMax"]):
               row.append('.')

            for x in range(self.enviroment_data["XMax"]):
                
                if (self.enviroment_data["Base"][0] == x and 
                    self.enviroment_data["Base"][1] == y):
                    row[x] = "B"

            for x in range(self.enviroment_data["XMax"]):
                for i in range(len(self.enviroment_data["Parede"])):
                
                    if (self.enviroment_data["Parede"][i][0] == x and 
                        self.enviroment_data["Parede"][i][1] == y):
                        row[x] = "#"


            for x in range(self.enviroment_data["XMax"]):
                for i in range(len(self.enviroment_data["Vitimas"])):
                
                    if (self.enviroment_data["Vitimas"][i][0] == x and 
                        self.enviroment_data["Vitimas"][i][1] == y):
                        row[x] = "V"

            env_map.append(row)
        
        return env_map

    def print_map(self):
        print('\n\t', end="  ")
        for i in range(len(self.env_map[0])):
            print(" " + str(i % 10), end="   ")
        print('\n')

        for i in range(len(self.env_map)):
            print(str(i) + '\t| ', end=" ")
            for j in range(len(self.env_map[i])):
                if self.env_map[i][j] == 'B':
                    print('\033[94m' + self.env_map[i][j] + '\033[0m', end="    ")
                elif self.env_map[i][j] == "#":
                    print('\033[92m' + self.env_map[i][j] + '\033[0m', end="    ")
                elif self.env_map[i][j] == "V":
                    print('\033[91m' + self.env_map[i][j] + '\033[0m', end="    ")
                else:
                    print('\033[0m' + self.env_map[i][j] + '\033[0m', end="    ")
            print('\n')
    
    def print_map_with_path(self, path):
        print('\n\t', end="  ")
        for i in range(len(self.env_map[0])):
            print(" " + str(i % 10), end="   ")
        print('\n')

        for i in range(len(self.env_map)):
            print(str(i) + '\t| ', end=" ")
            for j in range(len(self.env_map[i])):
                is_path = False

                for position in path:
                    if position[0] == j and position[1] == i:
                        print('\033[94m' + '+' + '\033[0m', end="    ")
                        is_path = True

                if is_path == False:
                    if self.env_map[i][j] == 'B':
                        print('\033[94m' + self.env_map[i][j] + '\033[0m', end="    ")
                    elif self.env_map[i][j] == "#":
                        print('\033[92m' + self.env_map[i][j] + '\033[0m', end="    ")
                    elif self.env_map[i][j] == "V":
                        print('\033[91m' + self.env_map[i][j] + '\033[0m', end="    ")
                    else:
                        print('\033[0m' + self.env_map[i][j] + '\033[0m', end="    ")

            print('\n')
                
    
    def get_victim_data(self):
        i = 0
        dictionary = {}
        for key in self.vital_signs_data:
            dictionary[key] = self.vital_signs_data[key]
            dictionary[key].append(self.enviroment_data["Vitimas"][i][0])
            dictionary[key].append(self.enviroment_data["Vitimas"][i][1])
            i += 1
        
        return dictionary