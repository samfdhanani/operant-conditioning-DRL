import os
import pandas as pd
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt


filelist = []
pathslist = []

datapath = os.path.normpath("/Users/samdhanani/Desktop/MuhleLab/Operant_Data_Folders/Cohort_Folder")
IDList = [1, 2, 3, 4]

for subdir, dirs, files in sorted(os.walk(datapath)):
    filelist.append(files)
    pathslist.append(subdir)

filelist.pop(0)
pathslist.pop(0)

def query(pathslist, querydate):  
    folderdates = []
    for x in pathslist:
        folderdates.append(os.path.basename(os.path.normpath(x))) #

    querypaths = []

    for i in range(0, len(folderdates)):
        if folderdates[i] == querydate:
            querypaths.append(pathslist[i]) 

    return(querypaths)

def data_pull(datapath, ID):
    
    for subdir, dirs, files in sorted(os.walk(datapath)):
        for file in files:
            temp = file.split('.')  
            sub = temp[1] 
            if ID == sub:
                x = os.path.join(subdir, file) 
                df = pd.read_csv(x, sep="[:\s]{1,}", skiprows=15, header=None, engine="python") 
                progline = pd.read_csv(x, skiprows=12, nrows = 1, header = None, engine="python")
                progline = progline.values.tolist()
                progline = progline[0][0].split(" ")
                if "_" in progline[1]:
                    progline = progline[1].split("_", 1) 
                progline = progline[1]
                df = df.drop(0,axis=1)
                df = df.stack()
                df = df.to_frame()
                df = df.to_numpy()

    try:
        return(df, progline) 
    except UnboundLocalError:
        df = []
        progline = None
        return(df, progline)   

def data_construct(data):

    events = np.remainder(data,10000) 
    times = data - events 

    StartTrial = times[np.where(events == 111)] 
    StartSess = times[np.where(events == 113)]
    EndSess = times[np.where(events == 114)]

    Sess_time = np.divide(np.subtract(EndSess, StartSess), 10000000)
    Sess_time = Sess_time.tolist() 
    Sess_time = Sess_time[0] 

    LLever = times[np.where(events == 27)]
    RLever = times[np.where(events == 28)]

    DipOn = times[np.where(events == 25)]
    DipOff = times[np.where(events == 26)]
    DipOff = DipOff.tolist()
    DipOff = DipOff[0]


    Lever_extensions = np.concatenate((LLever, RLever), axis = 0) 
    Lever_extensions = np.unique(Lever_extensions)  

    LLever_off = times[np.where(events == 29)]
    RLever_off = times[np.where(events == 30)]

    Reward = times[np.where(events == 25)]


    LPress = times[np.where(events == 1015)]
    RPress = times[np.where(events == 1016)]

    LeverPress = np.concatenate((LPress, RPress),axis=0)
    LeverPress = sorted(LeverPress)
    LeverPress = np.unique(LeverPress)
    
    
    rate = np.divide(len(LeverPress), Sess_time)
    rate = rate.tolist()
    x = 0

    LA = []

    for i in range (0, len(LeverPress)):
        p1 = np.divide(LeverPress[i], 10000000)
        try:
            p2 = np.divide(LeverPress[i+1], 10000000)
        except IndexError:
            break
        else:
            latency = p2 - p1
        LA.append(latency)
    
        def average_LA(LA_list):
            total = 0
            for i in LA_list:
                total += i
            return total/len(LA_list)
        
    Reward_Efficiency = np.divide(len(LeverPress), len(Reward))
    Reward_Efficiency = Reward_Efficiency.tolist()
    x = 0

    bursts = []
    burst_group = []

    for i in range(len(LA)):
    # Check if current value is less than or equal to 1 second
        if LA[i] <= 1:
            burst_group.append(LA[i])
        else:
            if len(burst_group) >= 1:
                bursts.extend(burst_group)  # Use extend instead of append to flatten the list
            burst_group = []

# After the loop ends, if there are any remaining latencies in the last burst_group, add them to the bursts list
    if len(burst_group) >= 1:
        bursts.extend(burst_group)

    bin_edges = np.arange(0, 1.1, 0.1)  # Create bin edges from 0 to 1 with a bin width of 0.1
    hist, _ = np.histogram(LA, bins=bin_edges)
    # Convert the histogram to a list
    binned_latencies = hist.tolist()

    average = average_LA(LA)
    print("The average of LA is:", average)
    print('Mouse - ', Full_ID)

    return(latency, average, Sess_time, len(Reward), len(LeverPress), rate, Reward_Efficiency, bursts, binned_latencies, LA)


def genotype(sub):
    # 1 = WT and 2 = Het
    g_type = None
    if sub == 1 or sub == 2:
        g_type = 'control'
    elif sub == 3 or sub == 4:
        g_type = 'experimental'

    return g_type

def sex(sub):
    s_type = None
    if sub == 1 or sub == 3:
        s_type = 'Male'
    elif sub == 2 or sub == 4:
        s_type = 'Female'

    return s_type

df_ind = 0 #index variable, add one everytime we run through a subject
sus_attn_df = pd.DataFrame(columns = ['Date', 'Subject', 'Program', 'Genotype', 'Sex', 'FirstLatency', 'AverageLatency', 'SessionTime', 'NumberOfRewards', 'Lever Press', 'Rate', 'Reward Efficiency', 'Burst','binned_latencies','all latency'])
def new_func(g_type, ID):
    g_type = genotype(ID)
    return g_type
def new_func(s_type, ID):
    s_type = sex(ID)
    return s_type

for dirs in pathslist:

    date = os.path.basename(os.path.normpath(dirs))
    csv_name = "\\" + date + ".csv"
    
    for ID in IDList: #run througb ID list one by one, add subj to this to prevent confusion
        Full_ID = "Subject " + str(ID)
        data, progline = data_pull(dirs, Full_ID) #calling datapull and putting it through dirs
        if len(data) == 0:
            continue
        latency, num_average, Sess_time, num_Rewards, num_LeverPress, rate, Reward_Efficiency, bursts,binned_latencies, LA = data_construct(data) #data construct, putting that all here
        g_type = genotype(ID)
        s_type = sex(ID)

        sus_attn_df.loc[df_ind] = [date, Full_ID, progline, g_type, s_type, latency, num_average, Sess_time, num_Rewards, num_LeverPress, rate, Reward_Efficiency, bursts, binned_latencies, LA ] #assigning variables one by one
        df_ind += 1 #location zero is populated with variables above, add one each time for it to be sequential

sus_attn_df.to_csv(datapath + "_Agg.csv")
