from tkinter import Tk, Text, W, N, E, S, Canvas, StringVar, OptionMenu
from tkinter.ttk import Frame, Button, Label

# Constants

TIMEOUT = 100 # Delay between generations
WIDTH = 666   # Width of displayed canvas
HEIGHT = 477  # Height of displayed canvas
SCALE = 9     # Relationship of cell coordinates to canvas coordinates

# Classes
    
class Colony:
    'class to represent a life colony'
    
    def __init__(self):
        'empty colony and reset generation'
        self.cells = {}
        self.generation = 1
        
    def addCell(self, x, y):
        'add cell to colony'
        self.cells[(x,y)] = True
        
    def getCells(self):
        'return list of cell coordinates'
        return self.cells.keys()
    
    def toggle(self, x, y):
        'toggle live/dead status of cell at x, y'
        if (x,y) in self.cells:
            del self.cells[(x,y)]
        else:
            self.cells[(x,y)] = True
    
    def countNeighbours(self, x, y):
        'count neighbours of cell at x, y'
        count = 0
        for nx in [x - 1, x, x + 1]:
            for ny in [y - 1, y, y + 1]:
                if ((x != nx or y != ny) and (nx,ny) in self.cells):
                    count += 1
                    # Greater than three is always bad
                    if (count > 3):
                        return count
        return count
    
    def getGeneration(self):
        return self.generation
    
    def getCellCount(self):
        return len(self.cells)
    
# Renegerate colony using rules from http://en.wikipedia.org/wiki/Conway's_Game_of_Life#Rules
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overcrowding.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction. 
         
    def regenerate(self):
        'regenerate colony using standard life rules'
        newCells = {}
        tested = {}
        # Loop through cells
        for cell in self.cells.keys():
            cx = cell[0]
            cy = cell[1]
            # Loop through cell and neighbours
            for x in (cx - 1, cx, cx + 1):
                for y in (cy - 1, cy, cy + 1):
                    # Only test each cell once
                    if ( not (x,y) in tested ):
                        tested[(x,y)] = True
                        # Count neighbours of cell and neighbours
                        count = self.countNeighbours(x, y)
                        if ( ( count == 3 ) or
                            (( count == 2 ) and (x,y) in self.cells ) ):
                            newCells[(x,y)] = True
        self.cells = newCells
        self.generation += 1

