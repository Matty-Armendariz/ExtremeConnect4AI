Project 2
Matty Armendariz
Python 3.10.1
What OS and its version are used to compile and run the codes.
Windows 11 Home | version: 21H2 | OS Build: 22000.613

Please install the colorama and numpy library if you do not have them already

* Commands and their expected outputs are in the commands.txt file *
* Instructions To Run the Code: 


* How The Code is constructed:

Note : I did not have time to implement a functional GUI so I used colorama library to at least make it pretty and easy to follow as you play the computer
Also using higher depths such as Depth 7 and 8 will take a few seconds to run but DO run so please just be patient :)

First the program reads in the input file and constructs the matrix that represents the connect 4 board. The game then checks what mode the game is in and then goes to the appropriate version of the game.

If the mode is interactive, it will then check the sys arg that was entered to tell you if it is the humans's turn or the AI turn and the number value telling you who is next on the input file and it assigns the human and the AI the appropriate value. You can then continue to play all cells have been filled up. 

If you chose one-move mode, it will take in all of the information from the sys args and make one move from only one of the players. You will repeatedly have to switch the red and green output text files for the program to run like a normal game

*** Explanation of the minimax and alpha-beta pruning ***
The minimax function is by far the longest function in the code and is not hard to spot when parsing through the code. The function intakes the following variables:
board, depth, alpha, beta, maximizing player turn?, MaximizingPlayer's number, and MinimizingPlayer's number

Where alpha and beta are always passed in as -inf and inf respectively on the first call of the fuction.

The code then checks if the MaximizingPlayer's turn variable is true and if so it will run through the loop in which to optimize the outcome. A recursive function of the minimax function is then called but the depth is decremented by 1, the MaximizingPlayer
s turn variable is set to false and a temporary board is passed into board (to prevent messing up the original board). This will then recall the function and hit the minimizing portion of the function. Where it will basically do the same thing but it will try to minimize the score. This goes back and forth.
After the recursive call returns it is stored to the newScore variable and compared to the existing value to see if it is a better or worse outcome and if it better the value is set to the result of the recursive function and the best column is set to the column that is also returned by the minimax function. After this, if you are the Maximizing player you will analyze the max falue of the Alpha (originally set to -inf) and the value from above and stores that value as the new alpha. The same thing happens with the Beta but it is trying to minimize the value so it stores the min value. Then alpha is compared to beta to determine if you should break/prune that branch.

In addition to this there are other smaller functions that help do repetative tasks, but the most important one that I can think of is the scoring function which evaluates the board and gives ceratain points for different scenarios. 
For example, the player calling the scoring function has 2 pieces in a row it will add a small amount of points to the score, if the player has 3 pieces in a row, that will add a some more points to the score (more than two in a row) if there are 4 in a row, the score gets +100 to incentivise getting 4 in a row since that is points. In addition if the opposing player has 3 in a row it will subtract points that way the AI is incentivised to block you when you are trying to score. 

These are the high points of the program, please reach out to me if you have any further questions about how my project works!
Thank you !!! 


* Compiling Instructions: 

There are no specific compiling constructions, your should be good to go as long as you are running the same python version.