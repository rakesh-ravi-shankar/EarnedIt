import fitbit
from . import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime

CLIENT_ID = '22D8NM'
CLIENT_SECRET = 'bcca650d25f46953dcd2016a7d19b828'

def main():
	print("Hello Fitbit Wrap")

def authorize():
	server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
	server.browser_authorize()
	ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
	REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
	auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

def getAverageSteps(fbuserID):
	# TODO: Query from fitbit
	return 15000

def getCurrentSteps(fbuserID):
	return 0

if __name__ == '__main__':
	authorize()
