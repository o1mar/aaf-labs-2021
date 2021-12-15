import re
import numpy as np
from tabulate import tabulate
from sortedcontainers import SortedDict


def select_with_indexes(curCol, condition, tb):
     rows, columns, indexes = tb
     if curCol[0] =='*':curCol = columns
     # indexes={col1:{'2':[1,2], '5':[3, 6, 8]}, 
     #col2:{'1':[1, 2, 3]}}
     ## col1 = 5
     if len(condition) == 3:
          if condition[0] in indexes.keys():
             selectedRows = []
             for key in indexes[condition[0]].keys():
               c = key, condition[1], condition[2]
               c = ''.join(c)
               if eval(c) == True:
                selectedRows.append(indexes[condition[0]][key])
          elif condition[2] in indexes.keys():
             selectedRows = []
             for key in indexes[condition[2]].keys():
               c = condition[0], condition[1], key
               c = ''.join(c)
               if eval(c) == True:
                selectedRows.append(indexes[condition[2]][key])
          temp = []
          selectedRows = list(np.concatenate(selectedRows))
          #print(selectedRows, 'rows')
          for i in curCol:
             #print('print what we need')
             row = [] 
             if i in columns:
                #print("i columns", i, columns, columns.index(i))
                #ind = columns.index(i)
                #[3 : [1, 2] 2: [5, 7] 8: [6] ]
                for j in selectedRows:
                 #print(rows[j-1][columns.index(i)], 'this')
                 row.append(rows[j-1][columns.index(i)])
                 #print(row, 'rownew')
             temp.append(row)
          selectedRows = temp
          #print('before zip')
          selectedRows = list(zip(*selectedRows))
          ##print(selectedRows, curCol, 'hi there')
          print(tabulate(selectedRows, curCol, tablefmt="grid"))
          return
     #elif curCol[0] == '*': 
      #  print(tabulate(rows, columns, tablefmt="grid"))
