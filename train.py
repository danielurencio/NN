import numpy as np

def sigmoid(x):
    return 1 / ( 1 + np.exp(-x) )

def sigmoidPrime(z):
    return z * ( 1 - z )

X = np.array([ [0,0,1],[0,1,1],[1,0,1],[1,1,1] ]);
y = np.array([ [0,1,1,0] ]).T
hidden = 4

W1 = 2*np.random.random((X.shape[1],hidden)) - 1
W2 = 2*np.random.random((hidden,y.shape[1])) - 1

z1 = X.dot(W1)
a1 = sigmoid(z1)
z2 = a1.dot(W2)
a2 = sigmoid(z2)


def train(X,y,W1,W2):
    z1 = X.dot(W1)
    a1 = sigmoid(z1)
    z2 = a1.dot(W2)
    a2 = sigmoid(z2)
    a2_err = -1*(y - a2)
    a2_delta = a2_err * sigmoidPrime(a2)
    a1_err = a2_delta.dot(W2.T)
    a1_delta = a1_err * sigmoidPrime(a1)
    dJdW1 = X.T.dot(a1_delta)
    dJdW2 = a1.T.dot(a2_delta)
    W1 -= dJdW1
    W2 -= dJdW2

for i in xrange(100000):
    train(X,y,W1,W2)

