import math

class ANode:
        def __init__(self, x_pos, y_pos, isBase, isVictim):
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.name = str(x_pos) + "," + str(y_pos)
            self.h_value = 0
            self.g_value = 0
            self.f_value = 0
            self.parent = None
            self.neighbors = None
            self.isBase = False
            self.isVictim = False
        
        def __str__(self):
            if self.parent == None:
                return "{name} [h:{h} g:{g} f:{f} parent:{parent}]".format(name=self.name, h=self.h_value, g=self.g_value, f=self.f_value, parent="None")
            else:
                return "{name} [h:{h} g:{g} f:{f} parent{parent}]".format(name=self.name, h=self.h_value, g=self.g_value, f=self.f_value, parent=self.parent.name)

class AStar:

    def __init__(self, env_map):
        self.env_map = env_map
        self.nodes = self.initialize_nodes()
    
    def get_nodes(self):
        return self.nodes

    def initialize_nodes(self):
        nodes = {}
        for y in range(len(self.env_map)):
            for x in range(len(self.env_map[y])):
                node_name = str(x) + "," + str(y)
                if self.env_map[x][y] != '#':
                    if self.env_map[x][y] == 'B':
                        new_node = ANode(x, y, True, False)
                    elif self.env_map[x][y] == 'V':
                        new_node = ANode(x, y, False, True)
                    elif self.env_map[x][y] == '.':
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

    def run(self, start, goal):
        self.calculate_heuristics(goal)

        start_node = self.get_node(start)
        start_node.f_value = start_node.h_value
        
        border = []
        border.append(start_node)

        while border:
            best_node = self.get_best_node(border)
            border.remove(best_node)

            if best_node.x_pos == goal[0] and best_node.y_pos == goal[1]:
                return best_node
            
            for neighbor in best_node.beighbors:
                

            


'''
Main (start, goal):
get list of all nodes (dict by pos x and y)
Calculate heuristics for each node, initializes g and f with 0

initializes first node with g = 0 and f = h

create list of border

add start node in border

while open is not empty
    gets node with lowest f
    if goal return path
    remove node from open

    get all neighbors add to lsit of neighbors in the class

    for each neighbor
        get neighbor cost
        if cost < neighbor(g)
            update values
            if neighbor not in open
                add to open

return None

----------

reconstruct path using the nodes parents


'''