import upwork
from pprint import pprint
from upwork.routers import auth
#from upwork.routers.jobs import search
#from upwork.routers.activities import team
#from upwork.routers.reports import time
#from urllib.parse import quote

def get_desktop_client():
    """Emulation of a desktop application.
    Your key should be created with the project type "Desktop".

    Returns: ``upwork.Client`` instance ready to work.

    """
    print("Emulating desktop app")

    consumer_key = input('Please enter consumer key: > ')
    consumer_secret = input('Please enter key secret: > ')
    config = upwork.Config({'consumer_key': consumer_key, 'consumer_secret': consumer_secret})
    """Assign access_token and access_token_secret if they are known
    config = upwork.Config({\
            'consumer_key': 'xxxxxxxxxxx',\
            'consumer_secret': 'xxxxxxxxxxx',\
            'access_token': 'xxxxxxxxxxx',\
            'access_token_secret': 'xxxxxxxxxxx'})
    """

    client = upwork.Client(config)

    try:
        config.access_token
        config.access_token_secret
    except AttributeError:
        verifier = input(
            'Please enter the verification code you get '
            'following this link:\n{0}\n\n> '.format(
                client.get_authorization_url()))

        print('Retrieving keys.... ')
        access_token, access_token_secret = client.get_access_token(verifier)
        print('OK')

    # For further use you can store ``access_toket`` and
    # ``access_token_secret`` somewhere

    return client

if __name__ == '__main__':
    client = get_desktop_client()

    try:
        print("My info")
        pprint(auth.Api(client).get_user_info())
        #pprint(search.Api(client).find({'q': 'php'}))
        #pprint(team.Api(client).add_activity('mycompany', 'mycompany', {'code': 'team-task-001', 'description': 'Description', 'all_in_company': '1'}))
        #pprint(time.Gds(client).get_by_freelancer_full('username', {'tq': quote('SELECT task, memo WHERE worked_on >= "2020-05-01" AND worked_on <= "2020-06-01"')}))
    except Exception as e:
        print("Catch or log exception details")
        raise e
