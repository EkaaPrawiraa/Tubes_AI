import numpy as np
import random
class DiagonalMagicCube:
    def __init__(self, n=5):
        self.n = n
        self.size = n**3
        self.magic_number = self.calculate_magic_number()
        self.cube = self.initialize_cube()
    
    def calculate_magic_number(self):
        return (self.size + 1) * self.n**2 // 2
    
    def initialize_cube(self):
        numbers = list(range(1, self.size + 1))
        random.shuffle(numbers)
        return np.array(numbers).reshape((self.n, self.n, self.n))
    
    def evaluate(self):
        total_deviation = 0
        
        # Check rows, columns, and pillars
        for i in range(self.n):
            total_deviation += abs(np.sum(self.cube[i, :, :]) - self.magic_number)
            total_deviation += abs(np.sum(self.cube[:, i, :]) - self.magic_number)
            total_deviation += abs(np.sum(self.cube[:, :, i]) - self.magic_number)
        
        # Check space diagonals
        total_deviation += abs(np.trace(self.cube) - self.magic_number)
        total_deviation += abs(np.trace(np.flip(self.cube, axis=0)) - self.magic_number)
        total_deviation += abs(np.trace(np.flip(self.cube, axis=1)) - self.magic_number)
        total_deviation += abs(np.trace(np.flip(self.cube, axis=2)) - self.magic_number)
        
        # Check plane diagonals (simplified, not all planes)
        for i in range(self.n):
            total_deviation += abs(np.trace(self.cube[i, :, :]) - self.magic_number)
            total_deviation += abs(np.trace(self.cube[:, i, :]) - self.magic_number)
            total_deviation += abs(np.trace(self.cube[:, :, i]) - self.magic_number)
        
        return int(np.sum(total_deviation))
    
    def swap(self, pos1, pos2):
        self.cube[pos1], self.cube[pos2] = self.cube[pos2].copy(), self.cube[pos1].copy()
    
    def get_random_position(self):
        return tuple(random.randint(0, self.n-1) for _ in range(3))

class GeneticAlgorithm:
    def __init__(self, population_size=100, mutation_rate=0.1, elite_size=10):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size

    def initialize_population(self, n):
        return [DiagonalMagicCube(n) for _ in range(self.population_size)]

    def fitness(self, cube):
        return 1 / (1 + cube.evaluate())  # Convert deviation to fitness (higher is better)

    def select_parents(self, population):
        fitnesses = [self.fitness(cube) for cube in population]
        return random.choices(population, weights=fitnesses, k=2)

    def crossover(self, parent1, parent2):
        child = DiagonalMagicCube(parent1.n)
        mask = np.random.choice([True, False], size=parent1.cube.shape)
        child.cube = np.where(mask, parent1.cube, parent2.cube)
        return child

    def mutate(self, cube):
        if random.random() < self.mutation_rate:
            pos1, pos2 = cube.get_random_position(), cube.get_random_position()
            cube.swap(pos1, pos2)

    def evolve(self, generations=1000):
        population = self.initialize_population(5)  # Assuming 5x5x5 cube

        for generation in range(generations):
            # Evaluate the population
            population.sort(key=lambda x: x.evaluate())

            # Select elite individuals
            new_population = population[:self.elite_size]

            # Create the rest of the new population
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population)
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_population.append(child)

            population = new_population

            # Print best fitness every 100 generations
            if generation % 100 == 0:
                best_fitness = self.fitness(population[0])
                print(f"Generation {generation}: Best Fitness = {best_fitness}")

        return population[0]  # Return the best individual

# Usage
ga = GeneticAlgorithm()
best_solution = ga.evolve()
print("Final solution evaluation:", best_solution.evaluate())
print("Final solution cube:\n", best_solution.cube)