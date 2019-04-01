# -*- coding: UTF-8 -*-
import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint
import json
from argparse import ArgumentParser
# ### ------- HERE ARE PARAMETERS TO CONFIGURE -------
parser = ArgumentParser()
parser.add_argument('-r', action="store_true",dest="restore",default=False,help='Restore existing crontabs to scheduled plans from json file')
parser.add_argument("-f","--filename", help="Fully-qualified path of json file containing scheduled_plan ids and cron schedules or a file to write to")
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

query_body ={
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

if args.restore:
    with open(args.filename) as json_schedules:
        data = json.load(json_schedules)
        for schedule in data:
            looker.update_schedule(schedule['scheduled_plan.id'], body={"crontab":schedule['scheduled_plan.cron_schedule']})
else:
    scheduler_data = looker.run_inline_query(body=query_body)
    with open(args.filename, 'w') as outfile:
        json.dump(scheduler_data, outfile)
    for schedule in scheduler_data:
        looker.update_schedule(schedule['scheduled_plan.id'], body={"crontab":"0 5 31 2 *"})
