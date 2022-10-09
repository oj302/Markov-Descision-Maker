import dice_game as dg
import numpy as np

from abc import ABC, abstractmethod


class DiceGameAgent(ABC):
    def __init__(self, game):
        self.game = game
    
    @abstractmethod
    def play(self, state):
        pass


class AlwaysHoldAgent(DiceGameAgent):
    def play(self, state):
        print(state[0])
        return (0, 1, 2)


class PerfectionistAgent(DiceGameAgent):
    def play(self, state):
        if state == (1, 1, 1) or state == (1, 1, 6):
            return (0, 1, 2)
        else:
            return ()
        
#my agents
        
class HybridAgent(DiceGameAgent): #theoretically would always hold instead of ever rolling for perfection
                                    #mean score of perfectionist is negative
    def play(self, state):
        # This gives you the current score if you end the game now.
        score = current_score = self.game.get_score()
        #print(state)
        #print(score)
        if(state == (1, 1, 1) or state == (1, 1, 6)):
            return(0, 1, 2)
        elif(state[0] == 1 and state[1] == 1 and score < 18 - 3):
            return(0, 1)
        elif(state[0] == 1 and state[2] == 6 and score < 18 - 6):
            return(0, 2)
        else:
            return(0, 1, 2)
        #elif(state[0] == 1 and state[1] == 1)
        # Your Code Here
        #pass


class OneStepValueIterationAgent(DiceGameAgent):
    def __init__(self, game):
        super().__init__(game)
        self.gamma = 1.0
        
        # Your Code Here
        self.values = np.zeros(len(self.game.states), dtype = float)
        
        _, self.values = self.perform_single_value_iteration()
        print(self.values)
        _, self.values = self.perform_single_value_iteration()
        print(self.values)
        print("\n\n\n")
    
    def perform_single_value_iteration(self): #!!!!!old single value iteration, works for gamma = 1!!!!!!
        # Your Code Here
        delta = 0 #not needed for single iteration???
        new_values = np.zeros(len(self.values), dtype = float)
        
        for i in range(0, len(self.values)):
            if(self.values[i] == 0):
                #should assign the value of each state to be the result of holding it if its uninitialised
                _, _, new_values[i], _ = self.game.get_next_states((0, 1, 2), self.game.states[i])
                #print(new_values[i])
            else:
                #for each action that can be taken from the state estimate new value of state using equation
                #updated value of state becomes the highest new value based on action
                currentHighest = 0
                for action in self.game.actions [0: len(self.game.actions) -1]: #every action in the current state apart from holding
                    total = -self.game._penalty
                    #every outcome from that action
                    outcomes, game_over, rewards, probabilities = game.get_next_states(action, self.game.states[i])
                    for outcome, probability in zip(outcomes, probabilities):
                        total += probability * (self.gamma * self.values[ self.game.states.index(outcome)])
                        #self.values[ self.game.states.index(outcome)] = the old value of the state being summed
                    if(total > currentHighest):
                        currentHighest = total
    
                _, _, holdReward, _ = self.game.get_next_states((0, 1, 2), self.game.states[i]) #testing hold action
                if(holdReward > currentHighest):
                    currentHighest = holdReward
                
                
                if(new_values[i] - self.values[i] > delta):
                    delta = new_values[i] - self.values[i] #supposed to be the biggest change this iteration???
                new_values[i] = currentHighest
        
        return delta, new_values
    
    def play(self, state):
        """
        given a state, return the chosen action for this state
        at minimum you must support the basic rules: three six-sided fair dice
        
        if you want to support more rules, use the values inside self.game, e.g.
            the input state will be one of self.game.states
            you must return one of self.game.actions
        
        read the code in dicegame.py to learn more
        """
        # Your Code Here
        ret = 0
        currentHighest = 0
        for action in self.game.actions [0: len(self.game.actions) -1]: #every action in the current state apart from holding
            total = -self.game._penalty
            #every outcome from that action
            outcomes, game_over, rewards, probabilities = game.get_next_states(action, state)
            for outcome, probability in zip(outcomes, probabilities):
                total += probability * (self.gamma * self.values[ self.game.states.index(outcome)])
                #self.values[ self.game.states.index(outcome)] = the old value of the state being summed
            if(total > currentHighest):
                currentHighest = total
                ret = action
        _, _, holdReward, _ = self.game.get_next_states((0, 1, 2), state) #testing hold action
        print("hold reward is: ",holdReward)
        if(holdReward > currentHighest):
            currentHighest = holdReward
            ret = self.game.actions[len(self.game.actions) -1]
            
        print("best action has value of ",currentHighest," and is ",ret)
            
        return ret
    
    
