python C:/Users/Joel/workspace/NetLogoHomeworkGrader/netlogohomeworkgrader/create_experiments.py
set cur_dir=%cd%
cd C:/Program Files (x86)/NetLogo 5.1.0
java -Xmx1024m -Dfile.encoding=UTF-8 -cp NetLogo.jar org.nlogo.headless.Main --model "C:/Users/Joel/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models/hw1/hw1_answers.nlogo" --setup-file "C:/Users/Joel/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models/hw1/hw1_experiments.xml" --experiment prob1 --table "C:/Users/Joel/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models/hw1/hw1_answers_1.csv"
java -Xmx1024m -Dfile.encoding=UTF-8 -cp NetLogo.jar org.nlogo.headless.Main --model "C:/Users/Joel/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models/hw1/hw1_studa.nlogo" --setup-file "C:/Users/Joel/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models/hw1/hw1_experiments.xml" --experiment prob1 --table "C:/Users/Joel/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models/hw1/hw1_studa_1.csv"
java -Xmx1024m -Dfile.encoding=UTF-8 -cp NetLogo.jar org.nlogo.headless.Main --model "C:/Users/Joel/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models/hw1/hw1_studb.nlogo" --setup-file "C:/Users/Joel/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models/hw1/hw1_experiments.xml" --experiment prob1 --table "C:/Users/Joel/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models/hw1/hw1_studb_1.csv"
java -Xmx1024m -Dfile.encoding=UTF-8 -cp NetLogo.jar org.nlogo.headless.Main --model "C:/Users/Joel/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models/hw1/hw1_studc.nlogo" --setup-file "C:/Users/Joel/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models/hw1/hw1_experiments.xml" --experiment prob1 --table "C:/Users/Joel/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models/hw1/hw1_studc_1.csv"
python --version
cd %cur_dir%