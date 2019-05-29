# ESSS1

import argparse
import sys


# Simple input validation function
def inputValidation(X, Y):    
    if (type(X)!=int or type(Y)!=int or X<=0 or Y<=0 or X>=2000 or Y>2000 or X>=Y):
        sys.exit("X and Y must be positive integers in the range [1, 2000] and Y must be greater than X.") 
 
 
def fizzBuzz(X, Y):
    
    for n in range(X, Y+1):  
        
        if (n%3==0 and n%5==0):
            s="FizzBuzz"
        elif (n%3==0):
            s="Fizz"
        elif (n%5==0):
            s="Buzz"
        else:
            s=str(n)
          
        print(s)     
        
def main(args):
    
    # Initialize inputs
    X = args.x
    Y = args.y

    # Validation inputs
    inputValidation(X, Y)
    
    # Print Fizz Buzz on terminal
    fizzBuzz(X, Y)
            
    return
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ESSS1')
    parser.add_argument(dest='x', type=int, help='X is a positive integer lesser than Y in the range [1, 2000[')
    parser.add_argument(dest='y', type=int, help='Y is a positive integer greater than x in the range ]1, 2000]')
    args = parser.parse_args()
    main(args)