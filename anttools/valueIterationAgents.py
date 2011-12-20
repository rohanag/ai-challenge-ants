import mdp, util, time


from abstractAgents import AbstractValueEstimationAgent

class ValueIterationAgent(AbstractValueEstimationAgent):
  """
      * Please read abstractAgents.py before reading this.*

      A ValueIterationAgent takes a markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations as well as a discount 
      value.
  """

  def __init__(self, starttime, sparetime, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    #print iterations
    self.oldV=util.Counter()
    self.newV=util.Counter()
    # Bellman Update procedure: 
    listOfState=self.mdp.getStates()

    for i in range(0,self.iterations):

        for state in listOfState:

            listValue=list()
            listOfActions=self.mdp.getPossibleActions(state)
            for eachAction in listOfActions:
                listOfNT_T=self.mdp.getTransitionStatesAndProbs(state,eachAction)
                tempSum=0
                for eachNT_T in listOfNT_T:
                    nextState,T=eachNT_T
                    R=self.mdp.getReward(state, eachAction, nextState)
                    tempSum+=T*(R+self.discount*self.oldV.getCount(nextState)) 
                listValue.append(tempSum)
                self.newV.setCount(state,max(listValue))
            if (time.time()-starttime >= sparetime):
		return
        #update Vector of Value         
        newKeys=self.newV.keys()
        for k in newKeys:
            newValue=self.newV.getCount(k)
            self.oldV.setCount(k, newValue)


  def getValue(self, state):
    """
      Return the value of the state 
      (after the indicated number of value iteration passes).      
    """
    "*** YOUR CODE HERE ***"
    return self.oldV.getCount(state)

  def getQValue(self, state, action):
    """
      Look up the q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    listOfStateandProbs=self.mdp.getTransitionStatesAndProbs(state,action) 
    sumTmp=0 
    for eachStateandProbs in listOfStateandProbs:
        nextState,tValue=eachStateandProbs
        sumTmp+=tValue*(self.mdp.getReward(state,action,nextState)+self.discount*self.getValue(nextState))
    return sumTmp

  def getPolicy(self, state):
    """
      Look up the policy's recommendation for the state
      (after the indicated number of value iteration passes).

      This method should return exactly one legal action for each state.
      You may break ties any way you see fit. The getPolicy method is used 
      for display purposes & in the getAction method below.
    """
    "*** YOUR CODE HERE ***"
    listOfActions=self.mdp.getPossibleActions(state)
    listQ=list()
    if self.mdp.isTerminal(state): return None
    for eachAction in listOfActions:
         listQ.append(self.getQValue(state, eachAction))
    maxIndex=listQ.index(max(listQ))
    return listOfActions[maxIndex]      

  def getAction(self, state):
    """
      Return the action recommended by the policy.  We have provided this
      for you.
    """
    return self.getPolicy(state)