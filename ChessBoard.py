import random
import time
import tkinter as tk
import os
from PIL import Image, ImageTk
import chess
from Genetic import Genetic

class ChessBoard(tk.Frame):
    def __init__(self, width=200, height=200, master=None):
        # Initialize the frame
        super().__init__(master)
        self.master = master
        self.width = width
        self.height = height
        self.board = chess.Board()
        self.tile_width = self.width / 8 - 4
        self.tile_height = self.height / 8 - 4
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()
        self.piece_images = []
        self.drawn_images = []
        self.pack()
        self.nb_moves = 0 # fifty moves rules
        
        # Genetic Algorithm
        self.genetic = Genetic(population_size=100, mutation_rate=0.1)
        self.moves_index = 0
        self.update_moves()
        
        self.initialize_board()

    def initialize_board(self):
        """ Initialize the chess board """
        for i in range(8):
            for j in range(8):
                back_color = self._from_rgb((181, 136, 99)) if (i + j) % 2 == 1 else self._from_rgb((240, 217, 181))
                tile = self.canvas.create_rectangle(i * int(self.tile_width), j * int(self.tile_height),
                                                    (i + 1) * self.tile_width,
                                                    (j + 1) * self.tile_height, fill=back_color)

        for i in range(8):
            text = self.canvas.create_text((self.tile_width * (i + 1 / 2), self.height - 24),
                                           text=(chr((ord('A') + i))))
            text = self.canvas.create_text((self.width - 24, (i + 1 / 2) * self.tile_height), text=chr((ord('8') - i)))

        self.parse_fen_position(self.board.fen())
        self.after(1,self.update)

    def parse_fen_position(self, fen_str):
        """ Draw chess piece """
        self.piece_images = []
        for img in self.drawn_images:
            self.canvas.delete(img)

        data = fen_str.split(' ')
        board_data = data[0].split('/')
        row_count = 0
        for row_data in board_data:
            current_position = 0
            for tile_data in row_data:
                if tile_data.isdigit() and 0 < int(tile_data) < 9:
                    current_position += int(tile_data)
                else:
                    picture_path = self.convert_character_to_image(tile_data)
                    img = Image.open(picture_path)
                    img = img.resize((int(self.width / 8), int(self.height / 8)))
                    tk_img = ImageTk.PhotoImage(img)
                    board_img = self.canvas.create_image(
                        ((current_position + 0.5) * self.tile_width, (row_count + 0.5) * self.tile_height),
                        image=tk_img)
                    self.drawn_images.append(board_img)
                    self.piece_images.append(tk_img)

                    current_position += 1

            row_count += 1
    
    def update_moves(self):
        """ Update the best moves """
        self.moves = self.genetic.get_best_moves(self.board)
        self.moves_index = 0

    def update(self):
        """ Update board """
        
        # check if there are still legal moves to play
        if len(self.moves) > 0:
            rand = random.randint(0,len(self.moves)-1)
            self.board.push(self.moves[rand]) # Play a random move between the best moves
            self.parse_fen_position(self.board.fen())
            self.nb_moves += 1
            
            if self.board.turn == chess.WHITE:
                print("White :", self.moves[rand])
            else:
                print("Black :", self.moves[rand])
 
        # check if the game is over
        if self.board.is_game_over() or self.board.is_checkmate() or self.nb_moves > 50:
            self.nb_moves = 0
            self.board.reset()
            self.after(1, self.update)
        else:
            self.update_moves()
            self.after(1, self.update)


    def convert_character_to_image(self, char):
        """ Convert chess piece to image """
        scriptDir = os.path.dirname(__file__)
        path = None
        if char == "r":
            path = "/Resources/br.png"
        elif char == "n":
            path = "/Resources/bn.png"
        elif char == "b":
            path = "/Resources/bb.png"
        elif char == "k":
            path = "/Resources/bk.png"
        elif char == "q":
            path = "/Resources/bq.png"
        elif char == "p":
            path = "/Resources/bp.png"
        elif char == "R":
            path = "/Resources/wr.png"
        elif char == "N":
            path = "/Resources/wn.png"
        elif char == "B":
            path = "/Resources/wb.png"
        elif char == "K":
            path = "/Resources/wk.png"
        elif char == "Q":
            path = "/Resources/wq.png"
        elif char == "P":
            path = "/Resources/wp.png"
        return (scriptDir + path)


    def _from_rgb(self, rgb):
        """translates an rgb tuple of int to a tkinter friendly color code """
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'
