#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Gabriele Cirulli's 2048 puzzle game.

    Python3/tkinter port by Raphaël Seban <motus@laposte.net>

    Copyright (c) 2014+ Raphaël Seban for the present code.

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""

import random
import numpy as np

try:
    import Tkinter as tk
    import ttk
    import tkMessageBox as messagebox
except:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
# end try

from src import game2048_score as GS
from src import game2048_grid as GG
from src import game_grid as GM


class GabrieleCirulli2048(tk.Tk):
    PADDING = 10
    START_TILES = 2

    def __init__(self, **kw):
        tk.Tk.__init__(self)
        for k, v in kw:
            print("Key = {}, value = {}".format(k, v))
        self.initialize(**kw)

        self.count = 0

    # end def

    def center_window(self, tk_event=None, *args, **kw):
        self.update_idletasks()
        _width = self.winfo_reqwidth()
        _height = self.winfo_reqheight()
        _screen_width = self.winfo_screenwidth()
        _screen_height = self.winfo_screenheight()
        _left = (_screen_width - _width) // 2
        _top = (_screen_height - _height) // 2
        self.geometry("+{x}+{y}".format(x=_left, y=_top))

    # end def

    def initialize(self, **kw):
        self.title("2048")
        self.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.resizable(width=False, height=False)
        self.withdraw()
        ttk.Style().configure(".", font="sans 10")
        _pad = self.PADDING
        self.grid = GG.Game2048Grid(self, **kw)
        self.hint = ttk.Label(
            self, text="Hint: use keyboard arrows to move tiles."
        )
        self.score = GS.Game2048Score(self, **kw)
        self.hiscore = GS.Game2048Score(self, label="Highest:", **kw)
        self.grid.pack(side=tk.TOP, padx=_pad, pady=_pad)
        self.hint.pack(side=tk.TOP)
        self.score.pack(side=tk.LEFT)
        self.hiscore.pack(side=tk.LEFT)
        ttk.Button(
            self, text="Quit!", command=self.quit_app,
        ).pack(side=tk.RIGHT, padx=_pad, pady=_pad)
        ttk.Button(
            self, text="New Game", command=self.new_game,
        ).pack(side=tk.RIGHT)
        ttk.Button(
            self, text="AI Game", command=self.ai_new_game,
        ).pack(side=tk.RIGHT)
        self.grid.set_score_callback(self.update_score)

    # end def

    def new_game(self, *args, **kw):
        self.unbind_all("<Key>")
        self.score.reset_score()
        self.grid.reset_grid()
        for n in range(self.START_TILES):
            self.after(
                100 * random.randrange(3, 7), self.grid.pop_tile
            )
        # end if
        self.bind_all("<Key>", self.on_keypressed)

    # end def

    def quit_app(self, **kw):
        if messagebox.askokcancel("Question", "Quit game?"):
            self.quit()
            self.destroy()
            # end if

    # end def

    def run(self, **kw):
        self.center_window()
        self.deiconify()
        self.new_game(**kw)
        self.mainloop()

    # end def

    def on_keypressed(self, tk_event=None, *args, **kw):

        _event_handler = {
            "left": self.grid.move_tiles_left,
            "right": self.grid.move_tiles_right,
            "up": self.grid.move_tiles_up,
            "down": self.grid.move_tiles_down,
            "escape": self.quit_app,
        }.get(tk_event.keysym.lower())
        try:
            _event_handler()
            self.hint.pack_forget()
        except:
            pass

        tiles = self.grid.tiles
        # print("tiles = {}".format(tiles))
        for t in tiles:
            print("Tile id = {}, tile row = {}, tile column = {}, value = {}".
                  format(t, tiles[t].row, tiles[t].column, tiles[t].value))
        print("--------------------------")

        # end try

    # end def

    def update_score(self, value, mode="add"):
        if str(mode).lower() in ("add", "inc", "+"):
            self.score.add_score(value)
        else:
            self.score.set_score(value)
        # end if
        self.hiscore.high_score(self.score.get_score())

    # end def

    def ai_new_game(self, *args, **kw):
        self.unbind_all("<Key>")
        self.score.reset_score()
        self.grid.reset_grid()
        for n in range(self.START_TILES):
            self.after(
                100 * random.randrange(3, 7), self.grid.pop_tile
            )
        # end if
        self.playloops = 0
        self.after(200, self.ai_pressed)  # 多长时间后调用下一次ai_pressed
        self.bind_all("<Key>", self.on_keypressed)

    # end def

    # 定义一个AI程序，按了界面上的ai运行按钮后会定时触发
    # 在这个子程序里面运行一次AI操作
    def ai_pressed(self, tk_event=None, *args, **kw):
        self.playloops += 1

        matrix = self.grid.matrix.matrix

        # get the values of cells
        tiles = self.grid.tiles
        for t in tiles:
            print("Tile id = {}, tile row = {}, tile column = {}, value = {}".
                  format(t, tiles[t].row, tiles[t].column, tiles[t].value))

        print("--------------------------")

        # add your AI program here to control the game
        # the control input is a number from 1-4
        # 1 move to left
        # 2 move to right
        # 3 move to up
        # 4 move to down
        # pressed = random.randint(1, 4)  # this is means random control

        if self.count == 0:
            self.after(200, self.ai_pressed)
            self.count += 1
        else:
            ai = AI(tiles)

            pressed = ai.ai_move() + 1
            del ai
            print("pressed: ", pressed)
            print("")

            # aaa = input()

            if pressed == 1:
                print("Move down")
                self.grid.move_tiles_down()
            elif pressed == 2:
                print("Move right")
                self.grid.move_tiles_right()
            elif pressed == 3:
                print("Move left")
                self.grid.move_tiles_left()
            elif pressed == 4:
                print("Move up")
                self.grid.move_tiles_up()
            else:
                pass

            if self.grid.no_more_hints():  # game over
                # self.ai_new_game()  # play ai again
                pass
            else:
                self.after(200, self.ai_pressed)  # ai press again after 200 ms


