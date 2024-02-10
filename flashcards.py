from tkinter import *
import tkinter.messagebox as tmsg 
from tkinter.filedialog import askopenfilename, asksaveasfilename #for saving files in a directory
import pickle #save draw object in pickle file
from tkinter.colorchooser import askcolor #custom color palates
import math
import dataEditor

#**********************************************************************
#**********************************************************************
# Large parts of this file are copied and modified from:
#   https://dev.to/fahad_islam/python-project-a-drawing-pad-gui-3f42
#**********************************************************************
#**********************************************************************

# Starting point of mouse dragging or shapes
global prev_x
global prev_y
prev_x = 0 
prev_y = 0 
# Current x,y position of mouse cursor or end position of dragging
x = 0 
y = 0
global created_element_info #list of all shapes objects for saving drawing
created_element_info = []
new = [] # Each shapes of canvas
created = [] # Temporary list to hold info on every drag
# shape = "Stroke" # Shape to draw
color = "blue" # Color of the shape

global colorList
global colorIndex
colorIndex = 0
colorList = ["red","orange", "green", "blue","purple"]
global saveFileName
saveFileName = "testfail.pkl"
global openFilePrefix
openFilePrefix = "Characters/"
global setNameVar
global givenPrefix
global cardIndex
cardIndex = 0
global line_width
line_width = 13 # Width of the line shape


# Update the previous position on mouse left click
def recordPosition(e=""):
    # colors if drawing kanji, black if its just the description
    #perhaps base this off another variable that can be toggled with a button or a hotkey for drawing kanji when quizzing oneself
    colors = globals()["colorList"]
    if globals()["openFilePrefix"] == "Characters/":
        globals()["color"] = colors[globals()["colorIndex"]%len(colors)]
        globals()["colorIndex"] +=1
    else:
        globals()["color"] = "black"
    globals()["prev_x"] = e.x
    globals()["prev_y"] = e.y
    
def release():
    print("released")
    #TODO: Why isnt this working?
    #TODO: eventually go through last few (~5?) linked lines unless there's a gap then stop, 
    #       reduce thickness of a line following curve

# Color Picker
def colorPicker(e=""):
    global color
    color = askcolor(color=color)[1]
    #Set the color of shapes
    root.config(cursor=f"cursor {color} {color}", insertbackground=f"{color}")

# Update the current shape
def shapechanger(e=""):
    global shape
    shape = radiovalue.get() #selected radio value

# Runs On scale value change and update line width
def setlinewidth(e=""):
    global line_width
    
    # Save the drawing on a file

# After Every drawing create info of drawing and add the element to new list and assign empty list to created

# Create Elements on canvas based on shape variable
def createElms():
    a = canvas.create_line(prev_x, prev_y, x, y,
                            width=line_width, fill=color,
                            capstyle=ROUND, smooth=TRUE, splinesteps=3)
    return a

# Create shapes on mouse dragging and resize and show the shapes on the canvas
def drawShapesOnDragging(e=""):
    global x,y
    
    try:
        # Update current Position
        x = e.x
        y = e.y
        if (x == globals()["prev_x"] and y == globals()["prev_y"] ):
            return 
        
        element = createElms()
        #ill be tweaking this till the day i die.
        width = 0.9* max(0,15+-1.2*math.sqrt(abs(x-globals()["prev_x"])**2 + abs(y-globals()["prev_y"])**2))
        globals()["line_width"] = width
        
        created_element_info_obj = {
        "c": color,
        "px": globals()["prev_x"],
        "py": globals()["prev_y"],
        "x": x,
        "y": y,
        "lw": width
    }
        
        globals()["created_element_info"].append(created_element_info_obj)
        globals()["prev_x"] = x
        globals()["prev_y"] = y
            
    except Exception as e:
        tmsg.showerror("Some Error Occurred!", e)
    
def updateStatus(message):
    globals()["status"].set(message)
    globals()["statusbar"].update()

def createCard(e=""):
    
    if (globals()["setNameVar"].get() == ""): return
    globals()["colorIndex"] = 0
    clearCanvas()
    name = globals()["setNameVar"].get() # TODO: set a text input box to allow name to go in
    globals()["saveFileName"] = name
    globals()["openFilePrefix"] = "Characters/"
    root.title(openFilePrefix+saveFileName)
    result = dataEditor.newCard(name)
    globals()["setNameVar"].set("")
    
    updateStatus(result)
    getsavedrawing()
    
def deleteCard(e=""):
    
    clearCanvas()
    dataEditor.removeCard(globals()["saveFileName"])
    globals()["cardIndex"] -= 1
    skipCard()
    updateStatus("Card Deleted")
    
# go to the next card in the list
def skipCard(e=""):
    
    clearCanvas()
    #fetch the next card in the list
    card = dataEditor.listCards[(globals()["cardIndex"])]
    globals()["saveFileName"] = card[0]
    #jiggle the values to make it lean towards the unpracticed card, but still include the well practiced one
    if ((int(card[1])+1) / (int(card[2])+1)*dataEditor.random.randint(50,200)/100> (int(card[3])+1) / (int(card[4])+1)*dataEditor.random.randint(50,200)/100): # TODO: add a jiggle
        globals()["openFilePrefix"] = "Descriptions/"
    else:
        globals()["openFilePrefix"] = "Characters/"
    #store the loaded card so that when flipped, scores can be applied appropriately
    globals()["givenPrefix"] = globals()['openFilePrefix']
    #load that card onto the canvas
    getsavedrawing()
    # reshuffle the cards every[16] cards, so that the whole list isnt run through every time
    # TODO: maybe add a slider in the program to adjust this easier, 
    # root.title(openFilePrefix+saveFileName) # i've elected not to update the card on changed card in order to
    # keep it hidden for learning sake
    globals()["cardIndex"]+=1
    if (globals()["cardIndex"]>= 16):
        print(dataEditor.listCards)
        dataEditor.shuffle()
        globals()["cardIndex"] = 0
    
    # if there aren't enough cards, loop TODO: improve this as this means no reshuffling... just add an if loop you dumbass
    globals()["cardIndex"]%=len(dataEditor.listCards)
    
    updateStatus("Next Card")
    

