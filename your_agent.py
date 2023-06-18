import random
import sys
   

class AgentQ:
    def __init__(self, memory):
        self.wins = 0 # Number of times agent has won an episode
        self.losses = 0 # Number of times agent has lost an episode
        self.Q = {} # Stores the quality of each action in relation to each state
        self.memory = memory # The number of previous states the agent can factor into its decision
        self.epsilon_counter = 1 # Inversely related to learning rate


#  # Lembrando a ultima acao
        self.last_opponent_action = None
    
#     # Flag indicando se essa seria a ultima rodada
        self.last_round = False
    
#   # Nome de seu agente deve ser colocado aqui  
#     def QAgent(self):
#      return "Grupo/Apelido"
        

    def get_q(self, state):
        quality1 = self.Q[str(state[-self.memory:])][0]
        quality2 = self.Q[str(state[-self.memory:])][1]

        return quality1, quality2

    def set_q(self, state, quality1, quality2):
        self.Q[str(state[-self.memory:])][0] = quality1
        self.Q[str(state[-self.memory:])][1] = quality2

    def normalize_q(self, state):
        quality1, quality2 = self.get_q(state)

        normalization = min(quality1, quality2)

        self.set_q(state, (quality1 - normalization) * 0.95, (quality2 - normalization) * 0.95)

    def max_q(self, state):
        quality1, quality2 = self.get_q(state)

        if quality1 == quality2 or random.random() < (1 / self.epsilon_counter):
            return random.randint(0, 1)
        elif quality1 > quality2:
            return 0
        else:
            return 1

    def pick_action(self, state):
        # Decrease learning rate
        self.epsilon_counter += 0.5

        # If the given state was never previously encountered
        if str(state[-self.memory:]) not in self.Q:
            # Initialize it with zeros
            self.Q[str(state[-self.memory:])] = [0, 0]
    
        return self.max_q(state)

    def reward_action(self, state, action, reward):
        # Increase the quality of the given action at the given state
        self.Q[str(state[-self.memory:])][action] += reward

        # Normalize the Q matrix
        self.normalize_q(state)

    def mark_victory(self):
        self.wins += 1

    def mark_defeat(self):
        self.losses += 1

    def analyse(self):
        # What percentage of games resulted in victory/defeat
        percent_won = 0
        if self.wins > 0:
            percent_won = float(self.wins) / (self.wins + self.losses)
        
        
        percent_lost = 0
        if self.losses > 0:
            percent_lost = float(self.losses) / (self.wins + self.losses)
        

        # How many states will result in cooperation/defection
        times_splited = 0
        times_stealed = 0

        for state in self.Q:
            action = self.max_q(eval(state))

            if action == 0:
                times_splited += 1
            else:
                times_stealed += 1

        # What percentage of states will result in cooperation/defection
        percent_cooperated = 0
        if times_splited > 0:
            percent_cooperated = float(times_splited) / len(self.Q)

        '''
        percent_defected = 0
        if times_defected > 0:
            percent_defected = float(times_defected) / len(self.Q)
        '''

        # Return most relevant analysis
        return self.wins, percent_won, percent_cooperated
    
        #return self.losses, percent_lost , percent_defected

    def reset_analysis(self):
        self.wins = 0
        self.losses = 0



  # Um exemplo basico de algo proximo de tit-for-tat
  # apenas como demonstracao. Agente de aprendizagem
  # por reforco seria o objetivo

  # def decision(self, amount, rounds_left, your_karma, his_karma):
  #   print(f"{amount=}, {rounds_left=}, {your_karma=}, {his_karma=}")
  #   self.last_round = True if rounds_left == 0 else False
    
  #   if self.last_opponent_action is None:
  #     return "split"
  #   elif self.last_opponent_action == "split":
  #     return "split"
  #   elif self.last_opponent_action == "steal":
  #     return "steal"
  #   else:
  #     raise RuntimeError("Unknown action")

  # # Receba as acoes de cada agente e o reward obtido (vs total possivel)
  # def result(self, your_action, his_action, total_possible, reward):
  #   if self.last_round:
  #     print("Forgetting last opponent action") # Vamos mudar de agente
  #     self.last_opponent_action = None;
  #   else:   
  #     self.last_opponent_action = his_action;
  #     print(f"For {self.get_name()=} {self.last_opponent_action=} ")   









