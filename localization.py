
#Localization through Bayes inference

from grid_world import grid_world
from komorka import komorka

 
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
