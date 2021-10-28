
import re

command = {"CREATE", "INSERT", "SELECT", "DELETE", "EXIT"}
#str = '   INSERT INTO table (5, 9, d);text;12345'
#str=input("Enter your command: ")
#str = str.strip()
def text_cleaner(str):
    
    inpt = re.sub(r'[;].*','', str )
    inpt=re.sub(r"(^\s+)|(\(\s+)", "", inpt)
    inpt=re.sub(r"\s+", " ", inpt)
    inpt= inpt.split(' ', 1)
    print(inpt)
    return inpt
#inpt=text_cleaner(str)

def comand_recog(inpt):
    
    if inpt[0] in command: 
        print("I know this command")
        print(inpt[0])
            
    else: 
        print("What is the command? O-o\n Enter an existing command, please. The command must be uppercase")
        str=input("Enter your command: ")
        inpt = text_cleaner(str)
        comand_recog(inpt)

    return inpt
#cmnd=comand_recog(inpt)
def command_type(cmnd):
  if cmnd[0] == "CREATE":
      print("The command is CREATE")
      tablename= cmnd[1].split(' ', 1)
      if len(tablename)<2:
          #tablename[1] = input("Enter names of columns: ")
          tablename.append(input("Enter names of columns: "))
          
      while re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', tablename[0]) == None:
          print("Wrong TableName pattern")
          tablename[0] = input("Try a correct name now ")
      print(cmnd)
      strtext=tablename[1]
      strtext=strtext[strtext.find("(")+1: strtext.find(')')].split(', ')
      print(strtext)
      isIndexed=[ ]
      for i in strtext:
          match = re.search(r"INDEXED", i)
          if match != None:
              #print("EL is INDEXED")
              i = re.sub(r'[ ].*','', i )
              isIndexed.append(i)
      print(isIndexed)
  if cmnd[0] == "INSERT":
      print("The command is INSERT")
      cmnd[1] = re.sub(r'INTO ','', cmnd[1] )
      print(cmnd)
      tablename = cmnd[1].split(' ', 1)
      while re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', tablename[0])  == None:
          print("TableName doesn`t exist")
          tablename[0] = input("Try an existing table now ")
      print(cmnd)
      strtext=tablename[1]
      #for arg in strtext[strtext.find("(")+1: strtext.find(')')].split(','):
      strtext=strtext[strtext.find("(")+1: strtext.find(')')].split(', ')
      for i in range (len(strtext)):
          while re.search(r'^[0-9]', strtext[i])  == None:
           print("You can insert only numbers. ", strtext[i], ": is not a number")
           strtext[i] = input("Replace it: ")
      print(strtext)
  if cmnd[0] == "SELECT":
      print("The command is SELECT")
      strtext=cmnd[1]
      selinf = strtext[0:strtext.find(' FROM')].replace(r',', ' ').split()
      print(selinf)
      if selinf[0]!='*':
          for i in selinf:
              match = re.search(r'COUNT|MAX|AVG', i)
              if match !=None: print(i)
      afterFrom = strtext[strtext.find('FROM ')+5:].split(' ', 1)
      print(afterFrom)
      while re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', afterFrom[0])  == None:
          print("TableName doesn`t exist")
          afterFrom[0] = input("Try an existing table now ")
      if  re.search(r'WHERE', afterFrom[1])!=None:
          while re.match(r'WHERE [a-zA-Z0-9_]+ [ = | != | > | < | >= | <= ] [a-zA-Z0-9_]+', afterFrom[1])==None:
              print("Whong syntax after WHERE")
              afterFrom[1] = input("Try again now ")
      if  re.search(r'GROUP_BY', afterFrom[1])!=None:
          aftGRBY = afterFrom[1]
          while re.match(r'GROUP_BY [a-zA-Z0-9_]+', aftGRBY[aftGRBY.find('GROUP_BY '):])==None:
              print("Whong syntax after GROUP_BY")
              #afterFrom[1] = input("Try again now ")
             # aftGRBY[aftGRBY.find('GROUP_BY ')+9:] = input("Try again now ")
              a = input("Try again now " )
              while re.match(r'GROUP_BY [a-zA-Z0-9_]+', a)==None:
                  a = input("Try again now " )
              aftGRBY = re.sub(r'GROUP_BY.*', a, aftGRBY)
              print(aftGRBY)
  if cmnd[0] == "DELETE":
      print("The command is DELETE")
      cmnd[1] = re.sub(r'FROM ','', cmnd[1] )
      tablename = cmnd[1].split(' ', 1)
      while re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', tablename[0])  == None:
          print("TableName doesn`t exist")
          tablename[0] = input("Try an existing table now ")
      if len(tablename)>1:
        if  re.search(r'WHERE', tablename[1])!=None:
          while re.match(r'WHERE [a-zA-Z0-9_]+ [ = | != | > | < | >= | <= ] [a-zA-Z0-9_]+', tablename[1])==None:
              print("Whong syntax after WHERE")
              tablename[1] = input("Try again now ")
  if cmnd[0] == "EXIT":
      print("The command is EXIT")
      print("Thanks, bye")
      SystemExit()
#command_type(cmnd)
while True:
    str=input("Enter your command: ")
    if str == "EXIT":
     print("The command is EXIT")
     print("Thanks, bye")
     break
    inpt=text_cleaner(str)
    cmnd=comand_recog(inpt)
    command_type(cmnd)



