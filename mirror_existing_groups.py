
# -*- coding: UTF-8 -*-
import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint
from argparse import ArgumentParser
### ------- HERE ARE PARAMETERS TO CONFIGURE -------
parser = ArgumentParser()
parser.add_argument("-g", "--groups", dest="groups",help="comma separated list of groups you want to create mirror groups for")

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

if args.groups:
    for source_group_id in args.groups.split(','):
        source_group_info = looker.get_group(group_id=source_group_id,fields='id,name')
        dest_group = looker.create_group(group_name=source_group_info['name'] + " " + "(Mirror)")
        create = looker.create_group_in_group(parent_group_id=dest_group['id'],child_group_id=source_group_info['id'])
else:
    all_groups = looker.get_all_groups(fields='id,name')
    for source_group in all_groups:
        dest_group = looker.create_group(group_name=source_group['name'] + " " + "(Mirror)",fields='id')
        create = looker.create_group_in_group(parent_group_id=dest_group['id'],child_group_id=source_group['id'])
