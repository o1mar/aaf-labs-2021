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
         #print (tabulate(tb[0], tb[1], tablefmt="grid"))
         print('1 row has been added')
         #print(tb[2], 'INDEXES')
     else: print("The amount of values must be equal the amount of columns!")
     return name, tb
     
    else: print("There is no such table")
    
def select(a, tables):
    a = re.sub(',', '', a)
    #a = a.lower()
    a = a.split()
    #match = re.search(r'COUNT|MAX|AVG', a, re.IGNORECASE)
    #print('Look: ', a)

    for i in range(0, len(a)): 
        if a[i] == 'from':
           name = a[i+1]
           agg = None
           if ('avg' in a[i-1]) or ('max' in  a[i-1]) or ('count' in a[i-1]):
             n = a[i-1][:3]
             a[i-1] = re.sub(r'avg|count|max', '', a[i-1])
             agg = (n, a[i-1])  
             curCol = a[:i-1]
           else: curCol = a[:i] 
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
     tb = tables.get(name)

     rows, columns, indexes = tb
     if curCol[0]=='*':
       curCol = columns
     if len(group) > 0:
      for i in curCol: 
        if i not in group:
          print('Invalid group by syntax')
          return
     if len(group) > 0:
       # 3: (1, 4, 6) 5: (2,3) 8: (5) group by
       if len(group) == 1 and group[0] in indexes:
         print('Using indexes')
         ourrows = []
         if agg != None:
          for i in indexes[group[0]].keys():
           row = []
           aggVal = []
           row.append(i)
           val = 0
           if agg[0] == 'avg':
            for j in indexes[group[0]][i] :
              aggVal.append(int(rows[j-1][columns.index(agg[1])]))
            val = sum(aggVal)/len(aggVal)
           if agg[0] == 'max':
            for j in indexes[group[0]][i] :
              aggVal.append(int(rows[j-1][columns.index(agg[1])]))
            val = max(aggVal)
           if agg[0] == 'cou': val = len(indexes[group[0]][i])
           row.append(val)
           print(row, "row")
           ourrows.append(row)
          curCol.append(agg[0])
          print(tabulate(ourrows, curCol, tablefmt="pretty"))
         else:
          row = []
          for i in indexes[group[0]].keys():
            row.append([i])
          print(tabulate(row, group[0], tablefmt="pretty"))

         
       else: 
         print('No use of indexes ')
         SelectedRows = []
         countAgg = []
         countAggt = []
         for i in rows:
           row = []
           for col in group:
             row.append(int(i[columns.index(col)]))

           if row not in SelectedRows: 
             countAgg.append(int(i[columns.index(agg[1])]))
             countAggt.append(1)
             SelectedRows.append(row)
           else: 
             countAggt[SelectedRows.index(row)]+=1
             if agg[0] == 'avg': countAgg[SelectedRows.index(row)]+=int(i[columns.index(agg[1])])
             if agg[0] == 'max': 
               if countAgg[SelectedRows.index(row)]<int(i[columns.index(agg[1])]):
                 countAgg[SelectedRows.index(row)] = i[columns.index(agg[1])]
        
         if agg[0] == 'avg':
          for j in range(0, len(countAgg)):
           countAgg[j] /= countAggt[j]
           SelectedRows[j].append(countAgg[j])
         elif agg[0] == 'max':
           for j in range(0, len(countAgg)):
             SelectedRows[j].append(countAgg[j])
         elif agg[0] == 'cou':
           for j in range(0, len(countAggt)):
             SelectedRows[j].append(countAggt[j])
         group.append(agg[0])
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
          if agg != None:
           if agg[0] ==  'avg':
            average = 0
            count = 0
            for el in selectedRows[curCol.index(agg[1])]:
              average += int(el)
              count+=1
            print('Average in column', agg[1],  average/count)
           if agg[0] ==  'max':
            maxi = 0  
            for el in selectedRows[curCol.index(agg[1])]:
              if maxi < int(el):
                maxi = int(el)
            print('Max in column', agg[1],  maxi)
           if agg[0] ==  'cou':
            print('Number of rows', agg[1],  len(selectedRows[0]))
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
         if agg != None:
          if agg[0] ==  'avg':
            average = 0
            count = 0
            for el in selectedRows[curCol.index(agg[1])]:
              average += int(el)
              count+=1
            print('Average in column', agg[1],  average/count)
          if agg[0] ==  'max':
            maxi = 0  
            for el in selectedRows[curCol.index(agg[1])]:
              if maxi < int(el):
                maxi = int(el)
            print('Max in column', agg[1],  maxi)
          if agg[0] ==  'cou':
            print('Number of rows', agg[1],  len(selectedRows[0]))
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
                 for key in indexes[a[2]]:
                   if i+1 in indexes[a[2]][key]:
                     indexes[a[2]][key].remove(i+1)
                 for key in indexes[a[4]]:
                   if i+1 in indexes[a[4]][key]:
                     indexes[a[4]][key].remove(i+1)
                 
                 #indexes[a[2]].index(i+1).remove(i+1)
                 #indexes[a[4]].index(i+1).remove(i+1)
                     
                   #for l, k in indexes[key].items():
                     #print(l, k, 'key: values')
                    # if i+1 in k:
                       #print(i+1 , "III")
                       #print(indexes[key][l], 'where del')
                       #indexes[key][l].remove(i+1)
                 print(indexes, 'DELETE prosess')
                 d += 1
                else: i +=1

        elif a[2] in columns:
             i = 0
             while i < len(rows):
                c = rows[i][columns.index(a[2])], a[3], a[4]
                c = ''.join(c)

                if eval(c) == True:
                 rows.pop(i)
                 for key in indexes[a[2]]:
                   if i+1 in indexes[a[2]][key]:
                     indexes[a[2]][key].remove(i+1)
                 d += 1
                else: i +=1

        elif a[4] in columns:
               i = 0
               while i < len(rows):
                c = a[2], a[3], rows[i][columns.index(a[4])]
                c = ''.join(c)

                if eval(c) == True:
                 rows.pop(i)
                 for key in indexes[a[4]]:
                   if i+1 in indexes[a[4]][key]:
                     indexes[a[4]][key].remove(i+1)
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

