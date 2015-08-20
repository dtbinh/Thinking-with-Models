from py4j.java_gateway import JavaGateway
import matplotlib.pyplot as plt
from os import listdir

# Global variables:
# The fields to record/check for each homework number and problem.
data_fields = {
        1 : { 
        1 : {'global' : (), 'turtle' : ('heading', 'xcor', 'ycor'), 
        'patch' : ('pcolor', )},
        2 : {'global' : (), 'turtle' : ('color', 'heading', 'xcor', 
        'ycor'), 'patch' : ('pcolor', )},
        3 : {'global' : (), 'turtle' : ('color', 'heading', 'xcor', 
        'ycor'), 'patch' : ('pcolor', )}
        }
        }
# The recording/checking order for each homework problem.
problem_order = {
        1 : { 1 : ['setup1', '*', 'go1', '*'],
        2 : ['setup2', '*', 'repeat 10 [go2]', '*'],
        3 : ['setup3', '*', 'repeat 50 [go3]', '*'] }
        }
# Default read/write directory
default_dir = ("/home/joel/Dropbox/Research/Philosophy of Science/" + 
        "Thinking with Models/Thinking-with-Models/")

def roughly_equal(val1, val2, error=.01):
    '''
    Checks whether two numbers are equal within an error margin.
    Args:
        val1: the first value
        val2: the second value
        error: the allowed error margin (default .01)
    Returns:
        A boolean which is true if the numbers are within the margin
    '''
    return abs(val1-val2) < error

def write_values(bridge, hw_number, problem_number, record_number):
    '''
    Record the values given in data_fields from a given open model.
    Args:
        bridge: The NetLogo Java object (must have an open model)
        hw_number: the homework number
        problem_number: the problem number
        record_number: the number of the file for this homework and problem
    '''
    # Open the write file and the correct dictionary of fields to write.
    answers = open('answers_{0}_{1}_{2}.txt'.format(hw_number, problem_number, 
            record_number), 'w')
    fields = data_fields[hw_number][problem_number]
    # Get necessary reporting info.
    num_turtles = int(bridge.report('count turtles'))
    min_pxcor = int(bridge.report('min-pxcor'))
    min_pycor = int(bridge.report('min-pycor'))
    max_pxcor = int(bridge.report('max-pxcor'))
    max_pycor = int(bridge.report('max-pycor'))
    # Write in globals.
    for f in fields['global']:
        answers.write(str(bridge.report('{0}'.format(f)))+', ')
    answers.write('\n')
    # Write in turtle variables.
    for i in range(num_turtles):
        for f in fields['turtle']:
            answers.write(str(bridge.report(
                    '[{0}] of turtle {1}'.format(f, i)))+', ')
        answers.write('\n')
    # Write in patch variables.
    for x in range(min_pxcor, max_pxcor):
        for y in range(min_pycor, max_pycor):
            for f in fields['patch']:
                answers.write(str(bridge.report(
                        '[{0}] of patch {1} {2}'.format(f, x, y)))+', ')
            answers.write('\n')
    # Close the file.
    answers.close()

def record_problem_answers(bridge, hw_number, problem_number):
    '''
    Helper method that records the necessary .txt answer files for the given 
    homework problem.
    Args:
        bridge: the open NetLogo java file with open model
        hw_number: the hw number
        problem_number: the hw problem number (default -1 records all problems)
    '''
    # Seed the model (used nlogo's new-seed to get)
    bridge.command('random-seed 17638974') 
    # Counter for the answer files
    record_number = 1
    for order in problem_order[hw_number][problem_number]:
        if order == '*':
            write_values(bridge, hw_number, problem_number, record_number)
            record_number += 1
        else:
            bridge.command(order)

def record_hw_answers(hw_number, problem_number=-1, directory=default_dir):
    '''
    Records the necessary .txt answer files for the given homework number
    or problem.
    Args:
        hw_number: the hw number
        problem_number: the hw problem number (default -1 records all problems)
        directory: the directory with the answer .nlogo file
    '''
    # Create a new gateway connection.
    gw = JavaGateway() 
    # Create the actual NetLogoBridge object and open answer model.
    bridge = gw.entry_point
    bridge.openModel(directory+'hw_{0}_answers.nlogo'.format(hw_number))
    # Record the answers for either all the problems (-1) or the given one.
    if problem_number == -1:
        for prob in range(len(data_fields[hw_number])):
            record_problem_answers(bridge, hw_number, prob+1)
            bridge.command('ca')
    else:
        record_problem_answers(bridge, hw_number, problem_number)

