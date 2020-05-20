import numpy as np
from scipy.stats import norm

class Event():

    def __init__(self, epsilon_mu, epsilon_sigma):
        self.epsilon_mu = epsilon_mu
        self.epsilon_sigma = epsilon_sigma

    def __str__(self):
        return "Event mit Mu: " + str(self.epsilon_mu) + ", Sigma: " + str(self.epsilon_sigma)

    def copy(self):
        return Event(self.epsilon_mu, self.epsilon_sigma)

    def getObservation(self):
        return self.observation

    def setObservation(self):
        self.epsilon = []
        for i in range(0, len(self.epsilon_mu)):
            self.epsilon.append(norm.rvs(loc=self.epsilon_mu[i], scale=self.epsilon_sigma[i]))
        self.observation = sum(self.epsilon) / len(self.epsilon)
