import pygame
import numpy as np
import matplotlib.pyplot as plt
import time
pygame.init()
size = width, height =600,600

nxC=60
nyC=60

dimCW=  (width-1)/nxC
dimCH= (height-1)/nyC

bg =25,25,25

screen =pygame.display.set_mode(size)
screen.fill(bg)

gameState=np.random.randint(0,2,(nxC,nyC))
#gameState=np.zeros((nxC,nyC))

#gameState[21,21]=1
#gameState[22,22]=1
#gameState[22,23]=1
#gameState[21,23]=1
#gameState[20,23]=1


while 1:
    new_gameState=np.copy(gameState)
    screen.fill(bg)
    for y in range(0,nyC):
        for x in range(0,nxC):
            n_neigh= gameState[(x-1) %nxC,(y-1)%nyC]+\
                       gameState[(x) % nxC, (y - 1) % nyC]+\
                       gameState[(x+1) % nxC, (y - 1) % nyC]+\
                       gameState[(x-1) % nxC, (y) % nyC]+\
                       gameState[(x + 1) % nxC, (y + 1) % nyC]+\
                       gameState[(x - 1) % nxC, (y + 1) % nyC]+ \
                       gameState[(x) % nxC,(y+1) % nyC]+\
                       gameState[(x+1)%nxC,(y) % nyC]
            if gameState[x,y]==0 and n_neigh==3:
                new_gameState[x,y]=1
            elif gameState[x,y]==1 and (n_neigh<2 or n_neigh>3):
                new_gameState[x,y]=0
            #Una célula muerta con exactamente 3 células vecinas vivas "nace" (es decir, al turno siguiente estará viva)
            np.sum(gameState[x-1:x+2,y-1:y+2])-gameState[x,y]
            #Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere (por "soledad" o "superpoblación")

            poly=[((x-1)*dimCW,(y-1)*dimCH),
                  ((x)*dimCW, (y-1)*dimCH),
                  ((x)*dimCW,(y)*dimCH),
                  ((x-1)*dimCW,(y)*dimCH)]
            pygame.draw.polygon(screen,(128,128,128),poly,int(abs(1-new_gameState[x,y])))
    gameState=new_gameState
    time.sleep(0.2)
    pygame.display.flip()
    #plt.matshow(gameState)
    #plt.show()

    #pygame.display.flip()
