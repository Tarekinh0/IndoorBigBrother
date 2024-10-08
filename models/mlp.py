# Support Vector Machine
# Maximize the margins between and the data points (the support vectors) 
# The boudary is a line when we have two variables (2D), it is a plane when we wave 3 variables (3D), etc.
# PS : The plane may not be a straight line
# When we have nD, we have nD hyperplanes
# Gamma: 
#   High Gamma, we only consider the support vectors that are close to the margin
#   Low Gamme: We alsoo consider the farthest support vectors
# Regularization:
#   High Regularization: We do not tolerate error, the line may be zigzaggy
#   Low Regularization: We accept that some may support vectors are on the wrong side of the margin line.

# Kernel: a kernel is a transformation that we apply on our entries so we can compute them easier. Think of z=x2 + y2

from sklearn.neural_network import MLPClassifier

def launchMLP(X_train, Y_train):

    model = MLPClassifier()
    model.fit(X_train, Y_train)

    return model

