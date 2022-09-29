class State:
    def __init__(self, x_pos, y_pos, is_victim):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.name = str(x_pos) + "," + str(y_pos)
        self.actions = ['up', 'down', 'left', 'right', 'scan']
        self.is_victim = is_victim

class Persistent:
    def __init__(self):
        self.previous_state = None
        self.previous_action = None
        self.results = {}
        self.untried = {}
        self.unbacktracked = {}
    
    def add_result(self, before_state, action, after_state):
        name = str(before_state) + "," + str(action)
        self.results[name] = after_state
    
    def add_untried(self, state, actions):
        self.untried[state] = actions
    
    def get_untried(self, state):
        return self.untried[state].pop()
    
    def remove_action(self, state, action):
        self.untried[state].remove(action)
    
    def is_untried_empty(self, state):
        return self.untried[state]

    def add_unbacktracked(self, current_state, previous_state):
        if not current_state in self.unbacktracked:
            self.unbacktracked[current_state] = []
            self.unbacktracked[current_state].append(previous_state)
        else:
            self.unbacktracked[current_state].append(0, previous_state)
    
    def is_unbacktracked_empty(self, state):
        return self.unbacktracked[state]
    
    def get_unbacktracked_state(self, state):
        return self.unbacktracked[state].pop()
    
    def get_unbacktracked_action(self, state):
        unbactracked_state = self.get_unbacktracked_state(state)
        actions = ['up', 'down', 'left', 'right']

        for action in actions:
            result_name = str(state) + "," + str(action)

            if result_name in self.results:
                if self.results[result_name] == unbactracked_state:
                    return action


class AgentExplorer:
    def __init__(self, base_map, start_state, action_points):
        self.base_map = base_map
        self.start_state = start_state
        self.current_state
        self.action_points = action_points
        self.distance_from_base = 0
    
    def update_state(self, current_state):
        self.current_state = current_state
    
    # TODO
    def get_distance_from_base(self):
        # use current_state and start_state
        return 0


'''
========================

class AgentExplorer:
position
actions_left = 400
dist_to_base

========================
base_map = environment.get_map
current_state = new state(base_map.get_base())

set goal

persistent.result.add_state(current_state)

all_states = new environment
all_states.append(current_state)

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