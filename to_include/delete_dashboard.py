import sys
import os
import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint 


### ------- HERE ARE PARAMETERS TO CONFIGURE -------

dashboards_to_delete = sys.argv[1]
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


### ------- HANDLE ARGUMENT FILELIST OR SINGLE LOOK -------

if os.path.isfile(dashboards_to_delete):
	filelist = open(dashboards_to_delete)
	for i in filelist:
		print "deleting dashboard id: " + i
		data = looker.delete_dashboard(i)
		pprint(data)
else:
	data = looker.delete_dashboard(dashboards_to_delete)
	pprint(data)

### ------- Done -------

print "Done"

