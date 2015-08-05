# Assuming in directory ~/Dropbox/Research/Philosophy of Science/Thinking with Models/Thinking-with-Models

# Compiles the file, with classpath and destination folder.
javac -cp .:/home/joel/anaconda/share/py4j/py4j0.8.2.1.jar:/opt/NetLogo/netlogo-5.0.5/NetLogo.jar -d bin/ src/py2NetLogo/NetLogoBridge.java
# Runs the output class file.
java -cp .:/home/joel/anaconda/share/py4j/py4j0.8.2.1.jar:/opt/NetLogo/netlogo-5.0.5/NetLogo.jar:./bin py2NetLogo.NetLogoBridge
