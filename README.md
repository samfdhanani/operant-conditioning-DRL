A massive thank you to [@Talaa202] for helping me write this code!

## Differential Reinforcement of Low Rate (DRL)
### Task Details
In the DRL assay the mice are presented with one lever the entire session which remained consistent throughout sessions. Training sessions began with a 2 second duration between lever presses and this duration increased by 2 seconds every 2 sessions until the duration between lever presses reached 14 seconds. Once the duration between lever presses was 14 seconds, the duration increased by 2 seconds every 3 days until the mice reached a 36 second duration. The mice then underwent 10 sessions at a 36 second duration between lever presses. Each session was programmed to end at 1 hour or 60 rewards, however, as the duration increased 60 rewards became impossible to reach, so that the sessions ended at 1 hour.  Of note, there was a disruption of the experiment for approximately 2 months due to a water leak in the room containing the operant boxes, the mice left off at the 26s duration session and returned to “reset” their DRL at the 22s duration session.
### Apparatus Information
The operant boxes were from Med Associates Inc. (Model 1820; Med Associates, St. Albans, VT) and MedScripts were used to run the program (Ward et al., 2015).

### Script Outputs

**DRL.py**

- Date: date of session
- Subject: subject number from the Med Associates data file
- Program: program name from the Med Associates data file
- Genotype: assigns a value to the subject based on a list defined by the user
- Sex: assigns a value to the subject based on a list defined by the user
- FirstLatency: the first lever press can be made within any time interval and is excluded in the rest of the latency measures
- AverageLatency: average latency between lever presses 
- SessionTime: total session time
- NumberOfRewards: number of rewards achieved
- Lever Press: total number of lever presses
- Rate: rate of lever presses per second
- Reward Efficiency: presses per reward
- Burst: lever press latencies less than a user defined time in seconds
- binned latencies: binned latencies within a user defined range
- all latency: a list of all latencies in the program

**BurstAnalysis.py**

- Date: date of session
- Subject: subject number from the Med Associates data file
- Genotype: assigns a value to the subject based on a list defined by the user
- Sex: assigns a value to the subject based on a list defined by the user
- FirstLatency: the first lever press can be made within any time interval and is excluded in the rest of the latency measures
- AverageLatency: average latency between lever presses 
- SessionTIme: total session time
- Program: program name from the Med Associates data file
- NumberOfRewards: number of rewards achieved
- no headpoke count: number of headpokes not made when a dipper was presented
- Lever Press: total number of lever presses
- Reward Rate: presses per reward
- lever press no reward: lever presses made within the designated time interval
- Rate (LP/SessTime): total lever presses divided by total session time
- all latency: a list of all latencies in the program
- plot: a list of the timestamps of latencies in seconds
- bursts: list of latencies under a certain time defined by the user
- number of bursts: number of bursts (defined as 2 or more presses under a time defined by a user)
- burst sums: total amount of time in each burst group
- average burst time: average of burst sums
- sum of all bursts: total bursting time
- average_burst_press_count: average presses in a burst

**BurstAnalysisAVG.py**

- calculates the average value across multiple session per subject
- calculates the averages for: the number of bursts, sum of all bursts, average burst time, average_burst_press_count

**Raster_All_GTandSex.py**
- creates a raster plot of all the lever presses made during a session
- creates raster plots based on date of the session and make sure to change the max_x_value based on your session time

