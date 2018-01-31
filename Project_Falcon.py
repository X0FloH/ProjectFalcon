import os
import random
import pygame
import sys
from time import *

settingsDataPath = 'ProjectFalconData/settings.txt'
settingsFolderPath = 'ProjectFalconData'
if not os.path.exists(settingsFolderPath):
    os.makedirs(settingsFolderPath)

displaySize = (1000, 900)
levelColor = [(0, 0, 0)]
playerColor = [(255, 255, 244)]

bottomPlatformOffset = 100

# Defining All Obstacles
levelObstacles = [[[1, displaySize[1] - bottomPlatformOffset, displaySize[0], bottomPlatformOffset - 10, "Rect", (255, 255, 255), 0, [False], [False], False], [1, 1, 1000, 50, "Rect", (255, 255, 255), 0, [False], [False], False], [201, 300, 100, 50, "Rect", (255, 0, 0), 0, [False], [True, 0, 0], True], [200, 200, 150, 50, "Rect", (255, 255, 0), 0, [False], [True, 0, 0], False]]]
levelText = [[[300, 300, 40, (255, 0, 255), 'Futura PT Light', 'Controls - WASD']]]


playerSize = 30
playerBounceDivider = 3

running = True

canJump = True
currentJumps = 0

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

pygame.display.set_caption("Project Faxon")
display = pygame.display.set_mode(displaySize)

currentLevel = 1

gravityScale = .003
currentYVelocity = 0

jumpForce = -.85

currentX = 30
currentY = 200

showingSettings = False
selected = "Gravity"
selectables = ["Gravity", "Quit"]


def writeSettings(txtPath, gravityAmount):
    openedFile = open(txtPath, 'w+')
    openedFile.write("gravity:" + str(gravityAmount))
    openedFile.close()

def openSettings(txtPath):
    createFile = open(txtPath, 'a+')
    createFile.close()
    openedFile = open(txtPath, 'r+')
    lines = openedFile.readlines()
    if lines:
        gravitySettings = lines[0]
        if gravitySettings[:7] == 'gravity':
            openedFile.close()
            if float(gravitySettings[8:]) < 0:
                return str(-float(gravitySettings[8:]))
            return gravitySettings[8:]
    else:
        writeSettings(settingsDataPath, 0.003)
        openedFile.close()
        return str(0.003)

gravityScale = float(openSettings(settingsDataPath))

# To not have to worry about forgetting to type sleep
def wait(time):
    sleep(time)
    return

# Define Draw Player Function
def drawPlayer(xPos, yPos, color, size):
    player = pygame.draw.rect(display, color, pygame.Rect(xPos, yPos, size, size))
    return player

# Define Draw Obstacle Function
def drawObstacle(objType, xPos, yPos, color, xSize, ySize, radiusCirc=0):
    if objType == "Rect":
        obst = pygame.draw.rect(display, color, pygame.Rect(xPos, yPos, xSize, ySize))
        return obst
    if objType == "Circle":
        obst = pygame.draw.circle(display, color, (xPos, yPos), radiusCirc)
        return obst

def Animate(animType, currentFrame, currentSubFrame, listFrames):
    if animType == "Pos":
        objX = listFrames[currentFrame][0]
        objY = listFrames[currentFrame][1]
        currentSubFrame = currentSubFrame + 1

        if currentSubFrame > listFrames[currentFrame][2]:
            currentSubFrame = 1
            currentFrame = currentFrame + 1

        if currentFrame == len(listFrames):
            currentFrame = 0


        return objX, objY, currentFrame, currentSubFrame


def addPhysics(xPos, yPos, data, gravityScale):
    data[1] += gravityScale
    yPos = yPos + data[1]
    return xPos, yPos, data

def changeGrav(gravityScale, jumpForce):
    gravityScale = -gravityScale
    jumpForce = -jumpForce
    return gravityScale, jumpForce
        

def DrawText(xPos, yPos, fontSize, color, fontName, text):
    newFont = pygame.font.SysFont(fontName, fontSize)
    textSurface = newFont.render(text, False, color)
    display.blit(textSurface, (xPos, yPos))

