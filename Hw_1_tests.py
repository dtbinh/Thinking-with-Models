from py4j.java_gateway import JavaGateway
import matplotlib.pyplot as plt
from os import listdir

# Global variables
data_fields = {}

# def Setup data_fields
def setup():
    global data_fields 
    data_fields = {
            '1 3' : {'global' : ('min-pxcor', 'max-pxcor', 'min-pycor', 'max-pycor'), 
            'turtle' : ('color', 'heading', 'xcor', 'ycor'), 'patch' : ('pcolor', )}
            }

# def run_model(bridge, density, steps):
def test1(bridge):
    '''
    Run the forest fire model, and return the number of trees burned.
     
    Args:
        bridge: The NetLogoBridge Java object
        density: Integer density percent, from 0 to 100
        steps: How many steps to run 
     
    Returns:
        The number of trees burned, as a float.
    '''
    # bridge.command("set density " + str(density))
    # bridge.command("setup")
    # bridge.command("repeat " + str(steps) + " [go]")
    bridge.command("setup1")
    bridge.command("go1")
    # return "fuck you"
    return bridge.report("[pycor] of turtle 0", "d") == 10.0

def test2(bridge):
    '''

    '''
    passed = True
    bridge.command("setup2")
    passed = (passed and bridge.report("count turtles", "d") == 4 and
            bridge.report("[count turtles-here] of patch 10 10", "d") == 1 and
            bridge.report("[count turtles-here] of patch -10 10", "d") == 1 and
            bridge.report("[count turtles-here] of patch 10 -10", "d") == 1 and
            bridge.report("[count turtles-here] of patch -10 -10", "d") == 1)
    # Need to check headings too
    for i in range(9):
        bridge.command("go2")
        passed = (passed and bridge.report("count turtles", "d") == 4 and
                bridge.report(
                "[count turtles-here] of patch {0} {0}".format(9-i), "d") == 1 and
                bridge.report(
                "[count turtles-here] of patch -{0} {0}".format(9-i), "d") == 1 and
                bridge.report(
                "[count turtles-here] of patch {0} -{0}".format(9-i), "d") == 1 and
                bridge.report(
                "[count turtles-here] of patch -{0} -{0}".format(9-i), "d") == 1)
        if not passed: print 'failure: ', i
        # print bridge.report("[xcor] of turtle 0", "d"), bridge.report("[ycor] of turtle 0", "d")
    bridge.command("go2")
    passed = (passed and bridge.report("count turtles", "d") == 4 and
            bridge.report("[count turtles-here] of patch 0 0", "d") == 4)
    return passed

def test3(bridge, student_name):
    passed = True
    bridge.command('export-world \
            (word "{0}-1-3-" date-and-time ".csv")'.format(student_name))
    return passed

def roughly_equal(val1, val2, error=.01):
    return abs(val1-val2) < error

# look into writing to a csv (doesn't matter too much)
# fix so report only needs one parameter
def write_values(bridge, hw_number, problem_number, record_number):
    # print data_fields
    # Open the write file and the correct dictionary of fields to write.
    answers = open('answers_{0}_{1}_{2}.txt'.format(hw_number, problem_number, record_number), 
            'w')
    fields = data_fields['{0} {1}'.format(hw_number, problem_number)]
    # Get necessary reporting info.
    num_turtles = int(bridge.report('count turtles', 'd'))
    min_pxcor = int(bridge.report('min-pxcor', 'd'))
    min_pycor = int(bridge.report('min-pycor', 'd'))
    max_pxcor = int(bridge.report('max-pxcor', 'd'))
    max_pycor = int(bridge.report('max-pycor', 'd'))
    # Write in globals.
    for f in fields['global']:
        # print f
        # w = bridge.report('{0}'.format(f), 'd')
        # print w, type(w)
        answers.write(str(bridge.report('{0}'.format(f), 'd'))+', ')
    answers.write('\n')
    # Write in turtle variables
    for i in range(num_turtles):
        for f in fields['turtle']:
            answers.write(str(bridge.report('[{0}] of turtle {1}'.format(f, i), 'd'))+', ')
        answers.write('\n')
    # Write in patch variables
    for x in range(min_pxcor, max_pxcor):
        for y in range(min_pycor, max_pycor):
            for f in fields['patch']:
                answers.write(str(bridge.report('[{0}] of patch {1} {2}'.format(f, x, y), 'd'))+', ')
            answers.write('\n')
    answers.close()

