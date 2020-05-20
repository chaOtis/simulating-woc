from Simulation import *
import sys
import Statistics as stats
import numpy as np

def proposition_1():
    print()
    print("########## Proposition 1: ##########")
    s = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P1_1")
    data = s.simulate()
    data.plotExpertPerformance(save=True)
    data.plotBoxplotExpertWeights(save=True)
    data.getStatistics()


def proposition_2():
    print()
    print("########## Proposition 2: ###########")
    ids = ["P2_1","P2_2","P2_3","P2_4"]
    for i in ids:
        s=Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id=i)
        data = s.simulate()
        data.plotMeanRPS(save=True)
        data.getStatistics()


def proposition_3():
    print()
    print(" ########## Proposition 3: ##########")
    s1 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P3_1")
    s2 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P3_2")
    s3 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P3_3")
    data1 = s1.simulate()
    data2 = s2.simulate()
    data3 = s3.simulate()
    data1.plotMeanRPS(save=True)
    data2.plotMeanRPS(save=True)
    data3.plotMeanRPS(save=True)
    data1.computeData()
    data2.computeData()
    data3.computeData()
    print("UWM1 <-> UWM3 " + stats.getFullStats(data1.uwm,data3.uwm,inter=True))
    print("CWM1 <-> CWM3 " + stats.getFullStats(data1.cwm,data3.cwm,inter=True))


def proposition_4():
    print()
    print("########## Proposition 4: ##########")
    results = []
    results_full = []
    s = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P4_1")
    experts = copy.deepcopy(s.experts)
    for e in experts:
        epsilon = np.zeros(len(e.epsilon))
        info_index = int(np.random.uniform(0,len(epsilon),1))
        epsilon[info_index] = 1
        e.epsilon = epsilon
    for i in range(2, len(s.experts)+1):
        s_temp = copy.deepcopy(s)
        s_temp.experts = []
        for j in range(0,i):
            s_temp.experts.append(copy.deepcopy(experts[j]))
        data_temp = s_temp.simulate()
        data_temp.computeData()
        results_full.append(data_temp.uwm)
        results.append(data_temp.getMeanRPS()[1][0])
    for i in range(0, len(results_full)-1):
        print("UWM ("+str(i+2)+" Exp) <-> UWM ("+str(i+3)+" Exp) " + stats.getFullStats(results_full[i],results_full[i+1],inter=True))
    print(results)


def proposition_5():
    print()
    print("########## Proposition 5: ##########")
    s1 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P5_1")
    data1 = s1.simulate()
    s2 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P5_2")
    data2 = s2.simulate()
    s3 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P5_3")
    data3 = s3.simulate()
    s4 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P5_4")
    data4 = s4.simulate()
    s5 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P5_5")
    data5 = s5.simulate()
    data1.plotMeanRPS(save=True)
    data2.plotMeanRPS(save=True)
    data3.plotMeanRPS(save=True)
    data4.plotMeanRPS(save=True)
    data5.plotMeanRPS(save=True)


def proposition_6():
    print()
    print("########## Proposition 6: ##########")
    s1 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P6_1")
    data1 = s1.simulate()
    s2 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P6_2")
    data2 = s2.simulate()
    data1.plotCumulativeExpertWeights(save=True)
    data1.plotMeanRPS(save=True)
    data2.plotMeanRPS(save=True)
    data1.getStatistics()
    data2.getStatistics()


def proposition_7():
    print()
    print("########## Proposition 7: ##########")
    s1 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P7_1")
    data1 = s1.simulate()
    s2 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P7_2")
    data2 = s2.simulate()
    s2 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P7_3")
    data3 = s2.simulate()
    s2 = Scenario(excel=True, excelName='./Scenarios_Propositions.xlsx', id="P7_4")
    data4 = s2.simulate()
    data1.plotMeanRPS(save=True)
    data2.plotMeanRPS(save=True)
    data3.plotMeanRPS(save=True)
    data4.plotMeanRPS(save=True)
    print(data1.getMeanRPS())
    print(data2.getMeanRPS())
    print(data3.getMeanRPS())
    print(data4.getMeanRPS())
    print(data1.getVarianceRPS())
    print(data2.getVarianceRPS())
    print(data3.getVarianceRPS())
    print(data4.getVarianceRPS())
    data1.computeData()
    data2.computeData()
    data3.computeData()
    data4.computeData()
    print("PWM1 <-> PWM4 " + stats.getFullStats(data1.pwm,data4.pwm,inter=True))
    print("CWM1 <-> CWM4 " + stats.getFullStats(data1.cwm,data4.cwm,inter=True))


sys.stdout = open('./data/output_proposition.txt', mode="w")
#proposition_1()
proposition_2()
#proposition_3()
#proposition_4()
#proposition_5()
#proposition_6()
#proposition_7()
sys.stdout.close()
