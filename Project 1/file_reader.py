class FileReader:
    def __init__(self):
        self.ambiente_path = "Resources\\ambiente.txt"
        self.sinais_vitais_path = "Resources\\sinais_vitais.txt"
    
    def get_environment_data(self):

        file = open(self.ambiente_path, 'r')
        lines = file.readlines()
        line_number = 1
        dictionary = {}
        for line in lines:
            if line_number < 6 and line_number != 3:
                line_split_ws = line.split()
                dictionary[line_split_ws[0]] = int(line_split_ws[1])
            elif line_number == 3:
                line_split_ws = line.split()
                line_split_comma = line_split_ws[1].split(',')
                line_split_comma[0] = int(line_split_comma[0])
                line_split_comma[1] = int(line_split_comma[1])
                dictionary[line_split_ws[0]] = line_split_comma
            else:
                line_split_ws = line.split()
                positions = []
                for i in range(1, len(line_split_ws)):
                    line_split_comma = line_split_ws[i].split(',')
                    line_split_comma[0] = int(line_split_comma[0])
                    line_split_comma[1] = int(line_split_comma[1])
                    positions.append(line_split_comma)
                dictionary[line_split_ws[0]] = positions

            line_number += 1
            
        file.close()
        return dictionary

    def get_vital_signs_data(self):
        file = open(self.sinais_vitais_path, 'r')
        lines = file.readlines()
        line_number = 1
        count = 0
        dictionary = {}
        for line in lines:
            line_split_comma = line.split(',')
            data = []
            for i in range(1, len(line_split_comma)):
                data.append(float(line_split_comma[i]))
            
            if len(data) != 0:
                if data[5] <= 25:
                    data.append(1)
                elif data[5] <= 50:
                    data.append(2)
                elif data[5] <= 75:
                    data.append(3)
                else:
                    data.append(4)
                
                dictionary[line_split_comma[0]] = {'data' : data}
            
        return dictionary
