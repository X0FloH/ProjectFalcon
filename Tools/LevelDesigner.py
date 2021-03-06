import pygame
import os
from time import *

displaySize = (1000, 900)
backgroundColor = (0, 0, 0)

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

mouseDown = False

pygame.display.set_caption("Project Falcon Level Designer")
display = pygame.display.set_mode(displaySize)

if not os.path.exists("Colors"):
    os.makedirs("Colors")

minSliderVal = 200
maxSliderVal = int((minSliderVal + 510))

sliders = [[maxSliderVal, 550, 50, 25, (255, 0, 0)], [maxSliderVal, 600, 50, 25, (0, 255, 0)], [maxSliderVal, 650, 50, 25, (0, 0, 255)]]

objects = []
history = []

heldObjIndex = -1
selectedSliderIndex = -1

currentColor = [255, 255, 255]

def drawSquare(xPos, yPos, xSize, ySize, color):
    obst = pygame.draw.rect(display, color, pygame.Rect(xPos, yPos, xSize, ySize))
    return obst

def drag(currentX, currentY, xSize, ySize, newX, newY):
    currentX = newX - (xSize/2)
    currentY = newY - (ySize/2)
    return currentX, currentY

def sliderDrag(currentX, xSize, mouseX):
    currentX = mouseX - (xSize/2)
    return currentX

def getIndex(find, listS):
    foundIndex = -1
    i = 0
    while i < len(listS):
        if find == listS[i]:
            foundIndex = i
        i = i + 1
    return foundIndex

def wait(time):
    sleep(time)
    return

def makeColorFile(fileName, rC, bC, gC):
    makeFile = open(fileName + ".txt", "a+")
    makeFile.close()
    file = open(fileName + ".txt", "r+")
    file.write(str(rC))
    file.write("\n")
    file.write(str(bC))
    file.write("\n")
    file.write(str(gC))
    file.close()

def readColorFile(fileName):
    file = open(fileName + ".txt", "r+")
    lines = file.readlines()
    return int(int(lines[0])*2) + minSliderVal, int(int(lines[1])*2) + minSliderVal, int(int(lines[2])*2) + minSliderVal

def isFile(name, folder):
    found = False
    for file in os.listdir(folder):
        if name == file[:-4]:
            found = True
    return found
    

running = True

placingObjs = True
changingColor = False

