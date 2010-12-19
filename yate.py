import random, math
from sys import argv

ascii_start = 32 #every character between SPACE ...
ascii_end = 126 #... and ~ 

pop_size = 500
max_generations = 10000

mutation_rate = 0.20
mutation_strength = 0.05
error = int(mutation_strength * (ascii_end-ascii_start)) #ASCII value range
clone_rate = 0.05
elitism = 0.0

class Word:

    def __init__(self, dna, fitness):
        self.dna = dna
        self.fitness = fitness
        
    def __repr__(self):
        return repr((self.dna, self.fitness))
        
    def calc_fitness(self, solution):
        self.fitness = 0.0
        values = string_to_vals(solution)
        for i in range(len(values)):
            self.fitness -= math.fabs(values[i] - ord(self.dna[i]))
        

def string_to_vals(chromosome):
    vals = []
    for char in chromosome:
        vals.append(ord(char))
    return vals


def initialize(population, solution):
    for i in range(pop_size):
        word = Word("", 0.0)
        for i in range(len(solution)):
            word.dna += chr(random.randint(ascii_start, ascii_end))
        population.append(word)

def fitness_sort(population):
    return sorted(population, key=lambda word: word.fitness, reverse=True)

def fitness_func(population, solution):
    for member in population:
        member.calc_fitness(solution)



def mutate(dna):
    strand = random.randint(0, len(dna)-1)
    x = ord(dna[strand])
    mutation = random.randint(x-error, x+error)
    if mutation < ascii_start:
        mutation = ascii_start
    elif mutation > ascii_end:
        mutation = ascii_end
    dna_list = list(dna)
    dna_list[strand] = chr(mutation)
    return "".join(dna_list)
    
def crossover(parent_a, parent_b):
    str_cha = ""
    str_chb = ""
    str_a = parent_a.dna
    str_b = parent_b.dna
    
    if len(str_a) != len(str_b):
        print str_a + " *** " + str_b
    
    start = random.randint(0, len(str_a)-1)
    str_cha = str_a[0:start] + str_b[start:len(str_a)]
    str_chb = str_b[0:start] + str_a[start:len(str_a)]
        
    child_a = Word(str_cha, 0.0)
    child_b = Word(str_chb, 0.0)
    return (child_a, child_b)
    
def mate(parent_a, parent_b):
    if (random.random() < clone_rate): #sometimes just clone the parents
        return (parent_a, parent_b)
    
    (child_a, child_b) = crossover(parent_a, parent_b) #mate (crossover)

    if (random.random() < mutation_rate): #sometimes mutate one of the kids
        if (random.random() < 0.5):
            child_a.dna = mutate(child_a.dna)
        else:
            child_b.dna = mutate(child_b.dna)

    return (child_a, child_b)
    
def elite(population):
    eli = []
    remainder = []
    total = int(elitism * pop_size)
    for i in range(0, total):
        eli.append(population[i])
    for i in range(total, len(population)):
        remainder.append(population[i])
    return (eli, remainder)
    
def two_parents(population):
    parents = []
    for i in range(2):
        parent_a = population[random.randint(0, len(population)-1)]
        parent_b = population[random.randint(0, len(population)-1)]
        if parent_a.fitness < parent_b.fitness:
            parents.append(parent_b)
        else:
            parents.append(parent_a)
    return (parents[0], parents[1])

    

if __name__ == "__main__":
    solution = argv[1] #take in the text to evolve from command line
    population = []
    initialize(population, solution)
    completed = False
    
    for i in range(max_generations):
        fitness_func(population, solution)
        fitness_sort(population)
        
        print "Generation %s Best: %s (%s)" % (i, population[0].dna, int(population[0].fitness))
        
        if population[0].fitness == 0:
            print "\nFinished at Generation %s!\nResult: %s" % (i, population[0].dna)
            completed = True
            break
            
        (eli, remainder) = elite(population)
        while (len(eli) < pop_size):
            #grab two random parents and mate
            (parent_a, parent_b) = two_parents(population)
            (child_a, child_b) = mate(parent_a, parent_b)
            eli.append(child_a)
            eli.append(child_b)
        population = eli
        
            
    if completed == False:
        print "Could not finish within %s generations!" % (max_generations)
        fitness_sort(population)
        print "Closest approximation: %s" % (population[0].dna)



        


