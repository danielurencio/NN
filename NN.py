from __future__ import division
import numpy as np
import pandas
import matplotlib.pyplot as plt

class NN(object):
    def __init__(self,data):
        self.data = data#.values
	self.X = 0
	self.y = 0
	self.W = 0
        self.lags = 3
	self.randX = 0
	self.randY = 0
        self.arq = {}
        self.mean = []
        self.std = []

    def normalize(self,x):
        X = []
        n = x.shape[1]
        for i in range(n):
            mean = np.mean(x[:,i]); self.mean.append(mean);
            std = np.std(x[:,i]); self.std.append(std);
            a = ( x[:,i] - mean ) / std
            a = a.reshape(a.shape[0],1)
            X.append(a)
        return np.hstack((X))

    def create_dataset(self,denormalized):
        dataX, dataY = [], []
        for i in range(len(self.data)-self.lags-1):
            a = self.data[i:(i+self.lags), 0]
            dataX.append(a)
            dataY.append(self.data[i + self.lags, 0])

        self.X = np.array(dataX)
        self.y = np.array(dataY)
        self.X = self.normalize(self.X)
        self.y = self.normalize(self.y.reshape((self.y.shape[0],1)))
        if(denormalized):
            return [ np.array(dataX), np.array(dataY).reshape(np.array(dataY).shape[0],1) ];

    def Weights(self,h):
        W = []
        W.append( 2*np.random.random(( self.X.shape[1], h[0] )) - 1 )
        for i,val in enumerate(h):
            if(i < len(h) - 1):
                W.append( 2*np.random.random(( h[i], h[i+1] )) - 1 )
        W.append( 2*np.random.random(( h[len(h) - 1], self.y.shape[1] )) - 1 )
        self.W=W

    def sigmoid(self,x):
        return 1 / (1+np.exp(-x))

    def sigmoidPrime(self,z):
        return z * (1-z)

    def feed(self):
        A = []
        z = self.X.dot(self.W[0])
        A.append( self.sigmoid(z) )
        for i,val in enumerate(self.W):
            if( i != 0 and i != len(self.W)-1 ):
                z = A[i-1].dot(self.W[i])
                A.append( self.sigmoid(z) )
            if( i == len(self.W)-1 ):
                A.append( A[i-1].dot(self.W[i]) )
        return A
#        return ( A[len(A)-1] * nn.std[len(nn.std)-1] ) + nn.mean[len(nn.mean)-1];

    def Feed(self):
        A = []
        z = self.X.dot(self.W[0])
        A.append( self.sigmoid(z) )
        for i,val in enumerate(self.W):
            if( i != 0 and i != len(self.W)-1 ):
                z = A[i-1].dot(self.W[i])
                A.append( self.sigmoid(z) )
            if( i == len(self.W)-1 ):
                A.append( A[i-1].dot(self.W[i]) )
#        return A
        return ( A[len(A)-1] * nn.std[len(nn.std)-1] ) + nn.mean[len(nn.mean)-1];

    def Deltas(self,A):
        index = len(A) - 1
        maxC = len(A) - 1
        deltas = [[] for _ in range(len(A))]
        while( index > -1 ):
            if(index == maxC):
                error = A[index] - self.y
                delta = error
                deltas[index] = delta
            else:
                error = deltas[index+1].dot(self.W[index+1].T)
                delta = error * self.sigmoidPrime(A[index])
                deltas[index] = delta
            index -= 1
        return deltas

    def updateWeights(self,A,deltas,alpha):
        gradients = []
        a = A[:]
        a.insert(0,self.X)
        for i in range(len(a) - 1):
            self.W[i] -= alpha * a[i].T.dot(deltas[i])
