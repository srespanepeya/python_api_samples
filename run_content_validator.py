import csv
import yaml ### install the pyyaml package
from lookerapi import LookerApi
from pprint import pprint

### in progress
### Requires API v. 3.1 -- set this in config.yml

### ------- HERE ARE PARAMETERS TO CONFIGURE -------

host = 'cse'
output_csv_name = 'output.csv'


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


### ------- GET AND PRINT THE LOOK -------

data = looker.get_content_validation()
# pprint(data)

host_url = my_host[:my_host.index(":19999")]
broken_content = data['content_with_errors']
# pprint(broken_content)
output = []
for item in broken_content:
    try:
        dashboard_id = item['dashboard']['id']
    except TypeError:
        print('No associated dashboard object. Skipping.')
        continue
    dashboard_name = item['dashboard']['title']
    space_id =  item['dashboard']['space']['id']
    space_name = item['dashboard']['space']['name']
    dashboard_element = item['dashboard_element']['title']
    errors = item['errors']
    dashboard_url =  '{}/dashboards/{}'.format(host_url,
                                               dashboard_id
                                               )
    space_url = '{}/spaces/{}'.format(host_url,
                                      space_id
                                      )
    # find parent_space
    space_data = looker.get_space(space_id)
    parent_space_id = space_data['parent_id']
    if parent_space_id is None:
        parent_space_name = None
        parent_space_url = None
        pass
    else:
        parent_space_url = '{}/spaces/{}'.format(host_url,
                                                 parent_space_id
                                                 )
        parent_space_data = looker.get_space(parent_space_id)
        print(parent_space_data)
        parent_space_name = parent_space_data['name']
    data = {
            'dashboard_name' : dashboard_name,
            'dashboard_url' : dashboard_url,
            'space_name' : space_name,
            'space_url' : space_url,
            'parent_space_name': parent_space_name,
            'parent_space_url': parent_space_url,
            'dashboard_element': dashboard_element,
            'errors': str(errors)
           }
    output.append(data)
    print(list(output[0].keys()))

try:
    with open(output_csv_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,
                               fieldnames=list(output[0].keys()))
        writer.writeheader()
        for data in output:
            writer.writerow(data)
except IOError:
    print("I/O error")

### ------- Done -------

print("Done")
