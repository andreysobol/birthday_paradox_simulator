"""
Unit tests for the Birthday Paradox Simulator.

Tests cover core functionality including:
- Birthday generation
- Collision detection
- Monte Carlo trials
- Theoretical probability calculations
- Simulation results validation
"""

import pytest
import numpy as np
from birthday_paradox import (
    BirthdayParadoxSimulator,
    compute_theoretical_probability
)


class TestBirthdayParadoxSimulator:
    """Test suite for BirthdayParadoxSimulator class."""
    
    def test_init_default_parameters(self):
        """Test initialization with default parameters."""
        simulator = BirthdayParadoxSimulator()
        assert simulator.days_in_year == 365
        assert simulator.trials == 10000
    
    def test_init_custom_parameters(self):
        """Test initialization with custom parameters."""
        simulator = BirthdayParadoxSimulator(days_in_year=366, trials=5000)
        assert simulator.days_in_year == 366
        assert simulator.trials == 5000
    
    def test_generate_birthdays_shape(self):
        """Test that generate_birthdays returns correct shape."""
        simulator = BirthdayParadoxSimulator()
        group_size = 23
        birthdays = simulator.generate_birthdays(group_size)
        assert birthdays.shape == (group_size,)
    
    def test_generate_birthdays_range(self):
        """Test that generated birthdays are within valid range."""
        simulator = BirthdayParadoxSimulator(days_in_year=365)
        birthdays = simulator.generate_birthdays(100)
        assert np.all(birthdays >= 1)
        assert np.all(birthdays <= 365)
    
    def test_generate_birthdays_custom_days(self):
        """Test birthday generation with custom days_in_year."""
        simulator = BirthdayParadoxSimulator(days_in_year=100)
        birthdays = simulator.generate_birthdays(50)
        assert np.all(birthdays >= 1)
        assert np.all(birthdays <= 100)
    
    def test_has_collision_with_duplicates(self):
        """Test collision detection with duplicate birthdays."""
        simulator = BirthdayParadoxSimulator()
        birthdays = np.array([1, 2, 3, 2, 5])  # Contains duplicate
        assert simulator.has_collision(birthdays) is True
    
    def test_has_collision_without_duplicates(self):
        """Test collision detection without duplicate birthdays."""
        simulator = BirthdayParadoxSimulator()
        birthdays = np.array([1, 2, 3, 4, 5])  # No duplicates
        assert simulator.has_collision(birthdays) is False
    
    def test_has_collision_all_same(self):
        """Test collision detection when all birthdays are the same."""
        simulator = BirthdayParadoxSimulator()
        birthdays = np.array([5, 5, 5, 5])
        assert simulator.has_collision(birthdays) is True
    
    def test_has_collision_single_birthday(self):
        """Test collision detection with single birthday (no collision)."""
        simulator = BirthdayParadoxSimulator()
        birthdays = np.array([5])
        assert simulator.has_collision(birthdays) is False
    
    def test_run_trials_return_structure(self):
        """Test that run_trials returns correct dictionary structure."""
        simulator = BirthdayParadoxSimulator(trials=100)
        result = simulator.run_trials(group_size=23)
        
        assert 'group_size' in result
        assert 'trials' in result
        assert 'collisions' in result
        assert 'probability' in result
        
        assert result['group_size'] == 23
        assert result['trials'] == 100
        assert isinstance(result['collisions'], int)
        assert isinstance(result['probability'], float)
    
    def test_run_trials_probability_range(self):
        """Test that probability is between 0 and 1."""
        simulator = BirthdayParadoxSimulator(trials=100)
        result = simulator.run_trials(group_size=23)
        assert 0.0 <= result['probability'] <= 1.0
    
    def test_run_trials_small_group(self):
        """Test that small groups have low collision probability."""
        simulator = BirthdayParadoxSimulator(trials=1000)
        result = simulator.run_trials(group_size=2)
        # With 2 people, probability should be very low (around 0.27%)
        assert result['probability'] < 0.05
    
    def test_run_trials_large_group(self):
        """Test that large groups have high collision probability."""
        simulator = BirthdayParadoxSimulator(trials=1000)
        result = simulator.run_trials(group_size=60)
        # With 60 people, probability should be very high (>99%)
        assert result['probability'] > 0.95
    
    def test_run_trials_collision_consistency(self):
        """Test that collision count matches probability calculation."""
        simulator = BirthdayParadoxSimulator(trials=100)
        result = simulator.run_trials(group_size=23)
        expected_probability = result['collisions'] / result['trials']
        assert result['probability'] == expected_probability
    
    def test_simulate_return_structure(self):
        """Test that simulate returns list of result dictionaries."""
        simulator = BirthdayParadoxSimulator(trials=100)
        group_sizes = [10, 20, 30]
        results = simulator.simulate(group_sizes)
        
        assert isinstance(results, list)
        assert len(results) == len(group_sizes)
        
        for i, result in enumerate(results):
            assert result['group_size'] == group_sizes[i]
    
    def test_simulate_single_group(self):
        """Test simulation with single group size."""
        simulator = BirthdayParadoxSimulator(trials=100)
        results = simulator.simulate([23])
        
        assert len(results) == 1
        assert results[0]['group_size'] == 23
    
    def test_simulate_increasing_probabilities(self):
        """Test that larger groups have higher probabilities."""
        simulator = BirthdayParadoxSimulator(trials=500)
        group_sizes = [5, 15, 25, 35, 45]
        results = simulator.simulate(group_sizes)
        
        probabilities = [r['probability'] for r in results]
        # Generally, probabilities should increase with group size
        # Allow for some statistical variation
        assert probabilities[-1] > probabilities[0]
    
    def test_generate_birthdays_randomness(self):
        """Test that birthday generation produces different results."""
        np.random.seed(42)
        simulator = BirthdayParadoxSimulator()
        birthdays1 = simulator.generate_birthdays(50)
        
        np.random.seed(43)
        birthdays2 = simulator.generate_birthdays(50)
        
        # They should not be identical
        assert not np.array_equal(birthdays1, birthdays2)


