from diagonal_magic_cube import DiagonalMagicCube
import numpy as np
import random
import bisect
import heapq
import time

e = 10e-6

class GeneticAlgorithm:
    def __init__(self, population_num=10):
        self.population_num = population_num
        self.list_state = []
        self.initial_population = self.generateRandomPopulation()
        self.population = self.initial_population
        self.priorqueue = None
        self.fitnessPopulation = self.fitness()
        self.duration = None

    def generateRandomPopulation(self):
        population = []
        for _ in range(self.population_num):
            population.append(DiagonalMagicCube().initialize_cube())
        return population

    def fitness(self):
        global e
        pq = []
        sum = 0
        fitness_population = []
        minscore = 10e9
        for i in range (len(self.population)):
            score = DiagonalMagicCube.constructor(self.population[i]).evaluate()
            minscore = min(minscore, score)
            fit = 1/(score + e)
            print(fit)
            print(score)
            heapq.heappush(pq,(score, i))
            fitness_population.append(fit)
            sum+=fit

        self.list_state.append([minscore, sum/len(self.population)])
        self.priorqueue = pq
        fitness_population = [fit/sum for fit in fitness_population]
        fitness_population_range = [fitness_population[0]]
        for i in range(1, len(fitness_population)):
            fitness_population_range.append(fitness_population[i]+fitness_population_range[i-1])
        return fitness_population_range

    def selection(self):
        idx_individu = []
        for _ in range(self.population_num):
            roulete_result = random.uniform(0,1)
            idx_individu.append(bisect.bisect_right(self.fitnessPopulation, roulete_result))
            roulete_result = random.uniform(0,1)
            idx_individu.append(bisect.bisect_right(self.fitnessPopulation, roulete_result))
        return idx_individu

    def reproduce(self):
        idx_reproduce = self.selection()
        isFound = False
        idx=0
        new_population = self.population
        while idx<self.population_num:
            shape3d = self.population[idx_reproduce[idx]].shape
            cube1 = self.population[idx_reproduce[idx]].flatten()
            cube2 = self.population[idx_reproduce[idx+1]].flatten()
            crossover_point = random.randint(1, len(cube1))
            cocube1 = np.concatenate([cube1[:crossover_point], cube2[crossover_point:]])
            cocube2 = np.concatenate([cube2[:crossover_point], cube1[crossover_point:]])
            newCube1 = DiagonalMagicCube.constructor(cocube1.reshape(shape3d))
            newCube2 = DiagonalMagicCube.constructor(cocube2.reshape(shape3d))
            obj_func1 = newCube1.evaluate()
            obj_func2 = newCube2.evaluate()
            if(obj_func1<obj_func2):
                if(obj_func1>=10): # threshold for mutation
                    mutation_point1 = random.randint(0,newCube1.n-1)
                    mutation_point2 = random.randint(0,newCube1.n-1)
                    cocube1[mutation_point1], cocube1[mutation_point2] = cocube1[mutation_point2], cocube1[mutation_point1]
                    newCube1 = DiagonalMagicCube.constructor(cocube1.reshape(shape3d))
                if(newCube1.evaluate()==0): isFound = True
                heapq.heappush(self.priorqueue,(obj_func1,self.population_num+idx))
                new_population.append(newCube1.cube)

            else:
                if(obj_func2>=10): # threshold for mutation
                    mutation_point1 = random.randint(0,newCube2.n-1)
                    mutation_point2 = random.randint(0,newCube2.n-1)
                    cocube2[mutation_point1], cocube2[mutation_point2] = cocube2[mutation_point2], cocube2[mutation_point1]
                    newCube2 = DiagonalMagicCube.constructor(cocube2.reshape(shape3d))
                if(newCube2.evaluate()==0): isFound = True
                heapq.heappush(self.priorqueue, (obj_func2,self.population_num+idx))
                new_population.append(newCube2.cube)

            idx+=1
        self.population = [new_population[indv[1]] for indv in heapq.nsmallest(self.population_num, self.priorqueue)]
        return isFound

    def run(self, iteration):
        start_time = time.time()
        isFound = False
        iter=0
        while(len(self.population)>1 and not isFound and iter<iteration):
            isFound = self.reproduce()
            self.fitnessPopulation = self.fitness()
            iter+=1
            print(f"kawin ke-{iter}")
        self.duration = time.time()-start_time
        


def play(population=10000, iteration=200):
    gene = GeneticAlgorithm(population)
    gene.run(iteration)
    final = heapq.nsmallest(1, gene.priorqueue)
    initial_population = gene.initial_population
    init_state = [[ind,DiagonalMagicCube.constructor(ind).evaluate()] for ind in initial_population]
    final_obj_func = final[0][0]
    final_state = gene.population[final[0][1]]
    list_state = gene.list_state
    duration = gene.duration
    return init_state, final_obj_func, list_state, duration, final_state

if __name__ == "__main__":
    population = int(input("Population num: "))
    iteration = int(input("Iteration: "))
    init_pop, obj_func, state, duration, final_state = play(population=population, iteration=iteration)
    print(f"Initial population: {init_pop}")
    for iter in range (len(state)):
        print(f"Fertilization: {iter}")
        print(f"Optimum value: {state[0]}")
        print(f"Average: {state[1]}")

    print(f"Final Objective function: {obj_func}")
    print(f"Final state: {final_state}")
    print(f"Duration: {duration}ms")

