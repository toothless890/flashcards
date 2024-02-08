import draw
import time
import os

#either update or add a new card (will update if name is in list(make a naming convention to avoid overriding cards!))
def newCard(name):
    #save the kanji
    #TODO: put the Characters/ and .pkl in the draw file, and edit the globals
    #save the description
    #create a data entry
    
    # if name is  not in data.txt then append it. else, just close
    if (not checkCard(name)): 
        file =  open("data.txt", "a")
        file.write(str(name) + ", 0, 0, 0, 0\n")
        file.close()
        return "Saved successfuly! Remember to flip!"
    else:
        
        return "Error! Card with that name already exists"
    
    

#get a list of all cards
# TODO: perhaps optimize to only get run once, and update internally. 
# But i'm not too worried, only runs every now and then, performance isnt a huge deal
def getCards():
    file = open("data.txt")
    data = {}
    for line in file.readlines(-1):
        line = line.replace("\n", "")
        lc = line.split(", ")
        data[lc[0]] = [lc[1], lc[2], lc[3], lc[4]]
    return data

# Check if the card is in the list
def checkCard(name):
    return getCards().get(name) != None

def removeCard(name):
    if(checkCard(name)):
        os.remove("Characters/"+name+".pkl")
        os.remove("Descriptions/"+name+".pkl")
        file = open("data.txt", "r+")
        replicated = file.readlines()
        file.seek(0) # is this necessary?
        for line in replicated:
            if line.split(", ")[0] != name:
                file.write(line)
        file.truncate()
        
# def viewCard(name):
#     draw.view

newCard("hi")
