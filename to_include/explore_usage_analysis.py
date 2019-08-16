from pprint import pprint as pp
from lookerapi import LookerApi
import json
import csv
import requests
import yaml

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

lis = {}

def write_fields(explore,value):
	model,exp= explore.split(',')

	# ### compile the line - this is possible to combine above, but here to keep things simple
	rowout = []
	rowout.append(model)
	rowout.append(exp)
	rowout.append(value)


	w.writerow(rowout)

## --------- csv formatting -------------

csvfile= open('explore_analysis.csv', 'wb')

w = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
header = ['model',
			'explore',
			'count_queries']

w.writerow(header)



## -- Get all models --
models = looker.get_model("")
for model in models:
	model_name = model['name']

	## -- Get single model --
	model_def = looker.get_model(model_name)
	# pp(model_def)

	## -- Get single explore --
	for explore_def in model_def['explores']:
		# print(model_name + " " + explore_def['name'])
		explore_name = model_name+','+explore_def['name']
		lis[explore_name]=0

body = {
  "model":"i__looker",
  "view":"history",
  "fields":["query.view","query.model","history.query_run_count"],
  "filters":{"history.most_recent_run_at_date":"90 days"},
  # "sorts":["products.count desc 0"],
  "limit":"500",
  "query_timezone":"America/Los_Angeles"
}

res = looker.run_inline_query(body)
for exp in res:
	explore_name =  exp['query.model']+','+exp['query.view']
	lis[explore_name]=exp['history.query_run_count']

for i in list(lis.keys()):
	write_fields(i, lis[i])
