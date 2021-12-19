import re
import indexes as inde
from tabulate import tabulate
from sortedcontainers import SortedDict

# tables:  keys(names) -> values(tb[rows, tables])


def create(a, tables):
    isIndexed=[ ]
    ind = a.split(' ', 1)[1]
    ind = ind.split(', ')
    for i in ind:
          match = re.search(r"INDEXED", i, re.IGNORECASE)
          if match != None:
              i = re.sub(r" INDEXED", '', i, flags=re.IGNORECASE)
              isIndexed.append(i)
    
    a = re.sub(r"INDEXED|(,)", '', a, flags=re.IGNORECASE)
    a = a.split()
    #print(a, 'ASZ')
    #print(isIndexed, 'isIndexed')
    name = a[0]
    if name in tables.keys(): print("Table already exists")
    else:
       indexes = SortedDict()
       for i in isIndexed:
         indexes[i] = { }
       columns = a[1:]
       rows = []
       tb = [rows, columns, indexes]
       print('Table', name, 'has been created')
       #print(indexes, 'indexes')
       return name, tb

def insert(a, tables):

    a = re.sub(r"(,)|(INTO)", '', a, flags=re.IGNORECASE)
    a = a.split()
    name = a[0]
    
    if name in tables.keys():
     tb = tables.get(name)
     rows, columns, indexes = tb
     row = a[1:]
     if len(row) == len(columns):
         rows.append(row) 
         for i in indexes.keys():
           x = row[columns.index(i)]
           #print(x)
           if x in indexes[i].keys():
             #print('exist')
             indexes[i][x].append(len(rows))
           else:
             indexes[i][x] = [len(rows)]
           #print(tb[2], 'indeses')
         tables.update({name: tb})
         #print (tabulate(tb[0], tb[1], tablefmt="grid"))
         print('1 row has been added')
         #print(tb[2], 'INDEXES')
     else: print("The amount of values must be equal the amount of columns!")
     return name, tb
     
    else: print("There is no such table")
    
def select(a, tables):
    a = re.sub(',', '', a)
    a = a.split()
    #match = re.search(r'COUNT|MAX|AVG', a, re.IGNORECASE)

    for i in range(0, len(a)): 
        if a[i] == 'from':
           name = a[i+1]
           curCol = a[:i] 
           condition = []
           group = []
        try:
           if a[i+2] == 'group' :
             group = a[i+4:]
           if a[i+2] == 'where':
            condition = a[i+3:]
           if 'group' in condition: condition = condition[:3]
           #print(condition, group)
        except: pass

    if name in tables.keys():
     t = tables.get(name)
     tb = t.copy()
     rows, columns, indexes = tb
     if curCol[0]=='*':
       curCol = columns
     if len(group) > 0:
      for i in curCol: 
        if i not in group:
          print('Invalid group by syntax')
          return
     if len(group) > 0:
       if len(group) == 1 and group[0] in indexes:
         print('Using indexes')
         row = []
         for i in indexes[group[0]].keys():
           row.append(i)
         print(tabulate(row, group[0], tablefmt="pretty"))
       else: 
         print('No use of indexes ')
         SelectedRows = []
         for i in rows:
           row = []
           #print(i, 'Current row')
           for col in group:
             #print(col, 'Group column')
             row.append(i[columns.index(col)])
           #print(row, 'we get this')
           if row not in SelectedRows: 
             #print('Unique')
             SelectedRows.append(row)
         #print(SelectedRows, "selectedRows")
         print(tabulate(SelectedRows, group, tablefmt="pretty"))

         

     elif len(condition) == 3:
          if condition[1] == '=': condition[1] = '=='
          if condition[0] in columns and condition[2] in columns:
            i = 0
            selectedRows = []
            while i < len(rows):
                c = rows[i][columns.index(condition[0])], condition[1], rows[i][columns.index(condition[2])]
                c = ''.join(c)
                if eval(c) == True:
                 selectedRows.append(rows[i])
                i +=1
          elif condition[0] in indexes or condition[2] in indexes:
            # col = col in indexes throw
            if condition[1] != '!=':
              print('Will count using indexes')
              inde.select_with_indexes(curCol, condition, tb)
              return 
          
          elif condition[0] in columns:
             i = 0
             selectedRows = []
             while i < len(rows):
                c = rows[i][columns.index(condition[0])], condition[1], condition[2]
                c = ''.join(c)
                if eval(c) == True:
                 selectedRows.append(rows[i])
                i +=1
          elif condition[2] in columns:
             i = 0
             selectedRows = []
             while i < len(rows):
                c = condition[0], condition[1], rows[i][columns.index(condition[2])]
                c = ''.join(c)
                if eval(c) == True:
                 selectedRows.append(rows[i])
                i +=1
          temp = []
          for i in curCol:
             row = []
             if i in columns:
                ind = columns.index(i)
                for j in range (len(selectedRows)):
                    row.append(selectedRows[j][ind])
             temp.append(row)
          selectedRows = temp
          selectedRows = list(zip(*selectedRows))
          print(tabulate(selectedRows, curCol, tablefmt="pretty"))
     
     else: 
         selectedRows = []
         
         for i in curCol:
          row = []
          if i in columns:
             ind = columns.index(i)
             for j in range (len(rows)):
              row.append(rows[j][ind])
          selectedRows.append(row)
         selectedRows = list(zip(*selectedRows))          
         print(tabulate(selectedRows, curCol, tablefmt="pretty"))
        
