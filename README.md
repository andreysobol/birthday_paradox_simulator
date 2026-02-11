# Birthday Paradox Simulator

## Overview
The Birthday Paradox Simulator is a probabilistic experiment framework designed to empirically estimate the likelihood that at least two individuals in a group share the same birthday.

Despite the counter-intuitive nature of the birthday paradox, the simulator demonstrates how collision probability grows rapidly as group size increases, validating theoretical results through Monte Carlo simulation.

## Objective
To compute and visualize the probability of birthday collisions as a function of group size by running repeated randomized trials.

## Methodology

### 1. Assumptions
- A year has 365 days (ignoring leap years)
- Birthdays are uniformly distributed across days
- Each trial samples birthdays independently

### 2. Simulation Procedure
For each group size **n**:
1. Generate **n** random integers in range [1, 365]
2. Interpret each integer as a simulated birthday
3. Check for duplicates (birthday collisions)
4. Record whether a collision occurred
5. Repeat for **T** trials

### 3. Collision Detection
A collision occurs if: `len(unique_birthdays) < n`

Implementation uses hash sets (numpy.unique) for efficient duplicate detection.

### 4. Probability Estimation
Empirical probability is computed as:

```
P(n) = Number of trials with ≥1 collision / T
```

Where:
- **n** — group size
- **T** — number of trials

Higher **T** improves statistical accuracy.

## Installation

### Requirements
- Python 3.7+
- NumPy >= 1.20.0
- Matplotlib >= 3.3.0

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install Development Dependencies (for testing)
```bash
pip install -r requirements-dev.txt
```

## Usage

### Basic Usage
Run the main simulator with default parameters:

```bash
python birthday_paradox.py
```

This will:
- Simulate group sizes from 2 to 70 (in steps of 2)
- Run 10,000 trials per group size
- Display results for each group size
- Compare empirical results with theoretical values
- Generate a visualization plot (`birthday_paradox.png`)

### Example Scripts
Run comprehensive examples demonstrating different use cases:

```bash
python example.py
```

This includes:
1. Basic simulation across a range of group sizes
2. Detailed analysis around the critical 23-person threshold
3. Comparison of empirical vs theoretical probabilities
4. Custom parameters (e.g., leap year with 366 days)

### Programmatic Usage

```python
from birthday_paradox import BirthdayParadoxSimulator, compute_theoretical_probability

# Initialize simulator
simulator = BirthdayParadoxSimulator(days_in_year=365, trials=10000)

# Run simulation for specific group sizes
group_sizes = [10, 20, 23, 30, 50]
results = simulator.simulate(group_sizes)

# Plot results
simulator.plot_results(results, save_path='my_plot.png', show=True)

# Get theoretical probability
theoretical = compute_theoretical_probability(23)
print(f"Theoretical probability for 23 people: {theoretical:.4f}")
```

## Expected Results

### Key Landmarks

| Group Size | Collision Probability |
|------------|----------------------|
| 10         | ~11.7%              |
| 23         | ~50.7%              |
| 30         | ~70.6%              |
| 50         | ~97.0%              |

The famous result is that with just **23 people**, there's a better than 50% chance that two share a birthday!

## Implementation Architecture

### Core Components

1. **Random Generator**: Uniform day sampling using NumPy
2. **Trial Engine**: Runs Monte Carlo simulation loops
3. **Collision Checker**: Detects duplicate birthdays using hash sets
4. **Aggregator**: Computes empirical probabilities
5. **Plotting Module**: Renders probability curves using Matplotlib

### Files

- `birthday_paradox.py`: Main simulator implementation
- `example.py`: Example usage scripts
- `requirements.txt`: Python dependencies
- `.gitignore`: Git ignore patterns

## Output

The simulator produces:
- Console output with detailed statistics for each group size
- Comparison with theoretical probabilities
- Visualization plot (PNG) showing probability vs group size curve

## Visualization

The plot displays:
- **X-axis**: Group size (n)
- **Y-axis**: Collision probability P(n)
- **Curve**: Shows exponential growth pattern
- **Reference lines**: 50% probability threshold
- **Annotations**: Key landmarks (e.g., 23 people)

## Testing

The project includes a comprehensive test suite with 35 tests covering:
- Core functionality (birthday generation, collision detection)
- Monte Carlo trial execution
- Theoretical probability calculations
- Edge cases and boundary conditions
- Integration tests

### Running Tests

Run all tests:
```bash
pytest test_birthday_paradox.py -v
```

Run tests with coverage report:
```bash
pytest test_birthday_paradox.py -v --cov=birthday_paradox --cov-report=term-missing
```

Run a specific test class:
```bash
pytest test_birthday_paradox.py::TestBirthdayParadoxSimulator -v
```

Run a specific test:
```bash
pytest test_birthday_paradox.py::TestBirthdayParadoxSimulator::test_run_trials_return_structure -v
```

### Continuous Integration

The project uses GitHub Actions to automatically run tests on:
- Multiple operating systems (Ubuntu, Windows, macOS)
- Multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)
- Every push and pull request to main/master/develop branches

See `.github/workflows/tests.yml` for the full CI configuration.

## License

This project is open source and available for educational and research purposes.