def checkCollision(xPos, yPos, xSize, ySize, playerX, playerY, playerSize, currentVelocity, currentJumps, bounceMultiplier, gravityScale, jumpForce, changeGravObj):
    if playerX + (playerSize) > xPos and playerX < xPos + (xSize/2) and playerY + (playerSize-.1) > yPos and (playerY) < (yPos + (ySize)-5):
        playerX = xPos - (playerSize)
        if changeGravObj == True:
            gravityScale, jumpForce = changeGrav(gravityScale, jumpForce)
    if playerX < (xPos + xSize) and playerX > xPos + (xSize/2) and (playerY + (playerSize) > yPos or (playerY + (playerSize)+.1) > yPos) and playerY < (yPos + (ySize)-5):
        playerX = (xPos + xSize)
        if changeGravObj == True:
            gravityScale, jumpForce = changeGrav(gravityScale, jumpForce)
    if playerX + (playerSize) > xPos and playerX < (xPos + xSize) and playerY + (playerSize+2) > yPos and playerY < yPos + (ySize/2):
        currentVelocity = -(currentVelocity/bounceMultiplier)
        currentJumps = 0
        playerY = (yPos - (playerSize)) - 2
        if changeGravObj == True:
            gravityScale, jumpForce = changeGrav(gravityScale, jumpForce)
    if playerX + playerSize > xPos and playerX < (xPos + xSize) and playerY + playerSize > yPos + (ySize/2) and playerY < yPos + ySize and gravityScale < 0:
        currentVelocity = -(currentVelocity/bounceMultiplier)
        currentJumps = 0
        playerY = yPos + ySize
        if changeGravObj == True:
            gravityScale, jumpForce = changeGrav(gravityScale, jumpForce)
    return playerX, playerY, currentVelocity, currentJumps, gravityScale, jumpForce


def checkCollisionObject(xPos, yPos, xSize, ySize, objects, currentVelocity, bounceDivider):
    for obj in objects:
        i = getIndex(obj, objects)
        #print("xPos: " + str(objects[i][0]) + " yPos: " + str(objects[i][1]))
        
        if not objects[i][0] == xPos:
            if not objects[i][1] == yPos:
                if xPos > objects[i][0] and xPos + xSize < objects[i][0] + objects[i][2] and yPos + ySize > objects[i][1] and yPos < objects[i][1]:
                    yPos = objects[i][1] - ySize
                    if bounceDivider == 0:
                        bounceDivider = 2
                    currentVelocity = -(currentVelocity/bounceDivider)
                if xPos + xSize > objects[i][0] and xPos < objects[i][0] + objects[i][2] and yPos > objects[i][1] and yPos < (objects[i][1] + objects[i][3]):
                    yPos = objects[i][1] + objects[i][3]
                    if bounceDivider == 0:
                        bounceDivider = 2
                    currentVelocity = -(currentVelocity/bounceDivider)
        i = i + 1
    return xPos, yPos, currentVelocity

def toggleBool(inputBool):
    if inputBool == True:
        inputBool = False
    elif inputBool == False:
        inputBool = True

    return inputBool

def getIndex(find, strList):
    foundIndex = -1
    i=0
    while i < len(strList):
        if find == strList[i]:
            foundIndex = i
        i = i + 1
    return foundIndex

def selectObject(current, selectableObjs, direction = "+"):
    currentID = getIndex(current, selectableObjs)
    if direction == "+":
        if currentID + 1 <= len(selectableObjs):
            currentID += 1
        if currentID + 1 > len(selectableObjs):
            currentID = 0
        if currentID > len(selectableObjs):
            currentID = 0
            
    elif direction == "-":
        currentID -= 1
        if currentID < 0:
            currentID = len(selectableObjs)-1
    print(str(currentID))
    newObj = selectableObjs[currentID]
    return newObj


