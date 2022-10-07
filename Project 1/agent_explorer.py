from a_star import AStar
from environment import Environment


class State:
    def __init__(self, position, tile_type):
        self.position = [position[0], position[1]]
        self.name = str(position[0]) + ',' + str(position[1])
        self.actions = ['right', 'down', 'up', 'left']
        self.type = tile_type

class Persistent:
    def __init__(self):
        self.previous_state = None
        self.previous_action = None
        self.results = {}
        self.untried = {}
        self.unbacktracked = {}
        self.explored_states = []
        self.seen_results = []
    
    def get_name_from_position(self, position):
        return str(position[0]) + "," + str(position[1])
    
    def add_final_state(self, state_position, tile_type):
        state = State(state_position, tile_type)
        self.explored_states.append(state)
    
    def add_result(self, before_state, action, after_state):
        before_state_name = self.get_name_from_position(before_state)
        name = str(before_state_name) + "," + str(action)
        self.results[name] = after_state
    
    def add_untried(self, state_position, tile_type):
        state = State(state_position, tile_type)
        self.untried[state.name] = state
    
    def get_next_action(self, state_name):
        action = self.untried[state_name].actions.pop(0)
        return action
    
    def is_in_untried(self, state_name):
        return state_name in self.untried
    
    def get_state(self, state_name):
        return self.untried[state_name]
    
    def get_untried(self, state_name):
        return self.untried[state_name].pop(0)

    def get_final_map(self):
        return self.explored_states
    
    def remove_action(self, state_name, action):
        self.untried[state_name].remove(action)
    
    def is_untried_empty(self, state_name):
        if len(self.untried[state_name].actions) > 0:
            return False
        else:
            return True 

    def add_unbacktracked(self, current_state_name, previous_state, previous_action):
        previous_state_name = self.get_name_from_position(previous_state)
        result_name = previous_state_name + ',' + previous_action + ',' + current_state_name
        if current_state_name != previous_state_name and not result_name in self.seen_results:
            if not current_state_name in self.unbacktracked:
                self.unbacktracked[current_state_name] = []
                self.unbacktracked[current_state_name].append(previous_state)
            else:
                self.unbacktracked[current_state_name].insert(0, previous_state)
    
    def is_unbacktracked_empty(self, state_name):
        if state_name in self.unbacktracked:
            if len(self.unbacktracked[state_name]) > 0:
                return False
            else:
                return True
        else:
            return True
    
    def get_unbacktracked_state(self, state_name):
        return self.unbacktracked[state_name].pop(0)
    
    def get_unbacktracked_action(self, state_name):
        unbactracked_state = self.get_unbacktracked_state(state_name)
        unbacktracked_state_name = self.get_name_from_position(unbactracked_state)
        actions = ['up', 'right', 'down', 'left']
        for action in actions:
            result_name = str(state_name) + "," + str(action)
            if result_name in self.results:
                if self.results[result_name] == unbactracked_state:
                    result_name = result_name + ',' + unbacktracked_state_name
                    self.seen_results.append(result_name)
                    return action


