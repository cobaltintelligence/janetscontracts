'''
client.py
Yuan Wang

This script runs on Janet's machine to send updates from the spreadsheet
'''

import requests
import json
import pandas as pd
import dateutil
import datetime
from dateutil.parser import parse
import moment
import numpy as np
## SHEET CONFIG
json_data = open('config.json').read()
config = json.loads(json_data )
# SPREADSHEET_FILEPATH = "/Users/janetwoolman/Google Drive File Stream/My Drive/Tracking Databases/Contract_Management_Database.xlsx"
SPREADSHEET_FILEPATH = config['SPREADSHEET_FILEPATH']
SHEET_NAME = config['SHEET_NAME']
STARTING_ROW = int(config['STARTING_ROW'])
EXPIRATION_COL_NAME = config['EXPIRATION_COL_NAME']
NAME_COL_NAME = config['NAME_COL_NAME']

## SERVER CONFIG
REQUEST_ENDPOINT = "https://hooks.slack.com/services/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"

## Open spreadsheet
#xl = pd.ExcelFile(SPREADSHEET_FILEPATH )
schedule = pd.read_excel(SPREADSHEET_FILEPATH, header = STARTING_ROW)
#schedule = xl.parse(SHEET_NAME)

## Reorganize dataframe
# schedule = schedule[STARTING_ROW:]

nat = np.datetime64('NaT')

def nat_check(nat):
    return nat == np.datetime64('NaT')

now = datetime.datetime.now()


notifs = []
MAX_ROWS = 10
count = 0
for index, row in schedule.iterrows():
	expiration_string = row[EXPIRATION_COL_NAME]
	try:
		expiration = parse(str(expiration_string))
	except:
		continue

	# if it's already past
	if expiration < now:
		continue
	
	# if it's not for a week
	if expiration > now + datetime.timedelta(days=21):
		continue

	notifs.append(row)
	count = count + 1
	if count >= MAX_ROWS:
		break
	

out_text = "Hello! You have "

if len(notifs) > 0:
	out_text = out_text + "the following tasks due within the next three weeks:\n"
	for row in notifs:
		name = row[NAME_COL_NAME]
		exp_date = str(row[EXPIRATION_COL_NAME].date())
		out_text = out_text + ("%s, due on %s \n" % (name, exp_date))
else:
	out_text = out_text + "no upcoming contract expirations these next two weeks."

message_data = {"text": out_text}
print(out_text)
try:
    r = requests.post(
		REQUEST_ENDPOINT, 
		data = json.dumps(message_data),
	    headers={'Content-Type': 'application/json'}
	)
    print(r)
except:
    print("==== WARNING: server not reachable ====")
