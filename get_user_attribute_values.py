import yaml
from lookerapi import LookerApi
import csv

f = open('config.yml')
params = yaml.load(f)
f.close()

host = 'localhost'

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = LookerApi(host=my_host,
                 token=my_token,
                 secret = my_secret)


all_users = looker.get_user()
user_attributes = looker.get_user_attributes()

writer = csv.writer(open('user-attributes.csv', 'w'), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
headers = ['group_ids']
for attribute in user_attributes:
    headers.append(attribute['name'])

writer.writerow(headers)

for u in all_users:
    values = []
    values.append(str(u['group_ids']).replace('[','').replace(']',''))
    for attribute in user_attributes:
        values.append(looker.get_user_attribute_values(u['id'],str(attribute['id']))[0]['value'])
    writer.writerow(values)