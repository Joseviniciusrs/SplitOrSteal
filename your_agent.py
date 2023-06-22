import random
import sys

class AgentQ:
    def __init__(self, memory):
        self.wins = 0 # Number of times agent has won an episode
        self.losses = 0 # Number of times agent has lost an episode
        self.Q = {} # Stores the quality of each action in relation to each state
        self.memory = memory # The number of previous states the agent can factor into its decision
        self.epsilon_counter = 1 # Inversely related to learning rate   -  Adjust how much of new information should be taken into account by the agents
    
#  # Lembrando a ultima acao
        self.last_opponent_action = None
    
#     # Flag indicando se essa seria a ultima rodada
        self.last_round = False
    
#   # Nome de seu agente deve ser colocado aqui  

    def get_name(self):
      return "AgenteQ"
        
        # help determine the best action to take based on its current state
    def get_q(self, state):
        quality1 = self.Q[str(state[-self.memory:])][0]
        quality2 = self.Q[str(state[-self.memory:])][1]

        return quality1, quality2

          # updates the Q dictionary with new quality values based on the state of the agent
    def set_q(self, state, quality1, quality2):
        self.Q[str(state[-self.memory:])][0] = quality1
        self.Q[str(state[-self.memory:])][1] = quality2

        # ensures that the Q-values does not overshadow each other
    def normalize_q(self, state):
        quality1, quality2 = self.get_q(state)

        normalization = min(quality1, quality2)

        self.set_q(state, (quality1 - normalization) * 0.95, (quality2 - normalization) * 0.95)

        # selects the action that the agent should take based on the quality values of actions for a given state

    def max_q(self, state):
        quality1, quality2 = self.get_q(state)

        if quality1 == quality2 or random.random() < (1 / self.epsilon_counter): # ensures that the agent explores the environment even after it has learned optimal action
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
        
        
        # percent_lost = 0
        # if self.losses > 0:
        #     percent_lost = float(self.losses) / (self.wins + self.losses)
        

        # How many states will result in split/steal
        times_splited = 0
        times_stealed = 0

        for state in self.Q:
            action = self.max_q(eval(state))

            if action == 0:
                times_splited += 1
            else:
                times_stealed += 1

        # What percentage of states will result in split/steal
        percent_splited = 0
        if times_splited > 0:
            percent_splited = float(times_splited) / len(self.Q)

        '''
        percent_stealed = 0
        if times_stealed > 0:
            percent_stealed = float(times_stealed) / len(self.Q)
        '''

        # Return most relevant analysis
        return self.wins, percent_won, percent_splited
    
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
