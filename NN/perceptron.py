import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sig_der(x):
    return x * (1 - x)


inputs = np.array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])

output = np.array([[0, 1, 1, 0]]).T
# sigmoid'=x(1-x)
# adjust weights=err*in*sig'
def train(iter):
    np.random.seed(1)
    weights = 2 * np.random.random((3, 1)) - 1
    print("weights are :\n", weights)
    for i in range(iter):
        outs = sigmoid(np.dot(inputs, weights))
        err = output - outs
        adj = err * sig_der(outs)
        weights += np.dot(inputs.T, adj)
    print("outputs: \n", outs)
    print("weights after train:\n", weights)


if __name__ == "__main__":
    i = input("enter number of training sessions")
    train(int(i))
