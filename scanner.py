## Project 1 - Scanner
## Jeremy Vidaurri
## CS 3361

import sys

#Linked List node
class node:
    #Function to initialize node object
    def __init__(self,data,tokenType):
        self.data = data #Assign the data
        self.type = tokenType #Assign the token's type
        self.next = None #Initialize next as null
        
#Linked list will store the tokens as they are received
class linkedList:
    #Function to initialize the linked list object
    def __init__(self):
        self.head = None

    #Function to add a node to the linked list
    def addNode(self,newData,tokenType):
        #Initialize the node with the given data
        newNode = node(newData,tokenType)

        #If there is no head on the linked list, the new node is the head
        if self.head is None:
            self.head = newNode
            return

        #Traverse the list until a space is found
        last = self.head
        while(last.next):
            last = last.next

        #Make the last node in the list point to the new node
        last.next = newNode

    #Function to traverse and print the linked list data in order    
    def printList(self):
        tList = "("
        temp = self.head
        #Traverse the list. Concatenation is more efficient than printing token by token.
        while(temp):
            tList = tList + temp.type
            if(temp.next):
                tList = tList + ", "
            temp = temp.next
        tList = tList + ")"
        print(tList)
            
class State(linkedList):
    #Function to initialize the states. Finals holds all of the accept states. currState describes the state that the DFA is currently at.
    def __init__(self):
        self.finals = [2,6,7,8,9,10,12,14,15,16,17,18]
        self.currState = 1 #Initialize to 1 as that is where the DFA begins.

    #Function to check if the token is done
    def finalState(self,pos,stringArray):
        #Check each final state and see if it matches the current state
        for x in self.finals:
            if x == self.currState:
                #If it is in state 2, it will be a final state if the next character is not / or *
                if x == 2:
                    try:
                        if stringArray[pos + 1] == "/" or stringArray[pos + 1] == "*":
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
                        if stringArray[pos + 1].isnumeric() or stringArray[pos + 1] == ".":
                            return False
                        else:
                            return True
                    except(IndexError):
                        return -1
                #If it is in state 15, it will be a final state if the next character is not a digit.
                elif x == 15:
                    try:
                        if stringArray[pos + 1].isnumeric() :
                            return False
                        else:
                            return True
                    except(IndexError):
                        return -1
                #If it is in state 16, it will be a final state if the next character is not a letter or digit.
                elif x == 16:
                    try:
                        if stringArray[pos + 1].isalnum():
                            return False
                        else:
                            return True
                    except(IndexError):
                        return -1
        #If it does not match any of the final states, it is not a final state.
        return False

    #Function to scan the file
    def scan(self,stringArray):
        #Token list to print at the end
        tokenList = linkedList()
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
            16: "id or keyword",
            17: "read",
            18: "write"
        }
        token = ""
        pos = 0
        ##Token Flag
        ##0 - No flag
        ##1 - 'read' or 'write' token
        ##2 - Comment or final state
        ##-1 - error
        tokFlag = 0

        while pos < len(stringArray):
            #Comment flag is used to determine if within a comment a newline is met
            commentFlag = 0
            ##STATE 1
            if self.currState == 1:
                if stringArray[pos] == "/":
                    self.currState = 2
                elif stringArray[pos] == "(":
                    self.currState = 6
                elif stringArray[pos] == ")":
                    self.currState = 7
                elif stringArray[pos] == "+":
                    self.currState = 8
                elif stringArray[pos] == "-":
                    self.currState = 9
                elif stringArray[pos] == "*":
                    self.currState = 10
                elif stringArray[pos] == ":":
                    self.currState = 11
                elif stringArray[pos] == ".":
                    self.currState = 13
                elif stringArray[pos].isnumeric():
                    self.currState = 14
                elif stringArray[pos] == "r" and pos + 3 < len(stringArray) and stringArray[pos + 1] == "e" and stringArray[pos + 2] == "a" and stringArray[pos + 3] == "d":
                    self.currState = 17
                    pos += 4
                    token = "read"
                    tokFlag = 1
                elif stringArray[pos] == "w" and pos + 4 < len(stringArray) and stringArray[pos + 1] == "r" and stringArray[pos + 2] == "i" and stringArray[pos + 3] == "t" and stringArray[pos + 4] == "e":
                    self.currState = 18
                    pos += 5
                    token = "write"
                    tokFlag = 1
                elif stringArray[pos].isalpha():
                    self.currState = 16
                elif stringArray[pos] == ' ' or stringArray[pos] == "\n":
                    self.currState = 1
                    tokFlag = 2
                else:
                    tokFlag = -1
                    break
                    
            ##STATE 2
            elif self.currState == 2:
                token = ""
                if stringArray[pos] == "/":
                    self.currState = 3
                    tokFlag = 2
                    while(pos+1 <= len(stringArray)-1 or commentFlag != 1):
                        pos +=1
                        if stringArray[pos] == "\n":
                            self.currState = 1
                            commentFlag = 1
                elif stringArray[pos] == "*":

                    self.currState = 4
                    tokFlag = 2
                    while(pos+2 <= len(stringArray)-1 and commentFlag != 1):
                        pos +=1
                        if self.currState == 4 and stringArray[pos] == "*":
                            self.currState = 5
                        elif self.currState == 5 and stringArray[pos] == "/":
                            self.currState = 1
                            commentFlag = 1
                        elif self.currState == 5:
                            self.currState == 4
                    pos +=1
                else:
                    tokFlag = -1
                    break
                
            ##STATE 11
            elif self.currState == 11:
                if stringArray[pos] == "=":
                    self.currState = 12
                else:
                    tokFlag = -1
                    break

            ##STATE 13
            elif self.currState == 13:
                if stringArray[pos].isnumeric():
                    self.currState = 15
                else:
                    tokFlag = -1
                    break

            ##STATE 14
            elif self.currState == 14:
                if stringArray[pos].isnumeric():
                    self.currState = 14
                elif stringArray[pos] == ".":
                    self.currState = 15
                else:
                    tokFlag = -1
                    break

            ##STATE 15
            elif self.currState == 15:
                if stringArray[pos].isnumeric():
                    self.currState = 15
                else:
                    tokFlag = -1
                    break

            ##STATE 16
            else:
                if stringArray[pos].isalnum():
                    self.currState = 16
                else:
                    tokFlag = -1
                    break

            ##Check to see if it is in a final state. If so, check the tokFlag to see if anything needs to be added to the token. Reset the token, flag, and currState.
            if self.finalState(pos,stringArray):

                if tokFlag != 1:
                    token = token + stringArray[pos]
                tokenList.addNode(token,stateDict[self.currState])
                token = ""
                tokFlag = 2
                self.currState = 1
            
            #Flag 0, normal character
            if tokFlag == 0:
                token = token + stringArray[pos]
                pos += 1
            #Flag 1, read or write token
            elif tokFlag == 1:
                tokFlag = 0
            #Flag 2, comment or final state
            elif tokFlag == 2:
                tokFlag = 0
                pos += 1
                
        #If tokFlag is -1, there was an error with the tokens. Print only an error. Otherwise, print the list of tokens.
        if tokFlag == -1:
                print("Error.")
        else:        
            tokenList.printList()

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
    token = State() #State used to begin the scan process
    token.scan(stringArr) #Scan the file using the array from the file.

#If the provided file does not exist, error out.
try:
    main()
except FileNotFoundError:
    print("The specified file does not exist!")