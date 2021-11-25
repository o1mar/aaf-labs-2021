from tabulate import tabulate
import re
#from itertools import izip
#a = input(" Enter: ")
#[create] [table ( t1 indexed, t2, t3)]

#t1 = ['Alex',13,1,'Chess',10]
#t2 = ['Zia',12,2,'Chess',25]
#table=[t1, t2]
#headers=["Name","Age", "Number of Games","Favourite Game","Cost of Game"]
#t3 = None
#print (tabulate(table, headers, tablefmt="grid"))
#tb = [headers, table]
#print(tabulate(tb, tablefmt="grid", headers='firstrow'))
#print(tabulate(tb, headers='firstrow'))
def create(a):
    #print("1")
    a = re.sub(r"(,)|(INDEXED)", '', a)
    a = a.split()
    #print (a)
    name = a[0]
    columns = a[1:]
    rows = []
    tb = [rows, columns]
    #print (tabulate(tb, tablefmt="grid", headers='firstrow'))
    print('Table', name, 'has been created')
    return name, tb

def insert(a, tables):
    #print("2")
    a = re.sub(r"(,)|(INTO)", '', a, flags=re.IGNORECASE)
    a = a.split()
    name = a[0]
    #print (a)
    #print(name, 'NAME')
    if name in tables.keys():
     tb = tables.get(name)
     row = a[1:]
     #print(row)
     tb[0].append(row)
     tables.update({name: tb})
     print (tabulate(tb[0], tb[1], tablefmt="grid"))
     print('1 row has been added')
     return name, tb
    else: print("There is no such table")
    
def select(a, tables):
    #print("3")
    a = re.sub(',', '', a)
    a = a.split()
    #print(a, "here is a")
    #print(tables, 'TABLES')
    for i in range(0, len(a)): 
        if a[i] == 'from':
           name = a[i+1]
           curCol = a[:i] 
    if name in tables.keys():
     #tcopy = tables.copy()
     #ttcopy = tcopy.copy()
     t = tables.get(name)
     tb = t.copy()
     rows, columns = tb
     newrows, newcolumns = rows, columns
     #print(curCol, 'curCol')
     #print(tb, 'table')
     #print(newcolumns, 'columns')
     #n = 0
     if curCol[0] == '*': print(tabulate(newrows, newcolumns, tablefmt="grid"))
     else: 
          '''rowind = []
          for i in curCol:
             rowind.append(columns.index(i))
          i = 0
          j = 0
          print(rowind, 'rowind')
          
          while i < len(rows):
           print(len(rows), 'len(row)')
           while j < len(rowind): 
              print(len(rowind), 'len(rowind)')
              print(j, 'j')
              print(rows, 'before')
              rows[i].pop(rowind[j])
              print(rows, 'after')
              j+=1
              #len(rowind)-=1
           i+=1
           print(rows)'''
          #print(tables, 'TABLES', tb, 'TB')
          # for i in range (0, len(curCol)):
          n = 0
          for k in newcolumns:
             #print('hello')
             #print(k, 'here is k')
             if not k in curCol:
          #for k in columns:
          #if not k in curCol:
                 #print('hi there')
                 i = newcolumns.index(k)
                 i = i+n
                 #print(i)
                 #for j in range(0, len(rows)): del rows[j][i]
                 j = 0
                 #print(len(newrows))
                 while j < len(newrows): 
                     #print(j)
                     #rows[j][i].delete
                     newrows[j].pop(i)
                     n -= 1
                     j+=1
                 #print(newrows)
             print(tabulate(newrows, curCol, tablefmt="grid"))
             #tb = tables.get(name)
             #rows, columns = tb
     #print(tables, 'TABLES')
        
   
     
    
     
    #name = a.find
def delete(a, tables):
    #print("4")
    a = a.split()
    name = a[0]
    #print(name, 'NAME')
    if name in tables.keys():
     tb = tables.get(name)
     #rows = tb[0]
     #columns = tb[1]
     rows, columns = tb
     #print (rows, columns)
     if len(a)>1:
        if a[3] == '=': a[3] = '=='
        #print ('delete with where')
        #print ("search", rows[0][1])
        d = 0
        if a[2] and a[4] in columns :
            #print('We almost there')
            i = 0
            while i < len(rows):
                c = rows[i][columns.index(a[2])], a[3], rows[i][columns.index(a[4])]
                c = ''.join(c)
                #print(c)
                if eval(c) == True:
                 rows.pop(i)
                 d += 1
                else: i +=1
        elif a[2] in columns:
             i = 0
             while i < len(rows):
                c = rows[i][columns.index(a[2])], a[3], a[4]
                c = ''.join(c)
                #print(c)
                if eval(c) == True:
                 rows.pop(i)
                 d += 1
                else: i +=1
                #print(tabulate(tb[0], tb[1], tablefmt="grid"))
        elif a[4] in columns:
               i = 0
               while i < len(rows):
                c = a[2], a[3], rows[i][columns.index(a[4])]
                c = ''.join(c)
                #print(c)
                if eval(c) == True:
                 rows.pop(i)
                 d += 1
                else: i +=1
        tb[0] = rows
        tables.update({name: tb})
        print(d, 'rows have been deleted from the table', name)
        print(tabulate(tb[0], tb[1], tablefmt="grid"))  
     else: 
         print('Table was deleted')
         tables.pop(name)
    else: print("There is no such table")
    return tables
#while True:
'''a = 'NewTable t1 INDEXED, t2, t3 '
rows = []
name, columns = create(a)
a = 'InTo NewTable 1, 2, 3'
tb=insert(a, name, columns, rows)
a = 'InTo NewTable 4, 7, 9'
tb=insert(a, name, columns, rows)
a = 'InTo NewTable 5, 9, 1'
tb=insert(a, name, columns, rows)
print (tb)
a = 'NewTable where t1 != 5'
delete(a)'''
#сделать многострочный ввод
#select
#проверка если таблица/колонка существует -- есть но дописать выводы
#проверка в insert что кол-во колонок = кол-во значений строки 
#чтоб не вылетало try except