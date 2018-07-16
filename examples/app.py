# Example application

import upwork
import requests

public_key = 'XXXXXXXXXXXXXXXXXXXXX'
secret_key = 'XXXXXXXXXXXXXXXXXXXXX'

client = upwork.Client(public_key, secret_key)

print client.auth.get_authorize_url()

verifier = raw_input('Enter oauth_verifier: ')
oauth_access_token, oauth_access_token_secret = client.auth.get_access_token(verifier)

client = upwork.Client(public_key, secret_key,
oauth_access_token=oauth_access_token,
oauth_access_token_secret=oauth_access_token_secret)

print client.auth.get_info()
