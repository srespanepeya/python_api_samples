
# -*- coding: UTF-8 -*-
import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint
from argparse import ArgumentParser
### ------- HERE ARE PARAMETERS TO CONFIGURE -------
parser = ArgumentParser()
parser.add_argument("-l", "--looks", dest="looks",help="comma separated list of look ids")
parser.add_argument("-m", "--model",dest="model",help="name of model to migrate looks to")

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

for look in args.looks.split(','):
        look_info = looker.get_look_info(look_id=look,fields='query_id')
        look_query_id = look_info['query_id']
        query_object = looker.get_query(look_query_id,fields='view,fields,pivots,fill_fields,filters,limit,column_limit,total,row_total,vis_config,filter_config,dynamic_fields,has_table_calculations,model,query_timezone')
        query_object['model'] = args.model
        new_query = looker.create_query(query_body=query_object,fields='id')
        look_patch_data = {}
        look_patch_data["query_id"] = new_query['id']
        output = looker.update_look(look,look_patch_data)
