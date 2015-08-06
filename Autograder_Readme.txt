The Autograder is currently located in Hw_1_tests.py. It is run in python, and requires the py4j module in order to connect to a python-compatible server which is hosted in java with the file src/py2NetLogo/NetLogoBridge.java. Running this java file will host a NetLogo server, and the python file will create a connection in order to control the NetLogo headless instance.

The following python methods are designed for front-end use:
record_hw_answers(hw_number, problem_number=-1, directory=default_dir)
The default value for problem_number records all problems and default directory value is one I am currently using for testing. This creates some files called answers_<hw number>_<problem>_<file number>.txt which hold the values needed for homework grading.
check_hw_answers(hw_number, directory=default_dir)
Assuming that the current directory already contains these generated answer files, this method will search for all student homework files of the given number in the given directory and grade them by the answer file values.
