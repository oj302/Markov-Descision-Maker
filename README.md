# Markov-Descision-Maker
## Description
An agent that finds the optimal action from any given state in a made up dice game using value iteration.

Included in the repository is dice_game.py which holds all of the code for the rules of the game and lets you play the game when run. Agents.py holds the code for the agents which have been desgined to play the game. The most successful and impressive of which being ValueIterationAgent which automatically runs 100 games and averages its score when the Agents file is run.

This agent works with many variations of the dice game (more dice, more numbers on dice ect.). Different variation can be played by changing the parameters when creating a dicegame object

## Dice Game Rules
* You start with 0 points
* Roll three fair six-sided dice
* Now choose one of the following:

   * Stick, accept the values shown. If two or more dice show the same values, then all of them are flipped upside down: 1 becomes 6, 2 becomes 5, 3 becomes 4, and vice versa. The total is then added to your points and this is your final score.
   * Reroll the dice. You may choose to hold any combination of the dice on the current value shown. Rerolling costs you 1 point – so during the game and perhaps even at the end your score may be negative. You then make this same choice again.

The best possible score for this game is 18 and is achieved by rolling three 1s on the first roll.

The reroll penalty prevents you from rolling forever to get this score. If the value of the current dice is greater than the expected value of rerolling them (accounting for the penalty), then you should stick.

The optimal decision is independent of your current score. It does not matter whether it is your first roll with a current score of 0, or your twentieth roll with a current score of -19 (in which case a positive end score is impossible), in either of these cases if you roll three 6s (which, if you stick, will only add 3 points) then you still expect to get a better end score by rerolling and taking the penalty. Almost any other roll will beat it, so it's still the right choice to maximise your score.

Credit to University of Bath Computer Science department for designing the game and writing the dice_game.py file.

## Algortihm Overview
The algorithm stores values for every possible state (dice combination) representing how good they are. 
These values are initialised at the score you would receive if you rolled these values on your first roll and held all of your dice (e.g. 4, 4, 5 would be valued at an 11)

The agent then uses value iteration to find a closer estimate to the "true" value of each state.
More specifically, the Bellman equation is used to update state values each iteration.
It does this by selecting a state and testing all possible actions from that state.
Every action will have a return value and the state is assigned the highest action return value.

Action return values are calculated as follows:

  p     = probability of this outcome occuring
  
  r     = reward for taking action (in the case of the dice game rewards will be -1 unless the action is holding all dice)
  
  gamma = discount factor (represents how highly future rewards are valued over current rewards)
  
  osv   = outcome state value
  
  return value = The sum of p*( r + (gamma * osv) ) for every outcome of the action

Once the algorithm has iterated enough times such that the change in state values are negligable (a parameter delta is used, if any states value changes more than delta iteration continues) iteration stops and the agent is ready to play the dice game.

When playing the agent simply chooses the highest valued action from its current state until the highest valued action is to hold its dice.
