import numpy as np
from scipy.stats import norm

class Expert():

    def __init__(self, delta, sigma, epsilon):
        self.delta = delta
        self.sigma = sigma
        self.epsilon = epsilon
        self.counts = 10
        self.currentEvent = None
        self.normalValues = None

    def getProbability(self, interval, id, event):
        if(self.currentEvent == None or self.currentEvent != event):
            self.currentEvent = event
            self.normalValues = 0
            for i in range(0, len(self.epsilon)):
                self.normalValues += self.epsilon[i] * event.epsilon[i]
            if(np.any(self.epsilon)):
                self.normalValues /= sum(np.abs(self.epsilon))
            self.normalValues = self.normalValues + self.delta + norm.rvs(0,self.sigma,self.counts)
        counter = 0
        for n in self.normalValues:
            if n > interval.a and n <= interval.b:
                counter += 1
        counter /= self.counts
        return counter

    #def getProbabilityOld(self, interval, id, event):
    #    cdf1 = norm.cdf(interval.b,loc=self.alpha*event.epsilon1 + self.beta*event.epsilon2 + self.delta, scale=self.sigma)
    #    cdf2 = norm.cdf(interval.a,loc=self.alpha*event.epsilon1 + self.beta*event.epsilon2 + self.delta, scale=self.sigma)
    #    return cdf1 - cdf2