from Scenario import Scenario
from Event import *
from multiprocessing import Process, Pool
from Expert import *
from scipy.stats import norm
from ResultData import *
import numpy as np
import Plotting
import matplotlib.pyplot as plt
import sys
import copy

def optimalSigma(scenario):
    numExperts = [12,12,6,6,6]
    start = 0
    sigma = np.power(scenario.target.epsilon_sigma,2)
    nsquared = np.power(len(scenario.target.epsilon_sigma),2)
    sigma = np.sqrt((sum(sigma))/nsquared)
    stop = 16*sigma
    opt = None
    rps = None
    for i in range(0,5):
        s = copy.deepcopy(scenario)
        s.experts = [copy.deepcopy(s.experts[0]) for i in range(0,numExperts[i])]
        for e in range(0,numExperts[i]):
            s.experts[e].sigma = start + (stop-start)*(1/(numExperts[i]-1))*e
        data = s.simulate(x=i+1,n=5)
        opt_index = np.argmax(data.getMeanExpertRPS())
        opt = s.experts[opt_index].sigma
        rps = max(data.getMeanExpertRPS())
        start = s.experts[max(0,opt_index-1)].sigma
        stop = s.experts[min(opt_index+1,len(s.experts)-1)].sigma
        if((stop-opt)<=(1/30)):
            break
    yield opt
    yield rps


def optimalWeights(scenario):
    numSims = [10,10,6,6,6]
    assert(len(scenario.experts) == 2)
    start = 0
    stop = 1
    opt = None
    opt_weights = None
    for i in range(0,5):
        opt = None
        opt_index = None
        for e in range(0,numSims[i]):
            s = copy.deepcopy(scenario)
            weight = start + (stop-start)*(1/(numSims[i]-1))*e
            weights = [weight, 1-weight]
            result = s.simulateDefaultWeights(weights).getMeanRPS()[1][0]
            if opt == None or result > opt:
                opt_weights = weights
                opt = result
                opt_index = e
        new_start = start + (stop-start)*(1/(numSims[i]-1))*(opt_index-1)
        new_start = max(0, new_start)
        stop = start + (stop-start)*(1/(numSims[i]-1))*(opt_index+1)
        stop = min(stop,1)
        start = new_start
        if((stop-start)<=(0.02)):
            break
    yield opt_weights
    yield opt

def optimalWeightsBruteForce(scenario):
    #numSims = [10,10,6,6,6]
    assert(len(scenario.experts) == 2)
    start = 0
    stop = 1
    opt = None
    opt_weights = None
    results = []
    for i in np.arange(0.97,1.00000001, 0.001): #for i in np.arange(0,1.009, 0.01):
        s = copy.deepcopy(scenario)
        weight = i
        weights = [weight, 1-weight]
        result = s.simulateDefaultWeights(weights).getMeanRPS()[1][0]
        if opt == None or result > opt:
            opt_weights = weights
            opt = result
        results.append(result)
    yield opt_weights
    yield opt
    yield results

# compare solo optimal sigma to group optimal sigma
def optimalGroupSigma(scenario, sigma1, sigma2):
    assert(len(scenario.experts) == 2)
    #start = 0
    #sigma = np.power(scenario.target.epsilon_sigma,2)
    #nsquared = np.power(len(scenario.target.epsilon_sigma),2)
    #sigma = np.sqrt((sum(sigma))/nsquared)
    #stop = 16*sigma
    stepsize = 0.1
    start1 = max(0, sigma1 - 0.5)
    stop1 = sigma1 + 0.5
    start2 = max(0, sigma2 - 0.5)
    stop2 = sigma2 + 0.5
    opt_uwm = None
    opt_cwm = None
    rps_uwm = None
    rps_cwm = None
    counter = 1
    for i in np.arange(start1, stop1, stepsize):
        for j in np.arange(start2, stop2, stepsize):
            s = copy.deepcopy(scenario)
            s.experts[0].sigma = i
            s.experts[1].sigma = j
            data = s.simulate(x=counter,
                              n=int((stop2-start2)/stepsize)*int((stop1-start1)/stepsize))
            counter += 1
            uwm = data.getMeanRPS()[1][0]
            cwm = data.getMeanRPS()[1][2]
            if rps_uwm == None or uwm > rps_uwm:
                rps_uwm = uwm
                opt_uwm = (i,j)
            if rps_cwm == None or cwm > rps_cwm:
                rps_cwm = cwm
                opt_cwm = (i,j)
    yield (opt_uwm, rps_uwm)
    yield (opt_cwm, rps_cwm)

