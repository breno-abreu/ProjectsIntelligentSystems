import random
import copy
from a_star import AStar
from random import randint

class GeneticAlgorithm:
    def __init__(self, environment, victims, population_size, n_generations):
        self.environment = environment
        self.base_position = environment.get_base_position()
        self.base_name = str(self.base_position[0]) + ',' + str(self.base_position[1])
        self.env_map = environment.get_map()
        self.victims = victims
        self.individuals = []
        self.cost_table = None
        self.population_size = population_size
        self.n_generations = n_generations
        self.crossover_n_individuals = 6
    
    def run(self):
        self.build_cost_table()
        self.create_population()
        self.set_fitness()
        self.sort_population()
        
        for i in range(self.n_generations):
            #print('Generation: ' + str(i))
            self.set_roulette_values()
            cross_indexes = self.select_n_individuals(self.crossover_n_individuals)
            
            n_parents = len(self.individuals)
            for i in range(0, len(cross_indexes), 2):
                self.do_crossover(80, cross_indexes[i], cross_indexes[i + 1])
            n_total = len(self.individuals)

            for i in range(n_parents, n_total):
                self.do_mutation(5, i)
            
            self.set_fitness()
            self.sort_population()
            self.remove_individuals()
        
        return self.get_best_individual()
    

    def get_best_individual(self):
        return self.individuals.pop(0)

    def remove_individuals(self):
        while len(self.individuals) > self.population_size:
            del self.individuals[-1]

    def do_mutation(self, p_mut, index):
        for i in range(1, len(self.individuals[index]['victims']) - 1):
            value = randint(0, 100)
            if value <= p_mut:
                value = randint(1, len(self.individuals[index]['victims']) - 2)
                temp = self.individuals[index]['victims'][i]
                self.individuals[index]['victims'][i] = self.individuals[index]['victims'][value]
                self.individuals[index]['victims'][value] = temp

    def do_crossover(self, p_cross, index_a, index_b):
        
        value = randint(0, 100)
        descendent_a = copy.deepcopy(self.individuals[index_a])
        descendent_b = copy.deepcopy(self.individuals[index_b])
        if value <= p_cross:
            value = randint(2, len(descendent_a['victims']) - 3)
            for i in range(value):
                temp = descendent_a['victims'][i]
                descendent_a['victims'][i] = descendent_b['victims'][i]
                descendent_b['victims'][i] = temp

            while self.get_n_duplicates(descendent_a) != 0:
                self.fix_duplicates(descendent_a, value)
            
            while self.get_n_duplicates(descendent_b) != 0:
                self.fix_duplicates(descendent_b, value)

            self.individuals.append(descendent_a)
            self.individuals.append(descendent_b)

    def fix_duplicates(self, descendent, half_n):    
        
        for i in range(half_n, len(descendent['victims']) - 1):
            for j in range(1, len(descendent['victims']) - 1):
                if i != j:
                    if descendent['victims'][i]['name'] == descendent['victims'][j]['name']:
                        descendent['victims'][i] = self.get_random_victim()
                        return

    
    def get_random_victim(self):
        value = randint(0, len(self.victims) - 1)
        return self.victims[value]

    def get_n_duplicates(self, descendent):
        n_duplicates = 0
        for i in range(1, len(descendent['victims']) - 2):
            for j in range(i + 1, len(descendent['victims']) - 1):
                if i != j:
                    if descendent['victims'][i]['name'] == descendent['victims'][j]['name']:
                        n_duplicates += 1
        return n_duplicates

    def select_n_individuals(self, n_individuals):
        index_list = []

        for _ in range(n_individuals):
            index = self.select_individual()
            while True:
                if index in index_list:
                    index = self.select_individual()
                else:
                    index_list.append(index)
                    break
        
        return index_list

    def create_population(self):
        for _ in range(self.population_size):
            self.create_individual()

    def get_cost(self, victim_a, victim_b):
        return self.cost_table[victim_a][victim_b]
    
    def set_roulette_values(self):
        max_fitness = 0
        for individual in self.individuals:
            if individual['fitness'] > max_fitness:
                max_fitness = individual['fitness']

        max_fitness += 1
        for individual in self.individuals:
            individual['fitness_aux'] = max_fitness - individual['fitness']

        fitness_sum = 0
        for individual in self.individuals:
            fitness_sum += individual['fitness_aux']
        
        for individual in self.individuals:
            individual['probability'] = int((individual['fitness_aux'] / fitness_sum) * 100)

        last_value = 0
        for individual in self.individuals:
            individual['roulette_values'] = [last_value, individual['probability'] + last_value]
            last_value = individual['probability'] + last_value
    
    def select_individual(self):
        value = randint(1, self.individuals[-1]['roulette_values'][1])

        for i in range(len(self.individuals)):
            if value > self.individuals[i]['roulette_values'][0] and value <= self.individuals[i]['roulette_values'][1]:
                return i
        
        return None

    def create_individual(self):
        n_victims = len(self.victims)
        order = random.sample(range(n_victims), n_victims)
        victims_order = []

        for i in range(n_victims):
            victims_order.append(self.victims[order[i]])

        victims_order.insert(0, {'name' : self.base_name, 'position' : self.base_position , 'class' : -1})
        victims_order.append({'name' : self.base_name, 'position' : self.base_position , 'class' : -1})

        self.individuals.append({'victims' : victims_order, 'fitness' : 0, 'fitness_aux' : 0, 'probability': 0, 'roulette_values' : [0, 0]})

    def sort_population(self):
        self.individuals = sorted(self.individuals, key=lambda d: d['fitness']) 

    def set_fitness(self):
        for individual in self.individuals:
            cost = 0
            for i in range(1, len(individual['victims'])):
                cost += self.get_cost(individual['victims'][i]['name'], individual['victims'][i - 1]['name'])
            
            individual['fitness'] = cost

    def build_cost_table(self):
        victims_base = self.victims.copy()
        victims_base.insert(0, {'name' : self.base_name, 'position' : self.base_position , 'class' : -1})
        self.cost_table = {}
        for victim_a in victims_base:
            self.cost_table[victim_a['name']] = {}
            for victim_b in victims_base:
                if victim_a['name'] != victim_b['name']:
                    a_star = AStar(self.env_map)
                    path = a_star.run(victim_a['position'], victim_b['position'])
                    self.cost_table[victim_a['name']][victim_b['name']] = path['cost']
                    


