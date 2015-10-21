'''autograde.py

This file contains functions which tie together the functionality of the other
modules in the autograder. It allows student files to be autgraded when placed 
in individual folders in a directory containing an answer folder. It has a main
method, and so can be run as a script. 

Created on Aug 18, 2015

@author: Joel McCarthy

command line sytax:
    autograde.py [-h] -n hw_number -p prob_number 
        [-m main_directory] [-d netlogo_directory]
    
args:
    -h, --help: Prints the help documentation for this script.
    -n hw_number, --hw_number hw_number: The number of the homework to be 
        graded.
    -p "problem_number1 problem_number2 ..." 
        --prob_numbers "problem_number1 problem_number2 ...": The numbers of 
        the problems to be graded. Can take of the form of a list of space-
        separated integers, as shown above, or a single integer with no quotes,
        for one problem (eg. -p 1).
    -m main_directory --main_dir main_directory: The main directory. Must 
        contain student folders with nlogo files, as well as an answer folder.
        with an answer nlogo file. Leaving this blank will cause a dialog box
        to open in which you may select your desired directory.
    -d netlogo_directory --netlogo_dir netlogo_directory: The netlogo 
        directory. Must contain NetLogo.jar, as well as the /lib directory.
        Leaving this blank will cause a dialog box to open in which you may 
        select your desired directory.
    -g --grade_only: Does not produce xml or csv files for grading. Instead,
        looks for pre-existing files and grades them.
        
example command:
    python autograde.py -n 1 -p "1 2 3" \
            -m "/home/joel/Dropbox/Research/Philosophy of Science/\
            Thinking with Models/Thinking-with-Models/autograde_sample/" \
            -d "/opt/NetLogo/netlogo-5.0.5"
            
        This command will execute the autograde.py script, grading homework 1,
        problems 1, 2, and 3 for all student folders which it finds in the
        directory after -m. It will expect to find the NetLogo.jar file in the
        directory after -d. (Please note, this cannot be directly copied into
        the terminal. Will require some spaces to be deleted before it is
        properly runnable.)
        
Attributes:
    answer_dir_name (str): The path of the directory containing the answer
        file, to which other grade files will be written.
    nlogo_command (str): The command to be run in opt for the behaviorspace
        experiments in NetLogo.
    data_file_name (str): The name of the 
'''

import sys
import getopt
import os
import csv
from Tkinter import Tk
from tkFileDialog import askdirectory, askopenfilename
from get_experiments import write_experiment_file
from grade_files import grade_problem, get_problem_grade
# from Tkinter import tkMessageBox

# Global values and names for running the script.
answer_dir_name = ''
nlogo_command = ''
data_file_name = ''

def get_script_values(main_dir, nlogo_dir):
    ''' This function sets the global values based on command line flags.
    
    This is a setup function which takes in directory names from the command
    line flags and uses a combination of automatic search and dialog boxes
    to set all of the critical file names and other values for creating
    files and running the grading script.
    
    args:
        main_dir (str): The name of the primary directory.
        nlogo_dir (str): The name of the directory containing the NetLogo.jar
            file and /lib subdirectory.
    returns:
        bool: True if successful, False otherwise.
    '''
    # If main_dir or nlogo_dir not set, allow user to select them in a dialog
    # box. Hide the root window of Tkinter.
    Tk().withdraw()
    if not os.path.isdir(str(main_dir)): 
        main_dir = askdirectory(title='Choose main directory') + '/'
    if not os.path.isdir(str(nlogo_dir)):
        nlogo_dir = askdirectory(title='Choose NetLogo directory') + '/'
    # Initialize some specific names for later commands.
    answer_dir_name = hw_name + '_files'
    data_file_name = '/' + hw_name + '_' + prob_name + '.csv'
    # Check that the directory which is supposed to contain the nlogo answer
    # file exists. If not, allow the opportunity to choose one.
    if (not os.path.isdir(main_dir + answer_dir_name) or 
            not os.path.isfile(main_dir + answer_dir_name + 
            '/' + hw_name + '_answers.nlogo')):
        a_d = askdirectory(initialdir=main_dir, 
                title='Choose an answer directory in your main directory.')
        # If the directory is valid (ie. directly in main_dir and containting
        # the netlogo answer file), then accept.
        if (main_dir in a_d and 
                os.path.isfile(a_d + '/' + hw_name + '_answers.nlogo')): 
            answer_dir_name = a_d.replace(main_dir, '')
        # Otherwise, print an error message and return False.
        else:
            print "Please choose a valid directory inside main_dir and " + \
                    "containing " + hw_name + "_answers.nlogo."
            return False
    # Initialize strings for NetLogo command. {0} is for a directory name, {1}
    # is for part of a file name (student_id or the string 'answers').
    model_path = '"' + main_dir + '{0}/' + hw_name + '_{1}.nlogo"'
    setup_file_path = '"' + main_dir + answer_dir_name + '/' + \
            hw_name + '_experiments.xml"'
    experiment = prob_name
    table_path = '"' + main_dir + '{0}' + data_file_name + '"'
    # Assemble the NetLogo command to be run for each student nlogo file. The
    # command is based on the function arguments, and has place holders for
    # student ids.
    nlogo_command='java -Xmx1024m -Dfile.encoding=UTF-8 -cp NetLogo.jar ' + \
            'org.nlogo.headless.Main' + \
            ' --model ' + model_path + \
            ' --setup-file ' + setup_file_path + \
            ' --experiment ' + experiment + \
            ' --table ' + table_path + \
            ' --threads 1 \n'
    
    return True

