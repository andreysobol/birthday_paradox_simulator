Birthday Paradox Simulator
Overview
The Birthday Paradox Simulator is a probabilistic experiment framework designed to empirically estimate the likelihood that at least two individuals in a group share the same birthday.
Despite the counter-intuitive nature of the birthday paradox, the simulator demonstrates how collision probability grows rapidly as group size increases, validating theoretical results through Monte Carlo simulation.
Objective
To compute and visualize the probability of birthday collisions as a function of group size by running repeated randomized trials.
Methodology
1. Assumptions
A year has 365 days (ignoring leap years).
Birthdays are uniformly distributed across days.
Each trial samples birthdays independently.
2. Simulation Procedure
For each group size 
n
n:
Generate 
n
n random integers in range 
[
1
,
365
]
[1,365].
Interpret each integer as a simulated birthday.
Check for duplicates (birthday collisions).
Record whether a collision occurred.
Repeat for 
T
T trials.