def correctAnswer(e=""):
    dataEditor.correct(globals()["saveFileName"], globals()["givenPrefix"])
    skipCard()
    
def incorrectAnswer(e=""):
    dataEditor.incorrect(globals()["saveFileName"], globals()["givenPrefix"])
    skipCard()

def flipCard(e=""):
    
    if (globals()["openFilePrefix"] == "Descriptions/"):
        
        globals()["openFilePrefix"] = "Characters/"
    else:
        globals()["openFilePrefix"] = "Descriptions/"
        
    clearCanvas()
    root.title(openFilePrefix+saveFileName)
    getsavedrawing()
    updateStatus("Card flipped")
    
# ----- below this point is much less custom and more direct from the page i got it from ------
# i've still made many changes, but its fairly trivial edits. 

# Save the list of shapes objects on a pickle file // lol pickle 
def saveDrawingFile(e=""):
    filename = openFilePrefix+globals()["saveFileName"] + ".pkl"
    # filename = asksaveasfilename(initialfile="drawing",defaultextension=".pkl",filetypes=[("Pickle Files", "*.pkl")]) #Save as
    if filename != None: 
        with open(filename, "wb") as f:
            pickle.dump(globals()["created_element_info"], f)
            updateStatus("Saved!")
    return
    


def getsavedrawing():
    global x, y, prev_x, prev_y, shape, color, line_width
    # filename = askopenfilename(defaultextension=".pkl", filetypes = [("Pickle Files", "*.pkl")])
    filename = openFilePrefix+globals()["saveFileName"] + ".pkl"
    if filename != None:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            for draw_info in data:
                x = draw_info["x"]
                y = draw_info["y"]
                prev_x = draw_info["px"]
                prev_y = draw_info["py"]
                # shape = draw_info["type"]
                color = draw_info["c"]
                line_width = draw_info["lw"]
                createElms() #Draw each shapes

# Clear the Canvas
def clearCanvas(e=""):
    globals()["colorIndex"] = 0
    global created_element_info, canvas, created, new
    canvas.delete("all")
    globals()["created_element_info"] = []
    created = []
    new = []
    
def edit(file):
    globals()["saveFileName"] = file
    global canvas
    global radiovalue
    global root
    root = Tk()
    root.title(openFilePrefix + saveFileName)
    root.minsize(600,300) #Minimum Size of the window
    # All Widgets here such as canvas, buttons etc

    # Canvas
    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 600
    
    canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
    canvas.pack()

    # Binding Events to canvas
    # Structure: canvas.bind("<eventcodename>", function-name)
    canvas.bind("<1>", recordPosition) #On Mouse left click
    canvas.bind("<B1-Motion>", drawShapesOnDragging) #Capture Mouse left click + move (dragging)
    canvas.bind("ButtonRelease-1", release) #When Mouse left click release
    
    frame = Frame(root)
    frame.pack(side=BOTTOM)
    
    radiovalue = StringVar()
    geometry_shapes = ["Stroke"]
    radiovalue.set("Line") #Default Select
    
    
    # okay i did add a bunch of buttons and stuff
    #Buttons
    Button(frame, text="Skip", font="comicsans 12 bold",
           command=skipCard).pack(side=LEFT, padx=0, pady=6)
    
    Button(frame, text="Flip", font="comicsans 12 bold",
           command=flipCard).pack(side=LEFT, padx=0, pady=6)
    
    Button(frame, text="Correct", font="comicsans 12 bold",
           command=correctAnswer).pack(side=LEFT, padx=(12,0), pady=6)
    
    Button(frame, text="Incorrect", font="comicsans 12 bold",
           command=incorrectAnswer).pack(side=LEFT, padx=0, pady=6)
    
    Button(frame, text="New", font="comicsans 12 bold",
           command=createCard).pack(side=RIGHT, padx=6, pady=6)
    # I forgot where i found about StringVar's but its just part of how this is supposed to be used so i don't feel bad about leaving out credit
    globals()["setNameVar"] = StringVar()
    Entry(frame, name="test", textvariable = setNameVar ).pack(side=RIGHT, padx=6, pady=6)
    
    Button(frame, text="Delete", font="comicsans 12 bold",
        command=deleteCard).pack(side=RIGHT, padx=12)
    
    Button(frame, text="Save", font="comicsans 12 bold",
        command=saveDrawingFile).pack(side=RIGHT, padx=0, pady=6)
    
    Button(frame, text="Clear", font="comicsans 12 bold",
        command=clearCanvas).pack(side=RIGHT, padx=12)

    root.bind('<Return>', createCard)
    
    global status
    global statusbar
    status = StringVar()
    statusbar = Label(root, textvariable=status, anchor="w", relief=SUNKEN)
    statusbar.pack(side=BOTTOM, fill=X)
    #load a card, idk why this got it working, but im not changing it
    try:
        dataEditor.getCards()
        skipCard()
        getsavedrawing()
        dataEditor.shuffle()
        skipCard()
        
    except:
        pass
    root.mainloop()
    
# o shoot, this explains a few of my problems
#
# welp, im not changing it now since it works :)
if __name__ == "__main__":
    edit("test1.pkl")
