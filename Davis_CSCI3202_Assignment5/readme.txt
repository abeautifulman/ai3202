README for Assignment 5 in CSCI3202: Artificial Intelligence

Can you find a value that changes the solution path of your program?

For my program I did all of my initial testing with the Epsilon value of 0.5, which was able to successfully find a path to the terminal node. After completing the assignment I played with the Epsilon value, which is used to calculate the maximum allowable error for the termination condition. 

I first checked values between .5 and 0, although this did not seem to change the path. I then tried counting up (by whole integers) until I got to an Epsilon value of 44. This changed the path of the search - it opts to go through 2 mountain spaces instead of a snake space (going up to begin instead of right.)

I believe this may have something to do with the fact that the Value Iteration function runs 43 times with an Epsilon value of .5, though I am not sure. Seemingly the lower the epsilon value, the greater number of steps it takes to converge upon a solution.