def optimalGroupSigma2(scenario, sigma1, sigma2):
    assert(len(scenario.experts) == 2)
    #start = 0
    #sigma = np.power(scenario.target.epsilon_sigma,2)
    #nsquared = np.power(len(scenario.target.epsilon_sigma),2)
    #sigma = np.sqrt((sum(sigma))/nsquared)
    #stop = 16*sigma
    stepsize = 0.1
    start1 = sigma1*0.9
    stop1 = sigma1*1.1
    start2 = sigma2*0.9
    stop2 = sigma2*1.1
    opt_uwm = None
    opt_cwm = None
    rps_uwm = None
    rps_cwm = None
    counter = 1
    for i in [(start1,start2),(sigma1, sigma2),(stop1, stop2)]:
        print(i)
        s = copy.deepcopy(scenario)
        s.experts[0].sigma = i[0]
        s.experts[1].sigma = i[1]
        data = s.simulate(x=counter, n=int((stop2-start2)/stepsize)*int((stop1-start1)/stepsize))
        counter += 1
        uwm = data.getMeanRPS()[1][0]
        cwm = data.getMeanRPS()[1][2]
        print("UWM:")
        print(uwm)
        print("CWM:")
        print(cwm)
    yield (opt_uwm, rps_uwm)
    yield (opt_cwm, rps_cwm)


# für nicht gebiasete Experten: Optimales Sigma bei unterschiedlichem Informationsgehalt
def scenarioLooper_InfoCount(scenario, save=False):
    #s = copy.deepcopy(scenario)
    end = len(scenario.seeds[0].epsilon_mu)
    result = []
    for i in range(0, end+1):
        s = copy.deepcopy(scenario)
        epsilon = []
        for j in range(0, i):
            epsilon.append(1)
        for j in range(i, end):
            epsilon.append(0)
        for j in range(0, len(s.experts)):
            s.experts[j].epsilon = epsilon
        sigma,_ = optimalSigma(s)
        result.append(sigma)
    Plotting.plotOptimalSigma_InfoCount(result, s.name, save)

# für nicht gebiasete Experten: Auswirkungen des optimalen Sigmas auf die absolute Performance
def scenarioLooper_RPS_InfoCount(scenario, save=False):
    #s = scenario
    end = len(scenario.seeds[0].epsilon_mu)
    result = []
    for i in [1,2,3]:
        s = copy.deepcopy(scenario)
        epsilon = []
        #line = []
        for j in range(0, i):
            epsilon.append(1)
        for j in range(i, end):
            epsilon.append(0)
        for j in range(0, len(s.experts)):
            s.experts[j].epsilon = epsilon
        sigma,rps = optimalSigma(s)
        #line.append((sigma,rps))

        start = len(s.experts)/2 * 0.1 * -1
        delta_sigma=[]
        s=copy.deepcopy(s)
        length = 20
        s.experts = [copy.deepcopy(s.experts[0]) for i in range(0,length)]
        for e in range(0, length):
            delta_sigma.append(start + e*0.1)
        for e in range(0, length):
            s.experts[e].sigma = max(0,sigma+delta_sigma[e])
        data = s.simulate()
        rps1 = data.getMeanExpertRPS()
        result.append((delta_sigma, rps1, (sigma,rps)))
    Plotting.plotOptimalSigma_RPS_InfoCount(result, s.name, save)

