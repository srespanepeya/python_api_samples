# Python API Samples
Python examples of how to use the Looker API

## What you can find here
- A simple Looker API 3.0 SDK
- A sample config.yml file for collecting API Tokens/Secrets
- Sample files of various tasks using the API

## Relevant Articles
**Moving Looks**: https://discourse.looker.com/t/moving-a-look-between-looker-servers-using-the-looker-api-and-the-python-requests-library/

## Getting Started
- Copy at minimum the configration_sample.yml and lookerapi.py files.
- Change the config_sample.yml to config.yml and update with your credentials. You can get API 3 credentials by:
   1) Go to Admin > Users in your Looker instance.
   2) Either make a new user or click to an existing users page using the "Edit" button. Remember the API user will have the same credentials as the user so keep that security point in mind when choosing a user.
   3) Click the "New API 3 Key" button to make API 3 credentials for the user.
   4) In the config.yml file, the "Client Secret" on the user page should be copied into the `secret:` string and the Client ID should be copied into the `token:` string. For the `host:` string replace the word `localhost` with your Looker instance domain name (i.e. _companyname_.looker.com).
   5) Make sure your Looker instance is configured to a working API Host URL by going to Admin > API in your Looker instance and checking the API Host URL field. A blank field is the default for Looker to auto-detect the API Host URL.
- Run any file in the shell with `python <<filename>>`

## Scripts

|File|Description|How to|
|----|----|----|
|delete_look.py|Illustrates how to delete a look or a list of looks delimited by newlines|Make sure you have the host in your config.yml file and adjust the source look variables at the top of the script.
|delete_dashboard.py|Illustrated how to delete a dashboard or a list of dashboards delimited by newlines|Make sure you have the host in your config.yml file and adjust the source look variables at the top of the script.
|get_look.py|Illustrates how to get the data from a look|Make sure you have the host in your config.yml file and adjust the source look variables at the top of the script.|
|move_look.py|Illustrates how to move a look between servers, or between the same server|Make sure you have both hosts in your config.yml file and adjust the source look, destination space variables at the top of the script.|
|get_data_dictionary.py|Put together a list of each field, and various attributes in your data model, this outputs a CSV|Make sure your host is configured in the config.yml file. If you change the 'localhost' variable in config.yml also change line 143 of get_data_dictionary.py to reference the proper credentials. The output file from the script is named dictionary.csv in the repository directory.|
|update_user.py|Update user parameters with a CSV| In the script, reference a CSV which maps individual user IDs to whichever user parameters you would like to update. Use the `/users/{user_id}/credentials_email` endpoint to update email/password login information.|
|update_static_filter.py|Update a static filter value on a look| Illustrates how to update a static value associated with a filter field|
|delete_expired_schedules.py|Delete schedules that have an expiry date in the title|Gets a list of all schedules and then checks the title for an expiry date specified in the title.  If the current date is past that date, delete the schedule|
|model_migration.py|Move a list of looks to use a new model| Illustrates how to update queries associated with looks to migrate a subset of content to a new model|
|soft_delete_content.py|Soft Delete a List of Dashboards and Associated Looks| Illustrates how to soft delete a dashboard and linked looks|
|dahsboard_filter_model_swap.py|Update model references in dashboard filter suggestions| Addresses a gap in the content validator to show how to repoint model references tied to dashboard filter suggestions|
|mirror_existing_groups.py|Mirror all or a subset of groups| Illustrates how to create new groups off existing ones and nest the existing groups in the newly created ones for a 1:1 mapping|
