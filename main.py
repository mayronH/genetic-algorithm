# Based on: https://www.youtube.com/watch?v=nhT56blfRpE

import time
from typing import Callable, List, Tuple
from random import choices, randint, random, randrange
from collections import namedtuple
from functools import partial


#Solution
Genome = List[int]
#The array of solutions
Population = List[Genome]

#Genetic Algorithm functions, the implementation in this code only works for the knapsack problem
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]

#Knapsack problem, list of items to be choosen

Thing = namedtuple('Thing', ['name', 'value', 'weight'])

things = [
    Thing('Laptop', 500, 2200),
    Thing('Headphone', 150, 160),
    Thing('Coffe mug', 60, 350),
    Thing('Notepad', 40, 333),
    Thing('Water bottle', 30, 192)
]

more_things = [
    Thing('Mints', 5, 25),
    Thing('Socks', 10, 38),
    Thing('Tissues', 15, 80),
    Thing('Phone', 500, 200),
    Thing('Baseball Cap', 100, 70)
] + things


#generate the genome of the solution(0 and 1s)
def generate_genome(length: int) -> Genome:
    return choices([0,1], k=length)

#generate the population of every generation
def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]

#return the fitness value of each list of things
def fitness(genome: Genome, things: [Thing], weight_limit: int) -> int:
    # the genome should have the same length of things, the genome is the solution of the problem.
    if len(genome) != len(things):
        raise ValueError("genome and things must be the same length")
    
    weigh = 0
    value = 0
    
    for i, thing in enumerate(things):
        if genome[i] == 1:
            weigh += thing.weight
            value += thing.value
            if weigh > weight_limit:
                return 0
    return value

#chooses the best parents based on the fitness func
def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population = population,
        weights = [fitness_func(genome) for genome in population],
        k=2
    )
 
 #crossover function, interchange some genes at random   
def single_point_crossover(a: Genome, b:Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("genomes must be of same length")
    
    length = len(a)
    if length < 2:
        return a, b
    
    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

#random mutations on genomes
def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        i = randrange(len(genome))
        # if random > probability do nothing
        # if random <= probability change 0 to 1 or 1 to 0
        genome[i] = genome[i] if random() > probability else abs(genome[i] - 1)
    return genome

#fitness_limit is the end goal of the problem(the best solution)
#generation_limit is the stopping point
def run_evolution(
    populate_func: PopulateFunc,
    fitness_func: FitnessFunc,
    fitness_limit: int,
    selection_func: SelectionFunc = selection_pair,
    crossover_func: CrossoverFunc = single_point_crossover,
    mutation_func: MutationFunc = mutation,
    generation_limit: int = 100
) -> Tuple[Population, int]:
    
    #gen 0
    population = populate_func()
    
    for i in range(generation_limit):
        #sorting the population help to decide if we reach the goal and help to choose the best genomes
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )
        #stop the algorithm if reach the limit
        if fitness_func(population[0]) >= fitness_limit:
            break
            
        #elitism
        next_generation = population[0:2]
        
        # population size = 10, 10/2 = 5 -1 = 4, 0-4
        # create 8 new genomes and keep the 2 selected by elitism
        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            child_a, child_b = crossover_func(parents[0], parents[1])
            child_a = mutation_func(child_a)
            child_b = mutation_func(child_b)
            next_generation += [child_a, child_b]
            print(next_generation, j)
        
        population = next_generation
            
    population = sorted(
        population,
        key=lambda genome: fitness_func(genome),
        reverse=True
    )
    
    return population, i

start = time.time()
population, generations = run_evolution(
    populate_func=partial(
        generate_population, size=10, genome_length=len(things)
    ),
    fitness_func=partial(
        fitness, things = things, weight_limit = 3000
    ),
    fitness_limit= 740,
    generation_limit=100
)
end = time.time()

def genome_to_things(genome:Genome, things: [Thing]) -> [Thing]:
    result = []
    for i, thing in enumerate(things):
        if genome[i] == 1:
            result += [thing.name]
    return result

print("geneations: ", generations)
# print("population:", population)
# print("best solution: ", genome_to_things(population[0], things))
# print("time: ", end-start)