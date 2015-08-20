'''
Created on Aug 18, 2015

@author: Joel
'''

import sys
import os
# from create_experiments import write_experiment_file

def write_grading_script(hw_num, prob_num,
        main_dir='C:/Users/Joel/Dropbox/Research/Philosophy of Science/' + 
        'Thinking with Models/Thinking-with-Models/hw1/',
        nlogo_command='java -Xmx1024m -Dfile.encoding=UTF-8 -cp NetLogo.jar ' +
        'org.nlogo.headless.Main --model "C:/Users/Joel/Dropbox/Research/' +
        'Philosophy of Science/Thinking with Models/Thinking-with-Models/' +
        'hw1/hw_1_joelm.nlogo" --setup-file "C:/Users/Joel/Dropbox/' +
        'Research/Philosophy of Science/Thinking with Models/' +
        'Thinking-with-Models/hw1/hw_1_grader.xml" --experiment step1 ' +
        '--table "C:/Users/Joel/Dropbox/Research/Philosophy of Science/' +
        'Thinking with Models/Thinking-with-Models/hw1/'):
    '''
    
    Args:
        hw_num (int): The homework number.
        prob_num (int): The problem number.
        main_dir (str): The name of the primary directory, which should contain
            student and answer nlogo files, and to which the script and csv
            files will be written.
    Returns:
        bool: True if successful, False otherwise.
    '''
    # Assemble the NetLogo command to be run for each student nlogo file. The
    # command is based on the main_dir, hw_num, and prob_num, and is complete
    # except for the student pennkey on the --model parameter, since this will
    # be different for each student.
    nlogo_command='java -Xmx1024m -Dfile.encoding=UTF-8 -cp NetLogo.jar ' + \
        'org.nlogo.headless.Main --model "' + main_dir + 'hw' + hw_num + '_{0}.nlogo" --setup-file "' + main_dir + 'hw' + hw_num + '_experiments.xml" --experiment prob' + prob_num + \
        ' --table "' + main_dir + 'hw' + hw_num + '_{0}_' + prob_num + '.csv"\n'
#     print nlogo_command
    # Open the script file for writing.
    script = open(main_dir + 'script.bat', 'w')
#     hws = [h for h in os.listdir(dirname) ]
#     write_experiment_file(nlogo_file, exp_file)
#     print __file__
    # This may need some alterations to be able to handle unix filesystems. -- \\
    script.write('python ' + __file__[0:-15].replace('\\', '/') + 
            'create_experiments.py\n')
#     print __file__, 'python ' + __file__[0:-15] + 'create_experiments.py\n'
    # Save the current directory for convenience.
    script.write('set cur_dir=%cd%\n')
    script.write('cd C:/Program Files (x86)/NetLogo 5.1.0\n')
    script.write(nlogo_command.format('answers'))
    for h in os.listdir(main_dir):
        if 'hw' + str(hw_num) in h and '.nlogo' in h and 'answers' not in h:
            student_name = h[4:h.find('.nlogo')]
#             print nlogo_command.format(student_name)
            script.write(nlogo_command.format(student_name))
    script.write('python --version\n')
    # Reset to the initial current directory for convenience.
    script.write('cd %cur_dir%')
    script.close()
    return True

def main(argv):
    '''The main method runs the write_script method.
    
    This method uses argument values for homework number and problem number and
    the defaults for directory paths.
    
    Args:
        argv (list): The list of system arguments passed through the terminal.
            The first two must be integers, corresponding to homework number
            and problem number, respectively.
    '''
    write_grading_script(argv[0], argv[1])
#     print int(argv[0]), int(argv[1])
    return True

if __name__ == '__main__':
    # Runs the main method if run as main.
    main(sys.argv[1:])