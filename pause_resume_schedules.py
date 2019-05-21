# -*- coding: UTF-8 -*-
import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint
import json
from argparse import ArgumentParser
# ### ------- HERE ARE PARAMETERS TO CONFIGURE -------
parser = ArgumentParser()

group = parser.add_mutually_exclusive_group()
# Find your schedule IDs in the History link of a schedule row on the Admin > Scheduled Plans page.
group.add_argument("-p","--pause",type=int,action="store",dest="pause",help='ID of a specific schedule to pause or -1 to pause all schedules.')
group.add_argument("-r","--resume",type=int,action="store",dest="resume",help='ID of a specific schedule to resume or -1 to resume all schedules.')

parser.add_argument("-f","--filename",default="schedules.json",help="JSON file to save your paused schedules to.")
args = parser.parse_args()

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
                 secret=my_secret)

# This JSON query retrieves all current scheduled plans from Looker
query_body = {
  "view": "scheduled_plan",
  "fields": [
    "scheduled_plan.id",
    "scheduled_plan.cron_schedule"
  ],
  "pivots": None,
  "fill_fields": None,
  "filters": {
    "scheduled_plan.run_once": "no"
  },
  "filter_expression": None,
  "sorts": None,
  "limit": "500",
  "column_limit": None,
  "total": None,
  "row_total": None,
  "subtotals": None,
  "dynamic_fields": None,
  "query_timezone": "America/Los_Angeles",
  "has_table_calculations": False,
  "model": "i__looker"
}

if args.resume:
    with open(args.filename) as json_schedules:
        data = json.load(json_schedules)
        print("Resumed from " + args.filename)
        for schedule in data:
            # resume all schedules, or a specific schedule if a id is passed as a command-line argument
            if (args.resume != -1 and int(schedule['scheduled_plan.id']) == int(args.resume)) or args.resume == -1:
                looker.update_schedule(schedule['scheduled_plan.id'], body={"crontab":schedule['scheduled_plan.cron_schedule']})
elif args.pause:
    scheduler_data = looker.run_inline_query(body=query_body)
    for schedule in scheduler_data:
        # Don't overwrite already-paused schedules
        if schedule['scheduled_plan.cron_schedule'] == "0 5 31 2 *":
          paused_id = schedule['scheduled_plan.id']

          try:
            with open(args.filename) as json_schedules:
                paused_data = json.load(json_schedules)
                for paused_schedule in paused_data:
                  # If a schedule has already been paused, preserve the existing paused value
                  if int(paused_id) == paused_schedule['scheduled_plan.id']:
                    schedule['scheduled_plan.cron_schedule'] = paused_schedule['scheduled_plan.cron_schedule']
          except:
            pass

    with open(args.filename, 'w') as outfile:
        json.dump(scheduler_data, outfile)
        print("Paused to " + args.filename)
    for schedule in scheduler_data:
        # Pause all schedules, or a specific schedule if a id is passed as a command-line argument
        if (args.pause != -1 and int(schedule['scheduled_plan.id']) == int(args.pause)) or args.pause == -1:
            looker.update_schedule(schedule['scheduled_plan.id'], body={"crontab":"0 5 31 2 *"}) # "Feb 31" doesn't exist and is therefore the equivalent of paused
