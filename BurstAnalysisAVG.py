import os
import pandas as pd
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt

datapath = "/filepath/data.csv"  
avg_df = pd.read_csv(datapath)

# List of columns to calculate averages for
averages = ['number of bursts', 'sum of all bursts', 'average burst time','average_burst_press_count']

for column in averages:
    if avg_df[column].dtype == 'object': # selects columns that match the names in averages
        avg_df[column] = avg_df[column].str.replace(r'[^0-9.]', '', regex=True) # in case brackets are left in the data this works around that, anything not a digit or period is removed
        avg_df[column] = pd.to_numeric(avg_df[column], errors='coerce') # turns string into numeric data

# group data by the following columns and then calculate the average for each group
avg_df = avg_df.groupby(['Program', 'Subject', 'Genotype', 'Sex'])[averages + ['Date']].agg({'Date': 'first', **{col: 'mean' for col in averages}}).reset_index()

csv_filepath = "/filepath/Cohort_AVGTEST.csv"

avg_df.to_csv(csv_filepath, index=False)

print(avg_df)
