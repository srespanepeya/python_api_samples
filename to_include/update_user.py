import yaml ### install the pyyaml package
from lookerapi import LookerApi
import csv
import json


### ------- HERE ARE PARAMETERS TO CONFIGURE -------

host = ''
csv_file = ''


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


def read_csv(file):
    f = open(file, 'rb')
    reader = csv.reader(f)
    header = reader.next()
    output = [dict(zip(header, map(str, row))) for row in reader]
    return output

data = read_csv(csv_file)

for i  in data:
    user_id = i['user_id']
    looker.update_user(user_id, i)
