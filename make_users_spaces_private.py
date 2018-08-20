
# -*- coding: UTF-8 -*-
import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint
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

spaces = looker.get_all_spaces(fields='id,is_personal,creator_id,is_personal_descendant,content_metadata_id')

for space in spaces:
    if space['is_personal'] and not space['is_personal_descendant']:
        content_metadata_access = looker.get_all_content_metadata_access(space['content_metadata_id'],fields='id,permission_type,group_id,user_id')
        for access_grant in content_metadata_access:
            if access_grant['user_id'] != space['creator_id']:
                print "deleting access on space " + str(space['id'])
                looker.delete_content_metadata(access_grant['id'])
