from turtle import st


class State:
    def __init__(self, position, tile_type):
        self.position = position
        self.name = str(position[0]) + ',' + str(position[1])
        self.actions = ['up', 'right', 'down', 'left']
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
        self.action_points = environment.get_te()
        self.distance_from_base = 0
        self.goal = goal
        self.persistent = Persistent()
    
    def set_current_state(self, state_position, tile_type):
        self.current_state = State(state_position, tile_type)

    def update_current_state(self, state_position, tile_type):
        if tile_type == '#':
            self.persistent.add_final_state(state_position, '#')
        else:
            self.current_state = State(state_position, tile_type)
    
    # TODO
    def get_distance_from_base(self):
        # use current_state and start_state
        return 0
    
    def online_dfs_agent(self, state_position, tile_type):
        action = ''
        state_name = self.persistent.get_name_from_position(state_position)

        if state_position == self.goal:
            return 'end'
        
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
        

    def explore(self):
        action = ''

        count = 0
        
        while action != 'end':
            state_position = self.current_state.position
            tile_type = self.current_state.type
            action = self.online_dfs_agent(state_position, tile_type)
            
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


        final_map = self.persistent.get_final_map()
        for tile in final_map:
            print(str(tile.position) + '   ' + str(tile.type))

'''
========================

while not goal:
    get_distance_to_base
    if distance = agent_actions_left:
        go_back_to_base

    if current_state is victim:
        agent.scan

    action = online_dfs(current_state)

    ' for each direction
    if action = up:
        base_map.whats_up(state) (write this function in the enviroment class)
        if not possible (wall):
            agent.stay
            all_states.append(wall)
        else:
            agent.go_up
            change current_state
            all_states.append(new_state)

the final map should be translated to the normal coordinate systems (>0, >0)


'''