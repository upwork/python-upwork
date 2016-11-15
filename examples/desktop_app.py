from __future__ import print_function

import upwork
from pprint import pprint

from six.moves import input


def desktop_app():
    """Emulation of desktop app.
    Your keys should be created with project type "Desktop".

    Returns: ``upwork.Client`` instance ready to work.

    """
    print("Emulating desktop app")

    public_key = input("Enter Public API Key > ")
    secret_key = input("Enter Private API Key > ")

    client = upwork.Client(public_key, secret_key)
    verifier = input(
        'Please enter the verification code you get '
        'following this link:\n{0}\n\n> '.format(
            client.auth.get_authorize_url()))

    print('Retrieving keys.... ')
    access_token, access_token_secret = client.auth.get_access_token(verifier)
    print('OK')

    # For further use you can store ``access_toket`` and
    # ``access_token_secret`` somewhere
    client = upwork.Client(public_key, secret_key,
                           oauth_access_token=access_token,
                           oauth_access_token_secret=access_token_secret)
    return client


if __name__ == '__main__':
    client = desktop_app()

    try:
        print("My info")
        pprint(client.auth.get_info())
        print("Team rooms:")
        pprint(client.team_v2.get_teamrooms())
        # HRv2 API
        try:
            print("HR: companies")
            pprint(client.hr.get_companies())
        except:
            print("No access to this portion of API")
        print("HR: teams")
        pprint(client.hr.get_teams())
        print("HR: userroles")
        pprint(client.hr.get_user_roles())
        print("Get jobs")
        pprint(client.provider_v2.search_jobs({'q': 'python'}))
    except Exception as e:
        print("Exception at %s %s" % (client.last_method, client.last_url))
        raise e
