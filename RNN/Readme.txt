The code for machine learning based approach is written using Python 2.7.
The dependecies that are required are described as below

First download the Glove embedding from https://nlp.stanford.edu/projects/glove/, This is a very large file(closely 1GB).
Place this file inside of project path and give the path in code where I have commented.

The libraries used are Keras,Matplotlib and Numpy. You must have these dependencies in order to run the code.

The code takes time in running as it is running on 40 epochs and they can be changed from inside of the code.

The input file is in raw_sent1.txt which takes sentences as input and converts the data into vectors.
The file labels.txt contains manually annotated labels.

data_ops.py ha sthe code for cleaning the data. we cleaned the Xml file and converted into the text file

References:

For implementing this code I have referred https://github.com/keras-team/keras for learning about using pretrained vectors and deep learning model implementation using keras.

