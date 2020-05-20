from JudgmentData import *
from Event import *
import numpy as np

class Algorithm():

    def __init__(self, judgmentData, performanceMeasure=None):
        self.judgmentData = judgmentData
        self.seeds = self.judgmentData.seeds
        self.target = self.judgmentData.target
        self.observationPDF = self.judgmentData.targetPDF
        self.seedPDF = self.judgmentData.seedPDF
        self.performanceMeasure = performanceMeasure

    def run(self):
        self.aggregate()
        return self.computeRPS()

    def aggregate(self):
        pass

    def computeCDF(self, estimation):
        return [sum(estimation[0:x]) for x in range(1, len(estimation)+1)]

    def computeRPS(self):
        F_obs = self.computeCDF(self.observationPDF)
        F_agg = self.computeCDF(self.aggregationPDF)
        sum = 0
        for i in range(0, len(F_obs)):
            sum += np.power(F_obs[i] - F_agg[i], 2)
        sum /= (len(F_obs)-1)
        sum = (1-sum)*100
        return sum

    def computePerformance(self):
        pass

    def setWeights(self, weights):
        self.weights = weights

    def getWeights(self):
        return self.weights

    def getPM(self):
        return self.performanceMeasure

    def setPM(self, pM):
        self.performanceMeasure = pM


class UWM(Algorithm):

    def aggregate(self):
        self.aggregationPDF = []
        data = self.judgmentData.getTargetJudgment()
        self.weights = [1/len(data[0]) for i in range(0,len(data[0]))]
        for i in range(0, len(data)):
            sum1 = sum(data[i])
            sum1 /= len(data[i])
            self.aggregationPDF.append(sum1)


class PWM(Algorithm):

    def aggregate(self):
        self.computePerformance()
        weight = np.asarray(self.performanceMeasure) / sum(self.performanceMeasure)
        self.weights = list(weight)
        self.aggregationPDF = []
        data = self.judgmentData.getTargetJudgment()
        for i in range(0, len(data)):
            sum1 = sum([data[i][e]*weight[e] for e in range(0,len(data[i]))])
            self.aggregationPDF.append(sum1)

    def computePerformance(self):
        if(self.performanceMeasure != None):
            pass
        scores = []
        for e in range(0,len(self.judgmentData.seedJudgments[0][0])):
            rps = 0
            for s in range(0,len(self.judgmentData.seedJudgments)):
                F_obs = self.computeCDF(self.seedPDF[s])
                F_exp = self.computeCDF([self.judgmentData.seedJudgments[s][x][e] for x in range(0,len(F_obs))])
                sum = 0
                for i in range(0, len(F_obs)):
                    sum += np.power(F_obs[i] - F_exp[i], 2)
                sum /= (len(F_obs)-1)
                sum = (1-sum)*100
                #print(sum)
                rps += sum
            rps /= len(self.judgmentData.seedJudgments)
            scores.append(rps)
            #print("")
        self.performanceMeasure = scores


class BestExpert(Algorithm):

    def aggregate(self):
        self.computePerformance()
        bestIndex = np.argmax(self.performanceMeasure)
        self.weights = [0 for i in range(0,len(self.performanceMeasure))]
        self.weights[bestIndex]=1
        data = self.judgmentData.getTargetJudgment()
        self.aggregationPDF = [data[i][bestIndex] for i in range(0,len(data))]

    def computePerformance(self):
        if(self.performanceMeasure != None):
            pass
        scores = []
        for e in range(0,len(self.judgmentData.seedJudgments[0][0])):
            rps = 0
            for s in range(0,len(self.judgmentData.seedJudgments)):
                F_obs = self.computeCDF(self.seedPDF[s])
                F_exp = self.computeCDF([self.judgmentData.seedJudgments[s][x][e] for x in range(0,len(F_obs))])
                sum = 0
                for i in range(0, len(F_obs)):
                    sum += np.power(F_obs[i] - F_exp[i], 2)
                sum /= (len(F_obs)-1)
                sum = (1-sum)*100
                rps += sum
            rps /= len(self.judgmentData.seedJudgments)
            scores.append(rps)
        self.performanceMeasure = scores