# end class


class AI:
    def __init__(self, tiles):
        self.tiles = tiles
        # 进行移动的矩阵
        self.matrix = np.zeros((4, 4))
        self.saved_matrix = np.zeros((4, 4))
        self.rows = 4
        self.columns = 4

        # 矩阵能否进行上下左右移动的标志
        self.flags = [0, 0, 0, 0]

    # 对各个方向的移动进行评价，并得出最优操作
    def ai_move(self):
        score = [0, 0, 0, 0]
        score_num = [0, 0, 0, 0]
        score_position = [0, 0, 0, 0]
        self.flags = [0, 0, 0, 0]

        score_num[0], score_position[0] = self.evaluate_move_down()
        score_num[1], score_position[1] = self.evaluate_move_right()
        score_num[2], score_position[2] = self.evaluate_move_left()
        score_num[3], score_position[3] = self.evaluate_move_up()

        for i in range(4):
            score[i] = score_num[i] * 2.0 + score_position[i] / 5.0

        print("num:  ", score_num[0], score_num[1], score_num[2], score_num[3])
        print("pos:  ", score_position[0], score_position[1], score_position[2], score_position[3])
        print("score:", score[0], score[1], score[2], score[3])
        print("flag: ", self.flags[0], self.flags[1], self.flags[2], self.flags[3])

        i = 0
        for j in range(0, 4):
            if self.flags[i] == 0:
                i = j
            if (score[i] < score[j]) and (self.flags[j] == 1):
                i = j
        return i

    # 还原矩阵
    def reset_matrix(self):
        self.matrix = np.zeros((4, 4))
        for t in self.tiles:
            # print("Tile id = {}, tile row = {}, tile column = {}, value = {}".
            #       format(t, self.tiles[t].row, self.tiles[t].column, self.tiles[t].value))
            self.matrix[self.tiles[t].row, self.tiles[t].column] = self.tiles[t].value

    # 对矩阵进行赋值
    def set_matrix(self, matrix):
        for i in range(self.rows):
            for j in range(self.columns):
                self.matrix[i, j] = matrix[i, j]

    # 保存当前矩阵
    def save_matrix(self):
        self.saved_matrix = np.zeros((4, 4))
        for i in range(self.rows):
            for j in range(self.columns):
                self.saved_matrix[i, j] = self.matrix[i, j]

    # 获取当前矩阵中不为零的元素个数
    def get_num_tiles(self):
        count = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.matrix[i, j] != 0:
                    count += 1
        return count

    # 利用模板对矩阵元素位置进行评价
    def evaluate_position(self):
        score = 0
        sequence = []

        # for i in range(self.rows-1, -1, -1):
        #     sequence.append(self.matrix[i, 3])
        # for i in range(self.rows):
        #     sequence.append(self.matrix[i, 2])
        # for i in range(self.columns-1, -1, -1):
        #     sequence.append(self.matrix[i, 1])
        # for i in range(self.columns):
        #     sequence.append(self.matrix[i, 0])

        # for j in range(self.columns):
        #     sequence.append(self.matrix[3, j])
        # for j in range(self.columns-1, -1, -1):
        #     sequence.append(self.matrix[2, j])
        # for j in range(self.columns):
        #     sequence.append(self.matrix[1, j])
        # for j in range(self.columns-1, -1, -1):
        #     sequence.append(self.matrix[0, j])

        # sequence = [self.matrix[3, 3], self.matrix[3, 2], self.matrix[2, 2], self.matrix[2, 3],
        #             self.matrix[1, 3], self.matrix[1, 2], self.matrix[1, 1], self.matrix[2, 1],
        #             self.matrix[3, 1], self.matrix[3, 0], self.matrix[2, 0], self.matrix[1, 0],
        #             self.matrix[0, 0], self.matrix[0, 1], self.matrix[0, 2], self.matrix[0, 3]]

        # sequence = [self.matrix[3, 0], self.matrix[3, 1], self.matrix[2, 1], self.matrix[2, 0],
        #             self.matrix[1, 0], self.matrix[1, 1], self.matrix[1, 2], self.matrix[2, 2],
        #             self.matrix[3, 2], self.matrix[3, 3], self.matrix[2, 3], self.matrix[1, 3],
        #             self.matrix[0, 3], self.matrix[0, 2], self.matrix[0, 1], self.matrix[0, 0]]

        # sequence = [self.matrix[3, 3], self.matrix[3, 2], self.matrix[2, 3], self.matrix[3, 1],
        #             self.matrix[2, 2], self.matrix[1, 3], self.matrix[3, 0], self.matrix[2, 1],
        #             self.matrix[1, 2], self.matrix[0, 3], self.matrix[2, 0], self.matrix[1, 1],
        #             self.matrix[0, 2], self.matrix[1, 0], self.matrix[0, 1], self.matrix[0, 0]]

        sequence = [self.matrix[3, 3], self.matrix[3, 2], self.matrix[3, 1], self.matrix[2, 1],
                    self.matrix[2, 2], self.matrix[2, 3], self.matrix[1, 3], self.matrix[1, 2],
                    self.matrix[1, 1], self.matrix[3, 0], self.matrix[2, 0], self.matrix[1, 0],
                    self.matrix[0, 3], self.matrix[0, 2], self.matrix[0, 1], self.matrix[0, 0]]

        for i in range(15):
            seq = []
            for j in range(16):
                seq.append(sequence[j] - sequence[i])
            for j in range(i + 1, 16):
                if seq[j] > 0:
                    score -= 1
            for j in range(0, i - 1):
                if seq[j] < 0:
                    score -= 1
        sequence.sort()
        if self.matrix[3, 3] < sequence[15]:
            score -= sequence[15] * 10
        return score

    # 评估向下移动
    def evaluate_move_down(self):
        num = [0, 0, 0, 0]
        self.reset_matrix()
        num1 = self.get_num_tiles()
        self.flags[0] = self.try_move_down()
        score = self.evaluate_position()
        self.save_matrix()

        self.set_matrix(self.saved_matrix)
        self.try_move_down()
        num2 = self.get_num_tiles()
        num[0] = num1 - num2

        self.set_matrix(self.saved_matrix)
        self.try_move_right()
        num2 = self.get_num_tiles()
        num[1] = num1 - num2

        self.set_matrix(self.saved_matrix)
        self.try_move_left()
        num2 = self.get_num_tiles()
        num[2] = num1 - num2

        self.set_matrix(self.saved_matrix)
        self.try_move_up()
        num2 = self.get_num_tiles()
        num[3] = num1 - num2

        return max(num), score

    # 评估向右移动
    def evaluate_move_right(self):
        num = [0, 0, 0, 0]
        self.reset_matrix()
        num1 = self.get_num_tiles()
        self.flags[1] = self.try_move_right()
        score = self.evaluate_position()
        self.save_matrix()

        self.set_matrix(self.saved_matrix)
        self.try_move_down()
        num2 = self.get_num_tiles()
        num[0] = num1 - num2

        self.set_matrix(self.saved_matrix)
        self.try_move_right()
        num2 = self.get_num_tiles()
        num[1] = num1 - num2

        self.set_matrix(self.saved_matrix)
        self.try_move_left()
        num2 = self.get_num_tiles()
        num[2] = num1 - num2

        self.set_matrix(self.saved_matrix)
        self.try_move_up()
        num2 = self.get_num_tiles()
        num[3] = num1 - num2

        return max(num), score

    # 评估向左移动
    def evaluate_move_left(self):
        num = [0, 0, 0, 0]
        self.reset_matrix()
        num1 = self.get_num_tiles()
        self.flags[2] = self.try_move_left()
        score = self.evaluate_position()
        self.save_matrix()

        self.set_matrix(self.saved_matrix)
        self.try_move_down()
        num2 = self.get_num_tiles()
        num[0] = num1 - num2

        self.set_matrix(self.saved_matrix)
        self.try_move_right()
        num2 = self.get_num_tiles()
        num[1] = num1 - num2

        self.set_matrix(self.saved_matrix)
        self.try_move_left()
        num2 = self.get_num_tiles()
        num[2] = num1 - num2

        self.set_matrix(self.saved_matrix)
        self.try_move_up()
        num2 = self.get_num_tiles()
        num[3] = num1 - num2

        return max(num), score

    # 评估向上移动
    def evaluate_move_up(self):
        num = [0, 0, 0, 0]
        self.reset_matrix()
        num1 = self.get_num_tiles()
        self.flags[3] = self.try_move_up()
        score = self.evaluate_position()
        self.save_matrix()

        self.set_matrix(self.saved_matrix)
        self.try_move_down()
        num2 = self.get_num_tiles()
        num[0] = num1 - num2

        self.set_matrix(self.saved_matrix)
        self.try_move_right()
        num2 = self.get_num_tiles()
        num[1] = num1 - num2

        self.set_matrix(self.saved_matrix)
        self.try_move_left()
        num2 = self.get_num_tiles()
        num[2] = num1 - num2

        self.set_matrix(self.saved_matrix)
        self.try_move_up()
        num2 = self.get_num_tiles()
        num[3] = num1 - num2

        return max(num), score

    def try_move_down(self):
        _acted = 0
        for _column in range(self.columns):
            for _row in range(self.rows - 1, -1, -1):
                _value1 = self.matrix[_row, _column]
                if _value1:
                    for _row2 in range(_row - 1, -1, -1):
                        _value2 = self.matrix[_row2, _column]
                        if _value2 and (_value1 == _value2):
                            self.matrix[_row, _column] += _value2
                            self.matrix[_row2, _column] = 0
                            _acted = 1
                        if _value2:
                            break
            _empty = None
            for _row in range(self.rows - 1, -1, -1):
                _value1 = self.matrix[_row, _column]
                if not _value1 and not _empty:
                    _empty = (_row, _column)
                elif _value1 and _empty:
                    self.matrix[_empty] = _value1
                    self.matrix[_row, _column] = 0
                    _empty = (_empty[0] - 1, _column)
                    _acted = 1
        return _acted

    def try_move_left(self):
        _acted = 0
        for _row in range(self.rows):
            for _column in range(self.columns - 1):
                _value1 = self.matrix[_row, _column]
                if _value1:
                    for _col in range(_column + 1, self.columns):
                        _value2 = self.matrix[_row, _col]
                        if _value2 and (_value1 == _value2):
                            self.matrix[_row, _column] += _value2
                            self.matrix[_row, _col] = 0
                            _acted = 1
                        if _value2:
                            break
            _empty = None
            for _column in range(self.columns):
                _value1 = self.matrix[_row, _column]
                if not _value1 and not _empty:
                    _empty = (_row, _column)
                elif _value1 and _empty:
                    self.matrix[_empty] = _value1
                    self.matrix[_row, _column] = 0
                    _empty = (_row, _empty[1] + 1)
                    _acted = 1
        return _acted

    def try_move_right(self):
        _acted = 0
        for _row in range(self.rows):
            for _column in range(self.columns - 1, -1, -1):
                _value1 = self.matrix[_row, _column]
                if _value1:
                    for _col in range(_column - 1, -1, -1):
                        _value2 = self.matrix[_row, _col]
                        if _value2 and (_value1 == _value2):
                            self.matrix[_row, _column] += _value2
                            self.matrix[_row, _col] = 0
                            _acted = 1
                        if _value2:
                            break
            _empty = None
            for _column in range(self.columns - 1, -1, -1):
                _value1 = self.matrix[_row, _column]
                if not _value1 and not _empty:
                    _empty = (_row, _column)
                elif _value1 and _empty:
                    self.matrix[_empty] = _value1
                    self.matrix[_row, _column] = 0
                    _empty = (_row, _empty[1] - 1)
                    _acted = 1
        return _acted

    def try_move_up(self):
        _acted = 0
        for _column in range(self.columns):
            for _row in range(self.rows - 1):
                _value1 = self.matrix[_row, _column]
                if _value1:
                    for _row2 in range(_row + 1, self.rows):
                        _value2 = self.matrix[_row2, _column]
                        if _value2 and (_value1 == _value2):
                            self.matrix[_row, _column] += _value2
                            self.matrix[_row2, _column] = 0
                            _acted = 1
                        if _value2:
                            break
            _empty = None
            for _row in range(self.rows):
                _value1 = self.matrix[_row, _column]
                if not _value1 and not _empty:
                    _empty = (_row, _column)
                elif _value1 and _empty:
                    self.matrix[_empty] = _value1
                    self.matrix[_row, _column] = 0
                    _empty = (_empty[0] + 1, _column)
                    _acted = 1
        return _acted


if __name__ == "__main__":
    GabrieleCirulli2048().run()
# end if
