## Differential Reinforcement of Low Rate (DRL)
### Task Details
In the DRL assay the mice are presented with one lever the entire session which remained consistent throughout sessions. Training sessions began with a 2 second duration between lever presses and this duration increased by 2 seconds every 2 sessions until the duration between lever presses reached 14 seconds. Once the duration between lever presses was 14 seconds, the duration increased by 2 seconds every 3 days until the mice reached a 36 second duration. The mice then underwent 10 sessions at a 36 second duration between lever presses. Each session was programmed to end at 1 hour or 60 rewards, however, as the duration increased 60 rewards became impossible to reach, so that the sessions ended at 1 hour.  Of note, there was a disruption of the experiment for approximately 2 months due to a water leak in the room containing the operant boxes, the mice left off at the 26s duration session and returned to “reset” their DRL at the 22s duration session.
### Apparatus Information
The operant boxes were from Med Associates Inc. (Model 1820; Med Associates, St. Albans, VT) and MedScripts were used to run the program (Ward et al., 2015).
### Script Outputs
The script outputs a csv file with the following data:
- subject number from the Med Associates data file
- program name from the Med Associates data file
- session type, might exclude
- genotype, needs to be defined in the code by the user
- first latency, the first lever press can be made within any time interval and is excluded in the rest of the latency measures
- average latency to press the lever
- total session time
- number of rewards achieved
- total number of lever presses
- rate of lever presses per second
- reward efficiency, presses per reward
- bursts, lever press latencies less than a user defined time in seconds
- binned latencies within a user defined range
- a list of all latencies in the program


