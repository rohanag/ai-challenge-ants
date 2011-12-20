#TODO: carryover prev policy, 2 hills? discRate, ant attack, roam in Pairs,

#TODO ATTACK when dense
#HIGH PRI TODO: fuse group of 4,9, or 16 cells, make their policy the same, could bring out pack behaviour

##TODO: instead of noofturns, a measure of number of ants, then explore for 100 turns
                ##OR reach a value of numants (row*col/150), then set BOUNDARY permanently to 50

                ##OR boundary= 75 for the nothermost point, southernmost.....



#!/usr/bin/env python
from ants import *
import gridworld, util, valueIterationAgents
import sys
import time
import random



# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us


class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
        pass
    

    def do_setup(self, ants):

        self.turn=0
        self.grid=[['#']*ants.cols for x in xrange(ants.rows)]
	self.gridu=[['u']*ants.cols for x in xrange(ants.rows)]

	self.MYANTS = 'S'
        self.ENEMYANTS = -100
	self.ENEMYANTS2 = 200

        self.MYHILL = -0.01
        self.MYHILL2 = 100
        self.ENEMYHILL = 1000

        self.FOOD = 50
        #self.FOOD2= 25

        self.BOUNDARY = ' '
        self.BOUNDARY2 = 50

        self.LAND = ' '
        self.WATER = '#'
    

    def do_turn(self, ants):
        # track all moves, prevent collisions
        orders = {}
        def do_move_direction(loc, direction):
            #Rrr destination takes care of wrapping around, returns the destination
            #issues the moving order
            new_loc = ants.destination(loc, direction)
            #Rrr orders is the dictionary of location of ants
            if (ants.unoccupied(new_loc) and new_loc not in orders):
                ants.issue_order((loc, direction))
                orders[new_loc] = loc
                return True
            else:
                return False

        targets = {}

        #ROHAN added the variable directn
        def do_move_location(loc, dirctn):
            #Rrr ants.direction takes a location and a destination and returns a list of the closest direction "as the crow flies".
            #If the target is up and to the left, it will return ['n', 'w'] and we should then try and move our ant one of the two directions.
            #If the target is directly down, it will return ['s'], which is a list of one item.
            directions = dirctn
            for direction in directions:
                if do_move_direction(loc, direction):
                    #targets[dest] = loc
                    return True
            return False

# --------------------------------starts from here--------------------------------------
# find close


        self.turn = self.turn + 1

	#MY HILLLLSSS                
        for hill_loc in ants.my_hills():
            x, y = hill_loc
            self.grid[x][y] = self.MYHILL
            #Rrr The dummy entry doesn't need a from location, so we just set the value to None.
	    #prevent stepping on own hill
            orders[hill_loc] = None
        #ENEMY HILLLSSSS
        for hill_loc, hill_owner in ants.enemy_hills():
            hillrow, hillcol=hill_loc
            self.grid[hillrow][hillcol]=self.ENEMYHILL

	
        #LAND, water food
        for i in range(ants.rows):
            for j in range(ants.cols):
                #if ((ants.visible((i,j))==True) or (self.grid[i][j]==(self.FOOD or self.ENEMYANTS or self.BOUNDARY2 or self.ENEMYANTS2))): 
                #    self.grid[i][j]=' '
		#    self.gridu[i][j]='v'
		if ants.visible((i,j))==True:
                    self.gridu[i][j]='v'
                    if (self.grid[i][j]!=(self.MYHILL or self.MYHILL2 or self.ENEMYHILL or self.WATER) ):
                        self.grid[i][j]=' '
                        
                elif self.grid[i][j]==(self.FOOD or self.ENEMYANTS or self.BOUNDARY2 or self.ENEMYANTS2 or self.MYANTS):
                    self.grid[i][j]=' '

                if ants.map[i][j]==-3:
                    self.grid[i][j]=self.FOOD
                elif ants.map[i][j]==-4:
                    self.grid[i][j]=self.WATER
                    
                # if i cant see my hill, retreat to it urgently
                if self.grid[i][j]==self.MYHILL:
                    if ants.visible((i,j))==False:
                        print >> sys.stderr, 'hill retreat', i, j
                        sys.stderr.flush()
                        self.grid[i][j]=self.MYHILL2
                    else:
                        self.grid[i][j]=self.MYHILL

                if self.grid[i][j]==self.ENEMYHILL:
                    print >> sys.stderr, 'hill attack!!!!!!!!!!!!!!!!!!', i, j
                    sys.stderr.flush()




        #MY ANTSSSSSSSSSS S
        num_ants=0
        sx=0
        sy=0
        for ant_loc in ants.my_ants():
            antrow, antcol=ant_loc
            sx=sx+antrow
            sy=sy+antcol
            #self.grid[antrow][antcol]=self.MYANTS
            num_ants=num_ants+1

        sx=int(sx/num_ants)
        sy=int(sy/num_ants)
        self.grid[sx][sy] = self.MYANTS
        
        ## change MODE------------------------------------------what do i do here ?????????
        if num_ants>=0:##(ants.rows*ants.cols/200):
            self.BOUNDARY=self.BOUNDARY2
        else:
            self.BOUNDARY=' '



        #ENEMYYYYYYYY ANTSSSSSSS
        for enemy_loc, enemy_owner in ants.enemy_ants():
            enemyrow, enemycol=enemy_loc
            #TO DO, if own ant concentration is good near enemy ant (enemy ant conc in the area), then a positive reward
            self.grid[enemyrow][enemycol]=self.ENEMYANTS
            
            #if they're near my base, retreat to base
            for hill_loc in ants.my_hills():
                x, y = hill_loc
                if ants.distance(hill_loc, enemy_loc)<9.0:
                    self.grid[enemyrow][enemycol]=self.ENEMYANTS2

            #if i can surround em attack :) TODO: also check the enemy density
            surround=0
            for ant_loc in ants.my_ants():
                antrow, antcol=ant_loc
                if ants.distance(ant_loc, enemy_loc)<6.0:
                    surround=surround+1

            if surround>=3:
                self.grid[enemyrow][enemycol]=self.ENEMYANTS2
                print >> sys.stderr, 'ursurrounded attack: ', enemyrow, enemycol
                sys.stderr.flush()

	#BOUNDARY EXPANDING !!!!!!!!!
        for i in range(ants.rows):
            for j in range(ants.cols):
                if (self.gridu[i][j]=='v' and self.grid[i][j]==' '): 
		    if(ants.visible(ants.destination((i,j), 'n'))==False or ants.visible(ants.destination((i,j), 'e'))==False or ants.visible(ants.destination((i,j), 'w'))==False or ants.visible(ants.destination((i,j), 's'))==False):
		        self.grid[i][j]=self.BOUNDARY
		        