def run_multiple_grading_commands(hw_num, prob_nums, main_dir, nlogo_dir, 
        grade_only):
    '''This function runs run_grading_commands on multiple problems at once.
    
    This is a wrapper function which enables grading multiple problems at once
    from a list of (hopefully valid) problems. There is no support for invalid
    problems. If the user gives one (ie. 11 on a 10 problem set), the function
    will break in the ordinary way, either failing to find an experiment in an
    nlogo file, or failing to find a csv file. The arguments are exactly the
    same as those of run_grading_commands, except for prob_nums, so see its
    docstring for more details.
    
    args:
        hw_num (int): The homework number.
        prob_nums (int): A list of problem numbers to be graded.
        main_dir (str): The name of the primary directory.
        nlogo_dir (str): The name of the directory containing the NetLogo.jar
            file and /lib subdirectory.
        grade_only (bool): If True, the function does not produce any new 
            files.
    returns:
        list: A list of boolean success values, returned from 
            run_grading_commands for each problem.
    '''
    # Run the grading commands for each problem in the list and record success.
    succ_list = []
    for prob_num in prob_nums:
        succ_list.append(run_grading_commands(hw_num, prob_num, main_dir, 
                nlogo_dir, grade_only))
    # Return success values.
    return succ_list

def run_grading_commands(hw_name, prob_name, main_dir, nlogo_dir, grade_only):
    '''This function runs all commands for grading a particular problem.
    
    Where applicable, commands are run through direct calls to python
    functions. Commands requiring Java are done using system calls to the
    terminal. Note that this method also avoids the issue of writing a script
    and so dealing with bash and bat differences.
    
    Args:
        hw_num (int): The homework number.
        prob_num (int): The problem number.
        main_dir (str): The name of the primary directory, which should contain
            a subdirectory for each student and one for answers. These 
            subdirectories should contain student and answer NetLogo files.
            Student csv files will be written into each student's subdirectory
            and all additional files will be written into the same subdirectory
            as the answer file.
        nlogo_dir (str): The name of the directory containing the NetLogo.jar
            file and /lib subdirectory.
        grade_only (bool): If True, the function does not run java commands to
            produce the experiment xml file or the data csv files from each 
            nlogo file. Instead, it assumes they already exist, and just grades 
            them.
    Returns:
        list: True if successful, False otherwise.
    '''        
    # If creating files, create the experiment file.
    if not grade_only:
        write_experiment_file(
                open(main_dir + answer_dir_name + 
                '/' + hw_name + '_answers.nlogo'), 
                open(main_dir + answer_dir_name + 
                '/' + hw_name + '_experiments.xml', 'w'))
    # If creating files, Change to directory containing NetLogo.jar and call
    # system to produce csv answer file. Get path of answer file.
    if not grade_only:
        os.chdir(nlogo_dir)
        os.system(nlogo_command.format(answer_dir_name, 'answers'))
    ans_path = main_dir + answer_dir_name + data_file_name
    
    # Grade student nlogo files.
    for h in os.listdir(main_dir):
        # Student subdirectories are identified as those directories which have
        # only digits in their names.
        if os.path.isdir(main_dir + h) and h.isdigit():
            # If creating files, create student csv files from nlogo files.
            if not grade_only:
                os.system(nlogo_command.format(h, h))
            # Grade csv files against answer file and record grades.
            stud_path = main_dir + h + data_file_name
            record_grade(get_problem_grade(grade_problem(ans_path, stud_path)),
                    h, hw_name, prob_name, 
                    main_dir + '/grades.csv')
    os.system('echo "Graded ' + hw_name + '.' + prob_name + '"')
    return True

