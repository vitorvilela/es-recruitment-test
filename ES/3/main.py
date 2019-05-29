# ESSS3

import argparse
import sys
import os

# Simple input validation function
def inputValidation(filename): 
    
    if (filename.split('.')[1] != 'txt'):
        sys.exit('You must call this function with a .txt file name.') 
       
 
# Print Graph on terminal 
def printGraph(log, numberOfRecords):
    
    accumulatedRecord = 0
    
    for key, value in sorted(log.items()):  
        
        s = ''       
        accumulatedRecord += value
        
        # Fill the upper side of the graph 
        for r in range(numberOfRecords-accumulatedRecord):
            s = s + '.'
            
        # Fill the curve    
        for v in range(value):
            s = s + '*'
          
        # Fill the down side of the graph 
        for r in range(numberOfRecords-len(s)):
            s = s + '.'
        
        print(s)
        
    print('\n')   
    
    
# Check if log is valid and account how many records shows a similar score    
def checkAndCount(line):
    
    counter = 0
    
    for s in line:
        if s not in ['.', '*', '\n']:
            msg = 'Invalid character found: \'{:s}\'.'.format(s)
            sys.exit(msg) 
        elif s == '*':
            counter += 1
    
    return counter
 
         
# Read text file and write logs into a list 
def chartingProgress(filename):         
    
    filePathName = os.path.join(os.getcwd(), filename)
        
    # Open and manage log file
    try: 
        
        with open(filePathName, 'r') as logfile:           
            log = {} 
            numberOfRecords = 0
            for row, line in enumerate(logfile):  
                if line in ['\n']:  
                    printGraph(log, numberOfRecords)
                    log = {}   
                    numberOfRecords = 0
                else:                 
                    log[str(row)] = checkAndCount(line) 
                    numberOfRecords = len(line.strip('\n'))                    
            printGraph(log, numberOfRecords)    
        
    except IOError:
        print('Error: couldn\'t find log file at current path.')   
    
    else:
        logfile.close()
         
        
def main(args):
    
    # Initialize inputs
    filename = args.filename

    # Validate input
    inputValidation(filename)
    
    # Print sorted logs on terminal
    chartingProgress(filename)
            
    return
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ESSS3')
    parser.add_argument(dest='filename', type=str, help='Log file name')
    args = parser.parse_args()
    main(args)