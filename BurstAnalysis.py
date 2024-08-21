import os
import pandas as pd
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt

# declaring empty list
filelist = []
pathslist = []

datapath = os.path.normpath("filepath to cohort folder") #add filepath here
IDList = [1, 2, 3, 4] 
# list of subject IDs as labelled in MED-PC

# walks through the filepath, filelist contains a list of all files and pathslist contains datapaths for subfolders
for subdir, dirs, files in sorted(os.walk(datapath)):
    filelist.append(files)
    pathslist.append(subdir)

filelist.pop(0) # get rid of elements in index zero
pathslist.pop(0) # get rid of elements in index zero

# this function is used to isolate and analyze a specific folder/date from the data; run at the botton of this script
def query(pathslist, querydate): 
    folderdates = [] # stores dates from folder path
    for x in pathslist: # goes through each path in pathslist
        folderdates.append(os.path.basename(os.path.normpath(x))) # extracts the date from the filepath

    querypaths = [] # stores paths that match query dates

    for i in range(0, len(folderdates)):
        if folderdates[i] == querydate: 
            querypaths.append(pathslist[i]) # pull specific date

    return(querypaths)

# this function extracts data from each specific data file by ID 
def data_pull(datapath, ID):
    df = []
    progline = None
    
    for subdir, dirs, files in sorted(os.walk(datapath)): # 
        for file in files:
            temp = file.split('.') # split string by '.', in this case the string is split into the sesion date (0) and Subject ID (1)
            sub = temp[1] # Subject ID
            if ID == sub:
                x = os.path.join(subdir, file) # specific file
                df = pd.read_csv(x, sep="[:\s]{1,}", skiprows=15, header=None, engine="python") # skips 15 rows to where the data actually starts
                progline = pd.read_csv(x, skiprows=12, nrows = 1, header = None, engine="python") # reads only 1 row, the program line in the 12th row
                progline = progline.values.tolist()
                progline = progline[0][0].split(" ") 
                if "_" in progline[1]:
                    progline = progline[1].split("_", 1) # splits up program name if an underscore is present
                progline = progline[1]
                df = df.drop(0,axis=1) # cleaning up the data
                df = df.stack() 
                df = df.to_frame() 
                df = df.to_numpy() # dataframe should be an array of each line containing the data, removed the row labels from the data file 
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
    if DipOff:
        DipOff = DipOff[0]
    else:
        DipOff = None

    headpoke = times[np.where(events == 1011)]


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

# number of missed headpoke code
    headpoke_count = 0 # counts the number of headpokes
    within_dipper = False # tracks if dipper is active
    headpoke_occurred = False # tracks if headpoke happens

    for event in events:
        if event == 25:  # DipOn
            within_dipper = True 
        elif event == 26:  # DipOff
            within_dipper = False
            headpoke_occurred = False

        if within_dipper and event == 1011 and not headpoke_occurred:
            headpoke_count += 1
            headpoke_occurred = True

    no_headpoke_count = len(DipOn) - headpoke_count
    
# calculates lever press rate per second
    LP_rate = np.divide(len(LeverPress), Sess_time)
    LP_rate = LP_rate.tolist()
    x = 0
# calculates lever presses per reward
    Reward_rate = np.divide(len(LeverPress),len(Reward))
    Reward_rate = Reward_rate.tolist()
    x = 0
# calculates the number of lever presses made without a reward
    LP_noReward = np.subtract(len(LeverPress),len(Reward))
    LP_noReward = LP_noReward.tolist()
    x = 0

# calculating the latency array by finding the time in between lever presses until the last one when LeverPress[i+1] doesn't exist
    LA = [] # stores individual latencies

    for i in range (0, len(LeverPress)):
        p1 = np.divide(LeverPress[i], 10000000)
        try:
            p2 = np.divide(LeverPress[i+1], 10000000)
        except IndexError:
            break
        else:
            latency = p2 - p1 # next lever press - current lever press
        LA.append(latency) # add latency to LA
    
        def average_LA(LA_list):
            total = 0 # stores sum of all latencies
            for i in LA_list:
                total += i # adds latencies values to total
            return total/len(LA_list) # returns the avg by dividing the total by the number of latencies recorded

# calculates a list of the timestamps of latencies in seconds                
    plot = [latency + sum(LA[:i+1]) for i in range(len(LA))]

    LA_array = np.array(LA)

    bursts = [] # stores all latency values part of a burst 
    burst_group = [] # holds latency values part of the same burst

    for i in range(len(LA_array)):
    # Check if current value is between 1-2s or less than 1s
        if LA_array[i] >= 1 and LA_array[i] <= 2: # if LA_array[i] <= 1:
            burst_group.append(LA_array[i])
        else:
            if len(burst_group) >= 2:  # ensures that the burst is 2 or more in a row
                bursts.append(burst_group)
            burst_group = []

    if len(burst_group) >= 2:  # ensures that the burst is 2 or more in a row
        bursts.append(burst_group)

# calculates the sum of each burst group
    burst_sums = [sum(group) for group in bursts]
    
# calculates the sum of every latency classified as a burst
    sum_allburst = [sum(burst_sums)]

