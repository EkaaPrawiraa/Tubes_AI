import random
import numpy as np

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
            if i == 0:
                print("baris\n")
                print(self.cube[i, :, :])
                print("KOLOM \n")
                print(self.cube[:, i, :])
                # print("baris\n")
                # print(self.cube[i, :, :])
        
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
        
        return int(np.sum(total_deviation))  # Sum all deviations and convert to integer
    
    def swap(self, pos1, pos2):
        x = self.cube[pos1] 
        y = self.cube[pos2]
        # print(x)
        # print(y)
        self.cube[pos1], self.cube[pos2] = y, x
    
    def get_random_position(self):
        return tuple(random.randint(0, self.n-1) for _ in range(3))

class HillClimbing:
    def __init__(self, cube, max_iterations=1):
        self.cube = cube
        self.max_iterations = max_iterations
    
    def run(self):
        current_score = self.cube.evaluate()
        
        for _ in range(self.max_iterations):
            if current_score == 0:  # Perfect solution found
                break
            
            best_neighbor = None
            best_score = current_score
            
            # Generate and evaluate all neighbors
            for _ in range(1):  # Limit neighbor evaluation to 100 for efficiency
                pos1 = self.cube.get_random_position()
                pos2 = self.cube.get_random_position()
                test = self.cube
                print(test)
                
                self.cube.swap(pos1, pos2)
                new_score = self.cube.evaluate()
                
                if new_score < best_score:
                    best_neighbor = (pos1, pos2)
                    best_score = new_score
                
                self.cube.swap(pos1, pos2)  # Undo the swap
            
            if best_neighbor is None:  # No improvement found
                break
            
            # Apply the best swap
            self.cube.swap(*best_neighbor)
            current_score = best_score
        
        return current_score

def main():
    cube = DiagonalMagicCube()
    initial_score = cube.evaluate()
    print(f"Initial score: {initial_score}")
    print("Initial cube configuration:")
    print(cube.cube)
    
    hill_climbing = HillClimbing(cube)
    final_score = hill_climbing.run()
    
    print(f"Final score: {final_score}")
    if final_score == 0:
        print("Perfect solution found!")
    else:
        print("Local optimum reached.")
    
    # print("Final cube configuration:")
    # print(cube.cube)

if __name__ == "__main__":
    main()