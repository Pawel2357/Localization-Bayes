
#Localization through Bayes inference

import numpy as np

class komorka:
    
    
    
    def __init__(self, P_old , P_new, position):
        self.P_old = P_old # a. probability of being in this position
        self.P_new = P_new # b. probability of being in this position
        self.position = position # list with three values x, y
        self.neighbours = [] # nearest spaces
        self.measurements_probab = {} # probabilities of measurements
        self.walls = {} # where are walls
        self.transition_probab = 0 # probability of going to nearest neighbour
        
    # change P_old to P_new
    # INPUT : P_old, P_new
    # OUTPUT : P_old
    def update_P(self):
        self.P_old = self.P_new
        
    # add nearest spaces
    # INPUT : neighbours, neigh_list
    # OUTPUT : neighbours
    def add_neighbours(self, neigh_list):
        for i in range(len(neigh_list)):
            self.neighbours.append(neigh_list[i])
            
    # recognize where are walls in this position
    # INPUT : neighbours
    # OUTPUT : walls - place 'W' if wall, 'N' if neighbour
    def find_walls(self):
        # initialization walls
        self.walls['L'] = 'W'
        self.walls['R'] = 'W'
        self.walls['U'] = 'W'
        self.walls['D'] = 'W'
        
        # adding neighbours to walls
        
        for i in range(len(self.neighbours)):
            if self.neighbours[i].position[0] == self.position[0]:
                if self.neighbours[i].position[1] == self.position[1] - 1:
                    self.walls['D'] = 'N' # neighbour down
                else:
                    self.walls['U'] = 'N'
                    #print 'hhaahahhahaha'
                    #print komorka.neighbours[i].position
            elif self.neighbours[i].position[0] == self.position[0] - 1:
                self.walls['L'] = 'N' # on the left L is neighbour
            else:
                self.walls['R'] = 'N'
        
    # find what are measurement probabilities in this position
    # INPUT : walls
    # OUTPUT : measurement_probab - probability of measurement (example prob. of finding wall 'L')
    def calculate_measurement_probab(self):
        #initialization
        self.measurements_probab['no'] = 0
        self.measurements_probab['L'] = 0
        self.measurements_probab['R'] = 0
        self.measurements_probab['U'] = 0
        self.measurements_probab['D'] = 0
        self.measurements_probab['DU'] = 0
        self.measurements_probab['DR'] = 0
        self.measurements_probab['DL'] = 0
        self.measurements_probab['LR'] = 0
        self.measurements_probab['LU'] = 0
        self.measurements_probab['RU'] = 0
        self.measurements_probab['DUL'] = 0
        self.measurements_probab['DUR'] = 0
        self.measurements_probab['DLR'] = 0
        self.measurements_probab['RLU'] = 0
        walls_list = []
        if self.walls['D'] == 'W':
            walls_list.append('D')
        if self.walls['U'] == 'W':
            walls_list.append('U')
        if self.walls['L'] == 'W':
            walls_list.append('L')
        if self.walls['R'] == 'W':
            walls_list.append('R')
        #print walls_list
        
        if len(walls_list) == 0:
            self.measurements_probab['no'] = 1
            self.transition_probab = 1.0 / 4.0
        
        if len(walls_list) == 1:
            self.measurements_probab[walls_list[0]] = 1
            self.transition_probab = 1.0 / 3.0
            
        if len(walls_list) == 2:
            self.transition_probab = 1.0 / 2.0
            for i in self.measurements_probab:
                if (walls_list[0] in i) and (walls_list[1] in i) and (len(i) == 2):
                    self.measurements_probab[i] = 1
                    
        if len(walls_list) == 3:
            self.transition_probab = 1.0 #is it really one for random wolk?
            for i in self.measurements_probab:
                if (walls_list[0] in i) and (walls_list[1] in i) and (walls_list[2] in i) and (len(i) == 3):
                    self.measurements_probab[i] = 1
            
        
    # calculate posteriori probability of finding robot in this position
    # INPUT : measurement - list of walls that robot observe, states - list of all states, P_measurement - probability
    # of getting measurement
    # OUTPUT : calculate P_new using Bayes rule
    def update_probabilities(self, measurement, states, P_measurement):
        
        #find measurement in dictionary measurement_probab
        measurement_sign = ''
        if len(measurement) == 1:
            measurement_sign = measurement[0]
            
        if len(measurement) == 2:
            for i in self.measurements_probab:
                if (measurement[0] in i) and (measurement[1] in i) and (len(i) == 2):
                    measurement_sign = i
                    
        if len(measurement) == 3:
            for i in self.measurement_probab:
                if (measurement[0] in i) and (measurement[1] in i) and (measurement[2] in i) and (len(i) == 3):
                    measurement_sign = i
        
        ### Use Bayes rule to update P_new based on P_old and P_olds of neighbours
        # 1. calculate probability of being in this position
        P_position = 0
        
        for i in self.neighbours:
            P_position += i.transition_probab * i.P_old
        # 2. calculate probability of this position based on measurement
        self.P_new = self.measurements_probab[measurement_sign] * P_position / P_measurement
            
        
        
        
