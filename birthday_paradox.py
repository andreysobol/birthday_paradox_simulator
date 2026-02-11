"""
Birthday Paradox Simulator

A Monte Carlo simulation framework for empirically estimating the probability 
that at least two individuals in a group share the same birthday.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict


class BirthdayParadoxSimulator:
    """
    Core simulator for the birthday paradox experiment.
    
    This class implements a Monte Carlo simulation to estimate collision
    probabilities as a function of group size.
    """
    
    def __init__(self, days_in_year: int = 365, trials: int = 10000):
        """
        Initialize the simulator.
        
        Args:
            days_in_year: Number of days in a year (default: 365)
            trials: Number of Monte Carlo trials per group size (default: 10000)
        """
        self.days_in_year = days_in_year
        self.trials = trials
        
    def generate_birthdays(self, group_size: int) -> np.ndarray:
        """
        Generate random birthdays for a group.
        
        Uses uniform random sampling to generate birthdays as integers
        in the range [1, days_in_year].
        
        Args:
            group_size: Number of people in the group
            
        Returns:
            Array of simulated birthdays
        """
        return np.random.randint(1, self.days_in_year + 1, size=group_size)
    
    def has_collision(self, birthdays: np.ndarray) -> bool:
        """
        Check if there are duplicate birthdays (collision).
        
        A collision occurs when len(unique_birthdays) < group_size.
        Uses hash set (np.unique) for efficient duplicate detection.
        
        Args:
            birthdays: Array of birthdays to check
            
        Returns:
            True if at least one collision exists, False otherwise
        """
        return len(np.unique(birthdays)) < len(birthdays)
    
    def run_trials(self, group_size: int) -> Dict[str, any]:
        """
        Run Monte Carlo trials for a specific group size.
        
        Args:
            group_size: Size of the group to simulate
            
        Returns:
            Dictionary containing:
                - group_size: The group size tested
                - trials: Number of trials run
                - collisions: Number of trials with at least one collision
                - probability: Empirical collision probability
        """
        collision_count = 0
        
        for _ in range(self.trials):
            birthdays = self.generate_birthdays(group_size)
            if self.has_collision(birthdays):
                collision_count += 1
        
        probability = collision_count / self.trials
        
        return {
            'group_size': group_size,
            'trials': self.trials,
            'collisions': collision_count,
            'probability': probability
        }
    
    def simulate(self, group_sizes: List[int]) -> List[Dict[str, any]]:
        """
        Run simulation for multiple group sizes.
        
        Args:
            group_sizes: List of group sizes to test
            
        Returns:
            List of result dictionaries, one per group size
        """
        results = []
        
        for size in group_sizes:
            result = self.run_trials(size)
            results.append(result)
            print(f"Group size {size:3d}: {result['probability']:.4f} "
                  f"({result['collisions']}/{result['trials']} collisions)")
        
        return results
    
    def plot_results(self, results: List[Dict[str, any]], 
                     save_path: str = None, show: bool = True):
        """
        Plot collision probability vs group size.
        
        Creates a visualization showing the exponential growth pattern
        of collision probability as group size increases.
        
        Args:
            results: List of result dictionaries from simulate()
            save_path: Optional path to save the plot (default: None)
            show: Whether to display the plot (default: True)
        """
        group_sizes = [r['group_size'] for r in results]
        probabilities = [r['probability'] for r in results]
        
        plt.figure(figsize=(10, 6))
        plt.plot(group_sizes, probabilities, 'b-o', linewidth=2, markersize=6)
        plt.xlabel('Group Size (n)', fontsize=12)
        plt.ylabel('Collision Probability P(n)', fontsize=12)
        plt.title('Birthday Paradox: Probability of Shared Birthday', fontsize=14)
        plt.grid(True, alpha=0.3)
        
        # Add reference lines for key landmarks
        plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='50% probability')
        
        # Annotate key points if they're in the data
        for size, prob in zip(group_sizes, probabilities):
            if size == 23:
                plt.annotate(f'{size} people: {prob:.1%}', 
                           xy=(size, prob), xytext=(size + 3, prob - 0.1),
                           arrowprops=dict(arrowstyle='->', color='red'),
                           fontsize=10, color='red')
        
        plt.legend()
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        if show:
            plt.show()
        
        plt.close()


def compute_theoretical_probability(group_size: int, days: int = 365) -> float:
    """
    Compute theoretical collision probability.
    
    Uses the formula: P(n) = 1 - (365!/((365-n)! * 365^n))
    Implemented using complementary probability to avoid large factorials.
    
    Args:
        group_size: Size of the group
        days: Number of days in year (default: 365)
        
    Returns:
        Theoretical collision probability
    """
    if group_size > days:
        return 1.0
    
    # Compute probability of no collision
    prob_no_collision = 1.0
    for i in range(group_size):
        prob_no_collision *= (days - i) / days
    
    # Collision probability is complement
    return 1.0 - prob_no_collision


def main():
    """
    Example usage of the Birthday Paradox Simulator.
    """
    print("=" * 60)
    print("Birthday Paradox Simulator")
    print("=" * 60)
    print()
    
    # Initialize simulator
    simulator = BirthdayParadoxSimulator(days_in_year=365, trials=10000)
    
    # Define group sizes to test
    group_sizes = list(range(2, 71, 2))  # 2, 4, 6, ..., 70
    
    print(f"Running simulation with {simulator.trials} trials per group size...")
    print()
    
    # Run simulation
    results = simulator.simulate(group_sizes)
    
    print()
    print("=" * 60)
    print("Key Landmarks (Theoretical vs Empirical):")
    print("=" * 60)
    
    # Compare with theoretical values for key landmarks
    landmarks = [10, 23, 30, 50]
    for size in landmarks:
        theoretical = compute_theoretical_probability(size)
        # Find empirical result
        empirical = None
        for r in results:
            if r['group_size'] == size:
                empirical = r['probability']
                break
        
        if empirical is not None:
            print(f"Group size {size:2d}: Theoretical={theoretical:.4f}, "
                  f"Empirical={empirical:.4f}, "
                  f"Difference={abs(theoretical - empirical):.4f}")
    
    print()
    print("Generating plot...")
    
    # Plot results
    simulator.plot_results(results, save_path='birthday_paradox.png', show=False)
    
    print("Done!")


if __name__ == "__main__":
    main()
