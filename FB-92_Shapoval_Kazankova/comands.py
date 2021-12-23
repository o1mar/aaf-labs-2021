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
    name = a[0]
    if name in tables.keys(): print("Table already exists")
    else:
       indexes = {}
       for i in isIndexed:
         indexes[i] = SortedDict()
       columns = a[1:]
       rows = []
       tb = [rows, columns, indexes]
       print('Table', name, 'has been created')
       return name, tb

def insert(a, tables):

    a = re.sub(r"(,)|(INTO)", '', a, flags=re.IGNORECASE)
    a = a.split()
    name = a[0]
    
    if name in tables.keys():
     tb = tables.get(name)
     rows, columns, indexes = tb
     row = list(map(int, a[1:]))
     if len(row) == len(columns):
         rows.append(row) 
         for i in indexes.keys():
           x = row[columns.index(i)]
           if x in indexes[i].keys():
             indexes[i][x].append(len(rows))
           else:
             indexes[i][x] = [len(rows)]
         print('1 row has been added')
     else: print("The amount of values must be equal the amount of columns!")
     return name, tb
     
    else: print("There is no such table")
    
def select(a, tables):
    a = re.sub(',', '', a)
    a = a.split()

    for i in range(0, len(a)): 
        if a[i] == 'from':
           name = a[i+1]
           j = 1
           agg = [ ]
           curCol = a[:i]
           while re.match(r'avg|max|count', a[i-j], re.IGNORECASE)!=None:
               n = a[i-j][:3]
               c = re.sub(r'avg|count|max', '', a[i-j], flags=re.IGNORECASE)
               agg.append((n, c))
               curCol = a[:(i-j)]
               j+=1
           
           condition = []
           group = []
        try:
           if a[i+2] == 'group_by' :
             group = a[i+3:]
           if a[i+2] == 'where':
            condition = a[i+3:]
           if 'group_by' in condition: condition = condition[:3]
           
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
       if len(group) == 1 and group[0] in indexes:
         print('Using indexes')
         ourrows = []
         if agg != None:
          for i in indexes[group[0]].keys():
           row = []
           aggVal = []
           row.append(i)
           val = 0
           for k in agg:
            if k[0] == 'avg':
             for j in indexes[group[0]][i] :
              aggVal.append(int(rows[j-1][columns.index(k[1])]))
             val = sum(aggVal)/len(aggVal)
            if k[0] == 'max':
             for j in indexes[group[0]][i] :
              aggVal.append(int(rows[j-1][columns.index(k[1])]))
             val = max(aggVal)
            if k[0] == 'cou': val = len(indexes[group[0]][i])
            row.append(val)
            curCol.append(k[0])
           ourrows.append(row)
          print(tabulate(ourrows, curCol, tablefmt="pretty"))
         else:
          row = []
          for i in indexes[group[0]].keys():
            row.append([i])
          print(tabulate(row, group[0], tablefmt="pretty"))

         
       else: 
         print('No use of indexes ')
         SelectedRows = []
         agval = {}
         for a in agg:
           agval[a]=[ ]
         for i in rows:
           row = []
           for col in group:
             row.append(int(i[columns.index(col)]))
           if row not in SelectedRows: 
             SelectedRows.append(row)
             if agg != None:
               for ag in agg:
                agval[ag].append([i[columns.index(ag[1])]])
           elif agg != None: 
             for ag in agg:
              agval[ag][SelectedRows.index(row)].append(i[columns.index(ag[1])])
         if agg != None:
          for ag in agg:
            if ag[0] == 'avg':
               for n, v in enumerate(agval[ag]):
                 res = sum(v)/len(v)
                 SelectedRows[n].append(res)
            elif ag[0] == 'max':
               for n, k in enumerate(agval[ag]):
                 res = max(k)
                 SelectedRows[n].append(res)
            elif ag[0] == 'cou':
               for n, s in enumerate(agval[ag]):
                 res = len(s)
                 SelectedRows[n].append(res)
            group.append(ag[0])
         if len(condition)!=3:
          print(tabulate(SelectedRows, group, tablefmt="pretty"))
        

     if len(condition) == 3:
          
          if len(group) > 0:  rows = SelectedRows
          #else: rows = SelectedRows
          #print(tabulate(SelectedRows, curCol, tablefmt="pretty"))
          if condition[1] == '=': condition[1] = '=='
          if condition[0] in columns and condition[2] in columns:
            i = 0
            selectedRows = []
            while i < len(rows):
                c = str(rows[i][columns.index(condition[0])]), str(condition[1]), str(rows[i][columns.index(condition[2])])
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
                c = str(rows[i][columns.index(condition[0])]), str(condition[1]), str(condition[2])
                c = ''.join(c)
                if eval(c) == True:
                 selectedRows.append(rows[i])
                i +=1
          elif condition[2] in columns:
             i = 0
             selectedRows = []
             while i < len(rows):
                c = str(condition[0]), str(condition[1]), str(rows[i][columns.index(condition[2])])
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
          
          
     
     if len(group)==0 and len(condition)==0: 
         selectedRows = []
         
         for i in curCol:
          row = []
          if i in columns:
             ind = columns.index(i)
             for j in range (len(rows)):
              row.append(rows[j][ind])
          selectedRows.append(row)
         if agg != None:
          for i in agg:
           if i[0] ==  'avg':
            average = 0 #row ((2,4,5), (0,8,6), (0,3,4))
            count = 0
            for e in rows:
              el = e[columns.index(i[1])]
              average += int(el)
              count+=1
            print('Average in column', i[1],  average/count)
           if i[0] ==  'max':
            maxi = 0  
            for e in rows:
              el = e[columns.index(i[1])]
              if maxi < int(el):
                maxi = int(el)
            print('Max in column', i[1],  maxi)
           if i[0] ==  'cou':
            print('Number of rows', i[1],  len(selectedRows[0]))
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
        print(d, 'rows have been deleted from the table', name)
     else: 
         print('Table was deleted')
         tables.pop(name)
    else: print("There is no such table")
    return tables