def Raycast(xPos, yPos, direction, width, length, objects, playerX, playerY, playerSize):
    foundObject = False
    objectIndex = -1
    foundPlayer = False
    X = xPos
    Y = yPos
    i = 0
    while i < length and foundObject == False:
        if direction == "Left":
            X = X - 5
        for obj in objects:
            if X > obj[0] and X < obj[0] + obj[2] and Y > obj[1] and Y < obj[1] + obj[3] and foundPlayer == False:
                foundObject = True
                objectIndex = getIndex(obj, objects)
                break
        if X > playerX and X < playerX + playerSize and Y > playerY and Y < playerY + playerSize and foundObject == False:
            foundPlayer = True
            break
        #pygame.draw.circle(display, (255, 255, 255), (int(X), int(Y)), 20)
        i = i + 1

    return foundPlayer, foundObject, objectIndex
        


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        # Jump
        if(event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE) and canJump:
            currentYVelocity = jumpForce
            currentJumps += 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            showingSettings = toggleBool(showingSettings)

    # Color the Window
    display.fill(levelColor[currentLevel - 1])

    raycast = Raycast(500, 700, "Left", 20, 100, levelObstacles[currentLevel-1], currentX, currentY, playerSize)

    
    if showingSettings == False:
        # Add Gravity
        currentYVelocity += gravityScale
        currentY = currentY + currentYVelocity

        # Stop falling through window
        # if currentY >= displaySize[1] - bottomPlatformOffset:
            # currentVelocity = 0
            # currentY = (displaySize[1] - bottomPlatformOffset) - 1
            # currentJumps = 0

        #User Input
        user_input = pygame.key.get_pressed()

        if user_input[pygame.K_LEFT] or user_input[pygame.K_a]:
            currentX -= 0.4
        if user_input[pygame.K_RIGHT] or user_input[pygame.K_d]:
            currentX += 0.4

        # Stop Infinite Jumps
        if currentJumps >= 2:
            canJump = False
        else:
           canJump = True

        # Drawing All Objects

        i = 0
        while i < len(levelObstacles[currentLevel - 1]):
            drawObstacle(levelObstacles[currentLevel-1][i][4], levelObstacles[currentLevel-1][i][0], levelObstacles[currentLevel-1][i][1], levelObstacles[currentLevel-1][i][5], levelObstacles[currentLevel-1][i][2], levelObstacles[currentLevel-1][i][3], levelObstacles[currentLevel-1][i][6])
            currentX, currentY, currentYVelocity, currentJumps, gravityScale, jumpForce = checkCollision(levelObstacles[currentLevel-1][i][0], levelObstacles[currentLevel-1][i][1], levelObstacles[currentLevel-1][i][2], levelObstacles[currentLevel-1][i][3], currentX, currentY, playerSize, currentYVelocity, currentJumps, playerBounceDivider, gravityScale, jumpForce, levelObstacles[currentLevel-1][i][9])
            if levelObstacles[currentLevel-1][i][7][0] == True:
                levelObstacles[currentLevel-1][i][0], levelObstacles[currentLevel-1][i][1], levelObstacles[currentLevel-1][i][7][2], levelObstacles[currentLevel-1][i][7][3] = Animate(levelObstacles[currentLevel-1][i][7][1], levelObstacles[currentLevel-1][i][7][2], levelObstacles[currentLevel-1][i][7][3], levelObstacles[currentLevel-1][i][7][4])
            if levelObstacles[currentLevel-1][i][8][0] == True:
                levelObstacles[currentLevel-1][i][0], levelObstacles[currentLevel-1][i][1], levelObstacles[currentLevel-1][i][8] = addPhysics(levelObstacles[currentLevel-1][i][0], levelObstacles[currentLevel-1][i][1], levelObstacles[currentLevel-1][i][8], gravityScale)
                levelObstacles[currentLevel-1][i][0], levelObstacles[currentLevel-1][i][1], levelObstacles[currentLevel-1][i][8][1] = checkCollisionObject(levelObstacles[currentLevel-1][i][0], levelObstacles[currentLevel-1][i][1], levelObstacles[currentLevel-1][i][2], levelObstacles[currentLevel-1][i][3], levelObstacles[currentLevel-1], levelObstacles[currentLevel-1][i][8][1], levelObstacles[currentLevel-1][i][8][2])
            i = i + 1

        # Drawing All Text
        f = 0
        while f < len(levelText[currentLevel - 1]):
            DrawText(levelText[currentLevel-1][f][0], levelText[currentLevel-1][f][1], levelText[currentLevel-1][f][2], levelText[currentLevel-1][f][3], levelText[currentLevel-1][f][4], levelText[currentLevel-1][f][5])
            f = f + 1
    
        player = drawPlayer(currentX, currentY, playerColor[currentLevel - 1], playerSize)

    # Pause Menu
    if showingSettings == True:
        DrawText(400, 300, 40, (255, 255, 255), 'Futura PT Light', 'Settings')
        if gravityScale > 0:
            if selected == "Gravity":
                DrawText(375, 400, 40, (0, 255, 0), 'Futura PT Light', 'Gravity Scale - ' + str(gravityScale)[:6])
            else:
                DrawText(375, 400, 40, (255, 255, 255), 'Futura PT Light', 'Gravity Scale - ' + str(gravityScale)[:6])
        elif gravityScale < 0:
            if selected == "Gravity":
                DrawText(375, 400, 40, (0, 255, 0), 'Futura PT Light', 'Gravity Scale - ' + str(gravityScale)[:6])
            else:
                DrawText(375, 400, 40, (255, 255, 255), 'Futura PT Light', 'Gravity Scale - ' + str(gravityScale)[:6])
        if selected == "Quit":
            DrawText(440, 450, 40, (0, 255, 0), 'Futura PT Light', 'Quit')
        else:
            DrawText(440, 450, 40, (255, 255, 255), 'Futura PT Light', 'Quit')

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            if selected == "Gravity" and showingSettings:
                gravityScale += 0.000005
        if keys[pygame.K_LEFT]:
            if selected == "Gravity" and showingSettings:
                gravityScale -= 0.000005
        if keys[pygame.K_UP]:
            selected = selectObject(selected, selectables, "-")
            sleep(0.2)
        if keys[pygame.K_DOWN]:
            selected = selectObject(selected, selectables, "+")
            sleep(0.2)
        if keys[pygame.K_RETURN]:
            if selected == "Quit" and showingSettings:
                break

    pygame.display.update()

writeSettings(settingsDataPath, gravityScale)
pygame.quit()
sleep(0.1)
exit()

