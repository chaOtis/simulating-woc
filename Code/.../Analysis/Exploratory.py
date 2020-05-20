from Simulation import *
from time import gmtime, strftime
from datetime import datetime

def crowdConstellation():
    print()

    # Describe weighting
    print("########## Exploratory: 4a - CROWD CONSTELLATION BASICS ##########")
    s1 = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="C2_1")
    s2 = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="C2_2")
    #s3 = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="C2_3")
    data1 = s1.simulate()
    data2 = s2.simulate()
    #data3 = s3.simulate()
    data1.plotCumulativeExpertWeights(save=True)
    data2.plotCumulativeExpertWeights(save=True)
    #data3.plotCumulativeExpertWeights(save=True)
    data1.plotMeanRPS(save=True)
    data2.plotMeanRPS(save=True)

    # How many seeds are necessary?
    '''print("########## Exploratory: 4a - CROWD CONSTELLATION HISTORY ##########")
    seed_count=[4,16,32,64,256]
    scen_count=[1,2] #[1,2,3]
    vari_count=[1/3,1,8/3]
    results1 = [[], [], []]
    results2 = [[], [], []]
    results3 = [[], [], []]
    dict = {1:results1, 2:results2, 3:results3}
    count = 1
    for i in scen_count:
        for j in [0,1,2]:
            for c in seed_count:
                s = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="C3_"+str(i))
                for e in s.experts:
                    e.sigma = e.sigma*vari_count[j]
                s.seeds = s.seeds[:c]
                #s.cycles = 2
                data=s.simulate()
                print(str(i)+" "+str(vari_count[j])+" "+str(c)+": "+str(data.getVarianceRPS()[1][2]))
                dict[i][j].append(data)
                sys.stderr.write("History scenario # "+str(count)+" of "+str(len(scen_count)*len(vari_count)*len(seed_count))+" is finished.\n")
                count = count + 1
    for i in scen_count:
        for j in [0,1,2]:
            results = []
            for c in range(0,len(seed_count)):
                results.append([])
                data = dict[i][j][c].getExpertWeights()
                data = np.matrix.transpose(np.array(data[1]))
                for e in range(0,len(data)):
                    #print("Variance for "+str(i)+" "+str(vari_count[j])+" "+str(seed_count[c])+" "+str(e)+": "+str(np.var(np.array(data[e]))))
                    results[c].append(np.var(np.array(data[e])))
                #for e in range(0,len(data)):
                #    print("Mean for "+str(i)+" "+str(vari_count[j])+" "+str(seed_count[c])+" "+str(e)+": "+str(np.mean(np.array(data[e]))))
            print("Resulting variance for Scenario C3_"+str(i)+" with sigma factor "+str(vari_count[j])+":")
            print(np.matrix.transpose(np.array(results)))

    # Drivers for weighting
    print("########## Exploratory: 4a - DRIVERS FOR WEIGHTING ##########")
    for i in range(0,11):
        s = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="C4_1")
        for j in range(0,i):
            s.experts[j].epsilon=[1,1]
        data = s.simulate()
        data.name = data.name + "_" + str(i)
        data.plotExpertWeights(save=True)
        data.plotCumulativeExpertWeights(save=True)'''


def structuralBreaks():
    print()
    print("########## Exploratory: 4b - STRUCTURAL BREAKS ##########")

    s1 = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="S1")
    scenarioLooper_Break(s1, mu=[0.0, 0.5, 2.0], sigma=[1, 1, 1], save=True)

    # ARCHIV - NICHT AKTUELL, NICHT KORREKT
    #s2 = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="S2")
    #s3 = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="S3")
    #scenarioLooper_Break(s2, mu=[0.50, 1.50, 1.0], sigma=[1, 1, 1], save=True)
    #scenarioLooper_Break(s3, mu=[0.75, 1.25, 1.0], sigma=[1, 1, 1], save=True)


def exploreHypotheses():
    print()
    print("########## Exploratory: 4c ##########")

    print("########## Exploratory: 4c - SINGLE DELETE ##########")

    # Single Delete Problem
    #s1_sd = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="C5_1a")
    #s2_sd = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="C5_1b")
    #s3_sd = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="C5_1c")
    #s4_sd = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="C5_1d")
    #s5_sd = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="C5_1d")

    #data1_sd = s1_sd.simulate()
    #data2_sd = s2_sd.simulate()
    #data3_sd = s3_sd.simulate()
    #data4_sd = s4_sd.simulate()
    #data5_sd = s5_sd.simulate()

    #data1_sd.plotExpertWeights(save=True)
    #data1_sd.plotMeanRPS(save=True)
    #data2_sd.plotExpertWeights(save=True)
    #data2_sd.plotMeanRPS(save=True)
    #data3_sd.plotExpertWeights(save=True)
    #data3_sd.plotMeanRPS(save=True)
    #data4_sd.plotExpertWeights(save=True)
    #data4_sd.plotMeanRPS(save=True)
    #data5_sd.plotExpertWeights(save=True)
    #data5_sd.plotMeanRPS(save=True)

    print("########## Exploratory: 4c - INDIVIDUAL UNCERTAINTY ##########")

    #s1 = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="I1_1")
    #s2 = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="I1_1")
    #opt, rps = optimalSigma(s1)
    #s2.experts[0].sigma = opt
    #s2.experts[1].sigma = max(opt-0.5, 0)
    #data = s2.simulate()
    #data.plotExpertPerformance(save=True)
    #s2 = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="I1_1")
    #scenarioLooper_InfoCount(s2, save=True)

    s2 = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="I1_1")
    compareGroupSoloSigma(s2)
    #s2 = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="I1_1")
    #scenarioLooper_RPS_InfoCount(s2, save=True)
    #s2 = Scenario(excel=True, excelName='./Scenarios_Exploratory.xlsx', id="I1_2")
    #scenarioLooper_Bias_InfoCount(s2, save=True)

def test():
    pass

#sys.stdout = open('./data/output_exploratory_'+strftime("%Y-%m-%d_%H-%M", gmtime())+'.txt', mode="w")
t1=datetime.now()
crowdConstellation()
#structuralBreaks() # CHRIS fuehrt aus
#exploreHypotheses() # DOMI fuehrt aus
#test()
t2=datetime.now()
delta = t2-t1
sys.stderr.write("\nIt took "+str(delta.seconds)+" seconds to complete the simulation.\n")
#sys.stdout.close()
