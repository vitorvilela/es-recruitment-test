# ESSS2

import argparse
import sys


# Simple input validation function
def inputValidation(X):    
    if (type(X)!=int or X<1E3 or X>1E9):
        sys.exit("X must be a positive integer in the range [1E3, 1E9].") 
 
 
def listGame(X):
    
    x = X
    y = 1
    score = 0
    
    while (x>1):         
        if (x%(y+1)==0):        
            score += 1  
            x = x/(y+1)
        else: 
            y += 1
           
    print(score)    
        
def main(args):
    
    # Initialize inputs
    X = args.x

    # Validation inputs
    inputValidation(X)
    
    # Print List Game score on terminal
    listGame(X)
            
    return
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ESSS2')
    parser.add_argument(dest='x', type=int, help='X is a positive integer in the range [1E3, 1E9]')
    args = parser.parse_args()
    main(args)