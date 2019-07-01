#!/usr/bin/python
# -*- coding: utf-8 -*-

### -------- This script was written to surface a list of top level, non personal spaces and the list of Groups and User who have 
### -------- explicitly been granted view/edit access to those spaces. It combines multiple API calls to get the Space, Group and
### -------- Content Metadata Accesses in line and passes them into a Pandas Dataframe object. 
### -------- This will also output a list of Space Ids for which no permission has explicitly been granted, but implicitly given 
### -------- via inheritence from a parent space, as is Looker's design i.e. a space in the Shared space will inherit all the 
### -------- Group/User access given to Shared unless a custom list of Groups/Users have been granted access to that space. 
### -------- NB: The lookerapi.py script has also been edited to add a new function, shown below. If your local file doesn't have this, add it.

# GET content_metadata_access
    # def get_all_content_metadata_access(self,content_metadata_id,fields=''):
    #      url = '{}{}'.format(self.host,'content_metadata_access')
    #      print(url)
    #      params = {'content_metadata_id':content_metadata_id,'fields':fields}
    #      r = self.session.get(url,params=params)
    #      if r.status_code == requests.codes.ok:
    #          return r.json()

import yaml  # ## install the pyyaml package
import pandas as pd
import ast
import json
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint

### ------- HERE ARE PARAMETERS TO CONFIGURE -------

host = 'saleseng'

### ------- OPEN THE CONFIG FILE and INSTANTIATE API -------

f = open('config.yml')
params = yaml.load(f)
f.close()

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = LookerApi(host=my_host, token=my_token, secret=my_secret)

# Pandas has a weird bug where it incorrectly calculates the output width and cuts off columns...

pd.set_option('display.expand_frame_repr', False)

# Create a dictionary of spaces:content_meta_data_ids so we can iterate through and check the accesses to those spaces

spaces = \
looker.get_all_spaces(fields='id,is_personal,creator_id,is_personal_descendant,content_metadata_id,name'
                      )

spaces_content_metadata_ids = {}

spacejson = json.loads(json.dumps(spaces))

# List of spaces that are sub spaces of users so we can include/exclude as needed

personal_descendant_ids = []
non_personal_descendant_ids = []

# Need to remove spaces that are is_personal_descendant, because we can't be auditing spaces that are sub-spaces of a user's personal space either

for space in spacejson:
	if space['is_personal_descendant'] == False and space['is_personal'
	        ] == False and space['id'] != 'lookml' and space['name'] \
	    != 'Users':
	    spaces_content_metadata_ids[space['id']] = \
	        space['content_metadata_id']
	    non_personal_descendant_ids.append(space['id'])
	else:
	    personal_descendant_ids.append(space['id'])

# for value in spaces_content_metadata_ids.iteritems():
# ....print "metadata",json.loads(json.dumps(looker.get_all_content_metadata_access(value,fields='id,content_metadata_id,permission_type,user_id,group_id')))

df2 = pd.DataFrame(spacejson, columns=['id', 'name',
               'content_metadata_id']).rename(index=str,
    columns={'id':'space_id','content_metadata_id': 'cmid', 'name': 'space_name'})
df2nonpersonalremoved = df2[df2.space_id.isin(non_personal_descendant_ids)]

# You don't want to list User spaces because they shouldn't be audited

df2usersremoved = df2nonpersonalremoved['space_name'] != 'Users'
df_spaces_filtered = df2nonpersonalremoved[df2usersremoved]

# Get the group names

groups = looker.get_all_groups(fields='id,name,user_count')
groupsdf = pd.DataFrame(groups, columns=['id', 'name', 'user_count'
                    ]).rename(index=str, columns={'id': 'group_id',
                              'name': 'group_name',
                              'user_count': '# users'})

print 'All Spaces: \n', df_spaces_filtered
print '+---------------+---------------+---------------+ \n'
print 'Each Top Level Space and user/group access levels \n'

# print spaces_content_metadata_ids, non_personal_descendant_ids
# Put all the dataframes in a list so we can concatenate at the end using pd.concat and get rid of headers

list_of_dataframes = []
inheriting_space_ids = []
admin_only_access_space_ids = []
for (key, value) in spaces_content_metadata_ids.iteritems():

# Pandas stuff - get the dataframe from the Looker API call, only use certain fields, turn those to columns, rename them so they look good, account for empty json responses

	df1 = \
	    pd.DataFrame(json.loads(json.dumps(looker.get_all_content_metadata_access(value,
	                 fields='content_metadata_id,permission_type,user_id,group_id'
	                 ))), columns=['content_metadata_id',
	                 'permission_type', 'user_id', 'group_id'
	                 ]).rename(index=str,
	                           columns={'permission_type': 'access',
	                           'content_metadata_id': 'cmid',
	                           'name': 'space_name'})

	if df1.empty:

	    # if the dataframe is empty, it either means that there's 0 groups/users and only Admins can access or the space has inherited permissions from a parent (likely Shared) space

	    inherited_spaces = looker.get_content_metadata(value)
	    if inherited_spaces['inherits'] == True \
	        and inherited_spaces['parent_id'] == 1:
	        inheriting_space_ids.append(value)
	    else:
	        admin_only_access_space_ids.append(value)
	else:
	    list_of_dataframes.append(pd.merge(pd.merge(df_spaces_filtered,
	                              df1, on=['cmid']), groupsdf,
	                              on=['group_id']))
		
new_clean_dfs = pd.concat(list_of_dataframes)
print new_clean_dfs
print 'Space Ids', inheriting_space_ids, \
'inherit their access from the Shared Space'
print 'Space Ids', admin_only_access_space_ids, \
'are all Admin-only access. No Group or User has been explicitly added to this space'
