import numpy as np
from scipy.stats import norm

class JudgmentData():

    def __init__(self, seeds, target):
        self.seedJudgments = []
        self.targetJudgments = np.zeros((1,1))
        self.seeds = seeds
        self.target = target

    def setSeedJudgments(self, seedJudgments):
        self.seedJudgments = seedJudgments

    def setTargetJudgments(self, targetJudgments):
        self.targetJudgments = targetJudgments

    def setTargetPDF(self, targetPDF):
        self.targetPDF = targetPDF

    def setSeedPDF(self, seedPDF):
        self.seedPDF = seedPDF

    def getSeedJudgment(self, num):
        return self.seedJudgments[num]

    def getTargetJudgment(self):
        return self.targetJudgments
