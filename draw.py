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

global cardIndex
cardIndex = 0
global line_width
line_width = 13 # Width of the line shape



# All the functions and logics go here
#Capture Motions on every mouse position change
def captureMotion(e=""):
    pass
    # #Update Status Bar
    # status.set(f"Position : x - {e.x} , y - {e.y}")
    
    # statusbar.update()
    # globals()["prev_x"] = e.x
    # globals()["prev_y"] = e.y
    


# Update the previous position on mouse left click
def recordPosition(e=""):
    colors = globals()["colorList"]
    if globals()["openFilePrefix"] == "Characters/":
        globals()["color"] = colors[globals()["colorIndex"]%len(colors)]
        globals()["colorIndex"] +=1
    else:
        globals()["color"] = "black"
    globals()["prev_x"] = e.x
    globals()["prev_y"] = e.y
    

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
        
        element = createElms()
        width = 0.7* max(0,25+-2*math.sqrt(abs(x-globals()["prev_x"])**2 + abs(y-globals()["prev_y"])**2))
        globals()["line_width"] = width
        # deleteUnwanted(element) # Delete unwanted shapes
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
    

def deleteUnwanted(element):
    global created
    created.append(element) #Elements that created
    for item in created[:-1]: 
        canvas.delete(item)
        
def createCard(e=""):
    clearCanvas()
    name = globals()["setNameVar"].get() # TODO: set a text input box to allow name to go in
    globals()["saveFileName"] = name
    globals()["openFilePrefix"] = "Characters/"
    root.title(openFilePrefix+saveFileName)
    result = dataEditor.newCard(name)
    globals()["setNameVar"].set("")
    
    globals()["status"].set(result)
    globals()["statusbar"].update()
    getsavedrawing()
    
def deleteCard(e=""):
    clearCanvas()
    dataEditor.removeCard(globals()["saveFileName"])
    globals()["cardIndex"] -= 1
    skipCard()

def skipCard(e=""):
    clearCanvas()
    card = dataEditor.listCards[(globals()["cardIndex"])]
    globals()["saveFileName"] = card[0]
    
    if ((int(card[1])+1) / (int(card[2])+1)*dataEditor.random.randint(50,200)/100> (int(card[3])+1) / (int(card[4])+1)*dataEditor.random.randint(50,200)/100): # TODO: add a jiggle
        globals()["openFilePrefix"] = "Descriptions/"
    else:
        globals()["openFilePrefix"] = "Characters/"
    getsavedrawing()
    
    globals()["cardIndex"]+=1
    if (globals()["cardIndex"]>= 16):
        dataEditor.shuffle()
        globals()["cardIndex"] = 0
        
    globals()["cardIndex"]%=len(dataEditor.listCards)
    

def correctAnswer(e=""):
    dataEditor.correct(globals()["saveFileName"], globals()["openFilePrefix"])
    skipCard()
    
def incorrectAnswer(e=""):
    dataEditor.incorrect(globals()["saveFileName"], globals()["openFilePrefix"])
    skipCard()

def flipCard(e=""):
    if (globals()["openFilePrefix"] == "Descriptions/"):
        
        globals()["openFilePrefix"] = "Characters/"
    else:
        globals()["openFilePrefix"] = "Descriptions/"
        clearCanvas()
    
    root.title(openFilePrefix+saveFileName)
    getsavedrawing()
    
# Save the list of shapes objects on a pickle file
def saveDrawingFile(e=""):
    
    filename = openFilePrefix+globals()["saveFileName"] + ".pkl"
    # filename = asksaveasfilename(initialfile="drawing",defaultextension=".pkl",filetypes=[("Pickle Files", "*.pkl")]) #Save as
    if filename != None: 
        with open(filename, "wb") as f:
            pickle.dump(globals()["created_element_info"], f)
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
    # canvas.bind("<B1-Motion>", generateShapesObj) #When Mouse left click release
    canvas.bind("<Motion>", captureMotion) #Mouse Motion
    frame = Frame(root)
    frame.pack(side=BOTTOM)
    
    radiovalue = StringVar()
    geometry_shapes = ["Stroke"]
    radiovalue.set("Line") #Default Select
    
    
    # Manupulates Radios from the list
    # for shape in geometry_shapes:
    #     radio = Radiobutton(frame, text=shape, variable=radiovalue, font="comicsans     12 bold", value=shape, command=shapechanger).pack(side=LEFT, padx=6,pady=3)

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
    
    globals()["setNameVar"] = StringVar()
    Entry(frame, name="test", textvariable = setNameVar ).pack(side=RIGHT, padx=6, pady=6)
    
    
    Button(frame, text="Delete", font="comicsans 12 bold",
        command=deleteCard).pack(side=RIGHT, padx=12)
    
    Button(frame, text="Save", font="comicsans 12 bold",
        command=saveDrawingFile).pack(side=RIGHT, padx=0, pady=6)
    
    Button(frame, text="Clear", font="comicsans 12 bold",
        command=clearCanvas).pack(side=RIGHT, padx=12)
    
    
    
    

    
    
    # Scale
    # scale = Scale(root, from_=1, to=20, orient=HORIZONTAL, command=setlinewidth)
    # scale.pack(side=BOTTOM)

    # Status Bar
    global status
    global statusbar
    status = StringVar()
    statusbar = Label(root, textvariable=status, anchor="w", relief=SUNKEN)
    statusbar.pack(side=BOTTOM, fill=X)
    #load the saved 
    try:
        dataEditor.getCards()
        skipCard()
        getsavedrawing()
    except:
        pass
    root.mainloop()
    
    
    
    
    
if __name__ == "__main__":
    edit("test1.pkl")