# finds the average of all burst sums, checks if there is a burst sum and returns an empty cell if there are no bursts found earlier
    if burst_sums:
        avg_allburst = [mean(burst_sums)]
    else:
        avg_allburst = []

# finds the number of presses made in each burst
    burst_press_counts = [len(group) for group in bursts]

# finds the average of lever presses made in a burst, returns 0 if there are no burst_press_counts found
    average_burst_press_count = mean(burst_press_counts) if burst_press_counts else 0 

# add code to get rid of extra brackets and unecessary punctuation here to allow values to be used in various calculations above
    burst_sums = str(burst_sums)[1:-1] 
    sum_allburst = str(sum_allburst)[1:-1] 
    avg_allburst = str(avg_allburst)[1:-1] 
    LA_array = str(LA_array)[1:-1]
    LA_array = LA_array.replace('\n', ' ')
    LA_array = ' '.join(LA_array.split())

    average = average_LA(LA)
    print("The average of LA is:", average)
    print('Mouse - ', Full_ID)
    print("Rewards - ", len(Reward))
    print("Headpoke - ", no_headpoke_count)

    return(latency, average, Sess_time, len(Reward), no_headpoke_count,len(LeverPress), Reward_rate, LP_noReward, LP_rate, LA_array, plot, bursts, len(bursts), burst_sums, avg_allburst, sum_allburst, average_burst_press_count)
 
# assigns a label for genotype to the subject
def genotype(sub):
    # 1 = WT and 2 = Het
    g_type = None
    if sub == 1 or sub == 2:
        g_type = 'WT'
    elif sub == 3 or sub == 4:
        g_type = 'Het'
    return g_type

# assigns a label for sex to the subject
def sex(sub):
    s_type = None
    if sub == 1 or sub == 3:
        s_type = 'M'
    elif sub == 2 or sub == 4:
        s_type = 'F'
    return s_type

# uncomment the line below to analyze one specific day in the data, date must match folder name
# pathslist = query(pathslist, '6-14-22')

df_ind = 0 # index variable, add one everytime we run through a subject

# comment the line below when running the script for one day only 
burst_df = pd.DataFrame(columns = ['Date', 'Subject', 'Genotype', 'Sex', 'Program', 'First Latency', 'Average Latency', 'Session Time',  'Number Of Rewards', 'Headpokes Missed','Lever Presses', 'Reward Efficiency', 'Lever Presses Made Without a Reward', 'Lever Presses per Second', 'All Latencies','Raster Plot Values','Latencies Defined as a Burst','Number of Bursts', 'Individual Burst Sums','Average Burst Length', 'Sum of all Bursts', 'Avg Presses in a Burst'])
def new_func(session_type, ID, progline):
    sess_type = session_type(progline, ID)
    return sess_type
def get_genotype(ID): # defines a function using ID and stores the genotype labels in g_type 
    g_type = genotype(ID)
    return g_type
def get_sex(ID): # defines a function using ID and stores the sex labels in s_type
    s_type = sex(ID)
    return s_type

for dirs in pathslist:

    date = os.path.basename(os.path.normpath(dirs))
    # uncomment the line below to analyze one specific day in the data
    # burst_df = pd.DataFrame(columns = ['Date', 'Subject', 'Genotype', 'Sex', 'Program', 'First Latency', 'Average Latency', 'Session Time',  'Number Of Rewards', 'Headpokes Missed','Lever Presses', 'Reward Efficiency', 'Lever Presses Made Without a Reward', 'Lever Presses per Second', 'All Latencies','Raster Plot Values','Latencies Defined as a Burst','Number of Bursts', 'Individual Burst Sums','Average Burst Length', 'Sum of all Bursts', 'Avg Presses in a Burst'])
    
    for ID in IDList: # run through ID list one by one, add 'Subject' to this to prevent confusion
        Full_ID = "Subject " + str(ID)
        data, progline = data_pull(dirs, Full_ID) # calling datapull and putting it through dirs
        if len(data) == 0:
            continue
        latency, num_average, Sess_time, num_Rewards, no_headpoke_count, num_LeverPress, Reward_rate, LP_noReward, LP_rate, LA_array, plot, bursts, num_bursts, burst_sums, sum_allburst, avg_allburst, average_burst_press_count = data_construct(data) #data construct, putting that all here
        g_type = genotype(ID)
        s_type = sex(ID)
        # comment the line below to analyze one specific day in the data
        burst_df.loc[df_ind] = [date, Full_ID, g_type, s_type, progline, latency, num_average, Sess_time, num_Rewards, no_headpoke_count , num_LeverPress, Reward_rate, LP_noReward, LP_rate, LA_array, plot, [lat for sublist in bursts for lat in sublist], num_bursts, burst_sums, sum_allburst, avg_allburst, average_burst_press_count] #assigning variables one by one
        df_ind += 1 # location zero is populated with variables above, add one each time for it to be sequential

    # uncomment the line below to analyze one specific day in the data
    # burst_df.to_csv(dirs + csv_name)

# comment the line below to analyze one specific day in the data
burst_df.to_csv(datapath + "burst_Xs.csv")
