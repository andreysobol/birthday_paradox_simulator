"""
Example usage of the Birthday Paradox Simulator.

This script demonstrates how to use the simulator to compute and visualize
collision probabilities for different group sizes.
"""

from birthday_paradox import BirthdayParadoxSimulator, compute_theoretical_probability


def basic_example():
    """
    Basic example: simulate for a range of group sizes.
    """
    print("Example 1: Basic Simulation")
    print("-" * 40)
    
    # Create simulator with 10,000 trials
    simulator = BirthdayParadoxSimulator(trials=10000)
    
    # Test group sizes from 5 to 60 in steps of 5
    group_sizes = list(range(5, 61, 5))
    
    # Run simulation
    results = simulator.simulate(group_sizes)
    
    # Plot results
    simulator.plot_results(results, save_path='example_basic.png', show=False)
    print()


def detailed_example():
    """
    Detailed example: focus on the critical region around 23 people.
    """
    print("Example 2: Detailed Analysis Around 23 People")
    print("-" * 40)
    
    # Create simulator with more trials for accuracy
    simulator = BirthdayParadoxSimulator(trials=20000)
    
    # Test group sizes from 15 to 35
    group_sizes = list(range(15, 36))
    
    # Run simulation
    results = simulator.simulate(group_sizes)
    
    # Plot results
    simulator.plot_results(results, save_path='example_detailed.png', show=False)
    print()


def comparison_example():
    """
    Example comparing empirical results with theoretical probabilities.
    """
    print("Example 3: Empirical vs Theoretical Comparison")
    print("-" * 40)
    
    simulator = BirthdayParadoxSimulator(trials=15000)
    
    # Test specific group sizes
    group_sizes = [10, 15, 20, 23, 25, 30, 40, 50]
    
    print(f"{'Group Size':<12} {'Empirical':<12} {'Theoretical':<12} {'Difference':<12}")
    print("-" * 50)
    
    for size in group_sizes:
        result = simulator.run_trials(size)
        theoretical = compute_theoretical_probability(size)
        difference = abs(result['probability'] - theoretical)
        
        print(f"{size:<12} {result['probability']:<12.4f} "
              f"{theoretical:<12.4f} {difference:<12.4f}")
    
    print()


def custom_parameters_example():
    """
    Example with custom parameters (different year length).
    """
    print("Example 4: Custom Parameters (Leap Year)")
    print("-" * 40)
    
    # Simulate with 366 days (leap year)
    simulator = BirthdayParadoxSimulator(days_in_year=366, trials=10000)
    
    group_sizes = [10, 20, 23, 30, 40, 50]
    
    results = simulator.simulate(group_sizes)
    
    print("\nComparison with standard 365-day year:")
    print(f"{'Group Size':<12} {'365 days':<12} {'366 days':<12}")
    print("-" * 40)
    
    for size in group_sizes:
        prob_365 = compute_theoretical_probability(size, 365)
        result_366 = [r for r in results if r['group_size'] == size][0]
        prob_366 = result_366['probability']
        
        print(f"{size:<12} {prob_365:<12.4f} {prob_366:<12.4f}")
    
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Birthday Paradox Simulator - Examples")
    print("=" * 60)
    print()
    
    # Run all examples
    basic_example()
    detailed_example()
    comparison_example()
    custom_parameters_example()
    
    print("All examples completed!")
    print("Check the generated PNG files for visualizations.")
