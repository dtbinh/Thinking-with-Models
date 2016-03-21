'''get_experiments.py

This is a module containing functions which can write an xml file of the
BehaviorSpace experiments from a chosen NetLogo model for use in checking 
homework answers.

Created on Aug 17, 2015

@author: Joel McCarthy
'''
    
def write_experiment_file(nlogo_file, exp_file):
    '''This copies behaviorspace experiments to an xml file.
    
    Args:
        nlogo_file (file): The NetLogo file from which to read experiments.
        exp_file (file): The xml file to which to write and save experiments.
    Returns:
        bool: True if successful, False otherwise.
    '''
    exp_list = []
    try:
        # Set DOCTYPE: necessary to run headless as experiment files.
        exp_file.write('<?xml version="1.0" encoding="us-ascii"?>\n' +
                '<!DOCTYPE experiments SYSTEM "behaviorspace.dtd">\n')
        # Read NetLogo file line by line until the BehaviorSpace section.
        next_line = nlogo_file.readline()
        while next_line != '' and next_line != '<experiments>\n':
            next_line = nlogo_file.readline()
        if next_line == '':
            print 'No experiments in this file'
            return []
        elif next_line == '<experiments>\n':
            # Copy over all lines in the BehaviorSpace section to the xml file.
            while next_line != '</experiments>\n':
                exp_file.write(next_line)
                next_line = nlogo_file.readline()
#                 print next_line, next_line.count('name=')
                if next_line.count('name=') != 0:
                    name = next_line.split()[1][6:-1]
#                     print name
                    exp_list.append(name)
            exp_file.write(next_line)
        return exp_list
    except AttributeError:
        # If no files were chosen, catch error.
        print 'Please choose valid files and try again.'
        return False
    finally:
        # Clean up files if they are open.
        if nlogo_file is not None: nlogo_file.close()
        if exp_file is not None: exp_file.close()