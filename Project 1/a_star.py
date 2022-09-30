import math

class ANode:
        def __init__(self, x_pos, y_pos, is_base, is_victim):
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.name = str(x_pos) + "," + str(y_pos)
            self.h_value = 0
            self.g_value = math.inf
            self.f_value = 0
            self.cost = 0
            self.parent = None
            self.neighbors = []
            self.is_base = is_base
            self.is_victim = is_victim
        
        def __str__(self):
            if self.parent == None:
                return "{name} [h:{h} g:{g} f:{f} parent:{parent}]".format(name=self.name, h=self.h_value, g=self.g_value, f=self.f_value, parent="None")
            else:
                return "{name} [h:{h} g:{g} f:{f} parent:{parent}]".format(name=self.name, h=self.h_value, g=self.g_value, f=self.f_value, parent=self.parent.name)

class AStar:

    def __init__(self, env_map):
        self.env_map = env_map
        self.nodes = self.initialize_nodes()
    
    def get_node_list(self):
        return self.nodes

    def initialize_nodes(self):
        nodes = {}
        for y in range(len(self.env_map)):
            for x in range(len(self.env_map[y])):
                node_name = str(x) + "," + str(y)
                
                if self.env_map[y][x] != '#':
                    if self.env_map[y][x] == 'B':
                        new_node = ANode(x, y, True, False)
                    elif self.env_map[y][x] == 'V':
                        new_node = ANode(x, y, False, True)
                    elif self.env_map[y][x] == '.':
                        new_node = ANode(x, y, False, False)
                    
                    nodes[node_name] = new_node
        
        return nodes

    def euclidian_distance(self, node, goal):
        return math.sqrt(math.pow((node[0] - goal[0]), 2) + math.pow((node[1] - goal[1]),2))
    
    def calculate_heuristics(self, goal):
        for key in self.nodes:
            self.nodes[key].h_value = self.euclidian_distance((self.nodes[key].x_pos, self.nodes[key].y_pos), goal)
    
    def get_node(self, pos):
        for key in self.nodes:
            if self.nodes[key].x_pos == pos[0] and self.nodes[key].y_pos == pos[1]:
                return self.nodes[key]
        
        return None
    
    def get_best_node(self, border):
        lowest_score = 1000000
        best_node = None
        
        if border:
            for node in border:
                if node.f_value < lowest_score:
                    lowest_score = node.f_value
                    best_node = node
        
        return best_node
    
    def set_all_neighbors(self):
        for key in self.nodes:
            self.nodes[key].neighbors = self.get_neighbors((self.nodes[key].x_pos, self.nodes[key].y_pos))
    
    def get_neighbors(self, pos):
        neighbors = []

        # N
        neighbors.append({"node" : self.get_node((pos[0], pos[1] - 1)), "cost" : 1})

        # NE
        if self.get_node((pos[0], pos[1] - 1)) != None and self.get_node((pos[0] + 1, pos[1])) != None:
            neighbors.append({"node" : self.get_node((pos[0] + 1, pos[1] - 1)), "cost" : 1.5})
        else:
            neighbors.append({"node" : None, "cost" : 0})

        # E
        neighbors.append({"node" : self.get_node((pos[0] + 1, pos[1])), "cost" : 1})

        # SE
        if self.get_node((pos[0], pos[1] + 1)) != None and self.get_node((pos[0] + 1, pos[1])) != None:
            neighbors.append({"node" : self.get_node((pos[0] + 1, pos[1] + 1)), "cost" : 1.5})
        else:
            neighbors.append({"node" : None, "cost" : 0})

        # S
        neighbors.append({"node" : self.get_node((pos[0], pos[1] + 1)), "cost" : 1})

        # SW
        if self.get_node((pos[0], pos[1] + 1)) != None and self.get_node((pos[0] - 1, pos[1])) != None:
            neighbors.append({"node" : self.get_node((pos[0] - 1, pos[1] + 1)), "cost" : 1.5}) 
        else:
            neighbors.append({"node" : None, "cost" : 0})

        # W
        neighbors.append({"node" : self.get_node((pos[0] - 1, pos[1])), "cost" : 1})

        # NW
        if self.get_node((pos[0], pos[1] - 1)) != None and self.get_node((pos[0] - 1, pos[1])) != None:
            neighbors.append({"node" : self.get_node((pos[0] - 1, pos[1] - 1)), "cost" : 1.5})
        else:
            neighbors.append({"node" : None, "cost" : 0})
        
        return neighbors

    def get_path(self, node):
        path = []
        current_node = node
        cost = 0

        while current_node != None:
            cost += current_node.cost
            path.append(current_node)
            current_node = current_node.parent

        return {'path' : path, 'cost' : cost}
    
    def get_path_only_positions(self, path):
        positions = []
        path = path['path']

        for node in path:
            positions.append([node.x_pos, node.y_pos])
        
        return positions
    
    def is_node_in_border(self, node, border):
        for item in border:
            if item.name == node.name:
                return True
        
        return False

    def run(self, start, goal):
        self.calculate_heuristics(goal)
        self.set_all_neighbors()

        start_node = self.get_node(start)
        start_node.f_value = start_node.h_value
        start_node.g_value = 0
        
        border = []
        border.append(start_node)

        while border:
            best_node = self.get_best_node(border)
            border.remove(best_node)

            if best_node.x_pos == goal[0] and best_node.y_pos == goal[1]:
                return self.get_path(best_node)
            
            for neighbor in best_node.neighbors:
                if neighbor['node'] != None:
                    score = best_node.g_value + neighbor['cost']
                    if score < neighbor['node'].g_value:
                        neighbor['node'].parent = best_node
                        neighbor['node'].g_value = score
                        neighbor['node'].cost = neighbor['cost']
                        neighbor['node'].f_value = score + neighbor['node'].f_value
                        if not self.is_node_in_border(neighbor['node'], border):
                            border.append(neighbor['node'])
        
        return None