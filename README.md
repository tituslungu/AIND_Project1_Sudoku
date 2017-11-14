# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: By applying naked_twins in the same iterative manner as elimate and only_choice in reduce_puzzle, we look for obvious constraints and indications for how we can reduce the Sudoku board. Within the while loop, after applying eliminate and only_choice, we apply naked_twins. naked_twins looks for two identical boxes of doubles in each unit on the board and, if any are found, eliminates those values from the other boxes in the unit. This helps us reduce the complexity of the board by reducing the number of options in the other boxes since we know that the two values in the naked twins must belong to those two boxes, and therefore cannot be part of any other box in the unit.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: For diagonal sudoku, we create two more units - one for each nine-box diagonal across the board - and add the other boxes on a diagonal as peers for each box on that diagonal. Since eliminate, only_choice, and naked_twins all use the unitlist or peers to perform constraint propogation, our additional constraint of diagonality will automatically be checked for and applied to our board with those respective functions.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

