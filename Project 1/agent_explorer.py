


'''
class state:
position = (,)
actions = up, down, left, right, scan
is_victim = False

========================

class AgentExplorer:
position
actions_left = 400
dist_to_base

========================

class persistent:

previous_state = None
preivous_ation = None
result
untried
unbacktracked

========================
base_map = environment.get_map
current_state = new state(base_map.get_base())

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


'''