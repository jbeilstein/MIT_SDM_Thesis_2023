###############################################################################################################################################################

#Author: John Beilstein
#This project was developed under the advisement of Dr. Eric Rebentisch, Ph.D.
#Special thanks to Dr. Johannes Norheim for providing feedback and guidance
#Massachusetts Institute of Technology, System Design and Management Program, 2023.
#This algorithm will load an ontology model from an .OWL and compare it to a requirements document.  You will need these two files to meet the description below:

#Note to the user: I apologize for the terrible code you are about to see, I'm not a computer scientist.

###############################################################################################################################################################

#The following packages must be installed for this algorithm to work:
#pip install matplotlib
#pip install numpy
#pip install pandas 
#pip install sentence_transformers
#pip install spacy

import csv
import math
import pandas as pd
import spacy
import sys

##Parts of the following code are derived from https://www.sbert.net/docs/pretrained_models.html and was accessed on 20 Oct 2023
from sentence_transformers import SentenceTransformer, util

import time
start = time.time()

###############################################################################################################################################################
#Instructions:

#The first file required by the system is the requirements document.  This document must be a .csv file and located in the same directory as this file.
#The document must have columns formatted in the following fashion:
# <req_id> <text> <entry_type> <ontology node name 1> <ontology node name 2> ... <ontology node name n>
# For the <req_id> column, the column header must be "req_id".  Every requirement must have a unique requirement identifier, and these must be integers.
# For the <text> column, the column header must be "text".  Every requirement statement can go into this column and must be in a string format.
# For the <entry_type> column, the column name must be "entry_type".  In its current configuration the algorithm will only analyze "individual" text requirements
# and will ignore "block" style requirement entries.  The purpose of this is to categorize requirements found in paragraphs or "blocks" as well as standalone or
# "individual" requirements. 
# For the <ontology node name x> there must be a column entry for every class (or node) in the .OWL model being imported.  The name of the class must match the name of the 
# column in the .csv file.  Under each column, the user must place a boolean "true" if that ontology node is related to that requirement statement.  
input_requirements_document = 'data2024_final.csv'

#The second required file is ontology model.  This file must be in a .OWL file format.
input_ontology_model = 'ontology_model.owl' 

# This section allows you to pick a specific requirement you wish to have analyzed.  After the requirement document has been evaluated, information pertaining to the desired requirement 
# number will be returned.  If you are using the default requirement document, please note that requirements #1, 4, 12, 48, 55, 93, 100, and 108 will not work.  These are blocks of text
# which contain requirements as well as non-requirement material.  As these blocks of text have non-requirement material they are not processed in the code's current configuration.
requirement_of_interest = 84

# These thresholds allow you to determine what the algorithm uses as a minimum semantic similarity score to declare a relationship between an ontology node and a requirement.
initial_semantic_threshold = 0.45 #WARNING: it is not recommended to set this lower than 0.40 unless you comment out the weighted_pathing_tool() function on line 91 below.
reevaluation_semantic_threshold = 0.40 #This is the threshold to re-evaluate nodes adjacent to nodes with high semantic similarity

# The last user input is a boolean value as to whether the analysis has already been completed or if this is the first time running the import, comparison, and 
# analysis process.  If you've already run the code completely and haven't made any changes to your requirements document or the ontology, you can set this to 
# "True" and speed up the process.
analysis_complete = False

###############################################################################################################################################################
#It's not recommended to change anything below this point

if (int(requirement_of_interest) == 1) or (int(requirement_of_interest) == 4) or (int(requirement_of_interest) == 12) or (int(requirement_of_interest) == 48) or (int(requirement_of_interest) == 55) or (int(requirement_of_interest) == 93) or (int(requirement_of_interest) == 100) or (int(requirement_of_interest) == 108):
    print('Requirements #1, 4, 12, 48, 55, 93, 100, and 108 will are not processed as they are blocks of text which also include non-requirement material.  If you are still interested in the material in that requirement, please select one of the individual requirement statements immediately following the requirement of interest.')
else:
    from final_ontology_importer import ontology_importer
    from final_comparison_req_to_req_with_semantics import requirement_to_requirement_comparison_tool
    from final_ontology_mapper import ontology_mapper
    from final_comparison_req_to_ont_with_semantics import requirement_to_ontology_comparison_tool
    from final_req_to_ontology_score_visualizer import requirement_to_ontology_score_visualizer
    from final_req_to_req_score_visualizer import requirement_to_requirement_score_visualizer
    from final_scores_to_pathing import adjacent_node_recommender
    from final_scores_to_pathing import weighted_pathing_tool
    from final_result_compiler import requirement_result_compiler

    if analysis_complete == False:
        ontology_importer(input_ontology_model)
        ontology_mapper
        requirement_to_requirement_comparison_tool(input_requirements_document)
        requirement_to_ontology_comparison_tool(input_requirements_document)
        requirement_to_ontology_score_visualizer(input_requirements_document) #allows the user to see how requirements semantically compare to ontology nodes
        requirement_to_requirement_score_visualizer(input_requirements_document) #allows the user to see how requirements semantically compare to each other
        adjacent_node_recommender(input_requirements_document, initial_semantic_threshold, reevaluation_semantic_threshold) #Will recommend nodes adjacent to high semantic similarity nodes based on the second semantic threshold
        
        ##WARNING: Do not use this with low semantic similarity thresholds (less than 0.40) as computation time required will be extremely high.  If lower semantic thresholds
        #are desired to analyze the other modules, comment out this line.  If pathing is desired at lower semantic thresholds this may need to run over night or on a cluster
        weighted_pathing_tool() #Cycles through requirements with multiple high semantic similarity nodes.  Finds the highest semantic similarity pathways between those nodes
        
    #This section will compile the results and store them in "final_output_compiled_results.txt"    
    f = open("final_output_compiled_results.txt",'w')
    sys.stdout = f

    requirement_result_compiler(input_requirements_document, requirement_of_interest, initial_semantic_threshold, reevaluation_semantic_threshold)

    f.close
        
    print(' ')
    print('This process took ' + str(time.time()-start) + ' seconds to complete')