class Life:
    'Class to manage the Life GUI'

    # Pre-defined shapes

    DEFAULT_SHAPE = "F-pentomino"

    shapes = {
        "Empty" : {
            "position" : "center",
            "rows" : []
        },
        "F-pentomino" : {
            "position" : "center",
            "rows" : [
                ".OO",
                "OO.",
                ".O."
            ]
        },
        "Acorn" : {
            "position" : "center",
            "rows" : [
                ".O.....",
                "...O...",
                "OO..OOO"
            ]
        },
        "Bunnies" : {
            "position" : "center",
            "rows" : [
                "O.....O.",
                "..O...O.",
                "..O..O O",
                ".O.O...."
            ]
        },
        "Lidka" : {
            "position" : "center",
            "rows" : [
                ".O.......",
                "O.O......",
                ".O.......",
                ".........",
                ".........",
                ".........",
                ".........",
                ".........",
                ".........",
                ".........",
                "........O",
                "......O.O",
                ".....OO.O",
                ".........",
                "....OOO.."
            ]
        },
        "Glider" : {
            "position" : "topleft",
            "rows" : [
                ".O.",
                "..O",
                "OOO"
            ]
        },
        "Lightweight Spaceship" : {
            "position" : "left",
            "rows" : [
                "O..O.",
                "....O",
                "O...O",
                ".OOOO"
            ]
        },
        "Gosper Glider Gun": {
            "position" : "topleft",
            "rows" : [
                "........................O",
                "......................O.O",
                "............OO......OO............OO",
                "...........O...O....OO............OO",
                "OO........O.....O...OO",
                "OO........O...O.OO....O.O",
                "..........O.....O.......O",
                "...........O...O",
                "............OO"
            ]
        },
        "Puffer Train": {
            "position" : "left",
            "rows" : [
                "...O.",
                "....O",
                "O...O",
                ".OOOO",
                ".....",
                ".....",
                ".....",
                "O....",
                ".OO..",
                "..O..",
                "..O..",
                ".O...",
                ".....",
                ".....",
                "...O.",
                "....O",
                "O...O",
                ".OOOO"
            ]
        },
    }

    def __init__(self):

        # Displacemet to put shape at 0,0 in center of canvas
        self.ox = 0
        self.oy = 0

        # Defaults
        self.scale = SCALE
        self.colony = None
        self.shape_name = Life.DEFAULT_SHAPE

        # Set up screen widgets
        root = Tk()

        title = Label(root, text="Life v3.0 by Jon Nixon",font='bold')
        title.grid(row=0,column=0,columnspan=2,padx=4,pady=4,sticky=W+E)

        help = Label(root, text="Choose a shape and press start, or click on cells to change them")
        help.grid(row=1,column=0,padx=4,pady=4,sticky=W+E)

        status = Label(root, text="Generation: 0, Cells: 0")
        status.grid(row=1, column=1, padx=4,pady=4,sticky=E)

        self.status = status

        row2a=Frame(root)
        row2a.grid(row=2,column=0,padx=4,pady=4,sticky=W+E)
        shape_label = Label(row2a, text="Shape:")
        shape_label.grid(row=0,column=0,sticky=W)
        shape_field = StringVar(row2a)
        shape_field.set(self.DEFAULT_SHAPE)
        shape_keys = Life.shapes.keys()
        shape_menu = OptionMenu(row2a, shape_field, *shape_keys, command=self.reset)
        shape_menu.grid(row=0,column=1,padx=4,sticky=W)

        start_button = Button(row2a, text="Start",command=self.start)
        start_button.grid(row=0,column=2,padx=2,sticky=W)
        stop_button = Button(row2a, text="Stop",command=self.stop)
        stop_button.grid(row=0,column=3,padx=2,sticky=W)
        reset_button = Button(row2a, text="Reset", command=self.reset)
        reset_button.grid(row=0,column=4,padx=2,sticky=W)

        row2b=Frame(root)
        row2b.grid(row=2,column=1,padx=4,pady=4,sticky=E)
        clear_button = Button(row2b, text="Clear", command=self.clear)
        clear_button.grid(row=0,column=0,sticky=W+E)

        canvas=Canvas(root,width=WIDTH,height=HEIGHT,bg="black")
        canvas.grid(row=3,column=0,columnspan=2,padx=4,pady=4,sticky=N+W)

        canvas.bind("<Button-1>", self.mouseclick)

        # Instance variables
        self.root = root
        self.job = None
        self.canvas = canvas

    def mouseclick(self, event):
        'Catch mouseclick in cavas and toggle cell at that locatio'
        x = event.x // self.scale - self.ox
        y = event.y // self.scale - self.oy
        self.colony.toggle(x, y)
        self.redraw()

    def stop(self):
        'Stop animation (cancel existig job)'
        if self.job != None:
            self.root.after_cancel(self.job)
            self.job = None

    def start(self):
        'start animation (create new job)'
        self.job = self.root.after(TIMEOUT, self.cycle)

    def clear(self):
        'Clear colony (stop, create empty colony abd redraw)'
        self.stop()
        self.colony = Colony()
        self.redraw()

    def reset(self, shape_name = None):
        'Reset colony to last reuested shape or default shape'

        # Allow reset to use previous shape name
        if shape_name == None:
            shape_name = self.shape_name
        else:
            self.shape_name = shape_name

        # Empty colony
        self.clear()
        self.scale = SCALE

        colony = self.colony
        scale = self.scale

        # Get shape from list
        shape = Life.shapes[shape_name]
        position = shape["position"]
        rows = shape["rows"]

        # Will determine size of shape
        maxX = 0
        maxY = 0

        # Loop through shape, adding cells to colony
        for y in range(len(rows)):
            row = rows[y]
            for x in range(len(row)):
                if row[x] == 'O':
                    colony.addCell(x, y)
                if x > maxY:
                    maxX = x
            maxY = y

        # Position colony on screen
        if position == "topleft":
            self.ox = 2
            self.oy = 2
        elif position == "left":
            self.ox = 2
            self.oy = int( ( HEIGHT / self.scale - maxY ) / 2 )
        else:
            self.ox = int( ( WIDTH / self.scale - maxX ) / 2 )
            self.oy = int( ( HEIGHT / self.scale - maxY ) / 2 )

        # First draw
        self.redraw()

    def redraw(self):
        'Redraw colony on canvas'

        canvas = self.canvas
        colony = self.colony
        scale = self.scale
        status = self.status
        ox = self.ox
        oy = self.oy

        # Draw grid
        canvas.delete("all")
        for y in range(int(HEIGHT / scale)):
            canvas.create_line(1, y * scale + 1, WIDTH + 1, y * scale + 1, fill="gray")
        for x in range(int(WIDTH / scale)):
            canvas.create_line(x * scale + 1, 1, x * scale + 1, HEIGHT + 1, fill="gray")
        # Loop through cells
        for cell in colony.getCells():
            x = ox + cell[0]
            y = oy + cell[1]
            if ( x >= 0 and x * scale < WIDTH and y >=0 and y * scale < HEIGHT):
                canvas.create_rectangle(x * scale + 2, y * scale + 2, (x + 1) * scale, (y + 1) * scale, fill="white")
                status.configure(text="Generation: "+str(colony.getGeneration())+", Cells: "+str(colony.getCellCount()))

    def cycle(self):
        'Cycle GUI (regenerate colony and the redraw it'
        colony = self.colony
        colony.regenerate()
        self.redraw()
        self.job = self.root.after(TIMEOUT, self.cycle)

    def run(self):
        'Start new GUI'
        self.reset(self.DEFAULT_SHAPE)
        self.redraw()
        self.root.mainloop()

# Start GUI
life = Life()
life.run()