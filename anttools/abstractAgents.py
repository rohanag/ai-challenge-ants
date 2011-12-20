

class AbstractValueEstimationAgent():
  """
    Abstract agent which assigns values to (state,action)
    Q-Values for an enviornment. As well as a value to a 
    state and a policy given respectively by,
    
    V(s) = max_{a in actions} Q(s,a)
    policy(s) = arg_max_{a in actions} Q(s,a)
    
    Both ValueIterationAgent and QLearningAgent inherit 
    from this agent. Whereas a ValueIterationAgent has
    a model of the environment via a MarkovDecisionProcess
    (see mdp.py) that is used to estimate Q-Values before
    ever actually acting, the QLearningAgent estimates 
    Q-Values while acting in the environment. 
  """
  ####################################
  #    Override These Functions      #  
  ####################################
  def getQValue(self, state, action):
    """
    Should return Q(state,action)
    """
    abstract
    
  def getValue(self, state):
    """
    What is the value of this state under the best action? 
    Concretely, this is given by
    
    V(s) = max_{a in actions} Q(s,a)
    """
    abstract  
    
  def getPolicy(self, state):
    """
    What is the best action to take in the state. Note that because
    we might want to explore, this might not coincide with getAction
    Concretely, this is given by
    
    policy(s) = arg_max_{a in actions} Q(s,a)
    
    If many actions achieve the maximal Q-value,
    it doesn't matter which is selected.
    """
    abstract  
    
  def getAction(self, state):
    """
    state: can call state.getLegalActions()
    Choose an action and return it. Be sure to
    inform the parent class via doAction(state, action)    
    """
    abstract    