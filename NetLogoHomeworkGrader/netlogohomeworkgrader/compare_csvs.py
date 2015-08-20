'''
Created on Aug 17, 2015

@author: Joel
'''

import sys
import csv
from Tkinter import Tk
from tkFileDialog import askdirectory
import ast

def grade_prob(dirname, hw_num, hw_prob, student_name='studa'):
    '''
    
    '''
    with open(dirname + '/hw1_answers_1.csv') as ans, \
            open(dirname + '/hw1_' + student_name + '_1.csv') as stud:
        for _ in range(6):
            ans.readline()
            stud.readline()
        ans_reader = csv.reader(ans)
        stud_reader = csv.reader(stud)
        # Store the list of the variable names.
        var_names = ans.next()
        # Make sure that both files have the same variables in the same order.
        if var_names != stud.next(): 
            print "Incorrect csv files: wrong variable names."
            return False
#         print ans_reader
        # Check the rows against eachother and record a table of the results.
        grade_table = [[vals_equal(ans_val, stud_val) for ans_val, stud_val 
                in zip(ans_row, stud_row)] 
                for ans_row, stud_row in zip(ans_reader, stud_reader)]
#         for ans_row in ans_reader, stud_row in stud_reader:
#             pass
#         for i, ans_row in enumerate(ans_reader):
#             stud_row = stud_reader.next()
# #             print i, ans_row, stud_row
#             grade_row = []
#             for cell in 
#                 
#             grade_table.append(grade_row)
        
    return grade_table

# Will probably want to add some relative error tolerance in here, ie. let 1000000001 == 1000000000
def vals_equal(ans_val, stud_val):
    '''This checks if two values are within tolerance of each other.
    
    This method can handle values that are given in string representation form.
    It attempts to convert them to the proper python type before comparing; if
    this fails, it compares them as strings. This method can also be used 
    recursively, to handle a value in the form of a list of values; for this
    type, a list of corresponding boolean values is returned.
    
    Args:
        ans_val (str): The answer value
        stud_val (str): The student value
    Returns:
        bool or list of bool: True if equal, False if not; A list of boolean
            values is returned when two lists are passed in for comparison.
    '''
    # First convert the values from string representations to their correct 
    # python types. A value which throws an error is either not a string 
    # representation of another type or not a string at all and so should 
    # remain the same.
    try: ans_val = ast.literal_eval(ans_val)
    except: pass 
    try: stud_val = ast.literal_eval(stud_val)
    except: pass
    # Make sure values are of the same type.
    if type(ans_val) != type(stud_val): return False
    # Return equality value according to type.
    if type(ans_val) is int:
        # Integers return normal equality comparison (for now -- see above comment).
        return ans_val == stud_val
    elif type(ans_val) is float:
        # Floats are equal if they are the same to 3 decimal places.
        return round(ans_val, 3) == round(stud_val, 3)
    elif type(ans_val) is list:
        # Make sure lists are of same length.
        if len(ans_val) != len(stud_val): return False
        # Lists return a list containing the value of their comparisons.
        return [vals_equal(ans_v, stud_v) 
                for ans_v, stud_v in zip(ans_val, stud_val)]
    elif type(ans_val) is str:
        # Strings return normal string comparison.
        return ans_val == stud_val

def grade_student_hw():
    pass

def main(argv):
    '''
    
    '''
    Tk().withdraw()
    dirname = askdirectory(
            initialdir='C:/Users/Joel/Dropbox/Research/' +
            'Philosophy of Science/Thinking with Models/' +
            'Thinking-with-Models/hw1', 
            title='Choose a directory containing homework and answer files.')
#     dirname = 'C:/Users/Joel/Dropbox/Research/Philosophy of Science/' + \
#             'Thinking with Models/Thinking-with-Models/hw1'
    print dirname
    print grade_prob(dirname, 1, 1)

if __name__ == '__main__':
    # Calls the main method if run as main.
    main(sys.argv[1:])