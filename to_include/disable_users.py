import yaml
from lookerapi import LookerApi
from datetime import datetime

f = open('config.yml')
params = yaml.load(f)
f.close()

host = 'teach'

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = LookerApi(host=my_host,
                 token=my_token,
                 secret = my_secret)


me = looker.get_current_user()['id']
# print(me)

all_users =  looker.get_user()
ids_to_disable = []
# print(all_users)

days_to_disable = 30

no_login_count = 0
good_user_count = 0
errors = 0
looker_user_count = 0


for u in all_users:
	login = None
	uid = u['id']
	# print(u)
	if u['presumed_looker_employee'] == True:
		looker_user_count += 1
	if u['presumed_looker_employee'] == False & u['id'] != me:
		try:
			login = u['credentials_email']['logged_in_at']
			login_date = datetime.strptime(login[0:9],"%Y-%M-%d")

			if (datetime.today()-login_date).days < days_to_disable:
				ids_to_disable.append(uid)
		except:
			print('No Login for ' + u['id'])
			no_login_count += 1
			ids_to_disable.append(uid)

print(ids_to_disable)
print("Disabling Users")
for u in ids_to_disable:
	user_info_body =  looker.get_user(u)
	# print(user_info_body)
	if user_info_body['presumed_looker_employee'] == False:

		try:
			try:
				email = user_info_body['email'].split('@')[1]
			except:
				email = "nothing.com"
				# raise
			print email
			if email != 'looker.com':

				#### Comment out the next line and uncomment the one after!
				print(user_info_body['email'] + "would be disabled if you uncommented the next line")
				# user_info_body['is_disabled'] = True


			# print(user_info_body.email)
			print(user_info_body)
			looker.update_user(u,user_info_body)
		except:
			print("email or update error")
			raise
			errors += 1

print(" ----------------------------- ")
print(" ---------- Summary ----------")
print(" ----------------------------- ")
print(" Users: "+ len(all_users))
print(" Looker Users: "+ looker_user_count)
print(" ----------------------------- ")
print(" Users Disabled: "+ len(ids_to_disable)
print(" Errors: "+ errors)
print(" No Login Users: " + no_login_count)
print(" ----------------------------- ")
