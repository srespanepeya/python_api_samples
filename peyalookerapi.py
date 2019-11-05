# -*- coding: UTF-8 -*-
import requests
from pprint import pprint as pp
import json
import re
import urllib.request
import yaml

import lookerapi as looker
from lookerapi.rest import ApiException

#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
f = open('config.yml')
conf = yaml.load(f,Loader=yaml.BaseLoader)
f.close()

my_host = conf['looker']['host']
my_secret = conf['looker']['secret']
my_token = conf['looker']['token']


class PeyaLookerApi(object):

    def __init__(self):
        print("--->Initiating PeyaLookerApi Instance...")
        self.token = my_token
        self.secret = my_secret
        self.host = my_host
        self.auth()

    def auth(self):
        print("--->Autenticating against Looker Server...")
        unauthenticated_client = looker.ApiClient(self.host)
        unauthenticated_authApi = looker.ApiAuthApi(unauthenticated_client)
        try:
            token = unauthenticated_authApi.login(client_id=self.token, client_secret=self.secret)
            lClient = looker.ApiClient(self.host, 'Authorization', 'token ' + token.access_token)
            print("--->CLIENT:{0}".format(lClient))
            userApi = looker.UserApi(lClient)
            me = userApi.me()
            self.client = lClient
            print("--->WELCOME {0}!".format(me.display_name))
        except:
            print("!--->Auth error")
        # self.peyaLooker = client

    def get_models(self,fields={}):
        api_instance = looker.LookmlModelApi(self.client)
        api_response = api_instance.all_lookml_models(fields="")
        print("--->Response Type:{0}".format(type(api_response)))
        return api_response

    # GET /lookml_models/
    def get_model_explore(self,modelName,exploreName):
        api_instance = looker.LookmlModelApi(self.client)
        api_response = api_instance.lookml_model_explore(modelName,exploreName, fields="")
        #api_response = api_instance.lookml_model_explore()
        #     print(api_response.fields)
        print("Dimensions:%s" % (len(api_response.fields.dimensions)))
        print("Measures:%s" % (len(api_response.fields.measures)))
        print("Parameters:%s" % (len(api_response.fields.parameters)))
        print("Filters:%s" % (len(api_response.fields.filters)))
        return api_response

    # GET /users/id
    def get_user_by_email(self,userEmail):
        #print('--->Getting user data for email *{0}*'.format(userEmail))
        api_instance = looker.UserApi(self.client)
        api_response = api_instance.search_users(email=userEmail)
        if len(api_response)==1:
            for u in api_response:
                return u
        else:
            return None

    def update_user(self,userId,body):
        #print('--->Getting user data for email *{0}*'.format(userId))
        api_instance = looker.UserApi(self.client)
        api_response = api_instance.update_user(user_id=userId,body=body)
        return api_response        