#            gradients.append(self.W[i])
#        return gradients

    def backprop(self,i,alpha):
        A = self.feed()
        deltas = self.Deltas(A)
        W = self.updateWeights(A,deltas,alpha)
        if (i%10000 == 0):
            print(i,np.sum( (A[len(A)-1]-self.y) **2 ))

    def train(self,iter,alpha):
        for i in xrange(iter):
            self.backprop(i,alpha)

    def arch(self,input,layers):
        self.lags = input
        self.create_dataset(0)
        self.Weights(layers)

    def graf(self):
        plt.plot(self.y)
        A = self.feed()
        plt.plot(A[len(A)-1])
        plt.show()

    def simpleFeed(self,data):
        A = []
        z = data.dot(self.W[0])
        A.append( self.sigmoid(z) )
        for i,val in enumerate(self.W):
            if( i != 0 and i != len(self.W)-1 ):
                z = A[i-1].dot(self.W[i])
                A.append( self.sigmoid(z) )
            if( i == len(self.W)-1 ):
                A.append( A[i-1].dot(self.W[i]) )
        return A;

    def simpleDeltas(self,A,Y):
        index = len(A) - 1
        maxC = len(A) - 1
        deltas = [[] for _ in range(len(A))]
        while( index > -1 ):
            if(index == maxC):
                error = A[index] - Y
                delta = error
                deltas[index] = delta
            else:
                error = deltas[index+1].dot(self.W[index+1].T)
                delta = error * self.sigmoidPrime(A[index])
                deltas[index] = delta
            index -= 1
        return deltas

    def SGD(self,alpha):
	self.randomData();
        for i in range( len(self.randX) ):
            A = self.simpleFeed(self.randX[i]);
            self.simpleBackprop(self.randX[i],A,self.randY[i],alpha);

    def cost(self):
        A = self.feed();
#	print( np.sum( (A[len(A)-1] - self.y ) ** 2 ) );
	return np.sum( (A[len(A)-1] - self.y ) ** 2 );


    def simpleBackprop(self,data,A,Y,alpha):
#        A = self.feed()
        deltas = self.simpleDeltas(A,Y)
        self.simpleUpdateWeights(data,A,deltas,alpha)
#        if (i%10000 == 0):
#            print(i,np.sum( (A[len(A)-1]-self.y) **2 ))

    def simpleUpdateWeights(self,data,A,deltas,alpha):
        gradients = []
        a = A[:]
        a.insert(0,data)
#        a.reshape(a.reshape(a.shape[0]),1);
        for i in range(len(a) - 1):
	    aa = a[i].reshape( 1, len(a[i]) );
	    delta = deltas[i].reshape( 1, len(deltas[i]) );
            self.W[i] -= alpha * aa.T.dot(delta)

    def randomData(self):
        DATA = np.column_stack((self.X,self.y))
        np.random.shuffle(DATA)
	self.randX = DATA[:,0:DATA.shape[1]-1]
	self.randY = DATA[:,DATA.shape[1]-1].reshape(len(DATA),1)

    def trainSGD(self,iter,alpha):
        costs = [];
        for i in range(iter):
            self.SGD(alpha);
            costs.append(self.cost());

        while self.cost() > np.round(np.min(costs))+1:
            self.SGD(iter);


    def predict(self,data):
        vals = []
        for i in range(len(data)):
            val = (data[i] - self.mean[i]) / self.std[i];
            vals.append(val);
        data = np.array(vals);
        A = []
        z = data.dot(self.W[0])
        A.append( self.sigmoid(z) )
        for i,val in enumerate(self.W):
            if( i != 0 and i != len(self.W)-1 ):
                z = A[i-1].dot(self.W[i])
                A.append( self.sigmoid(z) )
            if( i == len(self.W)-1 ):
                A.append( A[i-1].dot(self.W[i]) )
        return (A[len(A)-1] * self.std[len(self.std)-1] + nn.mean[len(self.mean)-1])[0];

    def difs(self,lag):
        self.lags = lag;
        arr = [];
        x = self.create_dataset(1)[0];
        for i in x:
            a = [];
            for j in range(len(i)):
                if( j != 0 ): a.append( i[len(i) - j - 1] - i[len(i) - j - 2] );
                if( j == len(i) - 1 ): arr.append(a);
        return arr;