def record_grade(grade, student_id, hw_name, prob_name, grade_file_path):
    '''This records the given grade in the correct location in the grade file.

    This functions maintains a csv grade file, where each row is a different
    student_id and each column a different problem labeled 
    <hw_number>.<problem_number>. Grades are recorded in this table.
    
    args:
        grade (int): The grade to record for this homework problem.
        student_id (str): The student_id with which the grade is associated.
        hw_num (str): The homework number.
        prob_num (str): The problem number.
        grade_file_path (str): The path at which to find or create the grade
            file.
    returns:
        boolean: True if successful, False otherwise.
    '''
    # Read the grade table completely out of the grade csv file.
    try:
        with open(grade_file_path, 'rb') as grade_file:
            grade_table = [row for row in csv.reader(grade_file)]
    except:
        grade_table = []
    # Add or change value in the grade table.
    col_name = hw_name + '.' + prob_name
    # If grade_table is empty, initialize it with the new student_id and value.
    if grade_table == []:
        grade_table.append(['*', col_name])
        grade_table.append([student_id, grade])
    # Otherwise, add the new value in at the correct place.
    else:
        # If this student_id is not in the grade table, add a new row for it.
        if student_id not in [row[0] for row in grade_table]:
            grade_table.append([student_id] + ['*'] * (len(grade_table[0]) - 1))
        row_index = [row[0] for row in grade_table].index(student_id)
        # If this column is in the grade table, set the student's value.
        if col_name in grade_table[0]:
            grade_table[row_index][grade_table[0].index(col_name)] = grade
        # Otherwise, add a new column, setting all values to '' and the
        # student's to grade.
        else:
            # Put a new column with the new value in at the end of grade_table.
            grade_table[0].append(col_name)
            for row in grade_table[1:]:
                row.append('')
            grade_table[row_index][-1] = grade
    # Write the grade table back into grade csv file.
    try:
        with open(grade_file_path, 'w+') as grade_file:
            grade_file_writer = csv.writer(grade_file)
            for row in grade_table:
                grade_file_writer.writerow(row)
    # If there is an error, print out the info and return False.
    except IOError:
        print 'Problem with writing to grade csv file.'
        print sys.exc_info()
        return False
    return True

def main(argv):
    '''The main method runs the run_grading_commands function.
    
    This method uses argument values given in the command line and parses them
    to decide which functionality to run.
    
    Args:
        argv (list): The list of system arguments passed through the terminal.
            See module docstring or type 'python autograde.py -h' for 
            documentation on which flags are valid.
    '''
    # Preset some variables for the function.
    hw_num, prob_num, main_dir, netlogo_dir, grade_only = -1, -1, -1, -1, False
    # Get the terminal flags from argv.
    try:
        opts, args =  getopt.getopt(argv, 'hn:p:d:m:g', ['help', 'hw_number=', 
                'prob_numbers=', 'main_dir=', 'netlogo_dir=', 'grade_only'])
    # If error, print the docstring for this script.
    except: 
        print('Problem with command flags. Please see documentation and ' + \
                'correct.\n')
        print(__doc__)
        sys.exit(2)
    # Set variables according to flags (see module __doc__ string or type
    # "python autograde.py -h" into terminal for details).
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(__doc__)
            sys.exit()
        elif opt in ('-n', '--hw_number'):
            hw_num = arg
        elif opt in ('-p', '--prob_numbers'):
            # Get problem arguments out of string and check all are numbers.
            arg = arg.split()
            if all([p.isdigit() for p in arg]):
                prob_num = arg
            # If not, print error message.
            else: 
                print 'All -p or --prob_numbers arguments must be numbers\n'
                print(__doc__)
                sys.exit(2)
        elif opt in ('-m', '--main_dir'):
            main_dir = arg
        elif opt in ('-d', '--netlogo_dir'):
            netlogo_dir = arg
        elif opt in ('-g', '--grade_only'):
            grade_only = True
    # No extra arguments
    for arg in args:
        pass
    # Must set homework number. If not, fail and print help.
    if hw_num == -1:
        print "Please use all required flags.\n"
        print(__doc__)
        
    # If no problem number set, find and grade all problems.
    if prob_num == -1:
        
    # If correct, run the autograde function.
    else:
        return run_multiple_grading_commands(hw_num, prob_num, main_dir, 
                netlogo_dir, grade_only)

if __name__ == '__main__':
    # Runs the main method if run as main.
    main(sys.argv[1:])