class grid_world:
    
    def __init__(self, position, states):
        self.position = position # initial position of robot
        self.states = states # list of states - komorka
        self.measurements = [] # list of all measurements that robot performed
        self.p_measurem = 0 #probability of last measurement
        self.signs_tab = ['no','L','R','U','D','DU','DR','DL','LR','LU','RU','DUL','DUR','DLR','RLU']
        self.space = {} # where are walls and free spaces
        
    # move robot randomly one step
    # INPUT : position
    # OUTPUT : updated position
    def move(self):
        p = True
        
        while(p):
            a = np.random.randint(1,5)
            
            if (a == 1) and (self.space['L'] == 'S'):
                self.position[0] = self.position[0] - 1
                p = False
            if (a == 2) and (self.space['R'] == 'S'):
                self.position[0] = self.position[0] + 1
                p = False
            if (a == 3) and (self.space['U'] == 'S'):
                self.position[1] = self.position[1] + 1
                p = False
            if (a == 4) and (self.space['D'] == 'S'):
                self.position[1] = self.position[1] - 1
                p = False
            
    # measure signals from environment
    # INPUT : current position of robot, states around robot
    # OUTPUT : space - where are walls in robot environment, measurements - list of all measurements performed by
    # robot. 'W' - wall, 'S' - free space
    def perform_measurement(self):
        
        self.space['L'] = 'W'
        self.space['R'] = 'W'
        self.space['U'] = 'W'
        self.space['D'] = 'W'
        
        # 1. find free spaces around robot 
        for i in range(len(self.states)):
            if (self.states[i].position[0] == self.position[0]-1) and (self.states[i].position[1] == self.position[1]):
                self.space['L'] = 'S'
            if (self.states[i].position[0] == self.position[0]+1) and (self.states[i].position[1] == self.position[1]):
                self.space['R'] = 'S'
            if (self.states[i].position[0] == self.position[0]) and (self.states[i].position[1] == self.position[1]-1):
                self.space['D'] = 'S'
            if (self.states[i].position[0] == self.position[0]) and (self.states[i].position[1] == self.position[1]+1):
                self.space['U'] = 'S'
        
        # add signs of walls to table signals
        signals = []
        for i in self.space:
            if self.space[i] == 'W':
                signals.append(i)
        
        # add sign of measurement to table self.measurements
        if len(signals)>0:
            for i in self.signs_tab:
                p = False
                for j in signals:
                    if j not in i:
                        p = True
                if len(i) != len(signals):
                    p = True
                if not p:
                    self.measurements.append(i)
                    break
        else: # no signal - no walls
            self.measurements.append('no')
        
        
        
    # calculate probability of getting measurement 
    # INPUT : states - possible states(positions of robot)
    # OUTPUT : p_measurem - calculate probability of current measurement
    def p_measurement(self):
        
        '''
        # 1. Find sign of last item of measurements
        signs = {}
        
        for i in range(len(self.signs_tab)):
            signs[ self.signs_tab[i] ] = 0
        
        measurement_sign = ''
        measurement = self.measurements[len(self.measurements) - 1]
        if len(measurement) == 1:
            measurement_sign = measurement[0]
            
        if len(measurement) == 2:
            for i in signs:
                if (measurement[0] in i) and (measurement[1] in i) and (len(i) == 2):
                    measurement_sign = i
                    
        if len(measurement) == 3:
            for i in signs:
                if (measurement[0] in i) and (measurement[1] in i) and (measurement[2] in i) and (len(i) == 3):
                    measurement_sign = i
        '''
        
        self.p_measurem = 0
        for i in self.states:
            P_position = 0
        
            for j in i.neighbours:
                P_position += j.transition_probab * j.P_old
            self.p_measurem += P_position * i.measurements_probab[ self.measurements[len(self.measurements) - 1] ]
        
    # update localization of robot
    def localize_step(self):
        # 1. perform_measurements of environment
        self.perform_measurement()
        # 2. calculate probability of getting measurement p_measurement
        self.p_measurement()
        # 3. update probabilities in all space()
        for i in self.states:
            i.update_probabilities(self.measurements[len(self.measurements) - 1], self.states, self.p_measurem)
        ''' 
        print "start"
        for i in self.states:
            print i.position
            print i.P_old
            '''
        '''   
        print self.position
        print [self.states[3].P_old, self.states[7].P_old, self.states[11].P_old, self.states[15].P_old]
        print [self.states[2].P_old, self.states[6].P_old, self.states[10].P_old, self.states[14].P_old]
        print [self.states[1].P_old, self.states[5].P_old, self.states[9].P_old, self.states[13].P_old]
        print [self.states[0].P_old, self.states[4].P_old, self.states[8].P_old, self.states[12].P_old]
        '''
        
          
        print self.position
        print [self.states[3].P_new, self.states[6].P_new, self.states[10].P_new, self.states[14].P_new]
        print [self.states[2].P_new, self.states[5].P_new, self.states[9].P_new, self.states[13].P_new]
        print [self.states[1].P_new, self.states[4].P_new, self.states[8].P_new, self.states[12].P_new]
        print [self.states[0].P_new, 10.0, self.states[7].P_new, self.states[11].P_new]
        
        # self.states[4].P_new
        # 4. Udate_P - change from P_old to P_new in all space()
        for i in self.states:
            i.update_P()
        # 5. move robot one step
        '''
        print self.measurements
        '''
        
        '''
        for i in self.states:
            if (self.position[0] == i.position[0]) and (self.position[1] == i.position[1]):
                #print i.P_old
                print i.P_new
        '''
        
        self.move()
    
    def robot_localization(self, num_steps):
        for i in range(num_steps):
           self.localize_step()
           
