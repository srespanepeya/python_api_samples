import yaml
from lookerapi import LookerApi

### ------- HERE ARE PARAMETERS TO CONFIGURE -------

look_id = 123 # Look created in part1
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

data = looker.get_look(look_id=look_id, format='json')


soft_delete = {"deleted": True} #applies to both look and dashboard patchs

for d in data:
    print('Soft deleting ' + d['content_usage.content_type'] + ': ' + d['content_usage.content_id'])
    if d['content_usage.content_type'] == 'look':
        # looker.update_look(d['content_usage.content_id'],body=soft_delete) # uncomment this line to soft delete

    elif d['content_usage.content_type'] == 'dashboard':
        looks_to_delete = []
        dashboard_looks = looker.get_dashboard(d['content_usage.content_id'],fields="dashboard_elements(look_id)")
        if dashboard_looks:
            looks_to_delete = looks_to_delete + [look['look_id'] for look in dashboard_looks['dashboard_elements']]
        # dashboard_updated = looker.update_dashboard(d['content_usage.content_id'],body=soft_delete) # uncomment this line to soft delete

        for look_id in looks_to_delete:
            # look_updated = looker.update_look(look_id,body=soft_delete,fields='id') # uncomment this line to soft delete
            if look_updated:
                print("Soft deleting look: " + str(look_updated['id']) + ' on dashboard: ' + str(d['content_usage.content_id']))