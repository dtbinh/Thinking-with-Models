'''autograde.py

This file contains functions which tie together the functionality of the other
modules in the autograder. It allows student files to be autgraded when placed 
in individual folders in a directory containing an answer folder. It has a main
method, and so can be run as a script. 

Created on Aug 18, 2015

@author: Joel McCarthy

command line sytax:
    python autograde.py [-h] -n hw_number -p prob_number 
        [-m main_directory] [-d netlogo_directory]
    
args:
    -h, --help: Prints the help documentation for this script.
    -n hw_number, --hw_number hw_number: The number of the homework to be 
        graded.
    -p problem_number --prob_number problem_number: The number of the problem
        to be graded.
    -m main_directory --main_dir main_directory: The main directory. Must 
        contain student folders with nlogo files, as well as an answer folder.
        with an answer nlogo file. Leaving this blank will cause a dialog box
        to open in which you may select your desired directory.
    -d netlogo_directory --netlogo_dir netlogo_directory: The netlogo 
        directory. Must contain NetLogo.jar, as well as the /lib directory.
        Leaving this blank will cause a dialog box to open in which you may 
        select your desired directory.
'''

import sys
import getopt
import os
import csv
from Tkinter import Tk
from tkFileDialog import askdirectory
from netlogohomeworkgrader.get_experiments import write_experiment_file
from netlogohomeworkgrader.grade_files import grade_problem, get_problem_grade

