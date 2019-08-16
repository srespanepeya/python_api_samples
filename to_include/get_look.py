import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint


### ------- HERE ARE PARAMETERS TO CONFIGURE -------

look_to_get = 123
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


### ------- GET AND PRINT THE LOOK -------

data = looker.get_look(look_to_get)

pprint(data)

### ------- Done -------

print("Done")
