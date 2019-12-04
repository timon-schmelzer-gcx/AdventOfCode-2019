My AdventOfCode Solutions (2019)
================================

To install the required dependencies, install [miniconda](https://docs.conda.io/en/latest/miniconda.html) and execute:

```
conda env create -f environment.yml
conda activate aoc
```

Run this bash script to recalculate the solution for all days:

```
for DAY in `ls days`; do echo "Day $DAY: " && cd days/$DAY && python solution.py && cd ../../; done
```
