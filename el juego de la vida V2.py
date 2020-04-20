import pygame
import numpy as np
import time

pygame.init( )
size = width, height = 1000, 1000

nxC = 100
nyC = 100

dimCW = (width - 1) / nxC
dimCH = (height - 1) / nyC

bg = 25, 25, 25

screen = pygame.display.set_mode(size)
screen.fill(bg)

gameState = np.random.randint(0, 2, (nxC, nyC))

# gameState=np.zeros((nxC,nyC))

## Autómata palo

# gameState[5, 3] = 1
# gameState[5, 4] = 1
# gameState[5, 5] = 1

## Autómata móvil
# gameState[21, 21] = 1
# gameState[22, 22] = 1
# gameState[22, 23] = 1
# gameState[21, 23] = 1
# gameState[20, 23] = 1

# control de la ejecución del juego
pauseExect = False

while True:
    new_gameState = np.copy(gameState)
    pygame.display.flip()
    screen.fill(bg)
    # Registramos eventos de teclado y ratón.
    ev = pygame.event.get()
    mouseClick = pygame.mouse.get_pressed()
    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        if event.type == pygame.QUIT:  # Cierra el programa
            raise SystemExit
        if sum(mouseClick) > 0:  # Crea nuevos células
            posX = pygame.mouse.get_pos()[0]
            posY = pygame.mouse.get_pos()[1]
            celX, celY = int(np.floor(posX / dimCW) + 1), int(np.floor(posY / dimCH) + 1)
            new_gameState[celX, celY] = not mouseClick[2]
    for y in range(0, nyC):
        for x in range(0, nxC):
            if not pauseExect:
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x) % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1) % nxC, (y) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC] + \
                          gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[(x) % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y) % nyC]
                if gameState[x, y] == 0 and n_neigh == 3:
                    new_gameState[x, y] = 1 # Una célula muerta con exactamente 3 células vecinas vivas "nace" (es decir, al turno siguiente estará viva)
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    new_gameState[x, y] = 0

                np.sum(gameState[x - 1:x + 2, y - 1:y + 2]) - gameState[x, y] # Una célula viva con 2 o 3 células vecinas vivas sigue viva, en otro caso muere (por "soledad" o "superpoblación")

            poly = [((x - 1) * dimCW, (y - 1) * dimCH),
                    ((x) * dimCW, (y - 1) * dimCH),
                    ((x) * dimCW, (y) * dimCH),
                    ((x - 1) * dimCW, (y) * dimCH)]
            if new_gameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)# Color gris de cuadricula
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)# Color blanco de célula
    gameState = np.copy(new_gameState)
    time.sleep(0.1)