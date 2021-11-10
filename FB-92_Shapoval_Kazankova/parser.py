
import re

command = {"CREATE", "INSERT", "SELECT", "DELETE", "EXIT"}
#str = '   INSERT INTO table (5, 9, d);text;12345'
#str=input("Enter your command: ")
#str = str.strip()
def text_cleaner(str):
    
    inpt = re.sub(r'[;].*','', str )
    inpt=re.sub(r"(^\s+)|(\(\s*)|(s*\))", "", inpt)
    inpt=re.sub(r"\s+", " ", inpt)
    inpt=re.sub(r"(\s*,)", ",", inpt)
    inpt= inpt.split(' ', 1)
    print(inpt)
    return inpt
#inpt=text_cleaner(str)

def comand_recog(inpt):
    inpt[0]=inpt[0].upper()
    print(inpt[0])
    if inpt[0] in command: 
        print("I know this command")
        #print(inpt[0])
            
    else: 
        print("What is the command? O-o\n Enter an existing command, please")
        return

    return inpt
#cmnd=comand_recog(inpt)
def command_type(cmnd):
  if cmnd[0] == "CREATE":
     # print("The command is CREATE")
      tablename= cmnd[1].split(' ', 1)
      #str = tablename[1].split(' ')
      #print(tablename,  "columns")
      if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', tablename[0]) == None:
          print("Wrong TableName pattern")
          return 
      #print(tablename[1], "columns here")
     # if re.match(r'[^\(*\)]', tablename[1]) != None:
        #  print ("you should put columns in brackets")
          #return

      if len(tablename)<2:
           print ("Where are column names? Try again")
           return

      print(cmnd)
      strtext=tablename[1]
      #print(strtext, "before split")
     # strtext=strtext[strtext.find("(")+1: strtext.find(')')].split(', ')
      strtext = strtext.split(', ') 
      #print(strtext, "after")
      for i in strtext:
       #print(i, "i column")
       if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', i) == None:
         print("Wrong ColumnName pattern")
         return 

     # print(strtext,  "ate")
      isIndexed=[ ]
      for i in strtext:
          match = re.search(r"INDEXED", i, re.IGNORECASE)
          if match != None:
              #print("EL is INDEXED")
              i = re.sub(r'[ ].*','', i )
              isIndexed.append(i)
      #print(isIndexed)
  if cmnd[0] == "INSERT":
     # print("The command is INSERT")
      cmnd[1] = re.sub(r'INTO ','', cmnd[1], flags = re.IGNORECASE)
     # print(cmnd)
      tablename = cmnd[1].split(' ', 1)
      if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', tablename[0])  == None:
          print("TableName doesn`t exist")
          return
      #print(cmnd)
      strtext=tablename[1]
      strtext=strtext.split(', ')
      for i in range (len(strtext)):
          if re.search(r'^([-]?[0-9]+$)', strtext[i])  == None:
           print("You can insert only numbers. ", strtext[i], ": is not a number")
           return
      print(strtext)
  if cmnd[0] == "SELECT":
     # print("The command is SELECT")
      strtext=cmnd[1]
      strtext = re.sub(r"FROM",   "FROM", strtext, flags = re.IGNORECASE)
     # print(strtext)
      selinf = strtext[0:strtext.find("FROM")].replace(r',', ' ').split()
      #print(selinf)
      for i in selinf:
              match = re.search(r'COUNT|MAX|AVG', i, re.IGNORECASE)
              if match !=None: print(i)
     # print(strtext)
      afterFrom = strtext[strtext.find("FROM")+5:].split(' ', 1)
      #print(afterFrom)
      if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', afterFrom[0])  == None:
          print("TableName doesn`t exist")
          return
      if len(afterFrom)>1:
       if  re.search(r'WHERE', afterFrom[1], re.IGNORECASE)!=None:
          if re.match(r'WHERE (-?[a-zA-Z0-9_]+ [ = | != | > | < | >= | <= ] -?[a-zA-Z0-9_]+)', afterFrom[1], re.IGNORECASE)==None:
              print("Whong syntax after WHERE")
              return
       if  re.search(r'GROUP_BY', afterFrom[1], re.IGNORECASE)!=None:
          aftGRBY = re.sub(r"group_by", "GROUP_BY", afterFrom[1], flags = re.IGNORECASE)
          if re.match(r'GROUP_BY [a-zA-Z0-9_]+', aftGRBY[aftGRBY.find('GROUP_BY '):])==None:
              print("Whong syntax after GROUP_BY")
              return
  if cmnd[0] == "DELETE":
      #print("The command is DELETE")
      cmnd[1] = re.sub(r'FROM ','', cmnd[1], flags = re.IGNORECASE)
      tablename = cmnd[1].split(' ', 1)
      if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', tablename[0])  == None:
          print("TableName doesn`t exist")
          return
      if len(tablename)>1:
        if  re.search(r'WHERE', tablename[1], re.IGNORECASE)!=None:
          if re.match(r'WHERE (-?[a-zA-Z0-9_]+ [ = | != | > | < | >= | <= ] -?[a-zA-Z0-9_]+)', tablename[1], re.IGNORECASE)==None:
              print("Whong syntax after WHERE")
              return
  if cmnd[0] == "EXIT":
      print("The command is EXIT")
      print("Thanks, bye")
      SystemExit()
#command_type(cmnd)

while True:
    str=input("Hello! Enter your command: ")
    #str = '   dElete  fRom table whERE 5 = 5 ;text;12345'
    #if str == "EXIT":
    if re.match(r'EXIT', str, re.IGNORECASE) !=None:
     #print("The command is EXIT")
     print("Thanks, bye")
     break
     #SystemExit()
    try:
     inpt=text_cleaner(str)
    except: print("Something went wrong in text_cleaner")
    try:
     cmnd=comand_recog(inpt)
    except: print("Something went wrong in comand_recog")
    try:
     command_type(cmnd)
    except: print("Something went wrong in command_type")
   # break



