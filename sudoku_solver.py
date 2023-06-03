import numpy as np


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    
    class Sudoku:

        def __init__(self, sudoku):
            self.sudoku = np.zeros((9,9),int)
            for i in range(0,9):
                for j in range(0,9):
                    self.sudoku[i][j] = sudoku[i][j]
                    sudoku[i][j] = self.sudoku[i][j]
            self.done = False
            self.row_max = 9
            self.rows = []
            self.cols = []
            self.boxes = []
            self.set_initial_constraints()

        def set_initial_constraints(self):
            # creating list of sets for keeping constraints
            for i in range(1,10):
                self.rows.append(set())
                self.cols.append(set())
                self.boxes.append(set())
            # setting initial constraints
            for row in range(0,9):
                for col in range(0,9):
                    if self.sudoku[row][col] != 0:
                        num_present = self.sudoku[row][col]
                        self.rows[row].add(num_present)
                        self.cols[col].add(num_present)
                        box_id = self.get_box_by_rowcol(row,col)
                        self.boxes[box_id].add(num_present)

        def check_col(self, col, num):
            if len(np.extract(self.sudoku[:,col] == num, self.sudoku[:,col])) == 1:
                return True
            else:
                return False

        def get_box_coordinates(self, box_id):
            # This method returns the coordinate of the particular square based on the box
            row_start,row_end,col_start,col_end=0,0,0,0
            if box_id == 1:
                row_start,row_end,col_start,col_end=0,3,0,3
            elif box_id == 2:
                row_start,row_end,col_start,col_end=0,3,3,6
            elif box_id == 3:
                row_start,row_end,col_start,col_end=0,3,6,9
            elif box_id == 4:
                row_start,row_end,col_start,col_end=3,6,0,3
            elif box_id == 5:
                row_start,row_end,col_start,col_end=3,6,3,6
            elif box_id == 6:
                row_start,row_end,col_start,col_end=3,6,6,9
            elif box_id == 7:
                row_start,row_end,col_start,col_end=6,9,0,3
            elif box_id == 8:
                row_start,row_end,col_start,col_end=6,9,3,6
            elif box_id == 9:
                row_start,row_end,col_start,col_end=6,9,6,9
            return row_start,row_end,col_start,col_end
            
        def get_num_missing_in_rows(self,num, start_row, end_row):
            missing_rows = []
            for i in range(start_row,end_row):
                val, = np.where(self.sudoku[i] == num)
                if len(val) == 0:
                    missing_rows.append(i)
            return missing_rows
        
        def get_num_missing_in_box(self, num,start_box, end_box):
            missing_box = []
            for i in range(start_box, end_box):
                row_start, row_end, col_start, col_end = self.get_box_coordinates(i)
                rows, col = np.where(self.sudoku[row_start:row_end,col_start:col_end] == num)
                if len(rows) == 0 and len(col) == 0:
                    missing_box.append(i)
            
            return missing_box

        def find_possible_cell_num(self, num_missing_row, num_missing_box_number):
            row_start, row_end, col_start, col_end = self.get_box_coordinates(num_missing_box_number)
            possibilities = []
            for row in num_missing_row:
                for i in range(col_start,col_end):
                    if self.sudoku[row][i] == 0:
                        possibilities.append((row,i))
            
            return possibilities

        def get_box_by_rowcol(self,row, col):
        
            if row <3 :
                if col < 3:
                    return 0
                elif col <6:
                    return 1
                elif col <9:
                    return 2
            elif row <6 :
                if col < 3:
                    return 3
                elif col <6:
                    return 4
                elif col <9:
                    return 5
            elif row <9 :
                if col < 3:
                    return 6
                elif col <6:
                    return 7
                elif col <9:
                    return 8

        def getNextCell(self, row, col):
            if col == 8:
                return row+1, 0
            else:
                return row, col+1
            
        def backtrack(self,row, col):
            if row == self.row_max:
                self.done = True
                return
            next_row, next_col  = self.getNextCell(row, col)
            if self.sudoku[row][col] == 0:
                for num in range(1,10):
                    box_id = self.get_box_by_rowcol(row, col)
                    if self.is_valid(row, col, num, box_id):
                        self.backtrack(next_row, next_col)
                        if not self.done:
                            self.remove_num_constraints(row, col, num, box_id)
            else:
                self.backtrack(next_row, next_col)
            
            
        def remove_num_constraints(self, row, col, num, box_id):
            self.rows[row].remove(num)
            self.cols[col].remove(num)
            self.boxes[box_id].remove(num)
            self.sudoku[row][col] = 0

        def is_valid(self, row, col, num, box_id):
            if num not in self.rows[row].union(self.cols[col],self.boxes[box_id]):
                self.rows[row].add(num)
                self.cols[col].add(num)
                self.boxes[box_id].add(num)
                self.sudoku[row][col] = num
                return True
            else:
                return False
            
        def check_set(self, i,row_num_start, row_num_end, box_set_start, box_set_end):
            num_missing_row = self.get_num_missing_in_rows(i, row_num_start, row_num_end) 
            num_missing_box = self.get_num_missing_in_box(i, box_set_start, box_set_end) 
            self.reduce_possibilities( i, num_missing_row, num_missing_box)

        def reduce_possibilities(self, i, num_missing_row, num_missing_box):
            if len(num_missing_row) >= 1:
                for missing_box in num_missing_box:
                    possibility_list = s.find_possible_cell_num(num_missing_row, missing_box)
                    self.calculate_further(i, possibility_list)  

        def calculate_further(self, i, possibility_list):
            if len(possibility_list) > 1:
                for possible in possibility_list.copy():
                    if self.check_col(possible[1], i):
                        possibility_list.remove(possible)
            elif len(possibility_list) == 1:
                if not self.check_col(possibility_list[0][1], i):
                    self.sudoku[possibility_list[0][0]][possibility_list[0][1]] = i 

        def is_duplicate_in_row(self, row, num):
                if len(np.extract(self.sudoku[row] == num, self.sudoku[row])) >1:
                    return True
                else:
                    return False

        def is_duplicate_in_col(self, col, num):
            if len(np.extract(self.sudoku[:,col] == num, self.sudoku[:,col])) > 1:
                return True
            else:
                return False

        def is_duplicate_in_box(self, box_id, num):
            row_start, row_end, col_start, col_end = self.get_box_coordinates(box_id)
            if len(np.extract(self.sudoku[row_start:row_end,col_start:col_end] == num, self.sudoku[row_start:row_end,col_start:col_end])) > 1:
                return True
            else:
                return False
            
        def is_invalid_sudoku(self):
                for num in range(1,10):
                    for i in range(9):
                        if self.is_duplicate_in_row(i, num) or self.is_duplicate_in_col(i, num) or self.is_duplicate_in_box(i+1, num):
                            return True
                        
                return False

    s = Sudoku(sudoku)
    if s.is_invalid_sudoku():
        s.sudoku[:,:] = -1
    else:
        while len(np.argwhere(s.sudoku == 0)) > 1:
            zeros_count_begin = len(np.argwhere(s.sudoku == 0))
            for i in range(1,10):
                s.check_set(i, 0, 3, 1, 4)
                s.check_set(i, 3, 6, 4, 7)
                s.check_set(i, 6, 9, 7, 10)
            if zeros_count_begin == len(np.argwhere(s.sudoku == 0)):
                break

        if(len(np.extract(s.sudoku[:,:] == 0, s.sudoku[:,:])) >= 1):
            s.backtrack(0,0)
        if(len(np.extract(s.sudoku[:,:] == 0, s.sudoku[:,:])) > 1):
            s.sudoku[:,:] = -1

        
    print(s.sudoku)


sudoku = [[1,0,4,3,8,2,9,5,6],
          [2,0,5,4,6,7,1,3,8],
          [3,8,6,9,5,1,4,0,2],
          [4,6,1,5,2,3,8,9,7],
          [7,3,8,1,4,9,6,2,5],
          [9,5,2,8,7,6,3,1,4],
          [5,2,9,6,3,4,7,8,1],
          [6,0,7,2,9,8,5,4,3],
          [8,4,3,0,1,5,2,6,9]]

sudoku_solver(sudoku)