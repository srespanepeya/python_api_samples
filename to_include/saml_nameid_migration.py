# -*- coding: UTF-8 -*-
import yaml ### install the pyyaml package
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint
from argparse import ArgumentParser
### ------- HERE ARE PARAMETERS TO CONFIGURE -------
parser = ArgumentParser()
parser.add_argument("-u", "--users", dest="users",help="comma separated list of users that need email credentials and saml credentials deleted")
args = parser.parse_args()
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

for user_id in args.users.split(','):
        user_email_info = looker.get_users_email_credentials(user_id=user_id,fields='email')
        user_saml_email_info = looker.get_users_saml_credentials(user_id=user_id,fields='email,saml_user_id')
        print(user_email_info)
        print(user_saml_email_info)
        if user_email_info != None:
            print("not none")
            if user_email_info['email'] != user_saml_email_info['email']:
                print("email misalignment for user " + user_id)
            else:
                looker.delete_users_saml_credentials(user_id=user_id)
        else:
            looker.create_users_email_credentials(user_id=user_id,email_address=user_saml_email_info['email'])
            looker.delete_users_saml_credentials(user_id=user_id)
