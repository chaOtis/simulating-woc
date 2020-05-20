import matplotlib.pyplot as plt
import numpy as np
import csv

def plotOptimalSigma_InfoCount(data, name, save=False):
    fig, ax1 = plt.subplots()
    line, = ax1.plot(range(0,len(data)), data, 'g-')
    ax1.set_xlabel('Amount of Information')
    ax1.set_ylabel('Optimal Sigma')
    plt.xticks(range(0,len(data)))
    plt.title('Optimal Sigma for Several Amounts of Information')
    with open('Plots/'+name+'_OptimalSigma_Bias0.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        spamwriter.writerow(range(0,len(data)))
        spamwriter.writerow(data)
    if(save):
        fig.savefig('Plots/'+name+"_OptimalSigma_Bias0.png")
    else:
        plt.show()

def plotOptimalSigma_Bias_InfoCount(data, name, save=False):
    x = [-0.5+y*0.1 for y in range(0,len(data))]
    colors = plt.cm.gist_rainbow(np.linspace(0, 1, 4))
    fig, ax1 = plt.subplots()
    handles = []
    info = [0,1,5,10]
    max1 = 6
    for i in range(0,len(data[0])):
        data1 = []
        for j in range(0,len(data)):
            data1.append(data[j][i])
        if(i==1):
            max1 = max(data1)+1
        line1, = ax1.plot(x,data1, color=colors[i%len(colors)], label="Info= "+str(info[i]))
        handles.append(line1)
    ax1.set_xlabel('Bias')
    ax1.set_ylabel('Optimal Sigma')
    ax1.set_ylim([0,max1])
    plt.xticks(x)
    plt.title('Optimal Sigma for Several Amounts of Information and Bias')
    plt.legend(handles=handles, loc='upper center', fancybox=True, shadow=True, ncol=4)
    with open('Plots/'+name+'_OptimalSigma_All.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        spamwriter.writerow(x)
        for i in range(0,len(data[0])):
            data1 = []
            for j in range(0,len(data)):
                data1.append(data[j][i])
            spamwriter.writerow(data1)
    if(save):
        fig.savefig('Plots/'+name+"_OptimalSigma_All.png")
    else:
        plt.show()

def plotStructuralBreak(data, t, name, save=False, conf=None):
    if(conf == None):
        uwm = [x[0] for x in data]
        pwm = [x[1] for x in data]
        cwm = [x[2] for x in data]
        con = [x[3] for x in data]
        bex = [x[4] for x in data]
        fig, ax1 = plt.subplots()
        plt.xticks(t)
        ax1.set_xticklabels(t)
        uwm_line, = ax1.plot(t, uwm, 'g-', label="UWM")
        pwm_line, = ax1.plot(t, pwm, 'b-', label="PWM")
        cwm_line, = ax1.plot(t, cwm, 'r-', label="CWM")
        con_line, = ax1.plot(t, con, 'c-', label="CON")
        bex_line, = ax1.plot(t, bex, 'm-', label="BEX")
        plt.title('Algorithm Performance: Structural Break at time t')
        ax1.set_xlabel('Time of Structural Break')
        ax1.set_ylabel('Mean RPS')
        ax1.set_xlim([min(t),max(t)])
        ax1.set_ylim([40,100])
        plt.legend(handles=[uwm_line, pwm_line, cwm_line, con_line, bex_line], loc='upper center', fancybox=True, shadow=True, ncol=2) # insert pwm_line here, if necessary
        with open('Data/'+name+'_StructuralBreak.csv', 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';')
            spamwriter.writerow(t)
            spamwriter.writerow(uwm)
            spamwriter.writerow(pwm)
            spamwriter.writerow(cwm)
            spamwriter.writerow(con)
            spamwriter.writerow(bex)
        if(save):
            fig.savefig('Plots/'+name+"_StructuralBreak.png")
        else:
            plt.show()
    else:
        conf_trans = np.transpose(np.array(conf), axes=list([1,0,2]))
        conf_trans_inf = np.transpose(np.array(conf), axes=list([2,1,0]))[0]
        conf_trans_sup = np.transpose(np.array(conf), axes=list([2,1,0]))[1]
        uwm = [x[0] for x in data]
        cwm = [x[2] for x in data]
        fig, ax1 = plt.subplots()
        plt.xticks(t)
        ax1.set_xticklabels(t)
        uwm_line, = ax1.plot(t, uwm, 'g-', label="UWM")
        cwm_line, = ax1.plot(t, cwm, 'r-', label="CWM")
        plt.title('Algorithm Performance: Structural Break at time t')
        ax1.set_xlabel('Time of Structural Break')
        ax1.set_ylabel('Mean RPS')
        ax1.set_xlim([min(t),max(t)])
        ax1.set_ylim([40,100])
        ax1.fill_between(t, conf_trans_inf[0], conf_trans_sup[0], color='#00ff80', interpolate=True)
        ax1.fill_between(t, conf_trans_inf[2], conf_trans_sup[2], color='#ff8000', interpolate=True)
        plt.legend(handles=[uwm_line, cwm_line], loc='upper center', fancybox=True, shadow=True, ncol=2) # insert pwm_line here, if necessary

        with open('Data/'+name+'_StructuralBreak_ConfInterval.csv', 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';')
            spamwriter.writerow(t)
            spamwriter.writerow(uwm)
            spamwriter.writerow(conf_trans[0])
            spamwriter.writerow(cwm)
            spamwriter.writerow(conf_trans[2])
        if(save):
            fig.savefig('Plots/'+name+"_StructuralBreak_ConfInterval.png")
        else:
            plt.show()


def plotStructuralBreakWeights(data, t, name, save=False, algo="cwm"):
    index = 1 if algo=="cwm" else 0
    colors = plt.cm.prism(np.linspace(0, 1, len(data[0][index][0])))
    fig, ax1 = plt.subplots()
    weights = []
    for i in range(0,len(data)):
        helper = np.mean(np.array(data[i][index]), axis=0)
        weights.append(helper)
    bottom=None
    handles=[]
    for i in range(0,len(weights[0])):
        helper = [weights[j][i] for j in range(0,len(weights))]
        handles.append(ax1.bar(t, helper, color=colors[i%len(colors)], bottom=bottom)[0])
        if(bottom is None):
            bottom=helper
        else:
            bottom=np.asarray(bottom)+np.asarray(helper)
    plt.title('Expert Weights depending on Time of Structural Break')
    ax1.set_xlabel('Time of Structural Break')
    ax1.set_ylabel('Weight')
    ax1.set_xlim([min(t),max(t)+1])
    ax1.set_ylim([0,1])
    plt.legend(handles, ["E"+str(i) for i in range(1,len(data[0][index][0])+1)])
    if(save):
        fig.savefig('Plots/'+name+"_StructuralBreakWeights_"+algo+".png")
    else:
        plt.show()

def plotOptimalSigma_RPS_InfoCount(data, name, save=False):
    csvfile = open('Data/' + name + '_DeviationOptimalSigma.csv', 'w')
    spamwriter = csv.writer(csvfile, delimiter=';')
    colors = plt.cm.gist_rainbow(np.linspace(0, 1, 4))
    fig, ax1 = plt.subplots()
    handles = []
    info = [1,2,3]
    for i in range(0,len(data)):
        data1 = [[],[]]
        for j in range(0, len(data[i][0])):
            if j+1 < len(data[i][0]) and data[i][0][j+1]+data[i][2][0] < 0:
                pass
            elif data[i][0][j] <= 0 and data[i][0][j+1] > 0:
                data1[0].append(0)
                data1[1].append(data[i][2][1])
            else:
                data1[0].append(data[i][0][j])
                data1[1].append(data[i][1][j])
        line1, = ax1.plot(data1[0],data1[1], color=colors[i%len(colors)], label="Info= "+str(info[i]))
        spamwriter.writerow(data1[0])
        spamwriter.writerow(data1[1])
        handles.append(line1)
    csvfile.close()
    ax1.set_xlabel('Delta Optimal Sigma')
    ax1.set_ylabel('RPS')
    ax1.set_ylim([0,110])
    ax1.set_xlim([min([min(data[i][0]) for i in range(0,len(data))]), max([max(data[i][0]) for i in range(0,len(data))])])
    plt.xticks(data[0][0])
    plt.axvline(x=0, linewidth=0.5, color='k',linestyle="--")
    plt.axhline(y=100, linewidth=0.5, color='k',linestyle="--")
    plt.title('RPS for Deviation from Optimal Sigma')
    plt.legend(handles=handles, loc='lower center', fancybox=True, shadow=True, ncol=4)
    if(save):
        fig.savefig('Plots/'+name+"_DeviationOptimalSigma.png")
    else:
        plt.show()