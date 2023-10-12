
#This module will create a truth DSM based on the interconnectedness of the various sub components of the CANSat system

import math
import matplotlib.pyplot as plot
import numpy as np
import pandas as pd


data_file = 'data2024_cleaned.csv'

dataframe = pd.read_csv(data_file,sep= ',')

dsm = pd.DataFrame(np.nan, index = ['audio_beacon','camera','cansat/payload/probe','data/kinematics/telemetry','egg/compartment','electrical','ground_station','heat_shield','materials/mechanical','nose_cone','parachute','radio','rocket','sensors','software'],columns=['audio_beacon','camera','cansat/payload/probe','data/kinematics/telemetry','egg/compartment','electrical','ground_station','heat_shield','materials/mechanical','nose_cone','parachute','radio','rocket','sensors','software'])
ontology_list = ['audio_beacon','camera','cansat/payload/probe','data/kinematics/telemetry','egg/compartment','electrical','ground_station','heat_shield','materials/mechanical','nose_cone','parachute','radio','rocket','sensors','software']
index_i = 1

#Each item within the ontology is compared to how many times it is referenced in a section with another piece of the ontology
for i in ontology_list:
    temp_dataframe_i = dataframe[dataframe[i]==True]
    index_j = 1
    for j in ontology_list:
        if i != j:
            temp_dateframe_j = temp_dataframe_i[temp_dataframe_i[j]==True]
            if temp_dateframe_j.empty:
                count = 0
            else:
                count = temp_dateframe_j.shape[0]
            dsm.at[i,j] = int(count)
        index_j = index_j + 1
    index_i = index_i + 1
                        
dsm.to_csv('dsm_truth.csv', index = False)


