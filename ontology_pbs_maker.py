import csv

from csv import writer

data_entry = ['component_id','component_title','parent_id','description','keyword1','keyword2','keyword3']
data_file = 'ontology.csv'

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close()   

data_entry = ['00','cansat/payload/probe','','A small satellite containing cargo and electronics','satellite','probe','payload']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['01','audio_beacon','00','emits a noise to aid recovery','audible','loud','sound']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
              
data_entry = ['02','camera','00','a small camera to record the parts of the mission','video','recorder','movie']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['03','data/kinematics/telemetry','00','the type of information recorded and how that information is formatted and transmitted','telemetry','data','kinematics']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['04','egg/compartment','00','the cargo to be transported and cannot be broken','breakable','carried','survive']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['05','electrical','00','the electrical and electronic subsystems','power','wires','connectors']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['06','ground_station','','sends commands and receives telemetry','computer','portable','processing']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['07','heat_shield','00','protects the cansat from friction and heat','deployable','detachable','protective']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['08','materials/mechanical','00','all mechanical equipment located on the craft','materials','structure','gear']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['9','nose_cone','00','protects rocket during ascent','top','light','deployable']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['10','parachute','00','slows the system during the descent phase','colored','light','deployable']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['11','radio','06','transmits telemetry to and from the craft and the ground station','receive','transmit','information']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['12','rocket','00','propels the craft into the sky','explosive','velocity','acceleration']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['13','sensors','00','collect information on the environment or system states','measure','collect','record']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 
    
data_entry = ['14','software','06','provides commands to the system in order to perform actions','code','instructions','program']

with open(data_file,'a',encoding = "utf-8",newline = '') as object:
    write_object = writer(object)
    write_object.writerow(data_entry)
    object.close() 