def delete(a, tables):
    a = a.split()
    name = a[0]
    if name in tables.keys():
     tb = tables.get(name)
     rows, columns, indexes = tb
     if len(a)>1:
        if a[3] == '=': a[3] = '=='
        d = 0
        #print(a[2], a[4])
        if a[2] in columns and a[4] in columns:
            i = 0
            while i < len(rows):
                c = rows[i][columns.index(a[2])], a[3], rows[i][columns.index(a[4])]
                c = ''.join(c)

#indexes={in1:{'3':[1], '4':[2,3]}, in2:{'3':[1,3], '2':[2]}}
                if eval(c) == True:
                 rows.pop(i)
                 #print(indexes.values())
                 for key in indexes.keys():
                   #print(key, 'column')
                   #print(indexes[key], 'aaa')
                   #print(indexes[key].keys(), 'bbb')
                   #print(indexes[key].values(), 'ccc')
                   for l, k in indexes[key].items():
                     #print(l, k, 'key: values')
                     if i+1 in k:
                       #print(i+1 , "III")
                       #print(indexes[key][l], 'where del')
                       indexes[key][l].remove(i+1)
                     
                 d += 1
                else: i +=1

        elif a[2] in columns:
             i = 0
             while i < len(rows):
                c = rows[i][columns.index(a[2])], a[3], a[4]
                c = ''.join(c)

                if eval(c) == True:
                 rows.pop(i)
                 for key in indexes.keys():
                   #print(key, 'column')
                   #print(indexes[key], 'aaa')
                   #print(indexes[key].keys(), 'bbb')
                   #print(indexes[key].values(), 'ccc')
                   for l, k in indexes[key].items():
                     #print(l, k, 'key: values')
                     if i+1 in k:
                       #print(i+1 , "III")
                       #print(indexes[key][l], 'where del')
                       indexes[key][l].remove(i+1)
                 d += 1
                else: i +=1

        elif a[4] in columns:
               i = 0
               while i < len(rows):
                c = a[2], a[3], rows[i][columns.index(a[4])]
                c = ''.join(c)

                if eval(c) == True:
                 rows.pop(i)
                 for key in indexes.keys():
                   #print(key, 'column')
                   #print(indexes[key], 'aaa')
                   #print(indexes[key].keys(), 'bbb')
                   #print(indexes[key].values(), 'ccc')
                   for l, k in indexes[key].items():
                     #print(l, k, 'key: values')
                     if i+1 in k:
                       #print(i+1 , "III")
                       #print(indexes[key][l], 'where del')
                       indexes[key][l].remove(i+1)
                 d += 1
                else: i +=1
        tb[0] = rows
        print(indexes, 'indexes')
        tables.update({name: tb})
        print(d, 'rows have been deleted from the table', name)
        #print(tabulate(tb[0], tb[1], tablefmt="grid"))  
     else: 
         print('Table was deleted')
         tables.pop(name)
    else: print("There is no such table")
    return tables