#-----------------------------------------------------------------------------------------VALUE ITERATION


        #opts={'agent': 'value', 'discount': 0.9, 'iters': 200, 'noise': 0.01, 'livingReward': 0.0, 'epsilon': 0.0, 'pause': False, 'manual': False, 'quiet': True, 'episodes': 100, 'learningRate': 0.5, 'grid': 'BookGrid', 'gridSize': 150, 'speed': 1000.0, 'textDisplay': False}
        opts={'livingReward': 0.0, 'discount': 0.9, 'iters': 300, 'noise': 0.05, 'epsilon': 0.0, 'manual': False, 'quiet': True, 'agent': 'value', 'pause': False, 'episodes': 100, 'learningRate': 0.5, 'grid': 'BookGrid', 'gridSize': 150, 'speed': 1000.0, 'textDisplay': False}
        
        mdp = gridworld.Gridworld(self.grid)
        mdp.setLivingReward(opts['livingReward'])
        mdp.setNoise(opts['noise'])
        env = gridworld.GridworldEnvironment(mdp)



        ###########################
        # GET THE AGENT
        ###########################
        
        #time_to_spare = (ants.turntime/1000.0) - (0.00064286 + 0.0000547619*num_ants + 0.0000065476*(num_ants*num_ants)) - 0.01
        if num_ants<=60:
            time_to_spare = (ants.turntime/1000.0) - 0.03
        else:
            time_to_spare = (ants.turntime/1000.0) - (-0.003512 + 0.00047632*num_ants -0.00000105286*(num_ants*num_ants)) - 0.005

        a = None
        a = valueIterationAgents.ValueIterationAgent(ants.turn_start_time, time_to_spare, mdp, opts['discount'], opts['iters'])

        #TIME TIME TIME TIME
        #t1 = time.time()

	
        for ant_loc in ants.my_ants():
            antcol, antrow=ant_loc
            antcol=ants.rows-antcol-1
            inverted_ant_loc=(antrow,antcol)
            if (a.getQValue(inverted_ant_loc,'north')==a.getQValue(inverted_ant_loc,'south')==a.getQValue(inverted_ant_loc,'east')==a.getQValue(inverted_ant_loc,'west')):
                direct=random.choice('sewn')
		do_move_location(ant_loc, direct)
            elif a.getPolicy(inverted_ant_loc)=='north':
                direct='n'
		do_move_location(ant_loc, direct)

            elif a.getPolicy(inverted_ant_loc)=='south':
                direct='s'
	        do_move_location(ant_loc, direct)
            elif a.getPolicy(inverted_ant_loc)=='east':
                direct='e'
                do_move_location(ant_loc, direct)
            elif a.getPolicy(inverted_ant_loc)=='west':
                direct='w'
                do_move_location(ant_loc, direct)
	    else:
		direct=random.choice('sewn')
		do_move_location(ant_loc, direct)
            
        #TIME 2 TIME 2 TIME 2
	#t2 = time.time() - t1
        print >> sys.stderr, 'turn: ', self.turn, 'ants :', num_ants , 'spare:', time_to_spare, 'time:', (time.time()-ants.turn_start_time)
	sys.stderr.flush()  

        # unblock own hill
        for hill_loc in ants.my_hills():
            if hill_loc in ants.my_ants() and hill_loc not in orders.values():
                for direction in ('s','e','w','n'):
                    if do_move_direction(hill_loc, direction):
                        break

          

#----------------------------------------------------------------------------------------VALUE ITERATION END

if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
