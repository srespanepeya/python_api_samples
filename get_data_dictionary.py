# -*- coding: UTF-8 -*-
import yaml
from peyalookerapi import PeyaLookerApi
from pprint import pprint as pp
import json
import csv
import requests

### ------- HERE ARE PARAMETERS TO CONFIGURE -------

host = 'peya-looker'

### ------- OPEN THE CONFIG FILE and INSTANTIATE API -------

f = open('config.yml')
params = yaml.load(f)
f.close()

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = PeyaLookerApi(host=my_host,token=my_token,secret = my_secret)


## --------- csv writing -------

def write_fields(explore, model_name =""):
# --------- csv formatting -------------
	csvfile= open('dictionary.csv', 'w',newline='')
	w = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)
	header = ['connection_name',
				'field_type',
				'project',
				'model',
				'explore',
				'view',
				'view_label',
				'name',
				'hidden',
				'label',
				'label_short',
				'description',
				'sql',
				'ftype',
				'value_format',
				'source']
	w.writerow(header)

	### First, compile the fields you need for your row
	explore_name = explore.name
	explore_model_name = model_name
	explore_fields=explore.fields
	WINDOWS_LINE_ENDING = '\r\n'
	UNIX_LINE_ENDING = '\n'
	try:
		connection_name = str(explore.connection_name)
	except:
		connection_name = ''
	
	for dimension in explore_fields.dimensions:
		#print(dimension)

		field_type = "Dimension"
		project = str(dimension.project_name)
		explore = str(explore_name)
		model = str(explore_model_name)
		view=str(dimension.view)
		view_label=str(dimension.view_label)
		name=str(dimension.name)
		hidden=str(dimension.hidden)
		label=str(dimension.label)
		label_short=str(dimension.label_short)
		description=str(dimension.description)
		sql=str(dimension.sql)
		ftype=str(dimension.type)
		value_format=str(dimension.value_format)
		source = str(dimension.source_file)

		### compile the line - this is possible to combine above, but here to keep things simple
		rowout = []	
		rowout.append(connection_name)
		rowout.append(field_type)
		rowout.append(project)
		rowout.append(model)
		rowout.append(explore)
		rowout.append(view)
		rowout.append(view_label)
		rowout.append(name)
		rowout.append(hidden)
		rowout.append(label)
		rowout.append(label_short)
		rowout.append(description)
		rowout.append(sql.replace(WINDOWS_LINE_ENDING,' ').replace(UNIX_LINE_ENDING,' ').replace('\"',"\\\\"))
		rowout.append(ftype)
		rowout.append(value_format)
		rowout.append(source)
		w.writerow(rowout)
	
	for dimension in explore_fields.measures:
    	#print(measuire)
		field_type = "Measures"
		project = str(dimension.project_name)
		explore = str(explore_name)
		model = str(explore_model_name)
		view=str(dimension.view)
		view_label=str(dimension.view_label)
		name=str(dimension.name)
		hidden=str(dimension.hidden)
		label=str(dimension.label)
		label_short=str(dimension.label_short)
		description=str(dimension.description)
		sql=str(dimension.sql)
		ftype=str(dimension.type)
		value_format=str(dimension.value_format)
		source = str(dimension.source_file)
		
		### compile the line - this is possible to combine above, but here to keep things simple
		rowout = []		
		rowout.append(connection_name)
		rowout.append(field_type)
		rowout.append(project)
		rowout.append(model)
		rowout.append(explore)
		rowout.append(view)
		rowout.append(view_label)
		rowout.append(name)
		rowout.append(hidden)
		rowout.append(label)
		rowout.append(label_short)
		rowout.append(description)
		rowout.append(sql.replace(WINDOWS_LINE_ENDING,' ').replace(UNIX_LINE_ENDING,' ').replace('\"',"\\\\"))
		rowout.append(ftype)
		rowout.append(value_format)
		rowout.append(source)
		w.writerow(rowout)

# ## --------- API Calls -------------
my_model_name = "prueba_Gitte"
my_explore_name = ""



## -- Get all models --
models = looker.get_models()
for model in models:
	model_name = model.name

	if model_name == "prueba_Gitte":
    		
    		
		print("-----------------------------------------------")
		#print(model)
		print(model_name)

		for explore in model.explores:
			#print(explore)
			explore_name = explore.name
			if explore_name =="fact_payment":
				print("--->Model:{0}---Explore:{1}".format(model_name,explore_name))
				super_explore = looker.get_model_explore(model_name,explore_name)
			 # try:
				write_fields(super_explore, model_name)
			# # except:
			# # 	print('Problem measure fields in ' + super_explore.name)
			# # try:
			# # 	write_fields(explore,'dimensions', model_name)
			# # except:
			# # 	print('Problem dimension fields in ' + explore_def['name'])
