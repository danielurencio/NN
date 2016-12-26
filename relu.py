from __future__ import division
import numpy
import numpy as np
import pandas
import matplotlib.pyplot as plt


#dataframe = pandas.read_csv('international-airline-passengers.csv', usecols=[1], engine='python', skipfooter=3)
dataframe = pandas.read_csv("sales.csv")
dataset = dataframe.values
dataset = dataset.astype('float32')

#train_size = int(len(dataset) * 0.67)
#test_size = len(dataset) - train_size
#train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)


look_back = 24
X, y = create_dataset(dataset, look_back)
y = y.reshape(y.shape[0],1)
#testX, testY = create_dataset(test, look_back)

def sigmoid(x):
    return 1 / (1+np.exp(-x))


def sigmoidPrime(z):
    return z * (1-z)


def tanh(x):
    return np.tanh(x)


def tanhPrime(z):
    return 1 - tanh(z)**2


def Weights(x,h,y):
    W = []
    W.append( 2*np.random.random(( x.shape[1], h[0] )) - 1 )
    for i,val in enumerate(h):
        if(i < len(h) - 1):
            W.append( 2*np.random.random(( h[i], h[i+1] )) - 1 )
    W.append( 2*np.random.random(( h[len(h) - 1], y.shape[1] )) - 1 )
    return W


def feed(X,W):
    A = []
    A.append( sigmoid( X.dot(W[0]) ) )
    for i,val in enumerate(W):
        if( i != 0 and i != len(W)-1 ):
            A.append( sigmoid( A[i-1].dot(W[i]) ) )
	if( i == len(W)-1 ):
            A.append( A[i-1].dot(W[i]) )
    return A


def Deltas(A,W,y):
    index = len(A) - 1
    maxC = len(A) - 1
    deltas = [[] for _ in range(len(A))]
    while( index > -1 ):
        if(index == maxC):
            error = A[index] - y
            delta = error# * sigmoidPrime(A[index])
            deltas[index] = delta
        else:
            error = deltas[index+1].dot(W[index+1].T)
            delta = error * sigmoidPrime(A[index])
            deltas[index] = delta
        index -= 1
    return deltas


def updateWeights(X,W,A,deltas,alpha):
    gradients = []
    a = A[:]
    a.insert(0,X)
    for i in range(len(a) - 1):
        W[i] -= alpha * a[i].T.dot(deltas[i])
        gradients.append(W[i])
    return gradients


def normalize(x):
    X = []
    n = x.shape[1]
    for i in range(n):
        mean = np.mean(x[:,i])
        std = np.std(x[:,i])
        a = ( x[:,i] - mean ) / std
        a = a.reshape(a.shape[0],1)
        X.append(a)
    return np.hstack((X))


X = normalize(X)
y = normalize(y)
ones = np.ones(( X.shape[0], 1))
X = np.hstack((ones,X))
hidden=12

W = Weights(X,[hidden,hidden,hidden,hidden],y)
A = feed(X,W)

def backprop(X,y,W1,W2,i):
    A = feed(X,W)
    deltas=Deltas(A,W,y)
    W = updateWeights(X,W,A,deltas,0.001)
    if (i%10000 == 0):
        print(i,np.sum( (A[len(A)-1]-y) **2 ))


def train(iter):
    for i in xrange(iter):
        backprop(X,y,W1,W2,i)


def graf():
    plt.plot(y)
    plt.plot(A[len(A)-1])
    plt.show()


