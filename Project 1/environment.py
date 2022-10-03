class Environment:
    def __init__(self, enviroment_data, vital_signs_data):
        self.enviroment_data = enviroment_data
        self.vital_signs_data = vital_signs_data
        self.victim_data = self.get_victim_data()
        self.env_map = self.build_map()

    def get_total_nof_victims(self):
        return len(self.victim_data)
    
    def get_weighted_victim_cost(self):
        v1 = 0
        v2 = 0
        v3 = 0
        v4 = 0
        for key in self.victim_data:
            if self.victim_data[key]['class'] == 1:
                v1 += 1
            elif self.victim_data[key]['class'] == 2:
                v2 += 1
            elif self.victim_data[key]['class'] == 3:
                v3 += 1
            elif self.victim_data[key]['class'] == 4:
                v4 += 1

        return 4 * v1 + 3 * v2 + 2 * v2 + v4
    
    def get_map(self):
        return self.env_map
    
    def get_te(self):
        return self.enviroment_data["Te"]
    
    def get_ts(self):
        return self.enviroment_data["Ts"]

    def print_victim_data(self):
        for key in self.victim_data:
            data = ""
            for i in range(len(self.victim_data[key])):
                data += "   " + str(self.victim_data[key][i])
            print(key + ":" + data)
    
    def build_map(self):
        env_map = []
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
        if self.vital_signs_data != None:
            i = 0
            dictionary = self.vital_signs_data
            for key in self.vital_signs_data:
                self.vital_signs_data[key]['class'] = self.vital_signs_data[key]['data'][6]
                self.vital_signs_data[key]['position_name'] = str(self.enviroment_data["Vitimas"][i][0]) + ',' + str(self.enviroment_data["Vitimas"][i][1])
                i += 1
            
            return dictionary
        return None
    
    def get_state(self, position):
        if (position[0] < 0 or position[1] < 0 or
            position[0] > self.enviroment_data["XMax"] - 1 or 
            position[1] > self.enviroment_data["YMax"] - 1): 
            return '#'

        else:
            for y in range(len(self.env_map)):
                for x in range(len(self.env_map[y])):
                    if x == position[0] and y == position[1]:
                        return self.env_map[y][x]
    
    def get_base_position(self):
        for y in range(len(self.env_map)):
            for x in range(len(self.env_map[y])):
                if self.env_map[y][x] == 'B':
                    return (x, y)