colorCircleRadius = 40

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    if pygame.mouse.get_pressed()[0]:
        mouseDown = True
    else:
        mouseDown = False

    if pygame.mouse.get_pressed()[1]:
        mouseDownRight = True
    else:
        mouseDownRight = False
        
    currentColor[0] = int((sliders[0][0] - minSliderVal)/2)
    currentColor[1] = int((sliders[1][0] - minSliderVal)/2)
    currentColor[2] = int((sliders[2][0] - minSliderVal)/2)

    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]

    display.fill(backgroundColor)

    if placingObjs:
        for obj in objects:
            if mouseDown and heldObjIndex == -1 and mouseX > obj[0] and mouseX < obj[0] + obj[2] and mouseY > obj[1] and mouseY < obj[1] + obj[3]:
                heldObjIndex = getIndex(obj, objects)
            elif mouseDown == False:
                heldObjIndex = -1

            if mouseDown and heldObjIndex == getIndex(obj, objects):
                obj[0], obj[1] = drag(obj[0], obj[1], obj[2], obj[3], mouseX, mouseY)

                #Temp Sizing

                keysS = pygame.key.get_pressed()

                if (keysS[pygame.K_RIGHT] or keysS[pygame.K_d]) and not keysS[pygame.K_LSHIFT]:
                    obj[2] += 0.1
                if (keysS[pygame.K_LEFT] or keysS[pygame.K_a]) and not keysS[pygame.K_LSHIFT]:
                    obj[2] -= 0.1
                if (keysS[pygame.K_RIGHT] or keysS[pygame.K_d]) and keysS[pygame.K_LSHIFT]:
                    obj[2] += 0.05
                if (keysS[pygame.K_LEFT] or keysS[pygame.K_a]) and keysS[pygame.K_LSHIFT]:
                    obj[2] -= 0.05
                if (keysS[pygame.K_UP] or keysS[pygame.K_w]) and not keysS[pygame.K_LSHIFT]:
                    obj[3] -= 0.1
                if (keysS[pygame.K_DOWN] or keysS[pygame.K_s]) and not keysS[pygame.K_LSHIFT]:
                    obj[3] += 0.1
                if (keysS[pygame.K_UP] or keysS[pygame.K_w]) and keysS[pygame.K_LSHIFT]:
                    obj[3] -= 0.05
                if (keysS[pygame.K_DOWN] or keysS[pygame.K_s]) and keysS[pygame.K_LSHIFT]:
                    obj[3] += 0.05
            obst = drawSquare(obj[0], obj[1], obj[2], obj[3], obj[5])

            if mouseDownRight and mouseX > obj[0] and mouseX < obj[0] + obj[2] and mouseY > obj[1] and mouseY < obj[1] + obj[3]:
                history.append(objects[getIndex(obj, objects)])
                del objects[getIndex(obj, objects)]

        
        if mouseDown and mouseX > 0 and mouseX < colorCircleRadius * 2 and mouseY > 0 and mouseY < colorCircleRadius * 2:
            changingColor = True
            placingObjs = False

        if mouseDown and heldObjIndex == -1 and placingObjs:
            newObj = objects.append([mouseX - (50/2), mouseY - (50/2), 50,50, "Rect", (currentColor[0], currentColor[1], currentColor[2]), 0, [False], [False], False])

        keys = pygame.key.get_pressed()

        if keys[pygame.K_z] and keys[pygame.K_LCTRL]:
            if history:
                objects.append(history[len(history)-2])
                del history[len(history)-2]
                wait(0.2)

        if keys[pygame.K_p] and keys[pygame.K_LCTRL] and not keys[pygame.K_c]:
            print("The current level: " + str(objects))
            wait(0.5)

        if keys[pygame.K_p] and keys[pygame.K_c] and keys[pygame.K_LCTRL]:
            print("The current color (RGB): " + "(" + str(currentColor[0]) + ", " + str(currentColor[1]) + ", " + str(currentColor[2]) + ")")
            wait(0.5)

        if keys[pygame.K_s] and keys[pygame.K_LCTRL] and keys[pygame.K_c]:
            print("Saving Color: " + "(" + str(currentColor[0]) + ", " + str(currentColor[1]) + ", " + str(currentColor[2]) + ")")
            name = input("What is the name for the color? ")
            makeColorFile("Colors/" + name, currentColor[0], currentColor[1], currentColor[2])
            wait(0.5)

        if keys[pygame.K_l] and keys[pygame.K_LCTRL] and keys[pygame.K_c]:
            name = input("What is the name of the color you want to load? ")
            if isFile(name, "Colors"):
                sliders[0][0], sliders[1][0], sliders[2][0] = readColorFile("Colors/" + name)
            wait(0.5)

            

        colorBlock = pygame.draw.circle(display, (currentColor[0], currentColor[1], currentColor[2]), (int(0 + (colorCircleRadius)), int(0 + (colorCircleRadius))), colorCircleRadius)

        #debug = pygame.draw.rect(display, (255, 0, 0), pygame.Rect(0 + (colorCircleRadius*2), 0 + (colorCircleRadius*2), 10, 10))

    if changingColor:
        colorBlock = pygame.draw.circle(display, (currentColor[0], currentColor[1], currentColor[2]), (int(displaySize[0]/2), int(displaySize[1]/2) - 200), colorCircleRadius * 6)

        backButton = pygame.draw.rect(display, (255, 0, 0), pygame.Rect(20, (displaySize[1]-20)-50, 100, 50))

        if mouseDown and mouseX > 20 and mouseX < 20 + 100 and mouseY > (displaySize[1]-20)-50 and mouseY < displaySize[1]-20:
            placingObjs = True
            changingColor = False
            wait(0.1)

        for slider in sliders:
            slid = drawSquare(slider[0], slider[1], slider[2], slider[3], slider[4])
            if mouseDown and mouseX > slider[0] and mouseX < slider[0] + slider[2] and mouseY > slider[1] and mouseY < slider[1] + slider[3]:
                selectedSliderIndex = getIndex(slider, sliders)
            elif mouseDown == False:
                selectedSliderIndex = -1

            if selectedSliderIndex == getIndex(slider, sliders):
                slider[0] = sliderDrag(slider[0], slider[2], mouseX)
                
                if slider[0] < minSliderVal:
                    slider[0] = minSliderVal
                if slider[0] > maxSliderVal:
                    slider[0] = maxSliderVal


    pygame.display.update()

pygame.quit()
quit()
