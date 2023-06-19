## Analysis of Data from the SC2 World Championship

*Read this in: [RU](README_ru.md), [DE](README_de.md), [EN](README.md)*

The StarCraft 2 World Championship in Katowice has recently concluded. In addition to the games themselves, it has provided an interesting data analysis task. The organizers have done extensive work and created a profile for each player, assigning numerical ratings to their parameters (e.g., speed). Consequently, it is interesting to determine which parameter correlates the most with a player's ranking.

## Input

The input consists of a CSV file containing participant data. An example is in the data directory.

## Output

A sorted list of ratings from best to worst for all possible parameters.

## Algorithm

For each player and each parameter, we have a set of data points (player's final ranking, parameter value). We will calculate correlation using two methods: absolute values (Pearson's method) and ranks (Spearman's method). In both cases, the result will be in the range (-1, 1) with a p-value indicating the level of confidence in the results.

## Result

```
parameter          Pear   PearP  Spear  SpearP
['place',          0.99,  0.00,  1.00,  0.00]
['versatility',   -0.65,  0.00,  0.66,  0.00]
['avg',           -0.53,  0.01,  0.49,  0.01]
['multitasking',  -0.46,  0.02,  0.49,  0.02]
['speed',         -0.45,  0.03,  0.49,  0.02]
['offense',       -0.42,  0.04,  0.46,  0.02]
['mechanics',     -0.5,   0.01,  0.43,  0.04]
['ept_points',    -0.34,  0.11,  0.33,  0.11]
['defense',       -0.36,  0.08,  0.33,  0.12]

```

## Analysis of Results

TBD
