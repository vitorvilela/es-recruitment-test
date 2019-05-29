# ESSS4

import argparse
import sys


# Simple input validation function
def inputValidation(X):    
    if (type(X)!=int or X<=0):
        sys.exit("X must be a positive integer.") 
 
 
def squareRoot(X):
    
    # Chosing initial boundary values so that SQRT(X) belongs to [s, X]
    S = 0.
    E = X
    
    # Setting precision
    EPS = 1E-5
       
    # Compare the length of the current interval with precision
    while(abs(E-S) >= EPS):
        
        # Actual Square Root approximation - the Middle value
        M = (S + E) / 2
        
        if M*M > X: 
            E = M
        else:
            S = M
            
    print('{:5.3f}'.format(M))    
    
    
        
def main(args):
    
    # Initialize inputs
    X = args.x

    # Validation inputs
    inputValidation(X)
    
    # Print Square Root of X on terminal
    squareRoot(X)
            
    return
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ESSS4')
    parser.add_argument(dest='x', type=int, help='X is a positive integer')
    args = parser.parse_args()
    main(args)