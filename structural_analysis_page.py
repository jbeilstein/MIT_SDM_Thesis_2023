import math
import matplotlib.pyplot as plot
import pandas as pd

###This section will analyze individual pages
data_file = 'data.csv'

dataframe = pd.read_csv(data_file,sep=',')

unique_pages = dataframe['page_id'].unique()

select_page = unique_pages[7]

temp_dataframe = dataframe.loc[(dataframe['page_id'] == select_page)]

start_hist = temp_dataframe.hist(column = 'x_start', bins = 50)
graph = plot.savefig('page_x_start_histogram.jpg')
start_hist = temp_dataframe.hist(column = 'y_start', bins = 100, orientation = 'horizontal')
graph = plot.savefig('page_y_start_histogram.jpg')

stop_hist = temp_dataframe.hist(column = 'x_stop', bins = 50)
graph = plot.savefig('page_x_stop_histogram.jpg')
stop_hist = temp_dataframe.hist(column = 'y_stop', bins = 100, orientation = 'horizontal')
graph = plot.savefig('page_y_stop_histogram.jpg')