class AgentExplorer:
    def __init__(self, environment, goal):
        self.environment = environment
        self.base_map = environment.get_map()
        self.start_state = State(environment.get_base_position(), 'B')
        self.current_state = self.start_state
        self.original_action_points = environment.get_te()
        self.action_points = environment.get_te()
        self.distance_from_base = 0
        self.goal = goal
        self.persistent = Persistent()
        self.map_temp = None
        self.victims = []
        #self.persistent.add_final_state(environment.get_base_position(), 'B')
    
    def get_points_used(self):
        return self.original_action_points - self.action_points

    def get_n_victims(self):
        return len(self.victims)
    
    def get_weighted_victim_cost(self):
        v = [0, 0, 0, 0]

        for victim in self.victims:
            if victim['class'] == 1:
                v[0] += 1
            elif victim['class'] == 2:
                v[1] += 1
            elif victim['class'] == 3:
                v[2] += 1
            elif victim['class'] == 4:
                v[3] += 1

        return 4 * v[0] + 3 * v[1] + 2 * v[2] + v[3]

    def get_env_map(self):
        return self.environment.env_map

    def get_victims(self):
        return self.victims

    def set_current_state(self, state_position, tile_type):
        self.current_state = State(state_position, tile_type)

    def update_current_state(self, state_position, tile_type):
        if tile_type == '#':
            self.persistent.add_final_state(state_position, '#')
        else:
            self.current_state = State(state_position, tile_type)
        
        self.action_points -= 1
    
    def print_final_map(self):
        for element in self.persistent.get_final_map():
            print(str(element.position) + '   ' + element.type)

    def build_explored_map(self):
        final_map_org = self.persistent.get_final_map()
        final_map = []

        for element in final_map_org:
            final_map.append(State(element.position, element.type))

        for element in final_map:
            element.position[0] += 1
            element.position[1] += 1
        
        x_max = -1

        for element in final_map:
            if element.position[0] > x_max:
                x_max = element.position[0]

        y_max = -1

        for element in final_map:
            if element.position[1] > y_max:
                y_max = element.position[1]

        map_dict = {"Te" : self.environment.get_te(), "Ts" : self.environment.get_ts(), "XMax" : x_max + 1, "YMax" : y_max + 1, "Base" : [], "Vitimas" : [], "Parede" : []}
        
        map_aux = []

        for y in range(y_max + 1):
            map_aux.append([])
            for x in range(x_max + 1):
                map_aux[y].append('#')
        
        for y in range(len(map_aux)):
            for x in range(len(map_aux[y])):
                for element in final_map:
                    if element.position[0] == x and element.position[1] == y:
                        map_aux[y][x] = element.type
        
        for y in range(len(map_aux)):
            for x in range(len(map_aux[y])):
                if map_aux[y][x] == 'B':
                    map_dict['Base'] = [x, y]
                elif map_aux[y][x] == 'V':
                    map_dict['Vitimas'].append([x, y])
                elif map_aux[y][x] == '#':
                    map_dict['Parede'].append([x, y])
        
        self.map_temp = map_aux
        return map_dict
    
    def online_dfs_agent(self, state_position, tile_type):
        action = ''
        state_name = self.persistent.get_name_from_position(state_position)

        '''if state_position[0] == self.goal[0] and state_position[1] == self.goal[1]:
            self.persistent.add_final_state(state_position, tile_type)
            return 'end' '''
        
        if not self.persistent.is_in_untried(state_name):
            self.persistent.add_untried(state_position, tile_type)
            self.persistent.add_final_state(state_position, tile_type)
        
        if self.persistent.previous_state != None:
            self.persistent.add_result(self.persistent.previous_state, 
                                       self.persistent.previous_action,
                                       state_position)
            self.persistent.add_unbacktracked(state_name, 
                                              self.persistent.previous_state, 
                                              self.persistent.previous_action)
        
        if self.persistent.is_untried_empty(state_name):
            if self.persistent.is_unbacktracked_empty(state_name):
                return 'end'
            else:
                action = self.persistent.get_unbacktracked_action(state_name)

        else:
            action = self.persistent.get_next_action(state_name)
        
        self.persistent.previous_state = state_position
        self.persistent.previous_action = action
        
        return action

    def get_path_to_base(self, base_position, agent_position):
        bx = base_position[0] + 1
        by = base_position[1] + 1

        ax = agent_position[0] + 1
        ay = agent_position[1] + 1

        environment = Environment(self.build_explored_map(), None)
        a_star = AStar(environment.env_map)
        path = a_star.run((bx, by), (ax, ay))
        return path
    
    def go_back_to_base(self, cost):
        self.action_points -= cost
        if self.action_points >= 0:
            self.current_state = self.start_state
            #print('Points left: ' + str(self.action_points))
            #print('Robot went back to the base!')
        else:
            print('[ERROR] Robot died in its way to the base :(')

    def scan_victim(self, position):
        vx = position[0] + 1
        vy = position[1] + 1
        state_name = self.persistent.get_name_from_position((vx, vy))
        original_state_name = self.persistent.get_name_from_position((vx - 1, vy - 1))
        if not self.in_victim_list(state_name):
            victim_id = self.get_victim_id(original_state_name)
            victim_data = self.environment.victim_data[victim_id]
            self.victims.append({'name' : state_name, 'position' : (vx, vy), 'class' : victim_data['class']})
            self.action_points -= 2
    
    def in_victim_list(self, state_name):
        for victim in self.victims:
            if victim['name'] == state_name:
                return True
        
        return False
    
    def get_victim_id(self, position_name):
        for victim_id in self.environment.victim_data:
            if self.environment.victim_data[victim_id]['position_name'] == position_name:
                return victim_id

    def explore(self):
        action = ''
        
        while action != 'end':
            state_position = self.current_state.position
            tile_type = self.current_state.type
            action = self.online_dfs_agent(state_position, tile_type)

            path_to_base = self.get_path_to_base(self.start_state.position, state_position)
            if self.action_points <= path_to_base['cost'] + 2 or action == 'end':
                action = 'end'
                self.go_back_to_base(path_to_base['cost'])

            
            if self.environment.get_state(state_position) == 'V':
                self.scan_victim(state_position)


            if action == 'up':
                new_tile_type = self.environment.get_state((state_position[0], state_position[1] - 1))
                self.update_current_state((state_position[0], state_position[1] - 1), new_tile_type)

            elif action == 'right':
                new_tile_type = self.environment.get_state((state_position[0] + 1, state_position[1]))
                self.update_current_state((state_position[0] + 1, state_position[1]), new_tile_type)

            elif action == 'down':
                new_tile_type = self.environment.get_state((state_position[0], state_position[1] + 1))
                self.update_current_state((state_position[0], state_position[1] + 1), new_tile_type)

            elif action == 'left':
                new_tile_type = self.environment.get_state((state_position[0] - 1, state_position[1]))
                self.update_current_state((state_position[0] - 1, state_position[1]), new_tile_type)