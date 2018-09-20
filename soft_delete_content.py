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

host = 'localhost'

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = LookerApi(host=my_host,
                 token=my_token,
                 secret = my_secret)

looks_to_delete = []
soft_delete = {"deleted": True} #applies to both look and dashboard patchs

for dashboard_id in args.dashboards.split(','):
    dashboard_looks = looker.get_dashboard(dashboard_id,fields="dashboard_elements(look_id)")
    if dashboard_looks:
        looks_to_delete = looks_to_delete + [look['look_id'] for look in dashboard_looks['dashboard_elements']]
    dashboard_updated = looker.update_dashboard(dashboard_id,body=soft_delete,fields='id')
    print("Soft deleted dashboard id " + str(dashboard_updated['id']))

for look_id in looks_to_delete:
    look_updated = looker.update_look(look_id,body=soft_delete,fields='id')
    if look_updated:
        print("Soft deleted look id " + str(look_updated['id']))
