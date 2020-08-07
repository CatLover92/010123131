import pygame

# Not Finished Work in progress

class Tree():

    def __init__(self , value): 
        self.value = value 
        self.left = None
        self.right = None

def isOperator(c): 
    if (c == '&' or c == '+' or c == '!') : 
        return True
    else: 
        return False

def evaluateBoolExpr(s): 
  
    n = len(s) 
      
    # Traverse all operands by jumping 
    # a character after every iteration. 
    for i in range(0, n - 2, 2): 
  
        # If operator next to current  
        # operand is AND.''' 
        if (s[i + 1] == "&"): 
  
            if (s[i + 2] == "0" or s[i] == "0"): 
                s[i + 2] = "0"
            else: 
                s[i + 2] = "1"
  
        # If operator next to current  
        # operand is OR. 
        elif (s[i + 1] == "+"): 
            if (s[i + 2] == "1" or s[i] == "1"): 
                s[i + 2] = "1"
            else: 
                s[i + 2] = "0"
  
        # If operator next to current operand 
        # is XOR (Assuming a valid input) 
        else: 
            if (s[i + 2] == s[i]): 
                s[i + 2] = "0"
            else: 
                s[i + 2] = "1"
  
    return ord(s[n - 1]) - ord("0") 
  
s = "1C1+1+0&0"
string=[s[i] for i in range(len(s))] 
print(evaluateBoolExpr(string)) 
