import csv
import matplotlib.pyplot as plt
import ast
import math
from matplotlib.backends.backend_pdf import PdfPages
import os

# Read data from CSV file
csv_file = "filepath/data.csv"
plot_date = "02-23-24"  # Specify date you want to plot
x = 2500  # Maximum value for the x-axis

pdf_file_path = "/Users/samdhanani/Desktop/06-05-24.pdf"
pdf_pages = PdfPages(pdf_file_path)

with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    groups_dict = {} # to store a group of data classified genotype and sex

    for row in reader: # goes through every row
        if row['Date'] == plot_date: # makes sure date matches the plot date
            genotype_sex = (row['Genotype'], row['Sex']) # makes a list of the genotype and sex columns
            if genotype_sex not in groups_dict: # add lists of not in the dictionary
                groups_dict[genotype_sex] = [] 
            groups_dict[genotype_sex].append(row) # current add row to list depending on genotype and sex

    with PdfPages(pdf_file_path) as pdf_pages:
        # Generate plots for each group
        for genotype_sex, subjects in groups_dict.items(): # goes through each group with corresponding subjects
            num_rows = math.ceil(len(subjects) / 2) # finds number of rows for subplots with two plots per row
            num_cols = min(len(subjects), 2) # sets column to the length of the number of subjects or two, whichever is less
            fig, axs = plt.subplots(num_rows, num_cols, figsize=(20, 10 * num_rows)) # adjust figure size based on rows
            genotype, sex = genotype_sex
            fig.suptitle(f'{genotype} - {sex} - {plot_date}', fontsize=14) # title of plots

            for i, subject in enumerate(subjects): # loops through each subject within a group
                event_occurrences = ast.literal_eval(subject['Raster Plot Values']) # converts csv data to a list of lists
                row_idx = i // num_cols # calculates indices
                col_idx = i % num_cols
                axs[row_idx, col_idx].eventplot(event_occurrences, lineoffsets=0.2, linelengths=0.1, linewidths=0.5) # plots event occurences
                axs[row_idx, col_idx].set_xlabel('Time') # labels
                axs[row_idx, col_idx].set_ylabel('Event')
                axs[row_idx, col_idx].set_title(subject['Subject'])
                axs[row_idx, col_idx].set_yticks([])
                axs[row_idx, col_idx].grid(True)
                axs[row_idx, col_idx].set_xlim(0, x) 

            fig.subplots_adjust(hspace=0.7, wspace=0.08, left=0.015, right=0.987) # adjust spacing between subplots for formatting
            
            pdf_pages.savefig()
