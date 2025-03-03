# NonogramSolverUsingLP
An interactive Nonogram puzzle game with a built-in solver powered by Linear Programming. Play Nonograms manually or let the solver find optimal solutions using mathematical optimization.

## Feature
- Play Nonogram puzzles interactively
- Solve puzzles using a Linear Programming-based solver
- New puzzle can be added to puzzles bank.

## Installation
- Ensure you have Python 3.7+ installed. 
- Make sure you have installed **gurobipy** and **tk** package.

## Usage

### Run the application

```sh
python src.py
```

### Choose difficulty of the puzzle
- **"Easy"**: A 5 x 5 puzzle
- **"Hard"**: 10 x 10 puzzle
- **"Exit"**: exit the program

![Interface](https://github.com/minhtran0901/NonogramSolverUsingLP/blob/main/Interface.png)

### Play Nonogram
- Click on the grid to color it
- Click **"Check"** to see if your solution is correct
- Click **"Solve"** to see the solution
### Example Screenshots:
- Unsolved Puzzle:
  
![unsolved problem](https://github.com/minhtran0901/NonogramSolverUsingLP/blob/main/unsolved%20easy%20puzzle.png)

- Solved Puzzle:

![solved problem](https://github.com/minhtran0901/NonogramSolverUsingLP/blob/main/solved%20hard%20puzzle.png)

## References
- Nonogram rules: Find the rules here (https://en.wikipedia.org/wiki/Nonogram)
- Scientific paper on LP for Nonogram solving: Read the paper here (https://www.researchgate.net/publication/220773955_Colored_Nonograms_An_Integer_Linear_Programming_Approach)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