# #
# import random
# import numpy as np 

# class ReinforcementLearningAgent:
#   # Nome de seu agente deve ser colocado aqui  
#   def get_name(self):
#     return "your_agent"
  
#   def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.1):
#     self.q_values = {}
    
#     # Lembrando a ultima acao
#     self.last_opponent_action = None
    
#     # Flag indicando se essa seria a ultima rodada
#     self.last_round = False
    
#     #learning rate
#     self.alpha = alpha
    
#     #discount factor
#     self.gamma = gamma
    
#     #exploration rate
#     self.epsilon = epsilon     
    
#   def get_q_values(self, state, action):
#     return self.q_values.get((state, action), 0.0)
    
#   def update_q_values(self, state, action, value):
#     self.q_values[(state, action)] = value

#   # Um exemplo basico de algo proximo de tit-for-tat
#   # apenas como demonstracao. Agente de aprendizagem
#   # por reforco seria o objetivo
#   #def decision(self, amount, rounds_left, your_karma, his_karma):
#    # print(f"{amount=}, {rounds_left=}, {your_karma=}, {his_karma=}")
#     #self.last_round = True if rounds_left == 0 else False
    
#     #if self.last_opponent_action is None:
#     #  return "split"
#     #elif self.last_opponent_action == "split":
#     #  return "split"
#     #elif self.last_opponent_action == "steal":
#     #  return "steal"
#     #else:
#     #  raise RuntimeError("Unknown action")

#   def choose_action(self, state):
#         if random.random() < self.epsilon:
#             return random.choice(["split", "steal"])
#         else:
#             split_q = self.get_q_value(state, "split")
#             steal_q = self.get_q_value(state, "steal")
#             if split_q > steal_q:
#                 return "split"
#             else:
#                 return "steal"
  
#   REWARD_SPLIT = 2
#   REWARD_STEAL = 3
#   PENALTY = -1

#   OUTCOMES = {
#     ("split", "split"): (REWARD_SPLIT, REWARD_SPLIT),
#     ("split", "steal"): (PENALTY, REWARD_STEAL),
#     ("steal", "split"): (REWARD_STEAL, PENALTY),
#     ("steal", "steal"): (0, 0),
#   }
  
#   def train(self, episodes):
#         for _ in range(episodes):
#             state = "start"
#             while state != "end":
#                 action = self.choose_action(state)
#                 reward = OUTCOMES[(state, action)]
#                 next_state = "end"  # Assuming the game ends after one round

#                 current_q = self.get_q_value(state, action)
#                 max_q = max(self.get_q_value(next_state, "split"), self.get_q_value(next_state, "steal"))
#                 new_q = (1 - self.alpha) * current_q + self.alpha * (reward + self.gamma * max_q)
#                 self.update_q_value(state, action, new_q)

#                 state = next_state

#   # Receba as acoes de cada agente e o reward obtido (vs total possivel)
#   #def result(self, your_action, his_action, total_possible, reward):
#   #  if self.last_round:
#   #    print("Forgetting last opponent action") # Vamos mudar de agente
#   #    self.last_opponent_action = None;
#   #  else:   
#   #    self.last_opponent_action = his_action;
#   #    print(f"For {self.get_name()=} {self.last_opponent_action=} ")    
#   def play(self):
#         state = "start"
#         while state != "end":
#             action = self.choose_action(state)
#             print("Agent chooses:", action)
#             state = "end"  # Assuming the game ends after one round

# # Create an instance of the agent and train it
# agent = ReinforcementLearningAgent()
# agent.train(episodes=1000)

# # Play the game using the trained agent
# agent.play()
