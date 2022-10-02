import random
from a_star import AStar
from random import randint, randrange

class GeneticAlgorithm:
    def __init__(self, environment, victims, population_size, n_generations):
        self.environment = environment
        self.base_position = environment.get_base_position()
        self.base_name = self.base_position[0] + ',' + self.base_position[1]
        self.env_map = environment.get_map()
        self.victims = victims
        self.individuals = []
        self.a_star = AStar(self.env_map)
        self.cost_table = {}
        self.population_size = population_size
        self.n_generations = n_generations
    
    def run(self):
        self.create_population()

        self.set_fitness()
        self.sort_population()
        
        for _ in range(self.n_generations):

            self.set_roulette_values()
            cross_indexes = self.select_n_individuals(4)

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
                value = randint(1, len(self.individuals[index]['victims']) - 1)
                temp = self.individuals[index]['victims'][i]
                self.individuals[index]['victims'][i] = self.individuals[index]['victims'][value]
                self.individuals[index]['victims'][value] = temp
    

    def do_crossover(self, p_cross, index_a, index_b):
        value = randint(0, 100)
        descendent_a = self.individuals[index_a].copy()
        descendent_b = self.individuals[index_b].copy()
        if value <= p_cross:
            value = randint(2, descendent_a['victims'] - 2)
            for i in range(1, value):
                temp = descendent_a['victims'][i]
                descendent_a['victims'][i] = descendent_b['victims'][i]
                descendent_b['victims'][i] = temp

            self.individuals.append(descendent_a)
            self.individuals.append(descendent_b)


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
        value = randint(1, 99)

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

        victims_order.insert(0, {'name' : self.base_name, 'position' : self.base_position , 'class' : 5})
        victims_order.append({'name' : self.base_name, 'position' : self.base_position , 'class' : 5})

        self.individuals.append({'victims' : victims_order, 'fitness' : 0, 'fitness_aux' : 0, 'probability': 0, 'roulette_values' : [0, 0]})

    def sort_population(self):
        self.individuals = sorted(self.individuals, key=lambda d: d['fitness']) 

    def set_fitness(self):
        for individual in self.individuals:
            cost = 0
            for i in range(1, len(individual)):
                cost += self.get_cost(individual['victims'][i]['name'], individual['victims'][i - 1]['name'])
            
            individual['fitness'] = cost

    def build_cost_table(self):
        victims_base = self.victims.copy()
        victims_base.insert(0, {'name' : self.base_name, 'position' : self.base_position , 'class' : 5})

        for victim_a in victims_base:
            self.cost_table[victim_a['name']] = {}
            for victim_b in victims_base:
                if victim_a['name'] != victim_b['name']:
                    path = self.a_star.run(victim_a['position'], victim_b['position'])
                    self.cost_table[victim_a['name']][victim_b['name']] = path['cost']


class AgentRescuer:
    def __init__(self, environment, victims, population_size, n_generations, ts):
        self.environment = environment
        self.victims = victims
        self.population_size = population_size
        self.n_generations = n_generations
        self.ts = ts
        self.genetic_algorithm = None
    
    def run(self):
        found = False
        individual = None
        while not found:
            
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

        return individual
            

    def remove_last_victim(self):
        lower_class = 10
        for victim in self.victims:
            if victim['class'] < lower_class:
                lower_class = victim['class']
        
        lower_class_list = []
        for victim in self.victims:
            if victim['class'] == lower_class:
                lower_class_list.append(victim)
        
        victim_name = ''
        max_cost = 0

        for victim in lower_class_list:
            cost = self.genetic_algorithm.get_cost(victim['name'], self.genetic_algorithm.base_name)
            if cost > max_cost:
                victim_name = victim['name']
                max_cost = cost
        
        for i in range(len(self.victims)):
            if self.victims[i]['name'] == victim_name:
                del self.victims[i]
                break