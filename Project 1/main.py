from agent_rescuer import AgentRescuer
from environment import Environment
from file_reader import FileReader
from a_star import AStar
from agent_explorer import AgentExplorer

def main():
    
    print('[STRART]')
    print('[LOADING] Carregando arquivos básicos')

    reader = FileReader()

    print('[LOADING] Carregando ambiente base')

    environment = Environment(reader.get_environment_data(), reader.get_vital_signs_data())

    print('[PRINTING] Desenhando mapa base')

    environment.print_map()

    print('[DATA] Carregando dados sobre as vítimas do mapa base')

    n_victims = environment.get_total_nof_victims()
    weighted_cost = environment.get_weighted_victim_cost()

    print('[LOADING] Carregando agente explorador')

    explorer = AgentExplorer(environment, (3, 3))

    print('[EXPLORING] Explorando mapa')

    explorer.explore()

    print('[BUILDING] Construindo mapa explorado')

    new_map = explorer.build_explored_map()

    print('[PRINTING] Desenhando mapa explorado')

    exp_environment = Environment(new_map, None)
    exp_environment.print_map()

    print('[DATA] Carregando dados sobre as vítimas do mapa explorado')

    victims = explorer.get_victims()
    exp_n_victims = explorer.get_n_victims()
    exp_weighted_cost = explorer.get_weighted_victim_cost()
    exp_points_used = explorer.get_points_used()

    pve = exp_n_victims / n_victims
    tev = exp_points_used / exp_n_victims
    veg = exp_weighted_cost / weighted_cost

    print('[LOADING] Carregando agente socorrista')
    
    rescuer = AgentRescuer(exp_environment,victims, 12, 200, environment.get_ts())

    print('[RESCUING] Encontrando melhor caminho para resgatar as vítimas')

    best_individual = rescuer.run()

    print('[DATA] Imprimindo dados sobre o melhor indivíduo encontrado no algoritmo genético\n')

    print(best_individual)

    print('\n[DATA] Carregando dados sobre as vítimas salvas')

    res_n_victims = rescuer.get_n_victims()
    res_weighted_cost = rescuer.get_weighted_victim_cost()
    res_points_used = rescuer.get_points_used()

    pvs = res_n_victims / n_victims
    tvs = res_points_used / exp_n_victims
    vsg = res_weighted_cost / weighted_cost

    print('\n\n--------Desempenho--------\n')
    print('[DATA] Desempenho do agente explorador')
    print('pve: ' + str(pve))
    print('tev: ' + str(tev))
    print('veg: ' + str(veg))
    print('\n[DATA] Desempenho do agente socorrista')
    print('pvs: ' + str(pvs))
    print('tvs: ' + str(tvs))
    print('vsg: ' + str(vsg))
    print('\n')
    

if __name__ == "__main__":
    main()