#### INITIALIZATION
position = [0, 0]
poz1 = komorka(1.0/15.0, 0, position)
position = [0, 1]
poz2 = komorka(1.0/15.0, 0, position)
position = [0, 2]
poz3 = komorka(1.0/15.0, 0, position)
position = [0, 3]
poz4 = komorka(1.0/15.0, 0, position)

#position = [1, 0]
#poz5 = komorka(1.0/15.0, 0, position)
position = [1, 1]
poz6 = komorka(1.0/15.0, 0, position)
position = [1, 2]
poz7 = komorka(1.0/15.0, 0, position)
position = [1, 3]
poz8 = komorka(1.0/15.0, 0, position)

position = [2, 0]
poz9 = komorka(1.0/15.0, 0, position)
position = [2, 1]
poz10 = komorka(1.0/15.0, 0, position)
position = [2, 2]
poz11 = komorka(1.0/15.0, 0, position)
position = [2, 3]
poz12 = komorka(1.0/15.0, 0, position)

position = [3, 0]
poz13 = komorka(1.0/15.0, 0, position)
position = [3, 1]
poz14 = komorka(1.0/15.0, 0, position)
position = [3, 2]
poz15 = komorka(1.0/15.0, 0, position)
position = [3, 3]
poz16 = komorka(1.0/15.0, 0, position)

lista = [poz2]
poz1.add_neighbours(lista)
poz1.find_walls()
#print poz1.walls
poz1.calculate_measurement_probab()
#print poz1.measurements_probab


lista = [poz1, poz3, poz6]
poz2.add_neighbours(lista)
poz2.find_walls()
poz2.calculate_measurement_probab()



lista = [poz2, poz4, poz7]
poz3.add_neighbours(lista)
poz3.find_walls()
#print poz3.walls
poz3.calculate_measurement_probab()
#print poz3.measurements_probab



lista = [poz3, poz8]
poz4.add_neighbours(lista)
poz4.find_walls()
#print poz3.walls
poz4.calculate_measurement_probab()
#print poz3.measurements_probab

"""
lista = [poz1, poz9, poz6]
poz5.add_neighbours(lista)
poz5.find_walls()
poz5.calculate_measurement_probab()
"""
lista = [poz7, poz2, poz10]
poz6.add_neighbours(lista)
poz6.find_walls()
poz6.calculate_measurement_probab()

lista = [poz3, poz8, poz11, poz6]
poz7.add_neighbours(lista)
poz7.find_walls()
poz7.calculate_measurement_probab()

lista = [poz4, poz7, poz12]
poz8.add_neighbours(lista)
poz8.find_walls()
poz8.calculate_measurement_probab()

lista = [poz10, poz13]
poz9.add_neighbours(lista)
poz9.find_walls()
poz9.calculate_measurement_probab()

lista = [poz11, poz9, poz14, poz6]
poz10.add_neighbours(lista)
poz10.find_walls()
poz10.calculate_measurement_probab()

lista = [poz7, poz10, poz12, poz15]
poz11.add_neighbours(lista)
poz11.find_walls()
poz11.calculate_measurement_probab()

lista = [poz8, poz11, poz16]
poz12.add_neighbours(lista)
poz12.find_walls()
poz12.calculate_measurement_probab()

lista = [poz14, poz9]
poz13.add_neighbours(lista)
poz13.find_walls()
poz13.calculate_measurement_probab()

lista = [poz10, poz13, poz15]
poz14.add_neighbours(lista)
poz14.find_walls()
poz14.calculate_measurement_probab()

lista = [poz11, poz14, poz16]
poz15.add_neighbours(lista)
poz15.find_walls()
poz15.calculate_measurement_probab()

lista = [poz12, poz15]
poz16.add_neighbours(lista)
poz16.find_walls()
poz16.calculate_measurement_probab()

states = [poz1, poz2, poz3, poz4, poz6, poz7, poz8, poz9, poz10, poz11, poz12, poz13, poz14, poz15, poz16]

world1 = grid_world([1,2], states)
'''
world1.perform_measurement()
world1.p_measurement()

poz1.update_probabilities(world1.measurements[0], states, world1.p_measurem)
'''
world1.robot_localization(15)





#print poz2.P_old
#print poz2.P_new
