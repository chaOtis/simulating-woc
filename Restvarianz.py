from scipy.stats import norm
import numpy as np
import properscoring as ps

result = []
obs = []
obs1 = []
crps = []
for j in range(0,50000):
    epsilon = []
    epsilon.append(norm.rvs(loc=0, scale=1))
    epsilon.append(norm.rvs(loc=0, scale=1))
    observation = sum(epsilon)
    obs.append(observation)
    observation1 = sum(epsilon[0:1]) / 1
    obs1.append(observation1)
    #crps.append(ps.crps_gaussian(observation*2, mu=observation1, sig=1))
    result.append(observation-observation1)
#print(np.sqrt(np.var(obs1)))
#print(np.sqrt(np.var(obs)))
print(np.sqrt(np.var(result)))
