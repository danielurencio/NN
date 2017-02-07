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
data = np.random.random((1500,1));

nn = NN(data);
nn.arch(5,[5]);
mins = 0;
arr = ["",""];
steps = [15,30,45,0];
c = 0;

for i in col.find({ 'year':2009 }):
    arr = arr[1:];
    arr.append(i)
    if i["minutes"] != mins and i["minutes"] == steps[c]:
        c += 1;
        mins = i["minutes"];
#        print arr[0];
        data = data[:-1]
        data[0] = arr[0]["ask"]
	if c > len(steps) -1: c = 0;
#        nn = NN(data)
#        nn.arch(5,[5]);
#        while nn.cost() > 20:
#            nn.SGD(0.1);
#            print nn.cost()
#        print counter;
#        counter += 1;
        if counter == 1500: break
#            counter = 0;
#            print data[0]
#            nn = NN(data)
#            nn.arch(5,[5]);
    #        while nn.cost() > 20:
#            nn.SGD(0.01);
#            nn.graf();
#        continue
