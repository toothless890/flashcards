import draw
import time
import os
import random
global listCards
listCards = []
#either update or add a new card (will update if name is in list(make a naming convention to avoid overriding cards!))
def newCard(name):
  
    # if name is  not in data.txt then append it. else, just close
    if (not fetchCardIndex(name)): 
        
        listCards.append(str(name) + ", 0, 0, 0, 0\n")
        saveList()
        return "Created successfuly! Remember to flip!"
    else:
        
        return "Error! Card with that name already exists"
    

def shuffle():
    # 0 = name, 1 = char succ, 2 = car total, 3= desc succ, 4 = desc total
    
    listCards.sort(key=lambda score: score[1]/score[2]+score[3]/score[4]* (random.randrange(90, 110)/100))
    pass

def correct(name, side):
    index = fetchCardIndex(name)
    if side == "Characters/":
        listCards[index][1]+=1
        listCards[index][2]+=1
    else:
        listCards[index][3]+=1
        listCards[index][4]+=1
    saveList()
def incorrect(name, side):
    index = fetchCardIndex(name)
    if side == "Characters/":

        listCards[index][2]+=1
    else:

        listCards[index][4]+=1
    saveList()

#get a list of all cards
def getCards():
    file = open("data.txt", "r")
    # data = {}
    for line in file.readlines(-1):
        line = line.replace("\n", "")
        lc = line.split(", ")
        listCards.append(lc)
    file.close()
    return listCards
    

# Check if the card is in the list


def fetchCardIndex(name):
    for x in range( len(listCards)):
        if listCards[x][0] == name:
            return x
    return False

def removeCard(name):
    os.remove("Characters/"+name+".pkl")
    os.remove("Descriptions/"+name+".pkl")
    index = fetchCardIndex(name)
    listCards.pop(index)
    saveList()
        
def saveList():
    file = open("data.txt", "r+")
    for line in listCards:
        file.write(line)
    file.truncate()
# def viewCard(name):
#     draw.view
