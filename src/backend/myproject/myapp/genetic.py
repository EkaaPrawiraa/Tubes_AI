from diagonal_magic_cube import DiagonalMagicCube
import numpy as np
import random
import bisect

e = 10e-6

class GeneticAlgorithm:
    def __init__(self, population_num=10):
        self.population_num = population_num
        self.population = self.generateRandomPopulation()
        self.fitnessPopulation = self.fitness()

    def generateRandomPopulation(self):
        population = []
        for _ in range(self.population_num):
            population.append(DiagonalMagicCube().initialize_cube())
        return population

    def fitness(self):
        global e
        sum = 0
        fitness_population = []
        for indv in self.population:
            fit = 1/(DiagonalMagicCube.constructor(indv).evaluate() + e)
            print(fit)
            fitness_population.append(fit)
            sum+=fit
        
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
        return idx_individu

    def reproduce(self):
        new_population = []
        idx_reproduce = self.selection()
        isFound = False
        idx=0
        while idx+1<self.population_num:
            shape3d = self.population[idx_reproduce[idx]].shape
            cube1 = self.population[idx_reproduce[idx]].flatten()
            cube2 = self.population[idx_reproduce[idx+1]].flatten()
            crossover_point = random.randint(1, len(cube1))
            # cocube1 = np.concatenate(cube1[:crossover_point],cube2[crossover_point:])
            cocube1 = np.concatenate([cube1[:crossover_point], cube2[crossover_point:]])
            cocube2 = np.concatenate([cube2[:crossover_point], cube1[crossover_point:]])
            # cocube2 = np.concatenate(cube2[:crossover_point],cube1[crossover_point:])
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
                new_population.append(newCube1.cube)
            else:
                if(obj_func2>=10): # threshold for mutation
                    mutation_point1 = random.randint(0,newCube2.n-1)
                    mutation_point2 = random.randint(0,newCube2.n-1)
                    cocube2[mutation_point1], cocube2[mutation_point2] = cocube2[mutation_point2], cocube2[mutation_point1]
                    newCube2 = DiagonalMagicCube.constructor(cocube2.reshape(shape3d))
                if(newCube2.evaluate()==0): isFound = True
                new_population.append(newCube2.cube)
            idx+=2
        self.population_num = len(new_population)
        return new_population, isFound

    def run(self):
        isFound = False
        iter=0
        while(len(self.population)>1 and not isFound):
            self.population, isFound = self.reproduce()
            self.fitnessPopulation = self.fitness()
            iter+=1
            print(f"kawin ke-{iter}")
            print(f"population size: {len(self.population)}")
        return DiagonalMagicCube.constructor(self.population[0])


def main():
    cube = DiagonalMagicCube()
    initial_score = cube.evaluate()
    print(f"Initial score: {initial_score}")
    print("Initial cube configuration:")
    # print(cube.cube)
    
    gene = GeneticAlgorithm(10000)
    final_score = gene.run()
    print(final_score.cube)
    print(final_score.evaluate())
    
    # print(f"Final score: {final_score[0]}")
    # print(f"Number of iterations: {final_score[1]}")
    # print(f"Final cube configuration:\n {final_score[2].cube}")
    # if final_score == 0:
    #     print("Perfect solution found!")
    # else:
    #     print("Local optimum reached.")
    
    # print("Final cube configuration:")
    # print(cube.cube)

if __name__ == "__main__":
    main()

