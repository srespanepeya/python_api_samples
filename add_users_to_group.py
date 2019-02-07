import yaml ### install the pyyaml package
from lookerapi import LookerApi
import argparse
import csv

# You can execute this script from the command line like this:
# python3 add_users_to_group.py --filename=/path/to/file.csv
#
# Don't forget to set the host value on line 19

parser = argparse.ArgumentParser(description="Load user IDs from the CSV file specified by filename")
parser.add_argument("-f","--filename", help="Fully-qualified path of CSV file to parse",
                    type=str)

args = parser.parse_args()

### ------- OPEN THE CONFIG FILE and INSTANTIATE API -------

host = "" # the name of a Looker environment specified in a config.yml file in the same directory as this script
f = open('config.yml')
params = yaml.load(f)
f.close()

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = LookerApi(host=my_host,
                 token=my_token,
                 secret=my_secret)


def parse_csv_file_and_add_users_to_groups():
    """Parse a CSV file containing a User ID in the first column and a Group ID in the second column and update groups for users"""

    f = open(args.filename, 'r', encoding='utf-8-sig') # the encoding may need to be updated depending on your file, see https://stackoverflow.com/a/17912811
    csv_reader = csv.reader(f, delimiter=',')

    line_number, count_of_updates = 0, 0
    for line in csv_reader:
        line_number = line_number + 1
        try:
            if int(line[0]) > 0 and int(line[1]) > 0:

                # Add the Looker user who has the ID in the first column to the group that has the ID in the second column
                looker.add_users_to_group(line[1], line[0])

                # Remove any roles that have been assigned individually to this user because their roles will now be inherited from their new group
                looker.set_user_role(line[0], [])

                count_of_updates = count_of_updates + 1

        except ValueError:
            print("Ignoring line number " + str(line_number) + ' because this row does not contain two integer values')

    print("Updated groups for " + str(count_of_updates) + " users")


if __name__ == "__main__":
    parse_csv_file_and_add_users_to_groups()

