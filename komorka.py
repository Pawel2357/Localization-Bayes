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