def run_grading_commands(hw_num, prob_num, main_dir, nlogo_dir):
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
    Returns:
        list: True if successful, False otherwise.
    '''
    # If main_dir or nlogo_dir not set, allow user to select them in a dialog
    # box. Hide the root window of Tkinter.
    Tk().withdraw()
    if not os.path.isdir(str(main_dir)): 
        main_dir = askdirectory(title='Choose main directory') + '/'
    if not os.path.isdir(str(nlogo_dir)):
        nlogo_dir = askdirectory(title='Choose NetLogo directory') + '/'
    # Initialize some specific names for later commands.
    answer_dir_name = 'hw' + hw_num + '_files'
    data_file_name = '/hw' + hw_num + '_prob' + prob_num + '.csv'
    # Check that the directory which is supposed to contain the nlogo answer
    # file exists. If not, allow the opportunity to choose one.
    if (not os.path.isdir(main_dir + answer_dir_name) or 
            not os.path.isfile(main_dir + answer_dir_name + 
            '/hw' + hw_num + '_answers.nlogo')):
        a_d = askdirectory(initialdir=main_dir, 
                title='Choose an answer directory in your main directory.')
        # If the directory is valid (ie. directly in main_dir and containting
        # the netlogo answer file), then accept.
        if (main_dir in a_d and 
                os.path.isfile(a_d + '/hw' + hw_num + '_answers.nlogo')): 
            answer_dir_name = a_d.replace(main_dir, '')
        # Otherwise, print an error message and return False.
        else:
            print "Please choose a valid directory inside main_dir and " + \
                    "containing hw" + hw_num + "_answers.nlogo."
            return False
    # Initialize strings for NetLogo command. {0} is for a directory name, {1}
    # is for part of a file name (student_id or the string 'answers').
    model_path = '"' + main_dir + '{0}/hw' + hw_num + '_{1}.nlogo"'
    setup_file_path = '"' + main_dir + answer_dir_name + '/hw' + \
            hw_num + '_experiments.xml"'
    experiment = 'prob' + prob_num
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
    # Create the experiment file.
    write_experiment_file(open(main_dir + answer_dir_name + '/hw' +  hw_num + 
            '_answers.nlogo'), open(main_dir + answer_dir_name + '/hw' + 
            hw_num + '_experiments.xml', 'w'))
    # Change to the directory containing NetLogo.jar.
    os.chdir(nlogo_dir)
    # Call system to create the csv answer file and then get its path.
    os.system(nlogo_command.format(answer_dir_name, 'answers'))
    ans_path = main_dir + answer_dir_name + data_file_name
    # Grade student nlogo files.
    for h in os.listdir(main_dir):
        # Student subdirectories are identified as those directories which have
        # only digits in their names.
        if os.path.isdir(main_dir + h) and h.isdigit():
            # Create student csv files from nlogo files.
            os.system(nlogo_command.format(h, h))
            # Grade csv files against answer file and record grades.
            stud_path = main_dir + h + data_file_name
            record_grade(get_problem_grade(grade_problem(ans_path, stud_path)),
                    h, hw_num, prob_num, 
                    main_dir + answer_dir_name + '/grades.csv')
    os.system('echo "Graded"')
    return True

def record_grade(grade, student_id, hw_num, prob_num, grade_file_path):
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
    col_name = hw_num + '.' + prob_num
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
    
# def get_grading_commands(hw_num, prob_num,
#         main_dir='C:/Users/Joel/Dropbox/Research/Philosophy of Science/' + 
#         'Thinking with Models/Thinking-with-Models/hw1/'):
#     '''This function returns a list of terminal commands for autograding.
#     
#     Args:
#         hw_num (int): The homework number.
#         prob_num (int): The problem number.
#         main_dir (str): The name of the primary directory, which should contain
#             a subdirectory for each student and one for answers. These 
#             subdirectories should contain student and answer NetLogo files.
#             Student csv files will be written into each student's subdirectory
#             and all additional files will be written into the same subdirectory
#             as the answer file.
#     Returns:
#         list: A list of strings, commands which can be run in the terminal or
#             written to a bash or bat script.
#     '''
#     # Assemble the NetLogo command to be run for each student nlogo file. The
#     # command is based on the main_dir, hw_num, and prob_num, and is complete
#     # except for the student id on the --model parameter, since this will be 
#     # different for each student.
#     nlogo_command='java -Xmx1024m -Dfile.encoding=UTF-8 -cp NetLogo.jar ' + \
#         'org.nlogo.headless.Main --model "' + main_dir + 'hw' + hw_num + '_{0}.nlogo" --setup-file "' + main_dir + 'hw' + hw_num + '_experiments.xml" --experiment prob' + prob_num + \
#         ' --table "' + main_dir + 'hw' + hw_num + '_{0}_' + prob_num + '.csv" --threads 1 \n'
#     # The list of commands.
#     comm_list = []
#     # Call the create_experiments module.
#     comm_list.append('python ' + __file__[0:-15].replace('\\', '/') + 
#             'create_experiments.py\n')
#     # 1 will instruct to save the current directory for convenience.
#     comm_list.append(1)
#     comm_list.append('cd C:/Program Files (x86)/NetLogo 5.1.0\n')
#     comm_list.append(nlogo_command.format('answers'))
#     for h in os.listdir(main_dir):
#         if 'hw' + str(hw_num) in h and '.nlogo' in h and 'answers' not in h:
#             student_name = h[4:h.find('.nlogo')]
# #             print nlogo_command.format(student_name)
#             comm_list.append(nlogo_command.format(student_name))
#     comm_list.append('python --version\n')
#     # Reset to the initial current directory for convenience.
#     comm_list.append('cd %cur_dir%')
#     return comm_list
# 
# def write_grading_script(hw_num, prob_num,
#         main_dir='C:/Users/Joel/Dropbox/Research/Philosophy of Science/' + 
#         'Thinking with Models/Thinking-with-Models/hw1/',
#         nlogo_command='java -Xmx1024m -Dfile.encoding=UTF-8 -cp NetLogo.jar ' +
#         'org.nlogo.headless.Main --model "C:/Users/Joel/Dropbox/Research/' +
#         'Philosophy of Science/Thinking with Models/Thinking-with-Models/' +
#         'hw1/hw_1_joelm.nlogo" --setup-file "C:/Users/Joel/Dropbox/' +
#         'Research/Philosophy of Science/Thinking with Models/' +
#         'Thinking-with-Models/hw1/hw_1_grader.xml" --experiment step1 ' +
#         '--table "C:/Users/Joel/Dropbox/Research/Philosophy of Science/' +
#         'Thinking with Models/Thinking-with-Models/hw1/'):
#     '''
#     
#     Args:
#         hw_num (int): The homework number.
#         prob_num (int): The problem number.
#         main_dir (str): The name of the primary directory, which should contain
#             student and answer nlogo files, and to which the script and csv
#             files will be written.
#     Returns:
#         bool: True if successful, False otherwise.
#     '''
#     # Assemble the NetLogo command to be run for each student nlogo file. The
#     # command is based on the main_dir, hw_num, and prob_num, and is complete
#     # except for the student pennkey on the --model parameter, since this will
#     # be different for each student.
#     nlogo_command='java -Xmx1024m -Dfile.encoding=UTF-8 -cp NetLogo.jar ' + \
#         'org.nlogo.headless.Main --model "' + main_dir + 'hw' + hw_num + '_{0}.nlogo" --setup-file "' + main_dir + 'hw' + hw_num + '_experiments.xml" --experiment prob' + prob_num + \
#         ' --table "' + main_dir + 'hw' + hw_num + '_{0}_' + prob_num + '.csv"\n'
# #     print nlogo_command
#     # Open the script file for writing.
#     script = open(main_dir + 'script.bat', 'w')
# #     hws = [h for h in os.listdir(dirname) ]
# #     write_experiment_file(nlogo_file, exp_file)
# #     print __file__
#     # This may need some alterations to be able to handle unix filesystems. -- \\
#     script.write('python ' + __file__[0:-15].replace('\\', '/') + 
#             'create_experiments.py\n')
# #     print __file__, 'python ' + __file__[0:-15] + 'create_experiments.py\n'
#     # Save the current directory for convenience.
#     script.write('set cur_dir=%cd%\n')
#     script.write('cd C:/Program Files (x86)/NetLogo 5.1.0\n')
#     script.write(nlogo_command.format('answers'))
#     for h in os.listdir(main_dir):
#         if 'hw' + str(hw_num) in h and '.nlogo' in h and 'answers' not in h:
#             student_name = h[4:h.find('.nlogo')]
# #             print nlogo_command.format(student_name)
#             script.write(nlogo_command.format(student_name))
#     script.write('python --version\n')
#     # Reset to the initial current directory for convenience.
#     script.write('cd %cur_dir%')
#     script.close()
#     return True

