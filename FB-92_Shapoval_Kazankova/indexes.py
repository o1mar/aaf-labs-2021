
import numpy as np
from tabulate import tabulate
from sortedcontainers import SortedList

def select_with_indexes(curCol, condition, tb):
     rows, columns, indexes = tb
     if curCol[0] =='*':curCol = columns
     if len(condition) == 3:
       op = condition[1]
       if condition[0] in indexes.keys():
         chosenCol = condition[0]
         num = int(condition[2])
       elif condition[2] in indexes.keys():
         chosenCol = condition[2]
         num = int(condition[0])
       position = SortedList(indexes[chosenCol].keys()).bisect_left(num)
       if op == '==':
         if indexes[chosenCol].keys()[position] == num:
           selected = indexes[chosenCol][num] 
       else:
        if op == '<':
         keys = indexes[chosenCol].keys()[:position]
        if op == '>':
         keys = indexes[chosenCol].keys()[position+1:]
        if op == '<=':
         keys = indexes[chosenCol].keys()[:position+1]
        if op == '>=':
         keys = indexes[chosenCol].keys()[position:] 
        selected = list(map(indexes[chosenCol].get, keys))
        selected = list(np.concatenate(selected))
       selectedRows = []
       for i in curCol:
             row = [] 
             for j in selected:
               row.append(rows[j-1][columns.index(i)])
             selectedRows.append(row)
       selectedRows = list(zip(*selectedRows))
       print(tabulate(selectedRows, curCol, tablefmt="pretty"))
       return



