class Environment:
    def __init__(self, enviroment_data, vital_signs_data):
        self.enviroment_data = enviroment_data
        self.vital_signs_data = vital_signs_data
        self.victim_data = self.get_victim_data()
        self.env_map = self.build_map()
    
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
        for i in range(self.enviroment_data["YMax"]):
            row = []
            for _ in range(self.enviroment_data["XMax"]):
               row.append('.')

            for x in range(self.enviroment_data["XMax"]):
                
                if (self.enviroment_data["Base"][0] == y_pos and 
                    self.enviroment_data["Base"][1] == x):
                    row[x] = "B"

            for x in range(self.enviroment_data["XMax"]):
                for j in range(len(self.enviroment_data["Parede"])):
                
                    if (self.enviroment_data["Parede"][j][0] == y_pos and 
                        self.enviroment_data["Parede"][j][1] == x):
                        row[x] = "#"


            for x in range(self.enviroment_data["XMax"]):
                for j in range(len(self.enviroment_data["Vitimas"])):
                
                    if (self.enviroment_data["Vitimas"][j][0] == y_pos and 
                        self.enviroment_data["Vitimas"][j][1] == x):
                        row[x] = "V"

            env_map.append(row)

            y_pos += 1
        
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
                
    
    def get_victim_data(self):
        i = 0
        dictionary = {}
        for key in self.vital_signs_data:
            dictionary[key] = self.vital_signs_data[key]
            dictionary[key].append(self.enviroment_data["Vitimas"][i][0])
            dictionary[key].append(self.enviroment_data["Vitimas"][i][1])
            i += 1
        
        return dictionary