from pymongo import MongoClient
from NN import NN
import pandas
import sys
import numpy as np

#arg = sys.argv[1].split(",");
#arg = [float(i) for i in arg]
#arg = np.array((arg)).reshape(len(arg),1);
#print arg.shape;
#nn = NN(arg)
#nn.arch(5,[5]);

col = MongoClient("mongodb://localhost:27017").fx.EURUSD;
counter = 0;
zeros = np.zeros((3000,1));

nn = NN(zeros);
nn.arch(5,[5]);

for i in col.find():
#    print counter;
    counter += 1;
    if counter == 3000:
        
        counter = 0;
        continue
