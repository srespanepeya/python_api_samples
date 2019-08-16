import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint
import json
import re

###############
# This script builds a list of all schedules for all users
# and deletes schedules that have an expiry date specified
# in the title.  Checks for format "DELETE:YYYY-MM-DD" in
# title, which can be changed in line 58
##############

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


### ------- GET ALL USERS -------

userlistarray = looker.get_all_users()
userlist = []

for user in userlistarray:
	userlist.append(user['id'])

### ------- GET ALL SCHEDULE ID/TITLES -----

scheduleattrlist = []

for user in userlist:
	data = looker.get_all_schedules(user)
	for schedule in data:
		scheduleattrlist.append({'id': schedule['id'],'title': schedule['title'] if schedule['title'] is not None else ""})

pprint(scheduleattrlist)

### ------- PARSE DATE IN TITLE AND DELETE EXPIRED SCHEDULES -----

for attrpair in scheduleattrlist:
	deletematch = re.search(r'DELETE\:\d{4}-\d{2}-\d{2}', attrpair['title'])
	if deletematch is None:
		break
	match = re.search(r'\d{4}-\d{2}-\d{2}', deletematch.group(0))
	if match is not None and datetime.strptime(match.group(0), '%Y-%m-%d').date() < datetime.today().date():
		print("FOUND EXPIRED SCHEDULE...DELETING")
		looker.delete_schedule(attrpair['id'])
### ------- Done -------

print("Done")