# für unterschiedlich gebiasete Experten: Optimales Sigma bei unterschiedlichem Informationsgehalt
def scenarioLooper_Bias_InfoCount(scenario, save=False):
    s = scenario
    end = len(s.seeds[0].epsilon_mu)
    result = []
    for k in range(0,11):
        s = scenario
        bias = -0.5+k*0.1
        for e in s.experts:
            e.delta = bias
        helper = []
        for i in [1,2,3]:
            epsilon = []
            for j in range(0, i):
                epsilon.append(1)
            for j in range(i, end):
                epsilon.append(0)
            for j in range(0, len(s.experts)):
                s.experts[j].epsilon = epsilon
            sigma,_ = optimalSigma(s)
            helper.append(sigma)
        print("Bias: "+str(bias))
        result.append(helper)
    Plotting.plotOptimalSigma_Bias_InfoCount(result, s.name, save)

# für Scenario 201
def scenarioLooper_Break(scenario, mu, sigma, save=False):
    periods = len(scenario.seeds)
    data1=[]
    data2=[]
    data3=[]
    data4=[]
    data5=[]
    data6=[]
    data7=[]
    data8=[]
    event_old = scenario.seeds[0].copy()
    mu = [mu[i]*event_old.epsilon_mu[i] for i in range(0,len(mu))]
    sigma = [sigma[i]*event_old.epsilon_sigma[i] for i in range(0,len(sigma))]
    event_new = Event(epsilon_mu=mu, epsilon_sigma=sigma)
    ts = []
    for t in np.arange(0, periods, 1):
        sys.stderr.write(str(t))
        s = scenario.copy()
        for i in range(0, t):
            s.seeds[i] = event_old.copy()
        for i in range(t, len(scenario.seeds)):
            s.seeds[i] = event_new.copy()
        s.target = event_new.copy()
        data = s.simulate()
        data1.append(data.getMeanRPS()[1])
        data2.append(data.getExpertWeights())
        data3.append(data.getConfInterval(confidence=0.67))
        data4.append(data.getConfInterval(confidence=0.90))
        data5.append(data.getConfInterval(confidence=0.95))
        data6.append(data.getConfInterval_old(confidence=0.67))
        data7.append(data.getConfInterval_old(confidence=0.90))
        data8.append(data.getConfInterval_old(confidence=0.95))
        ts.append(t)
    Plotting.plotStructuralBreak(data1, ts, s.name, save)
    #Plotting.plotStructuralBreak(data1, ts, s.name+"_0.90", save, conf=data4)
    #Plotting.plotStructuralBreak(data1, ts, s.name+"_0.95", save, conf=data5)
    #Plotting.plotStructuralBreak(data1, ts, s.name+"_0.67_old", save, conf=data6)
    #Plotting.plotStructuralBreak(data1, ts, s.name+"_0.90_old", save, conf=data7)
    #Plotting.plotStructuralBreak(data1, ts, s.name+"_0.95_old", save, conf=data8)
    Plotting.plotStructuralBreakWeights(data2, ts, s.name, save, algo="cwm")

def compareGroupSoloSigma(scenario):
    assert(len(scenario.experts) == 2)

    s=copy.deepcopy(scenario)
    s.experts = [s.experts[0]]
    opt,_ = optimalSigma(s)
    s=copy.deepcopy(scenario)
    s.experts = [s.experts[1]]
    opt1,_ = optimalSigma(s)

    group_uwm, group_cwm = optimalGroupSigma2(scenario, opt, opt1)
    #print("Optimal Solo Sigma")
    #print("E1:")
    #print(opt)
    #print("E2:")
    #print(opt1)
    #print("Optimal Group Sigma")
    #print("UWM:")
    #print(group_uwm[0])
    #print("CWM:")
    #print(group_cwm[0])
    print("\n")


def simulateScenario(scenario, save=False):
    data = scenario.simulate()
    #data.plotExpertPerformance(save=save)
    #data.plotExpertWeights(save=save)
    data.plotCumulativeExpertWeights(save=save)
    #data.plotMeanRPS(save=save)
    #data.plotBoxplotExpertWeights(save=save)

#s = [Scenario(i) for i in range(2,3)]
#p = Pool(len(s)+10)
#p.map(simulateScenario, s)