class CWM(Algorithm):

    def aggregate(self):
        self.computePerformance()
        posPerf = [max(x, 0) for x in self.performanceMeasure]
        weight = np.asarray(posPerf) / sum(posPerf)
        self.weights = list(weight)
        self.aggregationPDF = []
        data = self.judgmentData.getTargetJudgment()
        assert(max(weight) > 0)
        for i in range(0, len(data)):
            sum1 = sum([data[i][e]*weight[e] for e in range(0,len(data[i]))])
            self.aggregationPDF.append(sum1)

    def computePerformance(self):
        if(self.performanceMeasure != None):
            pass
        St = [] # BS for every seed s
        for s in range(0,len(self.judgmentData.seedJudgments)):
            data = self.judgmentData.seedJudgments[s]
            f_agg = []
            for i in range(0, len(data)):
                sum1 = sum(data[i])
                sum1 /= len(data[i])
                f_agg.append(sum1)
            f_obs = self.seedPDF[s]
            F_obs = self.computeCDF(f_obs)
            F_agg = self.computeCDF(f_agg)
            sum2 = 0
            for i in range(0, len(F_obs)):
                sum2 += np.power(F_obs[i] - F_agg[i], 2)
            sum2 /= (len(F_obs)-1)
            sum2 = 100 - 100*sum2
            St.append(sum2)

        Ste = [] # BS for every seed s minus expert e
        for s in range(0,len(self.judgmentData.seedJudgments)):
            x = []
            for e in range(0, len(self.judgmentData.seedJudgments[s][0])):
                newProb = [] #self.judgmentData.seedJudgments[s]
                for i in range(0, len(self.judgmentData.seedJudgments[s])):
                    newProb.append(np.delete(self.judgmentData.seedJudgments[s][i], e))
                f_agg = []
                for i in range(0, len(newProb)):
                    sum1 = sum(newProb[i])
                    sum1 /= len(newProb[i])
                    f_agg.append(sum1)
                f_obs = self.seedPDF[s]
                F_obs = self.computeCDF(f_obs)
                F_agg = self.computeCDF(f_agg)
                sum2 = 0
                for i in range(0, len(F_obs)):
                    sum2 += np.power(F_obs[i] - F_agg[i], 2)
                sum2 /= (len(F_obs)-1)
                sum2 = 100 - 100*sum2
                x.append(sum2)
            Ste.append(x)

        Ce = [] # computation of contribution
        for e in range(0, len(self.judgmentData.seedJudgments[0][0])):
            x = 0
            for s in range(0,len(self.judgmentData.seedJudgments)):
                x+= (St[s] - Ste[s][e])
            x /= len(self.judgmentData.seedJudgments)
            Ce.append(x)
        self.performanceMeasure = Ce


class Contribution(Algorithm):

    def aggregate(self):
        self.computePerformance()
        self.performanceMeasure = np.asarray([max(x, 0) for x in self.performanceMeasure])
        self.performanceMeasure[self.performanceMeasure > 0] = 1
        weight = self.performanceMeasure / sum(self.performanceMeasure)
        self.weights = list(weight)
        self.aggregationPDF = []
        data = self.judgmentData.getTargetJudgment()
        assert(max(weight) > 0)
        for i in range(0, len(data)):
            sum1 = sum([data[i][e]*weight[e] for e in range(0,len(data[i]))])
            self.aggregationPDF.append(sum1)

    def computePerformance(self):
        if(self.performanceMeasure != None):
            pass
        St = [] # BS for every seed s
        for s in range(0,len(self.judgmentData.seedJudgments)):
            data = self.judgmentData.seedJudgments[s]
            f_agg = []
            for i in range(0, len(data)):
                sum1 = sum(data[i])
                sum1 /= len(data[i])
                f_agg.append(sum1)
            f_obs = self.seedPDF[s]
            F_obs = self.computeCDF(f_obs)
            F_agg = self.computeCDF(f_agg)
            sum2 = 0
            for i in range(0, len(F_obs)):
                sum2 += np.power(F_obs[i] - F_agg[i], 2)
            sum2 /= (len(F_obs)-1)
            sum2 = 100 - 100*sum2
            St.append(sum2)

        Ste = [] # BS for every seed s minus expert e
        for s in range(0,len(self.judgmentData.seedJudgments)):
            x = []
            for e in range(0, len(self.judgmentData.seedJudgments[s][0])):
                newProb = [] #self.judgmentData.seedJudgments[s]
                for i in range(0, len(self.judgmentData.seedJudgments[s])):
                    newProb.append(np.delete(self.judgmentData.seedJudgments[s][i], e))
                f_agg = []
                for i in range(0, len(newProb)):
                    sum1 = sum(newProb[i])
                    sum1 /= len(newProb[i])
                    f_agg.append(sum1)
                f_obs = self.seedPDF[s]
                F_obs = self.computeCDF(f_obs)
                F_agg = self.computeCDF(f_agg)
                sum2 = 0
                for i in range(0, len(F_obs)):
                    sum2 += np.power(F_obs[i] - F_agg[i], 2)
                sum2 /= (len(F_obs)-1)
                sum2 = 100 - 100*sum2
                x.append(sum2)
            Ste.append(x)

        Ce = [] # computation of contribution
        for e in range(0, len(self.judgmentData.seedJudgments[0][0])):
            x = 0
            for s in range(0,len(self.judgmentData.seedJudgments)):
                x+= (St[s] - Ste[s][e])
            x /= len(self.judgmentData.seedJudgments)
            Ce.append(x)
        self.performanceMeasure = Ce

class DefaultWeight(Algorithm):

    def aggregate(self):
        self.aggregationPDF = []
        data = self.judgmentData.getTargetJudgment()
        assert(self.weights != None)
        for i in range(0, len(data)):
            sum1 = sum([data[i][e]*self.weights[e] for e in range(0,len(data[i]))])
            self.aggregationPDF.append(sum1)

class RandomExpert(Algorithm):

    def aggregate(self):
        self.aggregationPDF = []
        data = self.judgmentData.getTargetJudgment()
        numExperts = len(data[0])
        self.weights = np.zeros(numExperts)
        self.weights[np.random.randint(0,numExperts)] = 1
        for i in range(0, len(data)):
            sum1 = sum([data[i][e]*self.weights[e] for e in range(0,len(data[i]))])
            self.aggregationPDF.append(sum1)