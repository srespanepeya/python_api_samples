import yaml  # you must install the pyyaml package
from lookerapi import LookerApi
from pprint import pprint

# Set host to a hostname in your config.yml file
host = 'looker'

f = open('config.yml')
params = yaml.load(f)
f.close()

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = LookerApi(host=my_host,
                 token=my_token,
                 secret=my_secret)

look_id = 1

# First, retrieve the existing query attached to the look
query_id = looker.get_look_info(look_id, "query_id")

# Then, build a new query that doesn't contain the read-only fields from the original query
query = looker.get_query(query_id['query_id'], "model,view,pivots,row_total,query_timezone,limit,filters,filter_expression,fill_fields,fields,dynamic_fields,column_limit,total,sorts")
print("*** Existing query: ***")
pprint(query)
print("\n\n\n")

filter_field = "event.name"  # name (as it appears in the JSON) of the filter you want to update
existing_filter_value = "disabled^_chromium^_rendering,update^_user^_facts"  # existing filter value that you want to change to something else
new_filter_value = "create_query"  # new filter value

# Only modify the body of the query object to change the filter value if the filter value is set to what we expected
if query['filters'][filter_field] == existing_filter_value:

    query['filters'][filter_field] = new_filter_value

    # Now, create a new query with the updated query object
    post_query = looker.create_query(query, "id")
    print("*** New query: ***")
    pprint(post_query)
    print("\n\n\n")

    results = looker.run_query(post_query['id'])
    print("*** Query results after filter update: ***")
    pprint(results)

    # And update the existing look to use the new query (if desired)
    body = {"query_id": post_query['id']}
    look = looker.update_look(look_id,body)

else:
    raise Exception("Existing filter value '" + existing_filter_value + "' not found")