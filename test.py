import numpy as np

def sigmoid(x):
    return 1 / ( 1 + np.exp(-x) )

def sigmoidPrime(z):
    return z * (1-z)

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
        if( i != 0 ):
            A.append( sigmoid( A[i-1].dot(W[i]) ) )
    return A

def Deltas(A,W,y):
    index = len(A) - 1
    maxC = len(A) - 1
    deltas = [[] for _ in range(len(A))]
    while( index > -1 ):
        if(index == maxC):
            error = A[index] - y
            delta = error * sigmoidPrime(A[index])
            deltas[index] = delta
        else:
            error = deltas[index+1].dot(W[index+1].T)
            delta = error * sigmoidPrime(A[index])
            deltas[index] = delta
        index -= 1
    return deltas

def updateWeights(X,W,A,deltas):
    gradients = []
    a = A[:]
    a.insert(0,X)
    for i in range(len(a) - 1):
        W[i]-=a[i].T.dot(deltas[i])
        gradients.append(W[i])
    return gradients
 

X = np.array([ [0,0],[0,1],[1,0],[1,1] ])
y = np.array([ [0,1,1,0] ]).T
W = Weights(X,[4,4],y)
A = feed(X,W)

for i in range(60000):
    A = feed(X,W)
    deltas = Deltas(A,W,y)
    W = updateWeights(X,W,A,deltas)
