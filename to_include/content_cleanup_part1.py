import yaml 
from lookerapi import LookerApi


### ------- HERE ARE PARAMETERS TO CONFIGURE -------

days_since_last_accessed = 365
space_id = 3 # space used to save the Look
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


### ------- CREATE QUERY & SAVE LOOK -------


content_usage_query_body =  { "model": "system__activity"
			, "view": "content_usage"
			, "filters": {
					"content_usage.days_since_last_accessed": ">"+str(days_since_last_accessed)
					, "dashboard.deleted_date": "NULL"
					, "look.deleted_date": "NULL"
					}
			, "filter_expression": "NOT is_null(${dashboard.id}) OR NOT is_null(${look.id})"
			, "fields": [
					"content_usage.days_since_last_accessed"
					, "content_usage.content_id"
					, "content_usage.content_title"
					, "content_usage.content_type"
					, "dashboard.id"
					, "dashboard.user_id"
					, "dashboard.space_id"
					, "look.id"
					, "look.user_id"
					, "look.space_id"
					]
			, "dynamic_fields": "[{\"table_calculation\":\"user_id\",\"label\":\"User ID\",\"expression\":\"coalesce(${dashboard.user_id},${look.user_id})\"},{\"table_calculation\":\"space_id\",\"label\":\"Space ID\",\"expression\":\"coalesce(${dashboard.space_id},${look.space_id})\"}]"
			, "sorts": ["content_usage.days_since_last_accessed desc"]
			, "limit": "500"       
			, "vis_config": {
					"table_theme": "white"
					, "type": "table"
					, "hidden_fields": ["dashboard.id", "dashboard.user_id", "dashboard.space_id", "look.id", "look.user_id", "look.space_id"]
					}
			}

content_usage_query = looker.create_query(query_body=content_usage_query_body)

print ('Query Created: ' + str(content_usage_query['id']))

new_look = {}
new_look['space_id'] = space_id
new_look['query_id'] = content_usage_query['id']
new_look['title'] = "Unused Content"

look = looker.create_look(new_look)

print ('Look Saved: ' + str(look['id']))


### ------- GET USER EMAILS FROM USER_IDs -------


data = looker.run_query(query_id=content_usage_query['id'])
user_ids = {row['user_id'] for row in data}

print ('Users with unused content: ' + str(user_ids))

me = looker.get_current_user()
user_list = looker.get_all_users()
emails = {}
for u in user_list:
	if u['id'] in user_ids:
		emails[u['id']] = u['email']

print ('Emails will be sent to: ' + str(emails))


### ------- CREATE SCHEDULE AND SEND NOTICE -------

schedule_body = { "name": "Unused Content"
			, "title": "Unused Content"
			, "user_id": me['id']
			, "run_once": "true"
		}

for e in emails:
	if emails[e] is not None:
		content_usage_query_body['filter_expression'] = "(NOT is_null(${dashboard.id}) OR NOT is_null(${look.id})) AND (${dashboard.user_id} = %s OR ${look.user_id} = %s)" % (e,e)
		specific_user_query = looker.create_query(query_body=content_usage_query_body)
		schedule_body['query_id'] = specific_user_query['id']
		schedule_body['scheduled_plan_destination'] = [
				{ "format": "inline_table"
				, "apply_formatting": "true"
				, "apply_vis": "true"
				, "address": emails[e]
				, "type": "email"
				, "message": "Below is a list of content that you have created and not accessed for " + str(days_since_last_accessed) + " days. All content will be removed if it is not accessed within the next 7 days. Please click on any of the Content Title(s) that you want to keep."
			}]
		send_notice = looker.scheduled_plan_run_once(body=schedule_body)
		print ('Scheduled job ' + str(send_notice['id']) + '. Email sent to: ' +  emails[e])



### ------- Done -------

print("Emails have been sent to Looker users")

