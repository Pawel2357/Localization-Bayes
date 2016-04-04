import numpy as np

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
        
          
        print( self.position )
        print( [self.states[3].P_new, self.states[6].P_new, self.states[10].P_new, self.states[14].P_new] )
        print( [self.states[2].P_new, self.states[5].P_new, self.states[9].P_new, self.states[13].P_new] )
        print( [self.states[1].P_new, self.states[4].P_new, self.states[8].P_new, self.states[12].P_new] )
        print( [self.states[0].P_new, 10.0, self.states[7].P_new, self.states[11].P_new] )
        
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