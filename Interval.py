import numpy as np
from scipy.stats import norm

class Interval():

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return "]" +str(self.a) + ", " + str(self.b) + "]"

def getIntervalsForEvent(numIntervals, event):
    intervals = []
    mean = sum(event.epsilon_mu) / len(event.epsilon_mu)
    sigma = np.power(event.epsilon_sigma,2)
    nsquared = np.power(len(event.epsilon_sigma),2)
    sigma = np.sqrt((sum(sigma))/nsquared)
    quantile1 = mean - 2*sigma
    quantile2 = mean + 2*sigma
    length = (quantile2 - quantile1) / (numIntervals-2)
    intervals.append(Interval(float("-inf"), quantile1))
    for i in range(0,numIntervals-2):
        intervals.append(Interval(quantile1+i*length, quantile1+(i+1)*length))
    intervals.append(Interval(quantile2, float("inf")))
    return intervals