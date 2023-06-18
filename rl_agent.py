reward_matrix = [[[1, 1], # Both players split
                [0, -1], # Player 1 splits, player 2 steals
                [2, 0], # Player 1 steals, player 2 splits
                [0, 0]]] # Both players steal


import random
from collections import defaultdict
import numpy as np

class RLAgent:
  def __init__(self):
  
    # Learning rate
    self.alpha = 0.5
    # Discount factor
    self.gamma = 0.9
    # Exploration rate
    self.epsilon = 0.1
    # Lembrando a ultima acao
    self.last_opponent_action = None
    # Flag indicando se essa seria a ultima rodada
    self.last_round = False   
    # Q table
    self.Q = defaultdict(lambda: [0.0, 0.0])
    self.action_list = ["split", "steal"]
    
    self.current_input = None
    self.current_output = None    
    
  def extract_rl_state(self, state):
    return (state[-3], np.sign(state[-2]));
 
  def choose_action(self, state):
    state = self.extract_rl_state(state)
    if np.random.uniform(0, 1) < self.epsilon:
      # Explore: Choose a random action
      action = np.random.choice(["split", "steal"])
    else:
      # Exploit: Choose the action with the maximum Q-value
      action = self.action_list[np.argmax(self.Q[state])]
    return action
    
    
  def update_qtable(self, state, action, reward1, reward2, next_state):
    alp = self.alpha
    gam = self.gamma
    action_index = self.action_list.index(action)
    state = self.extract_rl_state(state)
    next_state = self.extract_rl_state(next_state)
    self.Q[state][action_index] = (1 - alp) * self.Q[state][action_index] + alp * (reward1 + reward2 + gam * np.max(self.Q[next_state]))  
    
  # Nome de seu agente deve ser colocado aqui  
  def get_name(self):
    return "SimpleRL"

  def decision(self, amount, rounds_left, your_karma, his_karma):
    print(f"{amount=}, {rounds_left=}, {your_karma=}, {his_karma=}")
    self.last_round = True if rounds_left == 0 else False
    
    novel_input = (amount, rounds_left, your_karma, his_karma, self.last_round)
    if (self.current_input is not None):
      self.update_qtable(self.current_input, self.current_output[0], self.current_output[-1], novel_input)
      
    self.current_input = novel_input

    print(self.Q)
    return self.choose_action(self.current_input)

  # Receba as acoes de cada agente e o reward obtido (vs total possivel)
  def result(self, your_action, his_action, total_possible, reward1, reward2):
    if self.last_round:
      print("Forgetting last opponent action") # Vamos mudar de agente
      self.last_opponent_action = None
    else:   
      self.last_opponent_action = his_action
      print(f"For {self.get_name()=} {self.last_opponent_action=} ")   
    
    # if your_action == "steal" and his_action == "steal": 
    #   reward = +0
    # elif your_action == "steal" and his_action == "split":
    #   reward = +2
    # elif your_action == "split" and his_action == "split":
    #   reward = +1
    # elif your_action == "split" and his_action == "steal":
    #   reward = -1
    # self.current_output = (your_action, his_action, total_possible, reward )
    


    if your_action == 0 and his_action == 0: # Both players cooperate
            reward1 = reward_matrix[0][0][0]
            reward2 = reward_matrix[0][0][1]
    elif your_action == 0 and his_action == 1: # Only player 2 steals
             reward1 = reward_matrix[0][1][0]
             reward2 = reward_matrix[0][1][1]
    elif your_action == 1 and his_action == 0: # Only player 1 steals
             reward1 = reward_matrix[0][2][0]
             reward2 = reward_matrix[0][2][1]
    elif your_action == 1 and his_action == 1: # Both players steal
             reward1 = reward_matrix[0][3][0]
             reward2 = reward_matrix[0][3][1]

    total_reward1 = reward1
    total_reward2 = reward2

    self.current_output = (your_action, his_action, total_possible, reward1, reward2 )



