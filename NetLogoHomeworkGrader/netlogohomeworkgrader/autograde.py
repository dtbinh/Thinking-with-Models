'''A wrapper called autograde.py that centralizes functions of the autograder.

This is a wrapper module which can call all outward facing methods from the
other modules in the autograder package. It can be run either through python
using the main method (and passing suitable parameters about which functions to
call), or from a terminal (or command line) window, with suitable flags 
instructing which functions to call.

Created on Aug 19, 2015

@author: Joel McCarthy

functions:
    main : The main function, which calls other functions depending on which
        parameters it is passed.
        
command line syntax:
    python autograde.py [-h] [-w ] [-g ]
    
args:
    -h: Prints the help documentation for this script.
    -w
    -g
'''

import write_script
import create_experiments
import compare_csvs
import sys, getopt

def main(argv):
    ''' The main method calls other functions from the autograde package.
    
    args:
        argv (list): The list of arguments passed in through the terminal 
            (or command line).
    '''
    try:
        opts, args =  getopt.getopt(argv, 'hw:g:', [""])
    except: 
        print 'autograde.py [-h] [-w] [-g]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (__doc__)
            sys.exit()
        elif opt == '-w':
            pass
        elif opt == '-g':
            pass
    for arg in args:
        pass

if __name__ == '__main__':
    main(sys.argv[1:])