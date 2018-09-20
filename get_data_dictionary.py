# -*- coding: UTF-8 -*-
import yaml
from lookerapi import LookerApi
from pprint import pprint as pp
import json
import csv
import requests

### ------- HERE ARE PARAMETERS TO CONFIGURE -------

host = 'localhost'

### ------- OPEN THE CONFIG FILE and INSTANTIATE API -------

f = open('config.yml')
params = yaml.load(f)
f.close()

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = LookerApi(host=my_host,
                 token=my_token,
                 secret = my_secret)


## --------- csv writing -------

def write_fields(explore, fields, model_name =""):

	### First, compile the fields you need for your row

	explore_fields=explore['fields']
	try:
		connection_name = str(explore['connection_name'])
	except:
		connection_name = ''
	for dimension in explore_fields[fields]:
		# print dimension

		field_type = fields
		project = str(dimension['project_name'])
		explore = str(explore_def['name'])
		model = str(model_name)
		view=str(dimension['view'])
		view_label=str(dimension['view_label'])
		name=str(dimension['name'])
		hidden=str(dimension['hidden'])
		label=str(dimension['label'])
		label_short=str(dimension['label_short'])
		description=str(dimension['description'])
		sql=str(dimension['sql'])
		ftype=str(dimension['type'])
		value_format=str(dimension['value_format'])
		source = str(dimension['source_file'])

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
		rowout.append(sql)
		rowout.append(ftype)
		rowout.append(value_format)
		rowout.append(source)

		w.writerow(rowout)

## --------- csv formatting -------------

csvfile= open('dictionary.csv', 'w')

w = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
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

## --------- API Calls -------------

## -- Get all models --
models = looker.get_model("")
pp(models)
for model in models:
	model_name = model['name']

	## -- Get single model --
	model_def = looker.get_model(model_name)
	# pp(model_def)

	## -- Get single explore --
	for explore_def in model_def['explores']:
		explore=looker.get_explore(model_name, explore_def['name'])
		# pp(explore)
		## -- parse explore --

		try:
			write_fields(explore,'measures', model_name)
		except:
			print('Problem measure fields in ' + explore_def['name'])
		try:
			write_fields(explore,'dimensions', model_name)
		except:
			print('Problem dimension fields in ' + explore_def['name'])