import time

class ValueIterationAgent(DiceGameAgent):
    def __init__(self, game):
        super().__init__(game)
        
        self.values = np.zeros(len(self.game.states), dtype = float)
        self.theta = 0.01
        self.gamma = 0.97
        
        self.value_iteration()
        
    
    def perform_single_value_iteration(self):
        delta = 0
        new_values = np.zeros(len(self.values), dtype = float)
        
        for i in range(0, len(self.values)):
            if(self.values[i] == 0):
                #should assign the value of each state to be the result of holding it if its uninitialised
                _, _, new_values[i], _ = self.game.get_next_states((0, 1, 2), self.game.states[i])
                new_values[i] /= 2
                delta = -1
                #print(new_values[i])
            else:
                #for each action that can be taken from the state estimate new value of state using equation
                #updated value of state becomes the highest new value based on action
                currentHighest = 0
                for action in self.game.actions [0: len(self.game.actions) -1]: #every action in the current state apart from holding
                    total = -self.game._penalty
                    #every outcome from that action
                    outcomes, game_over, rewards, probabilities = game.get_next_states(action, self.game.states[i])
                    for outcome, probability in zip(outcomes, probabilities):
                        total += probability * (self.gamma * self.values[ self.game.states.index(outcome)])
                        #self.values[ self.game.states.index(outcome)] = the old value of the state being summed
                    if(total > currentHighest):
                        currentHighest = total
    
                _, _, holdReward, _ = self.game.get_next_states((0, 1, 2), self.game.states[i]) #testing hold action
                if(holdReward > currentHighest):
                    currentHighest = holdReward
                
                
                new_values[i] = currentHighest
                if(new_values[i] - self.values[i] > delta):
                    delta = new_values[i] - self.values[i]
        
        return delta, new_values
        
    def value_iteration(self):
        #initialising delta as higher than theta
        delta = self.theta + 1
        
        counter = 0
        while(delta > self.theta or delta == -1):
            counter += 1 #for debugging
            delta, self.values = self.perform_single_value_iteration()
    
    def play(self, state):
        """
        given a state, return the chosen action for this state
        at minimum you must support the basic rules: three six-sided fair dice
        
        if you want to support more rules, use the values inside self.game, e.g.
            the input state will be one of self.game.states
            you must return one of self.game.actions
        
        read the code in dicegame.py to learn more
        """
        ret = 0
        currentHighest = 0
        for action in self.game.actions [0: len(self.game.actions) -1]: #every action in the current state apart from holding
            total = -self.game._penalty
            #every outcome from that action
            outcomes, game_over, rewards, probabilities = game.get_next_states(action, state)
            for outcome, probability in zip(outcomes, probabilities):
                total += probability * (self.gamma * self.values[ self.game.states.index(outcome)])
                #self.values[ self.game.states.index(outcome)] = the old value of the state being summed
            if(total > currentHighest):
                currentHighest = total
                ret = action
        _, _, holdReward, _ = self.game.get_next_states((0, 1, 2), state) #testing hold action
        print("hold reward is: ",holdReward)
        if(holdReward > currentHighest):
            currentHighest = holdReward
            ret = self.game.actions[len(self.game.actions) -1]
            
        print("best action has value of ",currentHighest," and is ",ret)
            
        return ret
    
    
def play_game_with_agent(agent, game, verbose=False):
    state = game.reset()
    
    if(verbose): print(f"Testing agent: \n\t{type(agent).__name__}")
    if(verbose): print(f"Starting dice: \n\t{state}\n")
    
    game_over = False
    actions = 0
    while not game_over:
        action = agent.play(state)
        actions += 1
        
        if(verbose): print(f"Action {actions}: \t{action}")
        _, state, game_over = game.roll(action)
        if(verbose and not game_over): print(f"Dice: \t\t{state}")

    if(verbose): print(f"\nFinal dice: {state}, score: {game.score}")
        
    return game.score


if __name__ == "__main__":
    # random seed makes the results deterministic
    # change the number to see different results
    # or delete the line to make it change each time it is run
    game = dg.DiceGame()
        
    #agent1 = AlwaysHoldAgent(game)
    #agent2 = PerfectionistAgent(game)
    #agent3 = HybridAgent(game)
    #agent4 = ManualAgent(game)
    #agent5 = OneStepValueIterationAgent(game)
    agent6 = ValueIterationAgent(game)
    
    
    count = 0
    for i in range(1, 256):
        np.random.seed(i)
        
        count += play_game_with_agent(agent6, game, verbose = False)
    
    print(count / 255)
    

