
import re
import sys

command = {"CREATE", "INSERT", "SELECT", "DELETE", "EXIT"}
def text_cleaner(str):
    
    inpt = re.sub(r'[;].*','', str )
    inpt=re.sub(r"(^\s+)|(\(\s*)|(s*\))", "", inpt)
    inpt=re.sub(r"\s+", " ", inpt)
    inpt=re.sub(r"(\s*,)", ",", inpt)
    inpt=inpt.strip()
    inpt= inpt.split(' ', 1)
    return inpt
def comand_recog(inpt):
    inpt[0]=inpt[0].upper()
    if inpt[0] in command: 
        pass
    else: 
        print("What is the command? O-o\n Enter an existing command, please")
        return
    return inpt
def command_type(cmnd):
  if cmnd[0] == "CREATE":
      
      tablename= cmnd[1].split(' ', 1)
      if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', tablename[0]) == None:
          print("Wrong TableName pattern")
          return 
      if len(tablename)<2:
           print ("Where are column names? Try again")
           return
      strtext=tablename[1]
      strtext = strtext.split(', ') 
      for i in strtext:
       if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', i) == None:
         print("Wrong ColumnName pattern")
         return 
      
      cmd = 1
  if cmnd[0] == "INSERT":
      
      cmnd[1] = re.sub(r'INTO ','', cmnd[1], flags = re.IGNORECASE)
      tablename = cmnd[1].split(' ', 1)
      if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', tablename[0])  == None:
          print("TableName doesn`t exist")
          return
      strtext=tablename[1]
      strtext=strtext.split(', ')
      for i in range (len(strtext)):
          if re.search(r'^([-]?[0-9]+$)', strtext[i])  == None:
           print("You can insert only numbers. ", strtext[i], ": is not a number")
           return
      cmd = 2
  if cmnd[0] == "SELECT":
      
      strtext=cmnd[1]
      strtext = re.sub(r"FROM",   "FROM", strtext, flags = re.IGNORECASE)
      selinf = strtext[0:strtext.find("FROM")].replace(r',', ' ').split()
      for i in selinf:
              match = re.search(r'COUNT|MAX|AVG', i, re.IGNORECASE)
              if match !=None: print('')
      afterFrom = strtext[strtext.find("FROM")+5:].split(' ', 1)
      if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', afterFrom[0])  == None:
          print("TableName doesn`t exist")
          return
      if len(afterFrom)>1:
       if  re.search(r'WHERE', afterFrom[1], re.IGNORECASE)!=None:
          if re.match(r'WHERE (-?[a-zA-Z0-9_]+ (=|!=|>|<|>=|<=) -?[a-zA-Z0-9_]+)', afterFrom[1], re.IGNORECASE)==None:
              print("Whong syntax after WHERE")
              return
       if  re.search(r'GROUP_BY', afterFrom[1], re.IGNORECASE)!=None:
          aftGRBY = re.sub(r"group_by", "GROUP_BY", afterFrom[1], flags = re.IGNORECASE)
          if re.match(r'GROUP_BY [a-zA-Z0-9_]+', aftGRBY[aftGRBY.find('GROUP_BY '):])==None:
              print("Whong syntax after GROUP_BY")
              return
      cmd = 3
  if cmnd[0] == "DELETE":
      
      cmnd[1] = re.sub(r'FROM ','', cmnd[1], flags = re.IGNORECASE)
      tablename = cmnd[1].split(' ', 1)
      if re.search(r'^([a-zA-Z][a-zA-Z0-9_]*)', tablename[0])  == None:
          print("TableName doesn`t exist")
          return
      if len(tablename)>1:
        if  re.search(r'WHERE', tablename[1], re.IGNORECASE)!=None:
          if re.match(r'WHERE (-?[a-zA-Z0-9_]+ (=|!=|>|<|>=|<=) -?[a-zA-Z0-9_]+)', tablename[1], re.IGNORECASE)==None:
              print("Whong syntax after WHERE")
              return
      cmd = 4
  if cmnd[0] == "EXIT":
      print("Thanks, bye")
      SystemExit()
  return cmd, cmnd[1]