class TestComputeTheoreticalProbability:
    """Test suite for compute_theoretical_probability function."""
    
    def test_theoretical_probability_group_2(self):
        """Test theoretical probability for group size 2."""
        prob = compute_theoretical_probability(2)
        expected = 1 - (364 / 365)
        assert abs(prob - expected) < 1e-10
    
    def test_theoretical_probability_group_23(self):
        """Test theoretical probability for group size 23 (famous case)."""
        prob = compute_theoretical_probability(23)
        # Should be approximately 0.507
        assert 0.50 <= prob <= 0.51
    
    def test_theoretical_probability_group_50(self):
        """Test theoretical probability for group size 50."""
        prob = compute_theoretical_probability(50)
        # Should be approximately 0.97
        assert 0.96 <= prob <= 0.98
    
    def test_theoretical_probability_group_1(self):
        """Test theoretical probability for group size 1 (no collision possible)."""
        prob = compute_theoretical_probability(1)
        assert prob == 0.0
    
    def test_theoretical_probability_exceeds_days(self):
        """Test theoretical probability when group exceeds days in year."""
        prob = compute_theoretical_probability(366, days=365)
        # By pigeonhole principle, must be 1.0
        assert prob == 1.0
    
    def test_theoretical_probability_equals_days(self):
        """Test theoretical probability when group equals days in year."""
        prob = compute_theoretical_probability(365, days=365)
        # Should be very close to 1.0 but not exactly 1.0
        assert prob > 0.999
    
    def test_theoretical_probability_custom_days(self):
        """Test theoretical probability with custom days parameter."""
        prob_365 = compute_theoretical_probability(23, days=365)
        prob_366 = compute_theoretical_probability(23, days=366)
        # With more days, probability should be slightly lower
        assert prob_366 < prob_365
    
    def test_theoretical_probability_increasing(self):
        """Test that probability increases with group size."""
        probs = [compute_theoretical_probability(i) for i in range(1, 51)]
        # Each probability should be >= the previous one
        for i in range(1, len(probs)):
            assert probs[i] >= probs[i-1]
    
    def test_theoretical_probability_range(self):
        """Test that theoretical probability is always between 0 and 1."""
        for group_size in [1, 10, 23, 50, 100, 365, 400]:
            prob = compute_theoretical_probability(group_size)
            assert 0.0 <= prob <= 1.0


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_zero_trials(self):
        """Test simulation with zero trials."""
        simulator = BirthdayParadoxSimulator(trials=0)
        # Zero trials will cause a division by zero error
        with pytest.raises(ZeroDivisionError):
            result = simulator.run_trials(group_size=23)
    
    def test_one_trial(self):
        """Test simulation with a single trial."""
        simulator = BirthdayParadoxSimulator(trials=1)
        result = simulator.run_trials(group_size=23)
        assert result['trials'] == 1
        assert result['probability'] in [0.0, 1.0]
    
    def test_empty_group_sizes(self):
        """Test simulation with empty group sizes list."""
        simulator = BirthdayParadoxSimulator(trials=100)
        results = simulator.simulate([])
        assert results == []
    
    def test_leap_year_simulation(self):
        """Test simulation with leap year (366 days)."""
        simulator = BirthdayParadoxSimulator(days_in_year=366, trials=500)
        result = simulator.run_trials(group_size=23)
        # Probability should be slightly less than with 365 days
        assert 0.0 <= result['probability'] <= 1.0
    
    def test_very_small_year(self):
        """Test simulation with very few days in year."""
        simulator = BirthdayParadoxSimulator(days_in_year=10, trials=500)
        result = simulator.run_trials(group_size=5)
        # With only 10 days and 5 people, collision probability should be significant
        assert result['probability'] > 0.2


class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_full_simulation_workflow(self):
        """Test complete simulation workflow."""
        simulator = BirthdayParadoxSimulator(trials=100)
        group_sizes = [10, 20, 30]
        results = simulator.simulate(group_sizes)
        
        # Verify all results
        assert len(results) == 3
        for i, result in enumerate(results):
            assert result['group_size'] == group_sizes[i]
            assert result['trials'] == 100
            assert 0.0 <= result['probability'] <= 1.0
    
    def test_empirical_vs_theoretical_alignment(self):
        """Test that empirical results align with theoretical values."""
        # Use many trials for better accuracy
        simulator = BirthdayParadoxSimulator(trials=5000)
        
        test_cases = [10, 23, 50]
        for group_size in test_cases:
            result = simulator.run_trials(group_size)
            theoretical = compute_theoretical_probability(group_size)
            empirical = result['probability']
            
            # Empirical should be within 5% of theoretical (allowing for random variation)
            difference = abs(empirical - theoretical)
            assert difference < 0.05, (
                f"Group size {group_size}: empirical {empirical:.4f} "
                f"differs from theoretical {theoretical:.4f} by {difference:.4f}"
            )
    
    def test_reproducibility_with_seed(self):
        """Test that results are reproducible with same random seed."""
        np.random.seed(12345)
        simulator1 = BirthdayParadoxSimulator(trials=100)
        result1 = simulator1.run_trials(group_size=23)
        
        np.random.seed(12345)
        simulator2 = BirthdayParadoxSimulator(trials=100)
        result2 = simulator2.run_trials(group_size=23)
        
        # Results should be identical with same seed
        assert result1['collisions'] == result2['collisions']
        assert result1['probability'] == result2['probability']