def main(argv):
    '''The main method runs the run_grading_commands function.
    
    This method uses argument values given in the command line and parses them
    to decide which functionality to run.
    
    Args:
        argv (list): The list of system arguments passed through the terminal.
            See module docstring or type 'python autograde.py -h' for 
            documentation on which flags are valid.
    '''
# #     write_grading_script(argv[0], argv[1])
#     run_grading_commands(argv[0], argv[1], 
#         main_dir='/home/joel/Dropbox/Research/Philosophy of Science/' + 
#         'Thinking with Models/Thinking-with-Models/autograde_sample/', 
#         nlogo_dir='/opt/NetLogo/netlogo-5.0.5')
# #     print int(argv[0]), int(argv[1])
    # Initialize values for function call
    hw_num, prob_num, main_dir, netlogo_dir = -1, -1, -1, -1
    # Get the terminal flags from argv.
    try:
        opts, args =  getopt.getopt(argv, 'hn:p:d:m:', ['help', 'hw_number=', 
                'prob_number=', 'main_dir=', 'netlogo_dir='])
    # If error, print the docstring for this script.
    except: 
        print(__doc__)
        sys.exit(2)
#     print opts
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(__doc__)
            sys.exit()
        elif opt in ('-n', '--hw_number'):
            hw_num = arg
        elif opt in ('-p', '--prob_number'):
            prob_num = arg
        elif opt in ('-m', '--main_dir'):
            main_dir = arg
        elif opt in ('-d', '--netlogo_dir'):
            netlogo_dir = arg
    for arg in args:
        pass
    if hw_num == -1 or prob_num == -1:
#         print hw_num, prob_num, main_dir, netlogo_dir
        print "Please use all required flags.\n"
        print(__doc__)
    else:
        return run_grading_commands(hw_num, prob_num, main_dir, netlogo_dir)

if __name__ == '__main__':
    # Runs the main method if run as main.
    main(sys.argv[1:])