class AgentRescuer:
    def __init__(self, environment, victims, population_size, n_generations, ts):
        self.environment = environment
        self.victims = victims
        self.population_size = population_size
        self.n_generations = n_generations
        self.ts = ts
        self.genetic_algorithm = None
        self.best_individual = None

    def run(self):
        found = False
        individual = None
        count = 1
        while not found:

            count += 1
            if len(self.victims) <= 2:
                found = True
                individual = None
                break

            self.genetic_algorithm = GeneticAlgorithm(self.environment, self.victims, self.population_size, self.n_generations)
            individual = self.genetic_algorithm.run()

            if individual['fitness'] <= self.ts:
                found = True
            else:
                self.remove_last_victim()

        self.best_individual = individual
        return individual
    
    def get_n_victims(self):
        return len(self.best_individual['victims']) - 2

    def get_points_used(self):
        return self.best_individual['fitness']

    
    def get_weighted_victim_cost(self):
        v1 = 0
        v2 = 0
        v3 = 0
        v4 = 0

        for victim in self.best_individual['victims']:
            if victim['class'] == 1:
                v1 += 1
            elif victim['class'] == 2:
                v2 += 1
            elif victim['class'] == 3:
                v3 += 1
            elif victim['class'] == 4:
                v4 += 1

        return 4 * v1 + 3 * v2 + 2 * v2 + v4

    def remove_last_victim(self):
        lower_class = 0
        for victim in self.victims:
            if victim['class'] > lower_class:
                lower_class = victim['class']
        
        lower_class_list = []
        for victim in self.victims:
            if victim['class'] == lower_class:
                lower_class_list.append(victim)

        victim_name = ''
        max_cost = 0

        for victim in lower_class_list:
            self.genetic_algorithm = GeneticAlgorithm(self.environment, self.victims, self.population_size, self.n_generations)
            self.genetic_algorithm.build_cost_table()
            cost = self.genetic_algorithm.get_cost(victim['name'], self.genetic_algorithm.base_name)
            if cost > max_cost:
                victim_name = victim['name']
                max_cost = cost
        
        for i in range(len(self.victims)):
            if self.victims[i]['name'] == victim_name:
                del self.victims[i]
                break