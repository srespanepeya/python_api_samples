import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint


### ------- HERE ARE PARAMETERS TO CONFIGURE -------

look_id = 123
filter_field = 'products.brand_name'
old_value = "Calvin Klein"
new_value = "Allegra K"
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

# GET request to /looks endpoint with look id and extract the query id

query_id = looker.get_look_info(look_id,"query_id")
pprint(query_id)

# GET request to /queries endpoint with query id from step 1 to get the query definition

query = looker.get_query(query_id['query_id'],"model,view,pivots,row_total,query_timezone,limit,filters,filter_expression,fill_fields,fields,dynamic_fields,column_limit,total,sorts")
pprint(query)

# Modify the body of the query object to change the filter value

if query['filters'][filter_field] == old_value:
    query['filters'][filter_field] = new_value
else:
    print("no match")


# # create a new query with the updated query object

post_query = looker.create_query(query,"id")
pprint(post_query)

# use the new query to update a look
body = {"query_id": post_query['id']}

look = looker.update_look(look_id,body)
pprint(look)
