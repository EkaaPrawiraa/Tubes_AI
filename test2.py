import random
import numpy as np
import time

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

class RandomRestartHillClimbing:
    def __init__(self, n=5, max_iterations=1000, max_restarts=10, max_plateau=100):
        self.n = n
        self.max_iterations = max_iterations
        self.max_restarts = max_restarts
        self.max_plateau = max_plateau
    
    def hill_climbing(self, cube):
        current_score = cube.evaluate()
        plateau_count = 0
        
        for _ in range(self.max_iterations):
            if current_score == 0:  # Perfect solution found
                return current_score, cube
            
            best_neighbor = None
            best_score = current_score
            
            # Generate and evaluate neighbors
            for _ in range(100):  # Limit neighbor evaluation to 100 for efficiency
                pos1 = cube.get_random_position()
                pos2 = cube.get_random_position()
                
                cube.swap(pos1, pos2)
                new_score = cube.evaluate()
                
                if new_score < best_score:
                    best_neighbor = (pos1, pos2)
                    best_score = new_score
                
                cube.swap(pos1, pos2)  # Undo the swap
            
            if best_neighbor is None:  # No improvement found
                plateau_count += 1
                if plateau_count >= self.max_plateau:
                    break
            else:
                plateau_count = 0
                cube.swap(*best_neighbor)
                current_score = best_score
        
        return current_score, cube
    
    def run(self):
        best_score = float('inf')
        best_cube = None
        
        for _ in range(self.max_restarts):
            cube = DiagonalMagicCube(self.n)
            score, cube = self.hill_climbing(cube)
            
            if score < best_score:
                best_score = score
                best_cube = cube
            
            if best_score == 0:  # Perfect solution found
                break
        
        return best_score, best_cube

def main():
    start_time = time.time()
    
    rrhc = RandomRestartHillClimbing(n=5, max_iterations=1000, max_restarts=100, max_plateau=100)
    final_score, best_cube = rrhc.run()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Final score: {final_score}")
    if final_score == 0:
        print("Perfect solution found!")
    else:
        print("Best solution found (may not be perfect)")
    
    print(f"Time taken: {elapsed_time:.2f} seconds")
    # print("Best cube configuration:")
    # print(best_cube.cube)

if __name__ == "__main__":
    main()