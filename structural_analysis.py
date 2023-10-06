
#Now that the pdf is extracted it will attempt to determine relational information between different pdf text boxes
#The 

import math
import matplotlib.pyplot as plot
import pandas as pd


data_file = 'data.csv'

dataframe = pd.read_csv(data_file,sep= ',')

start_hist = dataframe.hist(column = 'x_start', bins = 50)
graph = plot.savefig('x_start_histogram.jpg')
start_hist = dataframe.hist(column = 'y_start', bins = 100, orientation = 'horizontal')
graph = plot.savefig('y_start_histogram.jpg')

stop_hist = dataframe.hist(column = 'x_stop', bins = 50)
graph = plot.savefig('x_stop_histogram.jpg')
stop_hist = dataframe.hist(column = 'y_stop', bins = 100, orientation = 'horizontal')
graph = plot.savefig('y_stop_histogram.jpg')

for i, row in dataframe.iterrows():
    if row[0] != '' and row[0] != 'id_num' and math.isnan(row[0]) != True:
        current_id = row[0]
        current_page = row[1]        
        text = row[15]
        itemized = False
        temp_dataframe = dataframe[dataframe['page_id']==current_page]
        #This section will go through the dataframe again to compare
        for temp_index, temp_row in temp_dataframe.iterrows():
            temp_id = temp_row[0]
            temp_page = temp_row[1] 
            if temp_id != current_id:
                current_coord1 = row[3]
                current_coord2 = row[4]
                current_coord3 = row[5]
                current_coord4 = row[6]
                temp_coord1 = temp_row[3]
                temp_coord2 = temp_row[4]
                temp_coord3 = temp_row[5]
                temp_coord4 = temp_row[6]

                #This section will attempt to determine if there is a table which is associating text with some form of identifier, such as a requirement number.  i.e.  "Req 1    Requirements shall be recorded"
                if current_coord1 >= temp_coord3:                
                    #Getting here implies that the current text field is to the right of the temporary field    
                    # if current_coord2 >= temp_coord2 and current_coord4 <= temp_coord4:
                    if current_coord4 == temp_coord4:
                    #This is for top justified formatting
                        current_association = row[9]
                        #Check if current association exists. If so, append. Else, set association to current value
                        if isinstance(current_association,str) == True:
                            current_association = str(current_association) + "/" + str(temp_id) 
                        else:
                            current_association = str(temp_id) 
                        row[9] = current_association
                        dataframe.loc[i,"associated_with"] = current_association
                        # if isinstance(temp_association,str) == True:
                        #     temp_association = str(temp_association) + "/" + str(current_id) 
                        # else:
                        #     temp_association = str(current_id) 
                        # temp_row[14] = temp_association
                        
dataframe.to_csv('structure.csv', index = False)


