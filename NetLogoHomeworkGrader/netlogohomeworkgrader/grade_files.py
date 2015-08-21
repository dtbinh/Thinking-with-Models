'''grade_files.py

This is a module containing functions to grade csv output files by comparing 
their values to a given answer csv.

Created on Aug 17, 2015

@author: Joel McCarthy
'''

import sys
import csv
import ast

def grade_problem(ans_path, stud_path):
    '''Grades a single csv file against the given answer file.
    
    This method checks each cell of the student file against the answer file
    and outputs a table of booleans.
    
    args:
        ans_path (str): The path of the answer csv file.
        stud_path (str): The path of the csv file to be graded.
    returns:
        list or int: A 2-d array with the same dimensions as the answer file 
            containing boolean values (and lists of boolean values where lists
            are found in the original file) denoting whether each value is 
            correct or not. If there is an IOerror, returns 0.
    '''
    try:
        with open(ans_path) as ans, open(stud_path) as stud:
            # Skip first 6 lines (Not part of table).
            for _ in range(6):
                ans.readline()
                stud.readline()
            # Get cvs readers.
            ans_reader = csv.reader(ans)
            stud_reader = csv.reader(stud)
            # Store the list of the variable names.
            var_names = ans.next()
            # Make sure that both files have the same variables in the same order.
            if var_names != stud.next(): 
                print "Incorrect csv files: wrong variable names."
                return False
            # Check the rows against eachother and record a table of the results.
            grade_table = [[vals_equal(ans_val, stud_val) for ans_val, stud_val 
                    in zip(ans_row, stud_row)] 
                    for ans_row, stud_row in zip(ans_reader, stud_reader)]  
            return grade_table  
    # If fails, return 0 as a grade.
    except:
        print "Problem with grading csv files."
        print sys.exc_info()
        return 0

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

def get_problem_grade(grade_table):
    '''Returns a grade out of ten, given a grade_table
    
    This method returns a 0 if the file did not run at all, and a 3 or above if
    it did run. The remaining 7 points are added in direct proportion to the
    percentage of correct values in the problem.
    
    Note: This grading system will likely need significant fine-tuning in the
    future (ie. weight parts of the problem differently, nonlinear
    relationship, etc.).
    
    args:
        grade_table (list): A two dimensional list of booleans. The output of
            grade_problem.
    returns:
        int: A grade between 0 and 10 (inclusive).
    '''
    if grade_table == 0: return 0
    num_correct = 0
    total_num = 0
    for row in grade_table:
        for cell in row:
            if type(cell) is list:
                for v in cell:
                    num_correct += v
                    total_num += 1
            else:
                num_correct += cell
                total_num += 1
    percent_correct = num_correct/total_num
    return round(3 + (percent_correct * 7), 1)