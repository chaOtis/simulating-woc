import numpy as np
import scipy as sp
import scipy.stats

def mean_confidence_interval_t(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, sd = np.mean(a), scipy.stats.sem(a)
    t = scipy.stats.t.ppf((1-confidence)/2, n-1)
    #print(t)
    h = sd * t
    return m+h, m-h

def mean_confidence_interval_z(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, sd = np.mean(a), scipy.stats.sem(a)
    z = scipy.stats.norm.ppf((1-confidence)/2)
    #print(z)
    h = sd * z
    return m+h, m-h


a = np.asarray(np.random.poisson(1,10000))
print(mean_confidence_interval_t(a, confidence=0.99))
#print(mean_confidence_interval_z(a, confidence=0.95))
print(scipy.stats.t.interval(0.99, len(a)-1, loc=np.mean(a), scale=scipy.stats.sem(a)))