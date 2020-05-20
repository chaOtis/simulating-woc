import numpy as np
from JudgmentData import JudgmentData
from scipy.stats import norm

class Model():

    def __init__(self, experts, intervals, seeds, target):
        self.experts = experts
        self.intervals = intervals
        self.seeds = seeds
        self.target = target
        self.judgments = JudgmentData(self.seeds, self.target)
        self.setTargetPDF()
        self.setSeedPDF()
        self.setSeedJudgments()
        self.setTargetJudgments()

    def setSeedJudgments(self):
        seedJudgments = []

        for s in self.seeds:
            array = np.zeros((len(self.intervals), len(self.experts)))

            for i in range(0,len(self.intervals)):
                for e in range(0,len(self.experts)):
                    array[i,e]=self.experts[e].getProbability(self.intervals[i],i,s)

            seedJudgments.append(array)

        self.judgments.setSeedJudgments(seedJudgments)

    def setTargetJudgments(self):
        targetJudgments = np.zeros((len(self.intervals), len(self.experts)))

        for i in range(0,len(self.intervals)):
            for e in range(0, len(self.experts)):
                targetJudgments[i,e]=self.experts[e].getProbability(self.intervals[i],i,self.target)

        self.judgments.setTargetJudgments(targetJudgments)

    def setTargetPDF(self):
        targetPDF = []
        obs = self.target.observation
        for i in self.intervals:
            if obs > i.a and obs <= i.b:
                targetPDF.append(1)
            else:
                targetPDF.append(0)
        self.judgments.setTargetPDF(targetPDF)

    def setSeedPDF(self):
        seedArray = []
        for s in self.seeds:
            seedPDF = []
            obs = s.observation
            for i in self.intervals:
                if obs > i.a and obs <= i.b:
                    seedPDF.append(1)
                else:
                    seedPDF.append(0)
            seedArray.append(seedPDF)
        self.judgments.setSeedPDF(seedArray)


    def getJudgmentData(self):
        return self.judgments
