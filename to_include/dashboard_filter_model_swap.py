
# -*- coding: UTF-8 -*-
import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint
from argparse import ArgumentParser
### ------- HERE ARE PARAMETERS TO CONFIGURE -------
parser = ArgumentParser()
parser.add_argument("-d", "--dashboards", dest="dashboards",help="comma separated list of dashboards with field type filters that need to reference new models")
parser.add_argument("-s", "--source_model",dest="sourcemodel",help="name of source model to migrate dashboards off of")
parser.add_argument("-m", "--model",dest="destmodel",help="name of model to migrate dashboards to")

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
                 secret = my_secret)

for dashboard in args.dashboards.split(','):
        dashboard_filter_info = looker.get_dashboard_dashboard_filters(dashboard_id=dashboard,fields='')
        for filter in dashboard_filter_info:
            dashboard_filter_id = dashboard_filter_info[0]['id']
            dashboard_filter_model = dashboard_filter_info[0]['model']
            if dashboard_filter_model == args.sourcemodel:
                output = looker.update_dashboard_filter(dashboard_filter_id,args.destmodel,fields='')
