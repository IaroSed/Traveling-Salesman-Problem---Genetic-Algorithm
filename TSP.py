# -*- coding: utf-8 -*-
"""
Created on Fri May 31 14:39:00 2019

@author: iasedric
"""

import pygame
import random
import pandas as pd
import heapq
import numpy as np
from math import sqrt



# Defining constants
NUMBER_MODELS = 20

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480
TEXT_ZONE = 100


PROBA = 0.85

#bg_sprite = pygame.image.load('bg.jpg')

Exit_RS = open("ResultsPath.txt", 'w',encoding='utf-8')

#Office location as first element
Coordinates = [[int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2)]]

# Adding coordinates to visit (x,y) 
for i in range(0,10):
    Coordinates.append([random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT)])

# Initializing the distances matrix
Distances = np.zeros((len(Coordinates),len(Coordinates)))

# Populating the distances matrix
for i in range(len(Coordinates)):
    for j in range(len(Coordinates)):
        Distances[i][j] = sqrt((Coordinates[i][0]-Coordinates[j][0])**2 + (Coordinates[i][1]-Coordinates[j][1])**2)
        


## Defining functions

def crossover(fitness,the_best_fitness, the_best_path):
    

    best_fitness_temp = [0] * 30
    #print("1: " + str(best_classifiers[0].get_weights()[0][0]))
    
    #print(best_fitness)
    #print(fitness)

    best_fitness_temp = best_fitness + fitness

        
    best_parents_int = []
    best_parents_int = heapq.nlargest(30, enumerate(best_fitness_temp), key=lambda x: x[1])
    #print(best_parents_int)
    
    print("The last best is: " + str(heapq.nlargest(1, enumerate(best_fitness_temp), key=lambda x: x[1])[0][1]) + " the best is: " + str(best_fitness[0]))
    
    
    
    # Updating the Best path
    for i in range(0,10):
        Best_Path[i] = (Best_Path + Path)[best_parents_int[i][0]]
        best_fitness[i] = best_fitness_temp[best_parents_int[i][0]]

    #Replacing the first 5 classifiers by the best and no mutation authorized
    for i in range(0,5):
        Path[i] = Best_Path[i]

    # Keeping some bad ones for diversity   
    for i in range(5,10):
        Path[i] = (Best_Path + Path)[best_parents_int[i+5][0]]

    #Replacing the first 5 classifiers by the best and mutation authorized
    for i in range(10,15):
        Path[i] = Best_Path[i-10]

    CO = [0] * 5
    
    for i in range(15,20):
        #classifier[i].set_weights(best_classifiers[i-15].get_weights()) 
        CO[i-16] = Best_Path[i-15][int(len(Coordinates)/2+1):]
 

    for i in range(15,20):
        Path[i] = [x for x in Path[i] if x not in CO[i-15]] + CO[i-15]
        
    
    
    if best_fitness[0] > the_best_fitness:
        the_best_fitness = best_fitness[0]
        the_best_path = Best_Path[0][:]
        
    Exit_RS.write(str(Best_Path[0]) + "^" + str(best_fitness[0]) + "^" + str(the_best_path) + "^" + str(the_best_fitness) +  "\n")

    return the_best_fitness, the_best_path
   

     
def swap_random(seq):
    idx = range(len(seq))
    i1, i2 = random.sample(idx, 2)
    seq[i1], seq[i2] = seq[i2], seq[i1]        
       
    
    
def mutate():
    
    #Introducing mutations: with a probability of (100% - PROBA) two cities can be swaped in the path
    for i in range(NUMBER_MODELS):
        for j in range(1,NUMBER_MODELS):
            if Path[i] == Path[j]:
                swap_random(Path[j])
    
        
        #for k in range(len(Coordinates)):
        #if random.uniform(0,1) > PROBA:
            #swap_random(Path[i])


  

### Main    
    
pygame.init()
pygame.font.init()



#Opening the screen
win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT+TEXT_ZONE))        

Path = []

paths = []

for i in range(1,len(Coordinates)):
    paths.append(i)


for i in range(NUMBER_MODELS):
    random.shuffle(paths)
    Path.append([0] + paths)
    
Best_Path = [[0,0,0,0,0,0,0]] * 10
    
Best_Path[0] = []
for i in range(len(Coordinates)):
    Best_Path[0].append(i) 
    
best_fitness = [0] * 10
the_best_fitness = 0

the_best_path = []
for i in range(0,len(Coordinates)):
    the_best_path.append(i)

fitness = []

Score = 0
Generation = 1

myfont = pygame.font.SysFont('Comic Sans MS', 20)

    

    

run = True

while run:
    
    
    generation_info = myfont.render('Generation ' + str(Generation) + " Best fitness: " + str(the_best_fitness) + " Best Path: " + str(the_best_path) , False, (255, 255, 255))
    
    
    #win.blit(bg_sprite, (0,0))
    
    win.fill((0,0,0))
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            run = False
            
    for j in range(len(Coordinates)):
        #Draw end of distance between pipes at which birds are aiming
        pygame.draw.circle(win, (255,0,0), (Coordinates[j][0], Coordinates[j][1]), 4)
        
    for i in range(NUMBER_MODELS):
        #pygame.time.delay(100)
       
        
        #print(i)
        #List_Coord = [(Coordinates[Path[i][k]][0],Coordinates[Path[i][k]][1]) for k in range(0,len(Coordinates))]
        #pygame.draw.lines(win, (255,255,255), False, List_Coord ,2)
        

        fitness.append(sum([Distances[Path[i][k]][Path[i][k+1]] for k in range(0,len(Coordinates)-1)]))
        
        
    List_Coord_best = [(Coordinates[the_best_path[k]][0],Coordinates[the_best_path[k]][1]) for k in range(0,len(Coordinates))]
    pygame.draw.lines(win, (34,139,34), False, List_Coord_best ,2)
    
    fitness = [round(1000000/fitness[i],2) for i in range(len(fitness))]    
    shortest_path = [b for b, j in enumerate(fitness) if j == max(fitness)][0]
    
    #print(fitness,shortest_path)
    
    
    
    the_best_fitness, the_best_path = crossover(fitness,the_best_fitness, the_best_path)
    
    mutate()
    
    fitness = []  
    Generation +=1
    
    
    #Showing generation
    win.blit(generation_info,(5,SCREEN_HEIGHT + 2))
    
   
    
    
    
    #pygame.display.update()
    pygame.display.flip()
    

pygame.quit()

