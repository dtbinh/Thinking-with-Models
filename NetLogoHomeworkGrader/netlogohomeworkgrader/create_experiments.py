'''create_experiments.py

This is a module containing functions which can write an xml file of the
BehaviorSpace experiments from a chosen NetLogo model for use in checking 
homework answers.

Created on Aug 17, 2015

@author: Joel McCarthy
'''

from Tkinter import Tk
from tkFileDialog import askopenfile # , asksaveasfile

# def write_experiment(f, prob_num, repetitions):
#     f.write('\t<experiment name=\"prob{0}\" repetitions=\"{1}" runMetricsEveryStep=\"true\">')
#        
#    
# def create_experiment_file(file_name):
#     f = open(file_name)
#     f.write('')
#     write_experiment(f, 1)
    
def write_experiment_file(nlogo_file, exp_file):
    '''This copies behaviorspace experiments to an xml file.
    
    Args:
        nlogo_file (file): The NetLogo file from which to read experiments.
        exp_file (file): The xml file to which to write and save experiments.
    Returns:
        bool: True if successful, False otherwise.
    '''
#     nlogo_file = open(nlogo_file_path, 'r')
#     exp_file = open(exp_file_path, 'w')
    try:
        # Set DOCTYPE: necessary to run headless as experiment files.
        exp_file.write('<?xml version="1.0" encoding="us-ascii"?>\n' +
                '<!DOCTYPE experiments SYSTEM "behaviorspace.dtd">\n')
        # Read NetLogo file line by line until the BehaviorSpace section.
        next_line = nlogo_file.readline()
        while next_line != '' and next_line != '<experiments>\n':
            next_line = nlogo_file.readline()
        if next_line == '<experiments>\n':
            # Copy over all lines in the BehaviorSpace section to the xml file.
            while next_line != '</experiments>\n':
                exp_file.write(next_line)
                next_line = nlogo_file.readline()
            exp_file.write(next_line)
        return True
    except AttributeError:
        # If no files were chosen, catch error.
        print 'Please choose valid files and try again.'
        return False
    finally:
        # Clean up files if they are open.
        if nlogo_file is not None: nlogo_file.close()
        if exp_file is not None: exp_file.close()        

def choose_answer_file():
    '''Prompts the user to choose an answer nlogo file.
    
    Tk is used to open a NetLogo file for reading and the directory of this
    is used as the location for writing and saving an xml experiment file.

    returns:
        (file, file): The NetLogo answer file and the xml file to which to 
            write, both in the same directory.
    '''
    # Hide the root gui.
    Tk().withdraw()
    # Open the netlogo answer file with file explorer.
    nlogo_file = askopenfile(mode='r', 
            initialdir='C:/Users/Joel/Dropbox/Research/' + 
            'Philosophy of Science/Thinking with Models/Thinking-with-Models/', 
            title='Choose a netlogo file')
    # Open the xml experiment save file with file explorer.
#     exp_file = asksaveasfile(mode='w', 
#             initialdir='C:/Users/Joel/Dropbox/Research/Philosophy of Science/' + 
#             'Thinking with Models/Thinking-with-Models/hw1', 
#             title='Choose a name for an xml file')
    # Open an file, hw1_experiments.xml for writing in the same directory.
    exp_file = open(nlogo_file.name[:nlogo_file.name.rfind('/')] + 
            '/hw1_experiments.xml', 'w')
    # Return whether the write was successful or not.
    return (nlogo_file, exp_file)
        
def main():
    '''The main method selects files and runs write_experiment_file.
    
    This method calls the choose_answer_file and write_experiment_file methods.
    The result of write_experiment_file is printed.
    '''
    # Let the user choose the answer file.
    nlogo_file, exp_file = choose_answer_file()
    # Write the file and print success value.
    print 'Success: '+ str(write_experiment_file(nlogo_file, exp_file))
    
if __name__ == '__main__':
    # Calls the main method if run as main.
    main()
