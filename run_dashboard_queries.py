import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint
from argparse import ArgumentParser

### ------- HERE ARE PARAMETERS TO CONFIGURE -------
parser = ArgumentParser()
parser.add_argument("-d", "--dashboards", dest="dashboards",help="comma separated list of dashboards to soft delete")
args = parser.parse_args()

### ------- OPEN THE CONFIG FILE and INSTANTIATE API -------
f = open('config.yml')
params = yaml.load(f)
f.close()

host = 'cs_eng'

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = LookerApi(host=my_host,
                 token=my_token,
                 secret = my_secret)


dashboard_filters = [looker.get_dashboard_dashboard_filters(dashboard_id=dashboard,fields='') for dashboard in args.dashboards.split(',')]
