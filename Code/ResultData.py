import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy
import csv
import Statistics as stats

class ResultData():

    def __init__(self, rps_scores, name):
        self.rps_scores = rps_scores
        self.name = name

    def computeData(self):
        self.uwm = [self.rps_scores[i][0] for i in range(1,len(self.rps_scores))]
        self.pwm = [self.rps_scores[i][1] for i in range(1,len(self.rps_scores))]
        self.cwm = [self.rps_scores[i][2] for i in range(1,len(self.rps_scores))]
        self.con = [self.rps_scores[i][3] for i in range(1,len(self.rps_scores))]
        self.bex = [self.rps_scores[i][4] for i in range(1,len(self.rps_scores))]
        self.ran = [self.rps_scores[i][5] for i in range(1,len(self.rps_scores))]

    def computeDataDefaultWeight(self):
        self.dew = [self.rps_scores[i][0] for i in range(1,len(self.rps_scores))]

    def setExpertPerformance(self, ep):
        self.expertPerformance = ep

    def setExpertWeights(self, ew):
        self.expertWeights = ew

    def getExpertPerformance(self):
        return self.expertPerformance

    def getMeanExpertRPS(self):
        return np.mean(np.array(self.expertPerformance[0]), axis=0)

    def getExpertWeights(self):
        return self.expertWeights

    def getMeanRPS(self):
        array = [self.rps_scores[0], list(np.mean(np.array(self.rps_scores[1:]), axis=0))]
        return array

    def getConfInterval_old(self, confidence=0.95):
        n = len(self.rps_scores[1:])
        if(n<100):
            print("Please know that our confidence interval values are not correct for small samples!")
        inf = round(((1-confidence)/2)*n)
        sup = round(((1+confidence)/2)*n)
        data = np.array(self.rps_scores[1:])
        data1 = np.transpose(data)
        result = []
        for i in range(0, len(data1)):
            tmp = data1[i]
            #tmp = sorted(tmp)
            #tmp = tmp[inf:sup]
            result.append(scipy.stats.t.interval(confidence, len(tmp)-1, loc=np.mean(tmp, axis=0), scale=scipy.stats.sem(tmp)))
            #result.append((tmp[0], tmp[-1]))
        return result

    def getConfInterval(self, confidence=0.95):
        n = len(self.rps_scores[1:])
        if(n<100):
            print("Please know that our confidence interval values are not correct for small samples!")
        inf = round(((1-confidence)/2)*n)
        sup = round(((1+confidence)/2)*n)
        data = np.array(self.rps_scores[1:])
        data1 = np.transpose(data)
        result = []
        for i in range(0, len(data1)):
            tmp = data1[i]
            tmp = sorted(tmp)
            if i==2:
                print(tmp)
            tmp = tmp[inf:sup]
            #result.append(scipy.stats.t.interval(confidence, len(tmp)-1, loc=np.mean(tmp, axis=0), scale=scipy.stats.sem(tmp)))
            result.append((tmp[0], tmp[-1]))
        return result

    def getVarianceRPS(self):
        uwm = np.var([self.rps_scores[i][0] for i in range(1,len(self.rps_scores))])
        pwm = np.var([self.rps_scores[i][1] for i in range(1,len(self.rps_scores))])
        cwm = np.var([self.rps_scores[i][2] for i in range(1,len(self.rps_scores))])
        con = np.var([self.rps_scores[i][3] for i in range(1,len(self.rps_scores))])
        bex = np.var([self.rps_scores[i][4] for i in range(1,len(self.rps_scores))])
        ran = np.var([self.rps_scores[i][5] for i in range(1,len(self.rps_scores))])
        array = [self.rps_scores[0], [uwm,pwm,cwm,con,bex,ran]]
        with open("./Data/" + self.name + "_VarianceRPS.csv", mode="w") as file:
            filewriter = csv.writer(file, delimiter=";")
            filewriter.writerow(array[0])
            filewriter.writerow(array[1])
        return array

    def getStatistics(self):
        self.computeData()
        cases = 15
        print(self.name)
        print("UWM <-> PWM " + stats.getFullStats(self.uwm,self.pwm))
        print("UWM <-> PWM " + stats.getFullStats(self.uwm,self.cwm))
        print("UWM <-> PWM " + stats.getFullStats(self.uwm,self.con))
        print("UWM <-> PWM " + stats.getFullStats(self.uwm,self.bex))
        print("UWM <-> PWM " + stats.getFullStats(self.uwm,self.ran))
        print("UWM <-> PWM " + stats.getFullStats(self.pwm,self.cwm))
        print("UWM <-> PWM " + stats.getFullStats(self.pwm,self.con))
        print("UWM <-> PWM " + stats.getFullStats(self.pwm,self.bex))
        print("UWM <-> PWM " + stats.getFullStats(self.pwm,self.ran))
        print("UWM <-> PWM " + stats.getFullStats(self.cwm,self.con))
        print("UWM <-> PWM " + stats.getFullStats(self.cwm,self.bex))
        print("UWM <-> PWM " + stats.getFullStats(self.cwm,self.ran))
        print("UWM <-> PWM " + stats.getFullStats(self.con,self.bex))
        print("UWM <-> PWM " + stats.getFullStats(self.con,self.ran))
        print("UWM <-> PWM " + stats.getFullStats(self.bex,self.ran))

    def plotMeanRPS(self, save=False):
        array = self.getMeanRPS()
        with open("./Data/" + self.name + "_MeanRPS.csv", mode="w") as file:
            filewriter = csv.writer(file, delimiter=";")
            filewriter.writerow(array[0])
            filewriter.writerow(array[1])
        uwm = [x[0] for x in self.rps_scores[1:]]
        pwm = [x[1] for x in self.rps_scores[1:]]
        cwm = [x[2] for x in self.rps_scores[1:]]
        con = [x[3] for x in self.rps_scores[1:]]
        bex = [x[4] for x in self.rps_scores[1:]]
        ran = [x[5] for x in self.rps_scores[1:]]
        with open("./Data/" + self.name + "_MeanRPS_all_data.csv", mode="w") as file:
            filewriter = csv.writer(file, delimiter=";")
            filewriter.writerow([i for i in range(0,len(uwm))])
            filewriter.writerow(uwm)
            filewriter.writerow(pwm)
            filewriter.writerow(cwm)
            filewriter.writerow(con)
            filewriter.writerow(bex)
            filewriter.writerow(ran)
        fig, ax1 = plt.subplots()
        ax1.set_xticks(range(0, len(self.rps_scores[0])))
        ax1.set_xticklabels(self.rps_scores[0])
        ax1.boxplot([uwm,pwm,cwm,con,bex,ran])
        plt.xticks([1, 2, 3, 4, 5, 6], self.rps_scores[0])
        plt.title('Algorithm Performance: RPS Boxplot')
        ax1.set_ylim([0,105])
        if(save):
            fig.savefig('Plots/'+self.name+"_MeanRPS.png")
        else:
            plt.show()

    def plotExpertPerformance(self, save=False):
        data_abs = np.mean(np.array(self.expertPerformance[0]), axis=0)
        data_rel = np.mean(np.array(self.expertPerformance[1]), axis=0)
        e = [i for i in range(0,len(data_abs))]
        zero = [0 for i in range(0,len(data_abs))]
        abs = data_abs
        abs_c = data_abs
        rel = data_rel
        abs, f = zip(*sorted(zip(abs, e)))
        abs_c, rel = zip(*sorted(zip(abs_c,rel)))
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        pwm_line, = ax1.plot(e, abs, 'g-', label="PWM Performance")
        cwm_line, = ax2.plot(e, rel, 'b-', label="CWM Performance")
        with open("./Data/" + self.name + "_ExpertPerformance.csv", mode="w") as file:
            filewriter = csv.writer(file, delimiter=";")
            filewriter.writerow(list(np.array(f)+1))
            filewriter.writerow(abs)
            filewriter.writerow(rel)
        zero_line, = ax2.plot(e, zero, 'k-')
        ax1.set_xticks(range(0, len(data_abs)))
        ax1.set_xticklabels(tuple(np.array(f)+1))
        ax1.invert_xaxis()
        ax1.set_xlabel('EXPERT INDEX')
        ax1.set_ylabel('ABSOLUTE', color='g')
        ax2.set_ylabel('RELATIVE', color='b')
        plt.title('Expert Performance: RPS vs. Contribution')
        plt.legend(handles=[pwm_line, cwm_line])
        #ax1.set_ylim([0,105])
        #ax2.set_ylim([-20,20])
        if(save):
            fig.savefig('Plots/'+self.name+"_ExpertPerformance.png")
        else:
            plt.show()

    def plotExpertWeights(self, save=False):
        data_abs = np.mean(np.array(self.expertWeights[0]), axis=0)
        data_rel = np.mean(np.array(self.expertWeights[1]), axis=0)
        e = [i for i in range(0,len(data_abs))]
        abs = data_abs
        abs_c = data_abs
        rel = data_rel
        abs, f = zip(*sorted(zip(abs, e)))
        abs_c, rel = zip(*sorted(zip(abs_c,rel)))
        fig, ax1 = plt.subplots()
        #ax2 = ax1.twinx()
        pwm_line, = ax1.plot(e, abs, 'g-', label="PWM Weight")
        cwm_line, = ax1.plot(e, rel, 'b-', label="CWM Weight")
        with open("./Data/" + self.name + "_ExpertWeights_all_for_cwm.csv", mode="w") as file:
            filewriter = csv.writer(file, delimiter=";")
            filewriter.writerow(list(np.array(f)+1))
            cwm = np.matrix.transpose(np.array(self.expertWeights[1]))
            for i in range(0, len(cwm)):
                filewriter.writerow(cwm[i])
        with open("./Data/" + self.name + "_ExpertWeights.csv", mode="w") as file:
            filewriter = csv.writer(file, delimiter=";")
            filewriter.writerow(list(np.array(f)+1))
            filewriter.writerow(abs)
            filewriter.writerow(rel)
        ax1.set_xticklabels(tuple(np.array(f)+1))
        ax1.invert_xaxis()
        ax1.set_xlabel('EXPERT INDEX')
        ax1.set_ylabel('WEIGHT')
        #ax2.set_ylabel('RELATIVE', color='b')
        plt.title('Expert Weights: PWM vs. CWM')
        #pwm_patch = mpatches.Patch(color='green', label='PWM Weight')
        #cwm_patch = mpatches.Patch(color='blue', label='CWM Weight')
        plt.legend(handles=[pwm_line,cwm_line])
        if(save):
            fig.savefig('Plots/'+self.name+"_ExpertWeights.png")
        else:
            plt.show()

    def plotCumulativeExpertWeights(self, save=False):
        data_abs = np.mean(np.array(self.expertWeights[0]), axis=0)
        data_rel = np.mean(np.array(self.expertWeights[1]), axis=0)
        data_uwm = [1/len(data_rel) for i in range(0,len(data_rel))]
        data_con = np.mean(np.array(self.expertWeights[2]), axis=0)
        #for i in range(0,len(data_con)):
        #    if data_con[i] > 0:
        #        data_con[i] = 1
        #data_con = [data_con[i]/sum(data_con) for i in range(0,len(data_con))]
        e = [i/len(data_abs) for i in range(0,len(data_abs)+1)]
        abs = sorted(data_abs,reverse=True)
        rel = sorted(data_rel,reverse=True)
        con = sorted(data_con,reverse=True)
        abs = [sum(abs[0:i]) for i in range(0,len(data_abs)+1)]
        rel = [sum(rel[0:i]) for i in range(0,len(data_rel)+1)]
        uwm = [sum(data_uwm[0:i]) for i in range(0,len(data_uwm)+1)]
        con = [sum(con[0:i]) for i in range(0,len(data_con)+1)]
        fig, ax1 = plt.subplots()
        pwm_line, = ax1.plot(e, abs, 'g-', label="PWM Weight")
        cwm_line, = ax1.plot(e, rel, 'b-', label="CWM Weight")
        uwm_line, = ax1.plot(e, uwm, 'r-', label="UWM Weight")
        con_line, = ax1.plot(e, con, 'c-', label="CON Weight")
        with open("./Data/" + self.name + "_CumulativeExpertWeights.csv", mode="w") as file:
            filewriter = csv.writer(file, delimiter=";")
            filewriter.writerow(e)
            filewriter.writerow(abs)
            filewriter.writerow(rel)
            filewriter.writerow(uwm)
            filewriter.writerow(con)
        plt.xticks(e)
        ax1.set_xticklabels(e)
        ax1.set_xlim([0,1])
        ax1.set_xlabel('% EXPERTS')
        ax1.set_ylabel('CUMULATIVE WEIGHT')
        ax1.set_ylim([0, 1.05])
        plt.title('Cumulative Expert Weights: PWM vs. CWM vs. UWM vs. CON')
        plt.legend(handles=[pwm_line,cwm_line, uwm_line, con_line],loc='upper center', bbox_to_anchor=(0.65, 0.2), fancybox=True, shadow=True, ncol=2)
        if(save):
            fig.savefig('Plots/'+self.name+"_CumulativeExpertWeights.png")
        else:
            plt.show()

    def plotBoxplotExpertWeights(self, save=False):
        pwm = np.matrix.transpose(np.array(self.expertWeights[0]))
        cwm = np.matrix.transpose(np.array(self.expertWeights[1]))
        con = np.matrix.transpose(np.array(self.expertWeights[2]))
        bex = np.matrix.transpose(np.array(self.expertWeights[3]))
        fig, ax1 = plt.subplots()
        fig.set_figwidth(20)
        e = []
        for i in range(1, len(cwm)+1):
            for j in range(0,6):
                if(j%6==0):
                    e.append("E"+str(i))
                else:
                    e.append("")
        ax1.set_xticklabels(e)
        loc1=np.arange(1,6*len(cwm), 6)
        loc2 = loc1+1
        #loc1 = loc1-0.2
        #loc2 = loc2-0.6
        loc3 = loc1+2
        loc4 = loc1+3
        bp1 = ax1.boxplot([cwm[i] for i in range(0,len(cwm))], positions=loc1, patch_artist=True)
        bp2 = ax1.boxplot([pwm[i] for i in range(0,len(pwm))], positions=loc2, patch_artist=True)
        bp3 = ax1.boxplot([con[i] for i in range(0,len(con))], positions=loc3, patch_artist=True)
        bp4 = ax1.boxplot([bex[i] for i in range(0,len(bex))], positions=loc4, patch_artist=True)
        for i in range(1, len(cwm)+1):
            plt.axvline(x=i*6, ymin=0, ymax = 1.2, linewidth=0.7, color='k',linestyle="--")
        #plt.axvline(x=5, ymin=0, ymax = 1.2, linewidth=1, color='k')
        plt.setp(bp1['boxes'], facecolor='red')
        plt.setp(bp2['boxes'], facecolor='cyan')
        plt.setp(bp3['boxes'], facecolor='yellow')
        plt.setp(bp4['boxes'], facecolor='green')
        plt.xticks(range(1,6*len(cwm)+1), e)
        plt.title('Expert Weights: Boxplot')
        ax1.set_ylim([0,1.1])
        ax1.set_xlim([-0.5,6*len(cwm)])
        #plt.legend(handles=[bp1,bp2,bp3,bp4],loc='upper center', bbox_to_anchor=(0.65, 0.2), fancybox=True, shadow=True, ncol=2)
        if(save):
            fig.savefig('Plots/'+self.name+"_BoxplotExpertWeights.png")
        else:
            plt.show()
