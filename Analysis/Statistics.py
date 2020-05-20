import numpy as np
import scipy

def mean_test(a, b, inter=False):
    if(inter):
        pvalue = scipy.stats.mannwhitneyu(a,b).pvalue
    else:
        pvalue = scipy.stats.wilcoxon(a,b).pvalue
    sign = "."
    if pvalue <= 0.05:
        sign = "*"
    if pvalue <= 0.01:
        sign = "**"
    if pvalue <= 0.001:
        sign = "***"
    return str(pvalue) + sign

def effectsize_test(a, b, inter=False):
    if(inter):
        return cohen_d(a, b)
    else:
        return cohen_dz(a, b)

def cohen_d(a, b):
    return cohen_dz(a,b)
    mean1 = np.mean(np.asarray(a))
    mean2 = np.mean(np.asarray(b))
    var1 = np.var(np.asarray(a), ddof=1)
    var2 = np.var(np.asarray(b), ddof=1)
    return str((mean1-mean2)/np.sqrt((var1+var2)/2))

def cohen_dz(a, b):
    mean = np.mean(np.asarray(a)-np.asarray(b))
    std = np.std(np.asarray(a)-np.asarray(b))
    return str(mean/std)

def variance_test(a, b, inter=False):
    if(inter):
        pvalue = scipy.stats.fligner(a,b).pvalue
    else:
        pvalue = scipy.stats.fligner(a,b).pvalue
    sign = "."
    if pvalue <= 0.05:
        sign = "*"
    if pvalue <= 0.01:
        sign = "**"
    if pvalue <= 0.001:
        sign = "***"
    return str(pvalue) + sign

def getFullStats(a,b, inter=False):
    if(inter):
        return ("Mann-Whitney-U: " + '{0: <25}'.format(mean_test(a,b,inter))+ "Fligner-Killeen: " + '{0: <25}'.format(variance_test(a,b,inter))+ "Effect Size (d): "+cohen_d(a,b))
    else:
        return ("Wilcoxon: " + '{0: <25}'.format(mean_test(a,b,inter))+ "Fligner-Killeen: " + '{0: <25}'.format(variance_test(a,b,inter))+ "Effect Size (dz): "+cohen_d(a,b))
