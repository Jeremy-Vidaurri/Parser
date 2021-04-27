## Project 2 - Parsing
## Jeremy Vidaurri & Ryan Hernandez
## CS 3361



import sys
from os import system,name


class parseError(Exception):
    pass


def clear():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

            
class State(parseError):
    #Function to initialize the states. Finals holds all of the accept states. currState describes the state that the DFA is currently at.
    def __init__(self,stringArr):
        self.finals = [2,6,7,8,9,10,12,14,15,16,17,18]
        self.currState = 1 #Initialize to 1 as that is where the DFA begins.
        self.pos = 0
        self.indentation = 0
        self.inputToken = ""
        self.stringToken = ""
        self.stringArray = stringArr
        


    #Function to check if the token is done
    def finalState(self,):
        #Check each final state and see if it matches the current state
        for x in self.finals:
            if x == self.currState:
                #If it is in state 2, it will be a final state if the next character is not / or *
                if x == 2:
                    try:
                        if self.stringArray[self.pos + 1] == "/" or self.stringArray[self.pos + 1] == "*":
                            return False
                        else:
                            return True
                    except(IndexError):
                        return -1
                #States 6-10, 12, 17, and 18 are automatically final states regardless of the next character.
                elif (x > 5 and x < 11) or x == 12 or x == 17 or x == 18:
                    return True
                #If it is in state 14, it will be a final state if the next character is not a digit or a period.
                elif x == 14:
                    try:
                        if self.stringArray[self.pos + 1].isnumeric() or self.stringArray[self.pos + 1] == ".":
                            return False
                        else:
                            return True
                    except(IndexError):
                        return -1
                #If it is in state 15, it will be a final state if the next character is not a digit.
                elif x == 15:
                    try:
                        if self.stringArray[self.pos + 1].isnumeric() :
                            return False
                        else:
                            return True
                    except(IndexError):
                        return -1
                #If it is in state 16, it will be a final state if the next character is not a letter or digit.
                elif x == 16:
                    try:
                        if self.stringArray[self.pos + 1].isalnum():
                            return False
                        else:
                            return True
                    except(IndexError):
                        return -1
        #If it does not match any of the final states, it is not a final state.
        return False

    #Function to scan the file
    def scan(self):
        #Dictionary to differentiate accept states.
        stateDict = {
            2: "div",
            6: "lparen",
            7: "rparen",
            8: "plus",
            9: "minus",
            10: "times",
            12: "assign",
            14: "number",
            15: "number",
            16: "id",
            17: "read",
            18: "write"
        }
        self.currState = 1
        token = ""
        ##Token Flag
        ##0 - No flag
        ##1 - 'read' or 'write' token
        ##2 - Comment or final state
        ##-1 - error
        tokFlag = 0

        while self.pos < len(self.stringArray):
            #Comment flag is used to determine if within a comment a newline is met
            commentFlag = 0
            ##STATE 1
            if self.currState == 1:
                if self.stringArray[self.pos] == "/":
                    self.currState = 2
                elif self.stringArray[self.pos] == "(":
                    self.currState = 6
                elif self.stringArray[self.pos] == ")":
                    self.currState = 7
                elif self.stringArray[self.pos] == "+":
                    self.currState = 8
                elif self.stringArray[self.pos] == "-":
                    self.currState = 9
                elif self.stringArray[self.pos] == "*":
                    self.currState = 10
                elif self.stringArray[self.pos] == ":":
                    self.currState = 11
                elif self.stringArray[self.pos] == ".":
                    self.currState = 13
                elif self.stringArray[self.pos].isnumeric():
                    self.currState = 14
                elif self.stringArray[self.pos] == "r" and self.pos + 3 < len(self.stringArray) and self.stringArray[self.pos + 1] == "e" and self.stringArray[self.pos + 2] == "a" and self.stringArray[self.pos + 3] == "d":
                    self.currState = 17
                    self.pos += 4
                    token = "read"
                    tokFlag = 1
                elif self.stringArray[self.pos] == "w" and self.pos + 4 < len(self.stringArray) and self.stringArray[self.pos + 1] == "r" and self.stringArray[self.pos + 2] == "i" and self.stringArray[self.pos + 3] == "t" and self.stringArray[self.pos + 4] == "e":
                    self.currState = 18
                    self.pos += 5
                    token = "write"
                    tokFlag = 1
                elif self.stringArray[self.pos].isalpha():
                    self.currState = 16
                elif self.stringArray[self.pos] == ' ' or self.stringArray[self.pos] == "\n":
                    self.currState = 1
                    tokFlag = 2
                else:
                    tokFlag = -1
                    
                    
            ##STATE 2
            elif self.currState == 2:
                token = ""
                if self.stringArray[self.pos] == "/":
                    self.currState = 3
                    tokFlag = 2
                    while(self.pos+1 <= len(self.stringArray)-1 or commentFlag != 1):
                        self.pos +=1
                        if self.pos == len(self.stringArray) or self.stringArray[self.pos] == "\n":
                            self.currState = 1
                            commentFlag = 1
                elif self.stringArray[self.pos] == "*":

                    self.currState = 4
                    tokFlag = 2
                    while(self.pos+2 <= len(self.stringArray)-1 and commentFlag != 1):
                        self.pos +=1
                        if self.currState == 4 and self.stringArray[self.pos] == "*":
                            self.currState = 5
                        elif self.currState == 5 and self.stringArray[self.pos] == "/":
                            self.currState = 1
                            commentFlag = 1
                        elif self.currState == 5:
                            self.currState == 4
                    if self.currState == 4:
                        raise parseError
                    self.pos +=1
                else:
                    tokFlag = -1
                    
                
            ##STATE 11
            elif self.currState == 11:
                if self.stringArray[self.pos] == "=":
                    self.currState = 12
                else:
                    tokFlag = -1
                    

            ##STATE 13
            elif self.currState == 13:
                if self.stringArray[self.pos].isnumeric():
                    self.currState = 15
                else:
                    tokFlag = -1
                    raise parseError

            ##STATE 14
            elif self.currState == 14:
                if self.stringArray[self.pos].isnumeric():
                    self.currState = 14
                elif self.stringArray[self.pos] == ".":
                    self.currState = 15
                else:
                    tokFlag = -1
                    raise parseError

            ##STATE 15
            elif self.currState == 15:
                if self.stringArray[self.pos].isnumeric():
                    self.currState = 15
                else:
                    tokFlag = -1
                    raise parseError

            ##STATE 16
            else:
                if self.stringArray[self.pos].isalnum():
                    self.currState = 16
                else:
                    tokFlag = -1
                    raise parseError

            ##Check to see if it is in a final state. If so, check the tokFlag to see if anything needs to be added to the token. Reset the token, flag, and currState.
            if self.finalState():

                if tokFlag != 1:
                    token = token + self.stringArray[self.pos]

                self.pos += 1
                #print(token + ": " + stateDict[self.currState])
                return token,stateDict[self.currState]
                
            
            #Flag 0, normal character
            if tokFlag == 0:
                token = token + self.stringArray[self.pos]
                self.pos += 1
            #Flag 1, read or write token
            elif tokFlag == 1:
                tokFlag = 0
            #Flag 2, comment or final state
            elif tokFlag == 2:
                tokFlag = 0
                self.pos += 1
        else:
            return ("$$","$$")
                
        #If tokFlag is -1, there was an error with the tokens. Print only an error. Otherwise, print the list of tokens.
        if tokFlag == -1:
                print("Error.")

    def match(self,token,):
          
        if self.inputToken == token and not self.inputToken =="$$":
            self.indentation+=1
            print("\t"*self.indentation+"<"+self.inputToken+">")
            self.indentation+=1
            print("\t"*self.indentation + self.stringToken) 
            self.indentation-=1
            print("\t"*self.indentation+"</"+self.inputToken+">")
            self.indentation-=1
        elif self.inputToken =="$$":
            return
        else: 
            raise parseError
        self.stringToken, self.inputToken = self.scan()   
        


    def program(self):
         
        
        print("<Program>")
        self.stringToken, self.inputToken = self.scan() 
        self.stmt_list()
         
        self.match("$$")
        print("</Program>")
        
        
        
    def stmt_list(self):
         
        if self.inputToken == "id" or self.inputToken == "read" or self.inputToken == "write":
            self.indentation += 1
            print("\t"*self.indentation + "<stmt_list>")
            self.stmt()
            
            self.stmt_list()
            print("\t"*self.indentation + "</stmt_list>")
            self.indentation -= 1

        elif self.inputToken == "$$":
            self.indentation += 1
            print("\t"*self.indentation + "<stmt_list>")
            print("\t"*self.indentation + "</stmt_list>")
            self.indentation -= 1
            return
        else:
            raise parseError()
    

    def stmt(self):
        if self.inputToken == "id":
            self.indentation += 1
            print("\t"*self.indentation + "<stmt>")
            self.match("id")
             
            self.match("assign")
            self.expr()
            print("\t"*self.indentation + "</stmt>")
            self.indentation -= 1
        elif self.inputToken =="read":
            self.indentation += 1
            print("\t"*self.indentation + "<stmt>")
            self.match("read")
             
            self.match("id")
            print("\t"*self.indentation + "</stmt>")
            self.indentation -= 1
        elif self.inputToken == "write":
            self.indentation += 1
            print("\t"*self.indentation + "<stmt>")
            self.match("write")
            self.expr()
            print("\t"*self.indentation + "</stmt>")
            self.indentation -= 1
        else:
            raise parseError()
        

    def expr(self):
        
         
        if self.inputToken == "id" or self.inputToken == "number" or self.inputToken=="lparen":
            self.indentation +=1
            print("\t"*self.indentation +"<expr>")
            self.term()
            
            self.term_tail()

            print("\t"*self.indentation +"</expr>")
            self.indentation -=1
        else:
            raise parseError()

    def term_tail(self):
        self.indentation+=1
        print("\t"*self.indentation +"<term_tail>")
        # 
        if self.inputToken =="plus" or self.inputToken =="minus":
            
            self.add_op()
             
            self.term()
    

            self.term_tail()
            print("\t"*self.indentation +"</term_tail>")
            self.indentation-=1
        elif self.inputToken =="rparen" or self.inputToken =="id" or self.inputToken =="read" or self.inputToken =="write" or self.inputToken=="$$":
            print("\t"*self.indentation +"</term_tail>")
            self.indentation-=1    
            return
        else:
            raise parseError

    def term(self):       
        if self.inputToken == "id" or self.inputToken == "number" or self.inputToken == "lparen":
            self.indentation+=1
            print("\t"*self.indentation +"<term>")
            self.factor()
            
            self.factor_tail()
            print("\t"*self.indentation +"</term>")
            self.indentation-=1

        else:
            raise parseError

    def factor_tail(self):
        
        self.indentation +=1
        print("\t"*self.indentation +"<factor_tail>")
        if self.inputToken == "times" or self.inputToken == "div":
            self.mult_op()
             
            self.factor()
            self.factor_tail()
            print("\t"*self.indentation +"</factor_tail>")
            self.indentation-=1
        elif self.inputToken == "plus" or self.inputToken == "minus" or self.inputToken == "rparen" or self.inputToken == "id" or self.inputToken == "read" or self.inputToken == "write" or self.inputToken == "$$":
            print("\t"*self.indentation +"</factor_tail>")
            self.indentation-=1
            return
        else:
            raise parseError

    def factor(self):
        self.indentation+=1
        print("\t"*self.indentation +"<factor>")
        if self.inputToken == "id":
            self.match("id")
        elif self.inputToken == "number":
            self.match("number")
        elif self.inputToken == "lparen":
            self.match("lparen")
            self.expr()
            self.match("rparen")
        else:
            raise parseError
        print("\t"*self.indentation +"</factor>")
        self.indentation-=1

    def add_op(self):        
        self.indentation+=1
        print("\t"*self.indentation+"<add_op>")
        if self.inputToken == "plus":
            self.match("plus")
        elif self.inputToken == "minus":
            self.match("minus")
        else:
            raise parseError
        print("\t"*self.indentation+"</add_op>")  
        self.indentation-=1

    def mult_op(self):
        self.indentation+=1
        print("\t"*self.indentation+"<mult_op>")
        if self.inputToken == "times":
            self.match("times")
        elif self.inputToken == "div":
            self.match("div")
        else:
            raise parseError
        print("\t"*self.indentation+"</mult_op>")  
        self.indentation-=1


    def parse(self):  
        while (self.pos < len(self.stringArray) ):
            self.program()

class File():

    #Function to initialize the file for reading
    def __init__(self):
        self.file=open(sys.argv[1],"r")

    #Function to take the file and turn it into an array
    def filetoArray(self):
        charArray = []
        while 1:
            char = self.file.read(1)
            if not char:
                return charArray
            charArray.append(char)

def main():
    userfile = File() #Grab file from user
    stringArr = userfile.filetoArray() #Store each character in a single array
    token = State(stringArr) #State used to begin the scan process
    token.parse() #Scan the file using the array from the file.


#If the provided file does not exist, error out.
try:
    main()
except FileNotFoundError:
    print("The specified file does not exist!")
except parseError:
    clear()
    print("Error")