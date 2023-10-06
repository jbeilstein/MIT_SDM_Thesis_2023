import csv

from csv import writer

data_entry = ['component_id','component_title','parent_id','description','keyword1','keyword2','keyword3']
data_file = 'ontology.csv'

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close()   

data_entry = ['01','CANSat','','a satellite in a can','satellite','disposable','launched']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
              
data_entry = ['02','container','01','a small container to store items','cargo','equipment','enclosed']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 

data_entry = ['03','parachute','01','slows descent','colored','light','deployable']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['04','audio_beacon','02','emits a noise to aid recovery','audible','loud','repeating']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 