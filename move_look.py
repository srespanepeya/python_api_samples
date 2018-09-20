# -*- coding: UTF-8 -*-

import yaml  ### YOU NEED THE pyyaml PACKAGE : [sudo] pip install pyyaml
from lookerapi import LookerApi
from pprint import pprint as pp
import json

### ------- HERE ARE PARAMETERS TO CONFIGURE -------

source_name = 'sandbox'  ### The name in your config.yml file
source_look_id = 58  ### The look number you would like to move

destination_name = 'production'  ### The name in your config.yml file
destination_space_id = 769 ### The destination space ID to move the look to



### ------- OPEN THE CONFIG FILE and INSTANTIATE API -------

f = open('config.yml')
params = yaml.load(f)
f.close()

my_host = params['hosts'][source_name]['host']
my_secret = params['hosts'][source_name]['secret']
my_token = params['hosts'][source_name]['token']

dest_looker = LookerApi(host=my_host,
                 token=my_token,
                 secret = my_secret)


my_host = params['hosts'][destination_name]['host']
my_secret = params['hosts'][destination_name]['secret']
my_token = params['hosts'][destination_name]['token']


source_looker = LookerApi(host=my_host,
                 token=my_token,
                 secret = my_secret)


### ------- GET THE SOURCE LOOK -------

look_body = source_looker.get_look_info(source_look_id,'query_id, query, title'	)
print("---- Source Look Body ----")
pp(look_body)


print("---- Source query ----")
query_body = source_looker.get_query(look_body['query_id'])
pp(query_body)


### ------- BUILD THE TARGET LOOK -------

print("---- New query ----")
new_query = dest_looker.create_query(query_body,'id')
new_query_id = str(new_query['id'])
print(new_query_id + " is the new query id")

new_look = {}
new_look['space_id'] = destination_space_id
new_look['query_id'] = new_query_id
new_look['title'] = look_body['title'] + "from teach"
dest_looker.create_look(new_look)


### ------- DONE -------

print("Done")
