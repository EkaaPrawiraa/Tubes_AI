import time
import math
import random
import copy
class SimulatedAnnealing:
    def __init__(self, cube, max_iterations=100, initial_temperature=10000, cooling_rate=0.9999):
        self.cube = cube
        self.max_iterations = max_iterations
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.list_result = []

    def run(self):
        start_time = time.time()
        temperature = self.initial_temperature
        current_score = self.cube.evaluate()
        # print(self.cube.cube)
        iteration = 0
        freq_local = 0
        self.list_result.append((iteration,(self.cube.cube).copy(),current_score, freq_local,1))
        
        
        while temperature >  1e-5:  
            if current_score == 0:
                break
            
            pos1 = self.cube.get_random_position()
            pos2 = self.cube.get_random_position()
            while pos1 == pos2:  
                pos2 = self.cube.get_random_position()

            self.cube.swap(pos1, pos2)
            new_score = self.cube.evaluate()
            

            delta = new_score - current_score
            if delta < 0:
                # Accept the new state
                current_score = new_score
                iteration += 1
                self.list_result.append((iteration,(self.cube.cube).copy(),current_score, freq_local,1))
            else:
                freq_local += 1
                prob = math.exp(-delta / temperature)
                if random.random() < prob:
                    # Accept the new state
                    current_score = new_score
                    iteration += 1
                    self.list_result.append((iteration,(self.cube.cube).copy(),current_score, freq_local,prob))
                else:
                    # Revert to the previous state 
                    self.cube.swap(pos2, pos1)
            
            # Cool down the temperature
            temperature *= self.cooling_rate

        
        end_time = time.time()
        total_time = end_time - start_time
        return self.list_result, total_time