def check_values(bridge, hw_number, problem_number, record_number):
    '''
    Check the values of this model against the given answer file.
    Args:
        bridge: a NetLogo java file with open model
        hw_number: the homework number
        problem_number: the problem number
        record_number: the number of the file for this hw and problem
    Returns:
        A boolean which is true if the values are all the same as the answers
    '''
    # Set boolean for pass condition
    passed = True
    # Open the answer file and the correct dictionary of fields to write.
    answers = open('answers_{0}_{1}_{2}.txt'.format(hw_number, problem_number, 
        record_number), 'r')
    fields = data_fields[hw_number][problem_number]
    # Get necessary checking info.
    num_turtles = int(bridge.report('count turtles'))
    min_pxcor = int(bridge.report('min-pxcor'))
    min_pycor = int(bridge.report('min-pycor'))
    max_pxcor = int(bridge.report('max-pxcor'))
    max_pycor = int(bridge.report('max-pycor'))
    # Read in answer line and check globals.
    g = answers.readline().strip(' ,\n').split(', ')
    for i, f in enumerate(fields['global']):
        passed = passed and str(bridge.report('{0}'.format(f))) == g[i]
    # Check turtle variables, reading lines one turtle at a time.
    for i in range(num_turtles):
        ans = answers.readline().strip(' ,\n').split(', ')
        for j, f in enumerate(fields['turtle']):
            val = str(bridge.report('[{0}] of turtle {1}'.format(f, i)))
            passed = passed and val == ans[j]
    # Check patch variables, reading lines one patch at a time.
    for x in range(min_pxcor, max_pxcor):
        for y in range(min_pycor, max_pycor):
            p = answers.readline().strip(' ,\n').split(', ')
            for i, f in enumerate(fields['patch']):
                c = str(bridge.report('[{0}] of patch {1} {2}'.format(f, x, y)))
                passed = passed and c == p[i]
    # Close the answer file.
    answers.close()
    # Return true if all values were equal.
    return passed

def check_problem_answers(bridge, hw_number, problem_number):
    '''
    Helper method that checks the answers for a specific problem.
    Args:
    Returns:
    '''
    # Set up the passed variable
    passed = []
    # Seed the model (used nlogo's new-seed to get)
    bridge.command('random-seed 17638974') 
    # Counter for the answer files
    record_number = 1
    for order in problem_order[hw_number][problem_number]:
        if order == '*':
            passed.append(check_values(
                    bridge, hw_number, problem_number, record_number))
            record_number += 1
        else:
            bridge.command(order)
    return passed

def check_hw_answers(hw_number, directory=default_dir): 
    '''
    Run all the tests for each student homework file in the directory.
    Args:
        directory: The directory in which to find the .nlogo files
    Returns:
        A list of each student's performance on each problem.
    '''
    # Create a new gateway connection.
    gw = JavaGateway() 
    # Create the actual NetLogoBridge object.
    bridge = gw.entry_point 

    # Get a list of all the homework files in the directory and store grades.
    hw_files = [x for x in listdir(directory) 
            if "hw_{0}_".format(hw_number) in x and ".nlogo" in x 
            and not 'answers' in x]
    hw_grade = {}
    # Check each student's file one by one.
    for f in hw_files:
        # Get the student's name and open the model file.
        student_name = f[f.rindex('_')+1:f.rindex('.')]
        bridge.openModel(directory + f)
        # Check each problem.
        student_grades = {}
        for i in range(len(data_fields[hw_number])):
            student_grades[i+1] = check_problem_answers(
                    bridge, hw_number, i+1)
        hw_grade[student_name] = student_grades
    # Dispose of the thread.
    bridge.dispose()
    # Return the grades for the homework as a dictionary.
    return hw_grade