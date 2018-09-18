import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint
import json
import time

### ------- HERE ARE PARAMETERS TO CONFIGURE -------
dashboard_id = 7
host = 'cs_eng'

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

dashboard = looker.get_dashboard(dashboard_id)

# Collect dashboard filters
dashboard_filters = []
filter_params = ['id', 'title', 'default_value', 'dashboard_id']
for dashboard_filter_object in dashboard['dashboard_filters']:
    dashboard_filter = {param: dashboard_filter_object[param] for param in filter_params}
    dashboard_filters.append(dashboard_filter)


# Collect dashboard queries and associated filter listerners
query_params = ['model', 'view', 'fields', 'pivots', 'filters', 'sorts',
                'query_timezone', 'limit', 'total', 'row_total', 'fill_fields',
                'dynamic_fields' ]
dashboard_elements = []
for element in dashboard['dashboard_elements']:
    dashboard_element = {}
    # is element look or tile?
    if element['look_id'] is None:
        full_query = element['query']
    else:
        full_query = element['look']['query']
    # keep the query params we care about
    query = {param: full_query[param] for param in query_params}
    dashboard_element['query'] = query
    dashboard_element['filter_listeners'] = [filterable['listen'] for filterable
                    in element['result_maker']['filterables']][0]
    dashboard_elements.append(dashboard_element)

# # add default_value to listener array
for element in dashboard_elements:
    for filter_listener in element['filter_listeners']:
        default_value = list(
                        filter(
                            lambda dashboard_filter: dashboard_filter['title'] ==
                                filter_listener['dashboard_filter_name'],
                                    dashboard_filters))[0]['default_value']
        filter_listener['default_value'] = default_value

    # apply dashboard filters to queries with default values
    if element['query']['filters'] is None:
        element['query']['filters'] = {}
    for filter_listener in element['filter_listeners']:
        field = filter_listener['field']
        value = filter_listener['default_value']
        element['query']['filters'][field] = value
    looker.run_inline_query(element['query'])
