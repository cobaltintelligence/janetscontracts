'''
client.py
Yuan Wang

This script runs on Janet's machine to send updates from the spreadsheet
'''

import requests
import json
import pandas as pd
import dateutil
import moment

## SHEET CONFIG
SPREADSHEET_FILEPATH = "./demosheet.xlsx"
SHEET_NAME = "Sheet1"
STARTING_ROW = 2
EXPIRATION_COL_NAME = "Expiration"
NAME_COL_NAME = "Name"

## SERVER CONFIG
REQUEST_ENDPOINT = "https://hooks.slack.com/services/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"

## Open spreadsheet
#xl = pd.ExcelFile(SPREADSHEET_FILEPATH )
schedule = pd.read_excel(SPREADSHEET_FILEPATH, header = 2)
#schedule = xl.parse(SHEET_NAME)

## Reorganize dataframe
# schedule = schedule[STARTING_ROW:]

now = moment.now()

notifs = []
for index, row in schedule.iterrows():
	expiration_string = row[EXPIRATION_COL_NAME]
	expiration = moment.date(expiration_string)

	# if it's already past
	if expiration < now:
		continue

	# if it's not for a week
	if expiration > now.add(weeks=2):
		continue

	notifs.append(row)

out_text = "Hello! You have "

if len(notifs) > 0:
	out_text = out_text + "the following tasks due within the next two weeks:\n"
	for row in notifs:
		name = row[NAME_COL_NAME]
		exp_date = str(row[EXPIRATION_COL_NAME].date())
		out_text = out_text + ("%s, due on %s \n" % (name, exp_date))
else:
	out_text = out_text + "no upcoming contract expirations these next two weeks."

message_data = {"text": out_text}

try:
    r = requests.post(
		REQUEST_ENDPOINT, 
		data = json.dumps(message_data),
	    headers={'Content-Type': 'application/json'}
	)
    print(r)
except:
    print("==== WARNING: server not reachable ====")
