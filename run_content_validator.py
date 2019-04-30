import yaml ### install the pyyaml package
from lookerapi import LookerApi
from pprint import pprint

### in progress

### ------- HERE ARE PARAMETERS TO CONFIGURE -------

host = 'cse'


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

broken_content = data['content_with_errors']
pprint(broken_content)
output = []
for item in broken_content:
    data = {
            'dashboard_id': item['dashboard']['id'],
            'dashboard_title': item['dashboard']['title'],
            'space': item['dashboard']['space'],
            'element': item['dashboard_element']['title'],
            'errors': item['errors']
           }
    output.append(data)
pprint(output)


### ------- Done -------

print("Done")