# The procedure for when to run what and record what -- will want to make this a field.
def record_answers(bridge, hw_number):
    bridge.command('random-seed 17638974') # used nlogo's new-seed to get
    bridge.command('setup3')
    write_values(bridge, hw_number, 3, 0)
    bridge.command('repeat 50 [go3]')
    write_values(bridge, hw_number, 3, 1)

def check_values(bridge, hw_number, problem_number, record_number):
    passed = True
    # Open the write file and the correct dictionary of fields to write.
    answers = open('answers_{0}_{1}_{2}.txt'.format(hw_number, problem_number, record_number), 
            'r')
    fields = data_fields['{0} {1}'.format(hw_number, problem_number)]
    # Get necessary reporting info.
    num_turtles = int(bridge.report('count turtles', 'd'))
    min_pxcor = int(bridge.report('min-pxcor', 'd'))
    min_pycor = int(bridge.report('min-pycor', 'd'))
    max_pxcor = int(bridge.report('max-pxcor', 'd'))
    max_pycor = int(bridge.report('max-pycor', 'd'))
    # Write in globals.
    g = answers.readline().strip(' ,\n').split(', ')
    # print g
    for i, f in enumerate(fields['global']):
        # print f
        # w = bridge.report('{0}'.format(f), 'd')
        # print w, type(w)
        passed = passed and str(bridge.report('{0}'.format(f), 'd')) == g[i]
        # if passed == False: print g
    # answers.write('\n')
    # Write in turtle variables
    for i in range(num_turtles):
        t = answers.readline().strip(' ,\n').split(', ')
        # print t
        for j, f in enumerate(fields['turtle']):
            c = str(bridge.report('[{0}] of turtle {1}'.format(f, i), 'd'))
            # print f, c
            passed = passed and c == t[j]
            # if passed == False: print 't', t[i], 'c', c
        # answers.write('\n')
    # # Write in patch variables
    for x in range(min_pxcor, max_pxcor):
        for y in range(min_pycor, max_pycor):
            p = answers.readline().strip(' ,\n').split(', ')
            for i, f in enumerate(fields['patch']):
                c = str(bridge.report('[{0}] of patch {1} {2}'.format(f, x, y), 'd'))
                passed = passed and c == p[i]
                # if passed == False: print p
            # answers.write('\n')
    answers.close()
    return passed

def check_answers(bridge, hw_number):
    passes = []
    bridge.command('random-seed 17638974') # need to make seed a global
    bridge.command('setup3')
    passes.append(check_values(bridge, hw_number, 3, 0))
    bridge.command('repeat 50 [go3]')
    passes.append(check_values(bridge, hw_number, 3, 1))
    return passes

def run_tests(directory): 
    '''
    Run all the tests for each homework file in the directory.

    Args:
        directory: The directory in which to find the .nlogo files.

    Returns:
        A list of each student's performance on each test.
    '''
    gw = JavaGateway() # Create a new gateway connection.
    bridge = gw.entry_point # Create the actual NetLogoBridge object.

    setup()

    # Path to directory with hw_1 files.
    hw_1_directory = ("/home/joel/Dropbox/Research/Philosophy of Science/" +
            "Thinking with Models/Thinking-with-Models/")
    hw_1_files = [x for x in listdir(hw_1_directory) 
            if "hw_1_" in x and ".nlogo" in x]
    # Do each student one by one.
    for f in hw_1_files:
    # print hw_1_files[0], hw_1_directory + hw_1_files[0]
        # Open the model file.
        student_name = f[f.rindex('_')+1:f.rindex('.')]
        bridge.openModel(hw_1_directory + f)

        # Will need some error control in here
        # Run the necessary steps and export the world 

        # 
        # bridge.command('setup3')
        # write_values(bridge, 1, 3, 0)

        # record_answers(bridge, 1)
        print check_answers(bridge, 1)


        # print "Student: ", student_name
        # print "1: ", test1(bridge)
        # print "2: ", test2(bridge)
        # print "3: ", test3(bridge, student_name)

    # Dispose of the thread.
    bridge.dispose()

    return 

    # for f in hw_1_files:
    #     bridge.openModel(hw_1_directory + f)


    # burned_trees = [run_model(bridge, i, 100) for i in range(0,100)]
    # fig, ax = plt.subplots(figsize=(8,6))
    # ax.grid(True)
    # ax.set_xlabel("% Density")
    # ax.set_ylabel("# of Trees Burned")
    # plt.plot(burned_trees, linewidth=2)
    # plt.show()