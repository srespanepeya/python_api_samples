import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint
import json
import re

###############
# This script takes the schedule that's been made for a Look
# and updates it with the emails of users found in another Look
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

# These Look IDs should be updated to match the Look ID of 
# whatever the new reports will be.

author_report = 157
task_report = 158

# get emails from a Look(157) (Author Report)
print "Getting Look information"
emails = looker.get_look(author_report)
email_list = []
for email in emails:
	for key, value in email.iteritems():
		email_list.append(value)

print "Getting Schedule information from Look"
# get look plan ID from a Look(158). 
look_plan_id = looker.get_look_schedule(task_report)[0]['id']

# Pass those emails into an update_schedule call using the above look_plan_id into below plan
# Loop through the email list, appending to and creating and concatenating the string to be used for the 
# body of the API call in json form
i = 1
list_of_schedule_plan_destinations = ''

for email in email_list:
	if i == len(email_list):
		list_of_schedule_plan_destinations += ('{{"scheduled_plan_id": {},"format": "csv","address": "{}","type": "email"}}]}}'.format(look_plan_id,email))
	else:
		list_of_schedule_plan_destinations += ('{{"scheduled_plan_id": {},"format": "csv","address": "{}","type": "email"	}},'.format(look_plan_id,email))
	i += 1

start_string = '{"scheduled_plan_destination":['
full_body = start_string+list_of_schedule_plan_destinations

# Make the call
print "Updating Schedule"
looker.update_schedule(look_plan_id,body=full_body)

print "Done"