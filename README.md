A massive thank you to Tala Sohrabi (@Talaa202) for teaching me and helping me write this code and to the Balsam-Simpson Lab at the New York State Psychiatric Institute for letting me borrow their Med Associate operant boxes!

## Differential Reinforcement of Low Rate (DRL)
### Task Details
In the DRL assay the mice are presented with one lever the entire session which remained consistent throughout sessions. Training sessions began with a 2 second duration between lever presses and this duration increased by 2 seconds every 2 sessions until the duration between lever presses reached 14 seconds. Once the duration between lever presses was 14 seconds, the duration increased by 2 seconds every 3 days until the mice reached a 36 second duration. The mice then underwent 10 sessions at a 36 second duration between lever presses. Each session was programmed to end at 1 hour or 60 rewards, however, as the duration increased 60 rewards became impossible to reach, so that the sessions ended at 1 hour.  Of note, there was a disruption of the experiment for approximately 2 months due to a water leak in the room containing the operant boxes, the mice left off at the 26s duration session and returned to “reset” their DRL at the 22s duration session.
### Apparatus Information
The operant boxes were from Med Associates Inc. (Model 1820; Med Associates, St. Albans, VT) and MedScripts were used to run the program (Ward et al., 2015).

### Script Outputs

**DRL.py**

'Date', 'Subject', 'Program', 'Genotype', 'Sex', 'First Latency', 'Average Latency', 'Session Time', 'Number Of Rewards', 'Total Lever Presses', 'Rate of Lever Presses per Second', 'Reward Efficiency', 'Burst Latencies','Binned Latencies','All Latencies', 'Missed Headpokes', 'Raster Plot Values'])

- Date: date of session
- Subject: subject number from the Med Associates data file
- Program: program name from the Med Associates data file
- Genotype: assigns a value to the subject based on a list defined by the user
- Sex: assigns a value to the subject based on a list defined by the user
- First Latency: the first lever press can be made within any time interval and is excluded in the rest of the latency measures
- Average Latency: average latency between lever presses 
- Session Time: total session time
- Number Of Rewards: number of rewards achieved
- Total Lever Presses: total number of lever presses
- Rate of Lever Presses per Second: rate of lever presses per second
- Reward Efficiency: presses per reward
- Burst Latencies: lever press latencies less than or equal to 1 second
- Binned Latencies: binned latencies from 0 to 1 second with a width of 0.1 seconds
- All Latencies: a list of all latencies in the program
- Headpokes Missed: number of times when there was no headpoke during dipper presentation
- Raster Plot Values: a list of the timestamps of latencies in seconds

**BurstAnalysis.py**

- Date: date of session
- Subject: subject number from the Med Associates data file
- Genotype: assigns a value to the subject based on a list defined by the user
- Sex: assigns a value to the subject based on a list defined by the user
- Program: program name from the Med Associates data file
- First Latency: the first lever press can be made within any time interval and is excluded in the rest of the latency measures
- Average Latency: average latency between lever presses 
- Session Time: total session time
- Number Of Rewards: number of rewards achieved
- Headpokes Missed: number of times when there was no headpoke during dipper presentation
- Lever Presses: total number of lever presses
- Reward Efficiency: presses per reward
- Lever Presses Made Without a Reward: lever presses made within the designated time interval
- Lever Presses per Second: total lever presses divided by total session time
- All Latencies: a list of all latencies in the program
- Raster Plot Values: a list of the timestamps of latencies in seconds
- Latencies Defined as a Burst: list of latencies under a certain time defined by the user
- Number of Bursts: number of bursts (defined as 2 or more presses under a time defined by a user)
- Individual Burst Sums: total amount of time in each burst group
- Average Burst Length: average of burst sums
- Sum of all Bursts: total bursting time
- Avg Presses in a Burst: average presses in a burst

**BurstAnalysisAVG.py**

- calculates the average value across multiple session per subject
- calculates the averages for: the number of bursts, sum of all bursts, average burst time, average_burst_press_count

**Raster_All_GTandSex.py**
- creates a raster plot of all the lever presses made during a session
- creates raster plots based on date of the session and make sure to change the max_x_value based on your session time

