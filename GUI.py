import tkinter as tk
from tkinter import ttk
from Pieces.Bishop import *
from Pieces.King import *
from Pieces.Knight import *
from Pieces.Pawn import *
from Pieces.Queen import *
from Pieces.Rook import *
from Mouse import *
#import game

square_size = 64

WHITE_COLOUR = "#ffffff"
global DARKGREEN_COLOUR
DARKGREEN_COLOUR = "#006600"

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess Game")

class mainMenu(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container


        self.enterIpPlay = tk.Text(self, height=1)
        self.playGameButton = tk.Button(self, text="Play Game", command=self.playgamebuttonpressed)
        self.enterIpWatch = tk.Text(self, height=1)
        self.watchGameButton = tk.Button(self, text="Watch Game", command=self.watchgamebuttonpressed)
        self.settingsButton = tk.Button(self, text="Settings", command=self.settingsbuttonpressed)
        self.exitButton = tk.Button(self, text="Exit", command=tk._exit)

        self.place(relx=.5, rely=.5, anchor="center")
        self.enterIpPlay.grid(row=0, ipadx=64, sticky ="N, E, S, W")
        self.playGameButton.grid(row=1, ipadx=64, sticky ="N, E, S, W")
        self.enterIpWatch.grid(row=2, ipadx=64, sticky = "N, E, S, W")
        self.watchGameButton.grid(row=3, ipadx=64, sticky ="N, E, S, W")
        self.settingsButton.grid(row=4, ipadx=64, sticky ="N, E, S, W")
        self.exitButton.grid(row=5, ipadx=64, sticky ="N, E, S, W")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

    def playgamebuttonpressed(self):
        #just to get the ip address, idk what to do with it
        ipaddress = self.enterIpPlay.get("1.0",'end-1c')
        self.destroy()
        board = GameBoard(self.container)
        board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        board.mainloop()

    def watchgamebuttonpressed(self):
        #just to get the ip address, idk what to do with it:
        ipaddress = self.enterIpWatch.get("1.0", 'end-1c')
        self.destroy()
        board = GameBoard(self.container)
        board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        board.mainloop()

    def settingsbuttonpressed(self):

        self.settingsWindow = tk.Toplevel(self.container)
        self.settingsLabel = tk.Label(self.settingsWindow , text="Settings")
        self.settingsTextBox = tk.Text(self.settingsWindow, height=1)
        self.settingsButton = tk.Button(self.settingsWindow , text="Change Board Square Colour", command = self.swapColour)

        self.settingsLabel.grid(row=0, ipadx=64, sticky ="N, E, S, W")
        self.settingsTextBox.grid(row=2, ipadx=64, sticky ="N, E, S, W")
        self.settingsButton.grid(row=3, ipadx=64, sticky ="N, E, S, W")

    def swapColour(self):
        newColour = self.settingsTextBox.get("1.0", "end-1c")
        newColour = newColour.split()
        global DARKGREEN_COLOUR
        DARKGREEN_COLOUR = newColour[0]
        global WHITE_COLOUR
        WHITE_COLOUR = newColour[1]
        self.settingsWindow.destroy()


class Settings(ttk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

class GameBoard(ttk.Frame):
    def __init__(self, parent):
        #self.window = Tk()
        #self.window.title("Chess Game")
        tk.Frame.__init__(self, parent)
        self.colour1 = "#006600"
        self.colour2 = "#ffffff"
        self.dim = 8
        self.mouse = Mouse(self)
        self.square_size = 64
        self.canvas = tk.Canvas(self, width=self.square_size * self.dim, height=self.square_size * self.dim)
        self.canvas.pack()
        self.play_again()


        tk.Widget.bind(self.canvas, "<1>", self.mouse.mouseDown)
        tk.Widget.bind(self.canvas, "<B1-Motion>", self.mouse.mouseMove)
        tk.Widget.bind(self.canvas, "<ButtonRelease-1>", self.mouse.mouseUp)



    def deletePiece(self, dyingPiece):
        print("##deleting##")
        #delete from piece matrix and the lists
        #x, y = dyingPiece.position[0], dyingPiece.position[1]
        #self.canvas.delete(self.pieces[0][1])
        #self.pieces[y].pop(x)
        #self.piecesTwo[y].pop(x)
        
        #self.pieces_all.remove(dyingPiece)
        

    def checkBlocked(self, currentPiece, endx, endy):
        tempStartx = currentPiece.position[0]
        tempStartY = currentPiece.position[1]

        while tempStartx != endx or tempStartY != endy:
            if endx != tempStartx:
                if endx > tempStartx:
                    tempStartx += 1
                elif endx < tempStartx:
                    tempStartx -= 1
            if endy != tempStartY:
                if endy > tempStartY:
                    tempStartY += 1
                elif endy < tempStartY:
                    tempStartY -= 1
                    
            for piece in self.pieces_all:
                if piece.position[0] ==  tempStartx and piece.position[1] == tempStartY:
                    if piece.position[0] == endx and piece.position[1] == endy:
                        pass
                        #if the piece blocking is on the last square then its trying to take instead
                        #colour doesnt matter it was filtered out in legal moves first
                        return True
                    if type(currentPiece).__name__ != "Knight":
                        #if theres a piece in the path
                        #i want to know is it the last piece
                        print("blocked")
                        return False


    def checkIfLegalMove(self, startCoordX, startCoordY, endCoordX, endCoordY, currentPiece, targetSquare):
        availableMoves = currentPiece.check_valid_moves()
        valid = False
        if targetSquare != False:
            if currentPiece.color == targetSquare.color:
                return False
        for i in availableMoves:
            if i[0] == endCoordX and i[1] == endCoordY:
                valid = True
        if valid == False or self.checkBlocked(currentPiece, endCoordX, endCoordY) == False:
            return False            

    def showLegalMoves(self, piece):
        list_of_moves = piece.check_valid_moves()
        for coord in list_of_moves:
            if coord[0]+coord[1]%2:
                self.setColour(coord[0],coord[1])
            else:
                self.board[coord[0]][coord[1]] = self.canvas.create_rectangle(coord[0], coord[1],  coord[0]+square_size, coord[1]+square_size, outline="black", fill="#FFFDD0",
                                                                tags="square")

    def movePiece(self, pieceId, endCoordY, endCoordX):
        pass
        #moves a piece to the selected coords
        #so we can move the opponents pieces

        #this moves the white rook in the top left to the middle of the board
        #self.movePiece(self.pieces[0][0], 3, 3)
        startX = int(self.canvas.coords(pieceId)[0])
        startY = int(self.canvas.coords(pieceId)[1])
        endCoordX *= self.square_size
        endCoordY *= self.square_size
        self.canvas.tag_raise(pieceId)
        self.canvas.move(pieceId, (endCoordX-startX), (endCoordY-startY))

    def initialize_board(self):
        #creates a chess board and places the pieces
        #and stores the squares in a board matrix
        squareMatrix = [0] * self.dim
        for x in range(self.dim):
            squareMatrix[x] = [0] * self.dim

        self.board = squareMatrix

        self.pieces = squareMatrix

        self.piecesTwo = squareMatrix

        self.pieces_all = []

        self.row0 = [Rook("white", self,(0,0)),
        Knight("white", self,(1, 0)),
        Bishop("white", self,(2, 0)),
        King("white", self,(3, 0)),
        Queen("white", self,(4, 0)),
        Bishop("white", self,(5, 0)),
        Knight("white", self, (6, 0)),
        Rook("white", self,(7, 0))]

        self.row1 = [Pawn("white", self, (0, 1)),
        Pawn("white", self, (1, 1)),
        Pawn("white", self, (2, 1)),
        Pawn("white", self, (3, 1)),
        Pawn("white", self, (4, 1)),
        Pawn("white", self, (5, 1)),
        Pawn("white", self, (6, 1)),
        Pawn("white", self, (7, 1))]

        self.row6 = [Pawn("black", self, (0, 6)),
        Pawn("black", self, (1, 6)),
        Pawn("black", self, (2, 6)),
        Pawn("black", self, (3, 6)),
        Pawn("black", self, (4, 6)),
        Pawn("black", self, (5, 6)),
        Pawn("black", self, (6, 6)),
        Pawn("black", self, (7, 6))]

        self.row7 = [Rook("black", self, (0, 7)),
        Knight("black", self, (1, 7)),
        Bishop("black", self, (2, 7)),
        King("black", self, (3, 7)),
        Queen("black", self, (4, 7)),
        Bishop("black", self, (5, 7)),
        Knight("black", self, (6, 7)),
        Rook("black", self, (7, 7))]

        self.pieces_all += self.row0 + self.row1 + self.row6 + self.row7


        for row in range(self.dim):
            for col in range(self.dim):
                x1 = (col * self.square_size)
                y1 = (row * self.square_size)
                x2 = (x1 + self.square_size)
                y2 = (y1 + self.square_size)
                colour = self.setColour(col,row)
                self.board[row][col] = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=colour, tags="square")

                #temporary images for testing, will update for later versions
                #www.opengameart.org/content/pixel-chess-pieces
                #Author - Lucas312
                #CC BY 3.0
                #CC BY-SA 3.0

                # create canvas returns an integer id number for that object
                # tagOrId argument can be used to reference this

        for a in range(self.dim):
        #object ids of chess pieces is 65 to 96
        #the first 64 ids are the squares of the chess board
        #i see no way around this, less i make the chess pieces before the board squares
        #but i dont think its a big deal
            self.pieces[0][a] = self.canvas.create_image(a*self.square_size, 0, image = self.row0[a].image, anchor='nw')
            self.piecesTwo[0][a] = self.row0[a]

        for b in range(self.dim):
            self.pieces[1][b] = self.canvas.create_image(b*self.square_size, 64, image = self.row1[b].image, anchor='nw')
            self.piecesTwo[1][b] = self.row1[b]

        for c in range(self.dim):
            self.pieces[6][c] = self.canvas.create_image(c*self.square_size, 384, image = self.row6[c].image, anchor='nw')
            self.piecesTwo[6][c] = self.row6[c]

        for d in range(self.dim):
            self.pieces[7][d] = self.canvas.create_image(d*self.square_size, 448, image = self.row7[d].image, anchor='nw')
            self.piecesTwo[7][d] = self.row7[d]

    def setColour(self, col, row):
        if (col + row) % 2 == 1:
            colour = self.colour1
        else:
            colour = self.colour2
        return colour

    def play_again(self):
        self.canvas.delete("all")
        self.initialize_board()

if __name__ == "__main__":
    app = GUI()
    frame = mainMenu(app)
    app.mainloop()