# -*- coding: utf-8 -*-

# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2018 Upwork

from decimal import Decimal


from upwork import Client
from upwork import utils
from upwork.exceptions import (HTTP400BadRequestError,
                              HTTP401UnauthorizedError,
                              HTTP403ForbiddenError,
                              HTTP404NotFoundError,
                              ApiValueError,
                              IncorrectJsonResponseError)

from upwork.namespaces import Namespace
from upwork.oauth import OAuth
from upwork.routers.team import Team_V3
from upwork.http import UPWORK_ERROR_CODE, UPWORK_ERROR_MESSAGE

from nose.tools import eq_, ok_
from mock import Mock, patch
from upwork.compatibility import HTTPError, httplib, urlparse

try:
    import json
except ImportError:
    import simplejson as json


class MicroMock(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


sample_json_dict = {u'glossary':
                    {u'GlossDiv':
                     {u'GlossList':
                      {u'GlossEntry':
                       {u'GlossDef':
                        {u'GlossSeeAlso': [u'GML', u'XML'],
                         u'para': u'A meta-markup language'},
                         u'GlossSee': u'markup',
                         u'Acronym': u'SGML',
                         u'GlossTerm': u'Standard Generalized Markup Language',
                         u'Abbrev': u'ISO 8879:1986',
                         u'SortAs': u'SGML',
                         u'ID': u'SGML'}},
                         u'title': u'S'},
                         u'title': u'example glossary'}}


def patched_urlopen(*args, **kwargs):
    return MicroMock(data=json.dumps(sample_json_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen)
def test_client_urlopen():
    public_key = 'public'
    secret_key = 'secret'

    client = Client(public_key, secret_key,
                oauth_access_token='some access token',
                oauth_access_token_secret='some access token secret')

    #test urlopen
    data = [{'url': 'http://test.url',
             'data': {'foo': 'bar'},
             'method': 'GET',
             'result_data': None,
             'result_url': 'http://test.url?api_sig=ddbf4b10a47ca8300554441dc7c9042b&api_key=public&foo=bar',
             'result_method': 'GET'},
             {'url': 'http://test.url',
             'data': {},
             'method': 'POST',
             'result_data': 'api_sig=ba343f176db8166c4b7e88911e7e46ec&api_key=public',
             'result_url': 'http://test.url',
             'result_method': 'POST'},
             {'url': 'http://test.url',
             'data': {},
             'method': 'PUT',
             'result_data': 'api_sig=52cbaea073a5d47abdffc7fc8ccd839b&api_key=public&http_method=put',
             'result_url': 'http://test.url',
             'result_method': 'POST'},
             {'url': 'http://test.url',
             'data': {},
             'method': 'DELETE',
             'result_data': 'api_sig=8621f072b1492fbd164d808307ba72b9&api_key=public&http_method=delete',
             'result_url': 'http://test.url',
             'result_method': 'POST'},
             ]

    result_json = json.dumps(sample_json_dict)

    for params in data:
        result = client.urlopen(url=params['url'],
                            data=params['data'],
                            method=params['method'])
        assert result.data == result_json, (result.data, result_json)


def patched_urlopen_error(method, url, code=httplib.BAD_REQUEST,
                          message=None, data=None, **kwargs):
    getheaders = Mock()
    getheaders.return_value = {UPWORK_ERROR_CODE: code,
                               UPWORK_ERROR_MESSAGE: message}
    return MicroMock(data=data, getheaders=getheaders, status=code)


def patched_urlopen_incorrect_json(self, method, url, **kwargs):
    return patched_urlopen_error(
        method, url, code=httplib.OK, data='Service temporarily unavailable')


def patched_urlopen_400(self, method, url, **kwargs):
    return patched_urlopen_error(
        method, url, code=httplib.BAD_REQUEST,
        message='Limit exceeded', **kwargs)


def patched_urlopen_401(self, method, url, **kwargs):
    return patched_urlopen_error(
        method, url, code=httplib.UNAUTHORIZED,
        message='Not authorized', **kwargs)


def patched_urlopen_403(self, method, url, **kwargs):
    return patched_urlopen_error(
        method, url, code=httplib.FORBIDDEN,
        message='Forbidden', **kwargs)


def patched_urlopen_404(self, method, url, **kwargs):
    return patched_urlopen_error(
        method, url, code=httplib.NOT_FOUND,
        message='Not found', **kwargs)


def patched_urlopen_500(self, method, url, **kwargs):
    return patched_urlopen_error(
        method, url, code=httplib.INTERNAL_SERVER_ERROR,
        message='Internal server error', **kwargs)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_incorrect_json)
def client_read_incorrect_json(client, url):
    return client.read(url)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_400)
def client_read_400(client, url):
    return client.read(url)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_401)
def client_read_401(client, url):
    return client.read(url)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_403)
def client_read_403(client, url):
    return client.read(url)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_404)
def client_read_404(client, url):
    return client.read(url)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_500)
def client_read_500(client, url):
    return client.read(url)


@patch('urllib3.PoolManager.urlopen', patched_urlopen)
def test_client_read():
    """Test client read() method.

    Test cases:
      method default (get) - other we already tested

      format json|yaml ( should produce error)

      codes 200|400|401|403|404|500

    """
    public_key = 'public'
    secret_key = 'secret'

    client = Client(public_key, secret_key,
                oauth_access_token='some access token',
                oauth_access_token_secret='some access token secret')
    test_url = 'http://test.url'

    # Produce error on format other then json
    class NotJsonException(Exception):
        pass

    try:
        client.read(url=test_url, format='yaml')
        raise NotJsonException("Client.read() doesn't produce error on "
                               "yaml format")
    except NotJsonException as e:
        raise e
    except Exception:
        pass

    # Test get, all ok
    result = client.read(url=test_url)
    assert result == sample_json_dict, result

    # Test get and status is ok, but json is incorrect,
    # IncorrectJsonResponseError should be raised
    try:
        result = client_read_incorrect_json(client=client, url=test_url)
        ok_(0, "No exception raised for 200 code and "
               "incorrect json response: {0}".format(result))
    except IncorrectJsonResponseError:
        pass
    except Exception as e:
        assert 0, "Incorrect exception raised for 200 code " \
            "and incorrect json response: " + str(e)

    # Test get, 400 error
    try:
        result = client_read_400(client=client, url=test_url)
    except HTTP400BadRequestError as e:
        pass
    except Exception as e:
        assert 0, "Incorrect exception raised for 400 code: " + str(e)

    # Test get, 401 error
    try:
        result = client_read_401(client=client, url=test_url)
    except HTTP401UnauthorizedError as e:
        pass
    except Exception as e:
        assert 0, "Incorrect exception raised for 401 code: " + str(e)

    # Test get, 403 error
    try:
        result = client_read_403(client=client, url=test_url)
    except HTTP403ForbiddenError as e:
        pass
    except Exception as e:
        assert 0, "Incorrect exception raised for 403 code: " + str(e)

    # Test get, 404 error
    try:
        result = client_read_404(client=client, url=test_url)
    except HTTP404NotFoundError as e:
        pass
    except Exception as e:
        assert 0, "Incorrect exception raised for 404 code: " + str(e)

    # Test get, 500 error
    try:
        result = client_read_500(client=client, url=test_url)
    except HTTPError as e:
        if e.code == httplib.INTERNAL_SERVER_ERROR:
            pass
        else:
            assert 0, "Incorrect exception raised for 500 code: " + str(e)
    except Exception as e:
        assert 0, "Incorrect exception raised for 500 code: " + str(e)


def get_client():
    public_key = 'public'
    secret_key = 'secret'
    oauth_access_token = 'some token'
    oauth_access_token_secret = 'some token secret'
    return Client(public_key, secret_key,
                  oauth_access_token,
                  oauth_access_token_secret)


@patch('urllib3.PoolManager.urlopen', patched_urlopen)
def test_client():
    c = get_client()
    test_url = "http://test.url"

    result = c.get(test_url)
    assert result == sample_json_dict, result

    result = c.post(test_url)
    assert result == sample_json_dict, result

    result = c.put(test_url)
    assert result == sample_json_dict, result

    result = c.delete(test_url)
    assert result == sample_json_dict, result


@patch('urllib3.PoolManager.urlopen', patched_urlopen)
def test_namespace():
    ns = Namespace(get_client())
    test_url = "http://test.url"

    #test full_url
    full_url = ns.full_url('test')
    assert full_url == 'https://www.upwork.com/api/Nonev1/test', full_url

    result = ns.get(test_url)
    assert result == sample_json_dict, result

    result = ns.post(test_url)
    assert result == sample_json_dict, result

    result = ns.put(test_url)
    assert result == sample_json_dict, result

    result = ns.delete(test_url)
    assert result == sample_json_dict, result


teamrooms_dict = {'teamrooms':
                  {'teamroom':
                   {u'team_ref': u'1',
                    u'name': u'Upwork',
                    u'recno': u'1',
                    u'parent_team_ref': u'1',
                    u'company_name': u'Upwork',
                    u'company_recno': u'1',
                    u'teamroom_api': u'/api/team/v1/teamrooms/upwork:some.json',
                    u'id': u'upwork:some'}},
                  'teamroom': {'snapshot': 'test snapshot'},
                  'snapshots': {'user': 'test', 'snapshot': 'test'},
                  'data': {'user': 'test', 'snapshot': 'test'},
                  'snapshot': {'status': 'private'}
                 }


def patched_urlopen_team(*args, **kwargs):
    return MicroMock(data=json.dumps(teamrooms_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_team)
def test_team():
    te_v3 = Team_V3(get_client())

    #test full_url
    full_url = te_v3.full_url('test')
    assert full_url == 'https://www.upwork.com/api/team/v3/test', full_url

    #test get_snapshot by contract
    assert te_v3.get_snapshot_by_contract(1, 1) == teamrooms_dict['snapshot'], \
        te_v3.get_snapshot_by_contract(1, 1)

    #test update_snapshot by contract
    assert te_v3.update_snapshot_by_contract(1, 1, memo='memo', task='1234', task_desc='desc') == teamrooms_dict, \
        te_v3.update_snapshot_by_contract(1, 1, memo='memo', task='1234', task_desc='desc')

    #test delete_snapshot by contract
    assert te_v3.delete_snapshot_by_contract(1, 1) == teamrooms_dict, \
        te_v3.delete_snapshot_by_contract(1, 1)

    #test get_workdiaries
    eq_(te_v3.get_workdiaries(1, 1), [{'snapshot':'test', 'user':'test'}])

    #test get_workdiaries_by_contract
    eq_(te_v3.get_workdiaries_by_contract(1, 1), [])

    #test get_workdays
    eq_(te_v3.get_workdays_by_company(1, 1, 1), {})

    #test get_workdays_by_contract
    eq_(te_v3.get_workdays_by_contract(1, 1, 1), {})

    #test get_snapshot_by_contract
    eq_(te_v3.get_snapshot_by_contract(1, 1), {'status':'private'})


teamrooms_dict_none = {'teamrooms': '',
                       'teamroom': '',
                       'snapshots': '',
                       'snapshot': ''
                       }


def patched_urlopen_teamrooms_none(*args, **kwargs):
    return MicroMock(data=json.dumps(teamrooms_dict_none), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_teamrooms_none)
def test_teamrooms_none():
    te_v3 = Team_V3(get_client())

    #test full_url
    full_url = te_v3.full_url('test')
    assert full_url == 'https://www.upwork.com/api/team/v3/test', full_url


userroles = {u'userrole':
             [{u'parent_team__reference': u'1',
              u'user__id': u'testuser', u'team__id': u'test:t',
              u'reference': u'1', u'team__name': u'te',
              u'company__reference': u'1',
              u'user__reference': u'1',
              u'user__first_name': u'Test',
              u'user__last_name': u'Development',
              u'parent_team__id': u'testdev',
              u'team__reference': u'1', u'role': u'manager',
              u'affiliation_status': u'none', u'engagement__reference': u'',
              u'parent_team__name': u'TestDev', u'has_team_room_access': u'1',
              u'company__name': u'Test Dev',
              u'permissions':
                {u'permission': [u'manage_employment', u'manage_recruiting']}}]}

engagement = {u'status': u'active',
              u'buyer_team__reference': u'1', u'provider__reference': u'2',
              u'job__title': u'development', u'roles': {u'role': u'buyer'},
              u'reference': u'1', u'engagement_end_date': u'',
              u'fixed_price_upfront_payment': u'0',
              u'fixed_pay_amount_agreed': u'1.00',
              u'provider__id': u'test_provider',
              u'buyer_team__id': u'testteam:aa',
              u'engagement_job_type': u'fixed-price',
              u'job__reference': u'1', u'provider_team__reference': u'',
              u'engagement_title': u'Developer',
              u'fixed_charge_amount_agreed': u'0.01',
              u'created_time': u'0000', u'provider_team__id': u'',
              u'offer__reference': u'',
              u'engagement_start_date': u'000', u'description': u''}

engagements = {u'lister':
               {u'total_items': u'10', u'query': u'',
                u'paging': {u'count': u'10', u'offset': u'0'}, u'sort': u''},
               u'engagement': [engagement, engagement],
               }

offer = {u'provider__reference': u'1',
         u'signed_by_buyer_user': u'',
         u'reference': u'1', u'job__description': u'python',
         u'buyer_company__name': u'Python community',
         u'engagement_title': u'developer', u'created_time': u'000',
         u'buyer_company__reference': u'2', u'buyer_team__id': u'testteam:aa',
         u'interview_status': u'in_process', u'buyer_team__reference': u'1',
         u'signed_time_buyer': u'', u'has_buyer_signed': u'',
         u'signed_time_provider': u'', u'created_by': u'testuser',
         u'job__reference': u'2', u'engagement_start_date': u'00000',
         u'fixed_charge_amount_agreed': u'0.01', u'provider_team__id': u'',
         u'status': u'', u'signed_by_provider_user': u'',
         u'engagement_job_type': u'fixed-price', u'description': u'',
         u'provider_team__name': u'', u'fixed_pay_amount_agreed': u'0.01',
         u'candidacy_status': u'active', u'has_provider_signed': u'',
         u'message_from_provider': u'', u'my_role': u'buyer',
         u'key': u'~~0001', u'message_from_buyer': u'',
         u'buyer_team__name': u'Python community 2',
         u'engagement_end_date': u'', u'fixed_price_upfront_payment': u'0',
         u'created_type': u'buyer', u'provider_team__reference': u'',
         u'job__title': u'translation', u'expiration_date': u'',
         u'engagement__reference': u''}

offers = {u'lister':
          {u'total_items': u'10', u'query': u'', u'paging':
           {u'count': u'10', u'offset': u'0'}, u'sort': u''},
           u'offer': [offer, offer]}

job = {u'subcategory2': u'Development', u'reference': u'1',
       u'buyer_company__name': u'Python community',
       u'job_type': u'fixed-price', u'created_time': u'000',
       u'created_by': u'test', u'duration': u'',
       u'last_candidacy_access_time': u'',
       u'category2': u'Web',
       u'buyer_team__reference': u'169108', u'title': u'translation',
       u'buyer_company__reference': u'1', u'num_active_candidates': u'0',
       u'buyer_team__name': u'Python community 2', u'start_date': u'000',
       u'status': u'filled', u'num_new_candidates': u'0',
       u'description': u'test', u'end_date': u'000',
       u'public_url': u'http://www.upwork.com/jobs/~~0001',
       u'visibility': u'invite-only', u'buyer_team__id': u'testteam:aa',
       u'num_candidates': u'1', u'budget': u'1000', u'cancelled_date': u'',
       u'filled_date': u'0000'}

jobs = [job, job]

task = {u'reference': u'test', u'company_reference': u'1',
          u'team__reference': u'1', u'user__reference': u'1',
          u'code': u'1', u'description': u'test task',
          u'url': u'http://url.upwork.com/task', u'level': u'1'}

tasks = [task, task]

auth_user = {u'first_name': u'TestF', u'last_name': u'TestL',
             u'uid': u'testuser', u'timezone_offset': u'0',
             u'timezone': u'Europe/Athens', u'mail': u'test_user@upwork.com',
             u'messenger_id': u'', u'messenger_type': u'yahoo'}

user = {u'status': u'active', u'first_name': u'TestF',
        u'last_name': u'TestL', u'reference': u'0001',
        u'timezone_offset': u'10800',
        u'public_url': u'http://www.upwork.com/users/~~000',
        u'is_provider': u'1',
        u'timezone': u'GMT+02:00 Athens, Helsinki, Istanbul',
        u'id': u'testuser'}

team = {u'status': u'active', u'parent_team__reference': u'0',
         u'name': u'Test',
         u'reference': u'1',
         u'company__reference': u'1',
         u'id': u'test',
         u'parent_team__id': u'test_parent',
         u'company_name': u'Test', u'is_hidden': u'',
         u'parent_team__name': u'Test parent'}

company = {u'status': u'active',
             u'name': u'Test',
             u'reference': u'1',
             u'company_id': u'1',
             u'owner_user_id': u'1', }

hr_dict = {u'auth_user': auth_user,
           u'server_time': u'0000',
           u'user': user,
           u'team': team,
           u'company': company,
            u'teams': [team, team],
            u'companies': [company, company],
            u'users': [user, user],
            u'tasks': task,
            u'userroles': userroles,
            u'engagements': engagements,
            u'engagement': engagement,
            u'offer': offer,
            u'offers': offers,
            u'job': job,
            u'jobs': jobs}


def patched_urlopen_hr(*args, **kwargs):
    return MicroMock(data=json.dumps(hr_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_user():
    hr = get_client().hr

    #test get_user
    assert hr.get_user(1) == hr_dict[u'user'], hr.get_user(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_companies():
    hr = get_client().hr
    #test get_companies
    assert hr.get_companies() == hr_dict[u'companies'], hr.get_companies()

    #test get_company
    assert hr.get_company(1) == hr_dict[u'company'], hr.get_company(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_company_teams():
    hr = get_client().hr
    #test get_company_teams
    assert hr.get_company_teams(1) == hr_dict['teams'], hr.get_company_teams(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_company_users():
    hr = get_client().hr
    #test get_company_users
    assert hr.get_company_users(1) == hr_dict['users'], hr.get_company_users(1)
    assert hr.get_company_users(1, False) == hr_dict['users'], \
        hr.get_company_users(1, False)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_teams():
    hr = get_client().hr
    #test get_teams
    assert hr.get_teams() == hr_dict[u'teams'], hr.get_teams()

    #test get_team
    assert hr.get_team(1) == hr_dict[u'team'], hr.get_team(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_team_users():
    hr = get_client().hr
    #test get_team_users
    assert hr.get_team_users(1) == hr_dict[u'users'], hr.get_team_users(1)
    assert hr.get_team_users(1, False) == hr_dict[u'users'], \
        hr.get_team_users(1, False)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_userroles():
    hr = get_client().hr
    #test get_user_roles
    assert hr.get_user_roles() == hr_dict['userroles'], hr.get_user_role()


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_jobs():
    hr = get_client().hr
    #test get_jobs
    assert hr.get_jobs(1) == hr_dict[u'jobs'], hr.get_jobs()
    assert hr.get_job(1) == hr_dict[u'job'], hr.get_job(1)
    result = hr.update_job(1, 2, 'title', 'desc', 'public', budget=100,
                           status='open')
    eq_(result, hr_dict)
    assert hr.delete_job(1, 41) == hr_dict, hr.delete_job(1, 41)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_offers():
    hr = get_client().hr
    #test get_offers
    assert hr.get_offers(1) == hr_dict[u'offers'], hr.get_offers()
    assert hr.get_offer(1) == hr_dict[u'offer'], hr.get_offer(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_get_hrv2_engagements():
    hr = get_client().hr

    eq_(hr.get_engagements(), hr_dict[u'engagements'])

    eq_(hr.get_engagements(provider_reference=1), hr_dict[u'engagements'])
    eq_(hr.get_engagements(profile_key=1), hr_dict[u'engagements'])
    eq_(hr.get_engagement(1), hr_dict[u'engagement'])


adjustments = {u'adjustment': {u'reference': '100'}}


def patched_urlopen_hradjustment(*args, **kwargs):
    return MicroMock(data=json.dumps(adjustments), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hradjustment)
def test_hrv2_post_adjustment():
    hr = get_client().hr

    # Using ``charge_amount``
    result = hr.post_team_adjustment(
        1, 2, 'a test', charge_amount=100, notes='test note')
    assert result == adjustments[u'adjustment'], result

    try:
        # If ``charge_amount`` is absent,
        # error should be raised
        hr.post_team_adjustment(1, 2, 'a test', notes='test note', charge_amount=0)
        raise Exception('No error ApiValueError was raised when ``charge_amount`` is absent')
    except ApiValueError:
        pass


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_hr_end_contract():
    hr = get_client().hr

    result = hr.end_contract(1, 'API_REAS_JOB_COMPLETED_SUCCESSFULLY', 'yes')
    assert result == hr_dict, result

    # Test options validation
    try:
        result = hr.end_contract(1, 'reason', 'yes')
        assert result == hr_dict, result
    except ApiValueError:
        pass


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_hr_suspend_contract():
    hr = get_client().hr

    result = hr.suspend_contract(1, 'message')
    assert result == hr_dict, result


@patch('urllib3.PoolManager.urlopen', patched_urlopen_hr)
def test_hr_restart_contract():
    hr = get_client().hr

    result = hr.restart_contract(1, 'message')
    assert result == hr_dict, result


job_data2 = {
    'buyer_team_reference': 111,
    'title': 'Test job from API',
    'job_type': 'hourly',
    'description': 'this is test job, please do not apply to it',
    'visibility': 'upwork',
    'category2': 'Web, Mobile & Software Dev',
    'subcategory2': 'Web & Mobile Development',
    'budget': 100,
    'duration': 10,
    'start_date': 'some start date',
    'skills': ['Python', 'JS']
}


def patched_urlopen_job_data_parameters2(self, method, url, **kwargs):
    post_dict = urlparse.parse_qs(kwargs.get('body'))
    post_dict.pop('oauth_timestamp')
    post_dict.pop('oauth_signature')
    post_dict.pop('oauth_nonce')
    eq_(
        dict(post_dict.items()),
        {'buyer_team__reference': ['111'],
         'category2': ['Web, Mobile & Software Dev'],
         'subcategory2': ['Web & Mobile Development'],
         'title': ['Test job from API'],
         'skills': ['Python;JS'], 'job_type': ['hourly'],
         'oauth_consumer_key': ['public'],
         'oauth_signature_method': ['HMAC-SHA1'], 'budget': ['100'],
         'visibility': ['upwork'],
         'oauth_version': ['1.0'], 'oauth_token': ['some token'],
         'oauth_body_hash': ['2jmj7l5rSw0yVb/vlWAYkK/YBwk='],
         'duration': ['10'],
         'start_date': ['some start date'],
         'description': ['this is test job, please do not apply to it']})
    return MicroMock(data='{"some":"data"}', status=200)


def patched_urlopen_job_data_parameters(self, method, url, **kwargs):
    post_dict = urlparse.parse_qs(kwargs.get('body'))
    post_dict.pop('oauth_timestamp')
    post_dict.pop('oauth_signature')
    post_dict.pop('oauth_nonce')
    eq_(
        dict(post_dict.items()),
        {'category2': ['Web Development'], 'buyer_team__reference': ['111'],
         'subcategory2': ['Other - Web Development'],
         'title': ['Test job from API'],
         'skills': ['Python;JS'], 'job_type': ['hourly'],
         'oauth_consumer_key': ['public'],
         'oauth_signature_method': ['HMAC-SHA1'], 'budget': ['100'],
         'visibility': ['upwork'],
         'oauth_version': ['1.0'], 'oauth_token': ['some token'],
         'oauth_body_hash': ['2jmj7l5rSw0yVb/vlWAYkK/YBwk='],
         'duration': ['10'],
         'start_date': ['some start date'],
         'description': ['this is test job, please do not apply to it']})
    return MicroMock(data='{"some":"data"}', status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_job_data_parameters2)
def test_job_data_parameters_subcategory2():
    hr = get_client().hr
    hr.post_job(**job_data2)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_job_data_parameters)
def test_job_data_no_category():
    hr = get_client().hr

    try:
        hr.post_job('111', 'test', 'hourly', 'descr', 'upwork')
        raise Exception('Request should raise ApiValueError exception.')
    except ApiValueError:
        pass

provider_dict = {'profile':
                 {u'response_time': u'31.0000000000000000',
                  u'dev_agency_ref': u'',
                  u'dev_adj_score_recent': u'0',
                  u'dev_ui_profile_access': u'Public',
                  u'dev_portrait': u'',
                  u'dev_ic': u'Freelance Provider',
                  u'certification': u'',
                  u'dev_usr_score': u'0',
                  u'dev_country': u'Ukraine',
                  u'dev_recent_rank_percentile': u'0',
                  u'dev_profile_title': u'Python developer',
                  u'dev_groups': u'',
                  u'dev_scores':
                  {u'dev_score':
                   [{u'description': u'competency and skills for the job, understanding of specifications/instructions',
                     u'avg_category_score_recent': u'',
                     u'avg_category_score': u'',
                     u'order': u'1', u'label': u'Skills'},
                     {u'description': u'quality of work deliverables',
                      u'avg_category_score_recent': u'',
                      u'avg_category_score': u'', u'order': u'2', u'label': u'Quality'},
                      ]
                   }},
                   'providers': {'test': 'test'},
                   'jobs': {'test': 'test'},
                   'otherexp': 'experiences',
                   'skills': 'skills',
                   'tests': 'tests',
                   'certificates': 'certificates',
                   'employments': 'employments',
                   'educations': 'employments',
                   'projects': 'projects',
                   'quick_info': 'quick_info',
                   'categories': 'category 1',
                   'regions': 'region 1',
                   'tests': 'test 1',
                   }


def patched_urlopen_provider(*args, **kwargs):
    return MicroMock(data=json.dumps(provider_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_provider)
def test_provider():
    pr = get_client().provider

    #test full_url
    full_url = pr.full_url('test')
    assert full_url == 'https://www.upwork.com/api/profiles/v1/test', full_url

    #test get_provider
    assert pr.get_provider(1) == provider_dict['profile'], pr.get_provider(1)

    #test get_provider_brief
    assert pr.get_provider_brief(1) == provider_dict['profile'], \
        pr.get_provider_brief(1)

    result = pr.get_skills_metadata()
    assert result == provider_dict['skills']

    result = pr.get_regions_metadata()
    assert result == provider_dict['regions']

    result = pr.get_tests_metadata()
    assert result == provider_dict['tests']


rooms_dict = {u'rooms': []}

def patched_urlopen_rooms(*args, **kwargs):
    return MicroMock(data=json.dumps(rooms_dict), status=200)

@patch('urllib3.PoolManager.urlopen', patched_urlopen_rooms)
def test_get_rooms():
    messages = get_client().messages

    #test full_url
    full_url = messages.full_url('testcompany/rooms')
    assert full_url == 'https://www.upwork.com/api/messages/v3/testcompany/rooms', full_url

    #test get_rooms
    assert messages.get_rooms("testcompany") == rooms_dict, messages.get_rooms("testcompany")

room_dict = {u'room': {}}

def patched_urlopen_room(*args, **kwargs):
    return MicroMock(data=json.dumps(room_dict), status=200)

@patch('urllib3.PoolManager.urlopen', patched_urlopen_room)
def test_get_room_details():
    messages = get_client().messages

    #test get_room_details
    assert messages.get_room_details("testcompany", "room-id") ==\
	room_dict, messages.get_room_details("testcompany", "room-id")

@patch('urllib3.PoolManager.urlopen', patched_urlopen_room)
def test_get_room_by_offer():
    messages = get_client().messages

    #test get_room_by_offer
    assert messages.get_room_by_offer("testcompany", "1234") ==\
	room_dict, messages.get_room_by_offer("testcompany", "1234")

@patch('urllib3.PoolManager.urlopen', patched_urlopen_room)
def test_get_room_by_application():
    messages = get_client().messages

    #test get_room_by_applications
    assert messages.get_room_by_application("testcompany", "1234") ==\
	room_dict, messages.get_room_by_application("testcompany", "1234")

@patch('urllib3.PoolManager.urlopen', patched_urlopen_room)
def test_get_room_by_contract():
    messages = get_client().messages

    #test get_room_by_contract
    assert messages.get_room_by_contract("testcompany", "1234") ==\
	room_dict, messages.get_room_by_contract("testcompany", "1234")

read_room_content_dict = {"room": {"test": '1'}}

def patched_urlopen_read_room_content(*args, **kwargs):
    return MicroMock(data=json.dumps(read_room_content_dict), status=200)

@patch('urllib3.PoolManager.urlopen', patched_urlopen_read_room_content)
def test_create_room():
    messages = get_client().messages

    message = messages.create_room('testcompany', {'roomName': 'test room'})
    assert message == read_room_content_dict, message

@patch('urllib3.PoolManager.urlopen', patched_urlopen_read_room_content)
def test_send_message_to_room():
    messages = get_client().messages

    message = messages.send_message_to_room('testcompany', 'room-id', {'message': 'test message'})
    assert message == read_room_content_dict, message

@patch('urllib3.PoolManager.urlopen', patched_urlopen_read_room_content)
def test_update_room_settings():
    messages = get_client().messages

    message = messages.update_room_settings('testcompany', 'room-id', 'userid', {'isFavorite': 'true'})
    assert message == read_room_content_dict, message

@patch('urllib3.PoolManager.urlopen', patched_urlopen_read_room_content)
def test_update_room_metadata():
    messages = get_client().messages

    message = messages.update_room_metadata('testcompany', 'room-id', {'isReadOnly': 'true'})
    assert message == read_room_content_dict, message


timereport_dict = {u'table':
     {u'rows':
      [{u'c':
        [{u'v': u'20100513'},
         {u'v': u'company1:team1'},
         {u'v': u'1'},
         {u'v': u'1'},
         {u'v': u'0'},
         {u'v': u'1'},
         {u'v': u'Bug 1: Test'}]}],
         u'cols':
         [{u'type': u'date', u'label': u'worked_on'},
          {u'type': u'string', u'label': u'assignment_team_id'},
          {u'type': u'number', u'label': u'hours'},
          {u'type': u'number', u'label': u'earnings'},
          {u'type': u'number', u'label': u'earnings_offline'},
          {u'type': u'string', u'label': u'task'},
          {u'type': u'string', u'label': u'memo'}]}}


def patched_urlopen_timereport_content(*args, **kwargs):
    return MicroMock(data=json.dumps(timereport_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_timereport_content)
def test_get_provider_timereport():
    tc = get_client().timereport

    read = tc.get_provider_report('test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == timereport_dict, read

    read = tc.get_provider_report('test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)),
                                                hours=True)
    assert read == timereport_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_timereport_content)
def test_get_company_timereport():
    tc = get_client().timereport

    read = tc.get_company_report('test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == timereport_dict, read

    read = tc.get_company_report('test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)),
                                  hours=True)
    assert read == timereport_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_timereport_content)
def test_get_agency_timereport():
    tc = get_client().timereport

    read = tc.get_agency_report('test', 'test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == timereport_dict, read

    read = tc.get_agency_report('test', 'test',\
        utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)),
                                  hours=True)
    assert read == timereport_dict, read

fin_report_dict = {u'table':
     {u'rows':
      [{u'c':
        [{u'v': u'20100513'},
         {u'v': u'upwork:upworkps'},
         {u'v': u'1'},
         {u'v': u'1'},
         {u'v': u'0'},
         {u'v': u'1'},
         {u'v': u'Bug 1: Test'}]}],
         u'cols':
         [{u'type': u'date', u'label': u'worked_on'},
          {u'type': u'string', u'label': u'assignment_team_id'},
          {u'type': u'number', u'label': u'hours'},
          {u'type': u'number', u'label': u'earnings'},
          {u'type': u'number', u'label': u'earnings_offline'},
          {u'type': u'string', u'label': u'task'},
          {u'type': u'string', u'label': u'memo'}]}}


def patched_urlopen_fin_report_content(*args, **kwargs):
    return MicroMock(data=json.dumps(fin_report_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_billings():
    fr = get_client().finreport

    read = fr.get_provider_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_teams_billings():
    fr = get_client().finreport

    read = fr.get_provider_teams_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_companies_billings():
    fr = get_client().finreport

    read = fr.get_provider_companies_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_earnings():
    fr = get_client().finreport

    read = fr.get_provider_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_teams_earnings():
    fr = get_client().finreport

    read = fr.get_provider_teams_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_provider_companies_earnings():
    fr = get_client().finreport

    read = fr.get_provider_companies_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_buyer_teams_billings():
    fr = get_client().finreport

    read = fr.get_buyer_teams_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_buyer_companies_billings():
    fr = get_client().finreport

    read = fr.get_buyer_companies_billings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_buyer_teams_earnings():
    fr = get_client().finreport

    read = fr.get_buyer_teams_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_buyer_companies_earnings():
    fr = get_client().finreport

    read = fr.get_buyer_companies_earnings('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_financial_entities():
    fr = get_client().finreport

    read = fr.get_financial_entities('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


@patch('urllib3.PoolManager.urlopen', patched_urlopen_fin_report_content)
def test_get_financial_entities_provider():
    fr = get_client().finreport

    read = fr.get_financial_entities_provider('test', utils.Query(select=['1', '2', '3'], where=(utils.Q('2') > 1)))
    assert read == fin_report_dict, read


task_dict = {u'tasks': 'task1'}

def patched_urlopen_task(*args, **kwargs):
    return MicroMock(data=json.dumps(task_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_get_team_tasks():
    task = get_client().task

    assert task.get_team_tasks(1, 1) == task_dict, \
        task.get_team_tasks(1, 1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_get_company_tasks():
    task = get_client().task

    assert task.get_company_tasks(1) == task_dict, \
        task.get_company_tasks(1)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_get_team_specific_tasks():
    task = get_client().task

    assert task.get_team_specific_tasks(1, 1, [1, 1]) == task_dict['tasks'], \
        task.get_team_specific_tasks(1, 1, [1, 1])


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_get_company_specific_tasks():
    task = get_client().task

    assert task.get_company_specific_tasks(1, [1, 1]) == task_dict['tasks'], \
        task.get_company_specific_tasks(1, [1, 1])


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_post_team_task():
    task = get_client().task

    assert task.post_team_task(1, 1, 1, '1', 'ttt',
                               engagements=[1, 2],
                               all_in_company=True) == task_dict, \
        task.post_team_task(1, 1, 1, '1', 'ttt', engagements=[1, 2],
                            all_in_company=True)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_post_company_task():
    task = get_client().task

    assert task.post_company_task(1, 1, '1', 'ttt',
                                  engagements=[1, 2],
                                  all_in_company=True) == task_dict, \
        task.post_company_task(1, 1, '1', 'ttt')


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_put_team_task():
    task = get_client().task

    assert task.put_team_task(1, 1, 1, '1', 'ttt',
                              engagements=[1, 2],
                              all_in_company=True) == task_dict, \
        task.put_team_task(1, 1, 1, '1', 'ttt', engagements=[1, 2],
                           all_in_company=True)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_put_company_task():
    task = get_client().task

    assert task.put_company_task(1, 1, '1', 'ttt', engagements=[1, 2],
                                 all_in_company=True) == task_dict, \
        task.put_company_task(1, 1, '1', 'ttt', engagements=[1, 2],
                              all_in_company=True)

@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_assign_to_engagement():
    task_v2 = get_client().task_v2

    assert task_v2.assign_to_engagement(1, "1;2") == task_dict, \
        task_v2.task_assign_to_engagement(1, "1;2")


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_archive_team_task():
    task = get_client().task

    assert task.archive_team_task(1, 1, 1) == task_dict, \
        task.archive_team_task(1, 1, 1)

    # Test multiple task codes
    assert task.archive_team_task(1, 1, [1, 2]) == task_dict, \
        task.archive_team_task(1, 1, [1, 2])


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_archive_company_task():
    task = get_client().task

    assert task.archive_company_task(1, 1) == task_dict, \
        task.archive_company_task(1, 1)

    # Test multiple task codes
    assert task.archive_company_task(1, [1, 2]) == task_dict, \
        task.archive_company_task(1, [1, 2])


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_unarchive_team_task():
    task = get_client().task

    assert task.unarchive_team_task(1, 1, 1) == task_dict, \
        task.unarchive_team_task(1, 1, 1)

    # Test multiple task codes
    assert task.unarchive_team_task(1, 1, [1, 2]) == task_dict, \
        task.unarchive_team_task(1, 1, [1, 2])


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_unarchive_company_task():
    task = get_client().task

    assert task.unarchive_company_task(1, 1) == task_dict, \
        task.unarchive_company_task(1, 1)

    # Test multiple task codes
    assert task.unarchive_company_task(1, [1, 2]) == task_dict, \
        task.unarchive_company_task(1, [1, 2])


@patch('urllib3.PoolManager.urlopen', patched_urlopen_task)
def test_update_batch_tasks():
    task = get_client().task

    assert task.update_batch_tasks(1, "1;2;3") == task_dict, \
        task.update_batch_tasks(1, "1;2;3")


def test_gds_namespace():
    from upwork.namespaces import GdsNamespace
    gds = GdsNamespace(get_client())

    assert gds.post('test.url', {}) is None, \
        gds.post('test.url', {})
    assert gds.put('test.url', {}) is None, \
        gds.put('test.url', {})
    assert gds.delete('test.url', {}) is None, \
        gds.delete('test.url', {})


@patch('urllib3.PoolManager.urlopen', patched_urlopen)
def test_gds_namespace_get():
    from upwork.namespaces import GdsNamespace
    gds = GdsNamespace(get_client())
    result = gds.get('http://test.url')
    assert isinstance(result, dict), type(res)
    assert result == sample_json_dict, (result, sample_json_dict)


def setup_oauth():
    return OAuth(get_client())


def test_oauth_full_url():
    oa = setup_oauth()
    request_token_url = oa.full_url('oauth/token/request')
    access_token_url = oa.full_url('oauth/token/access')
    assert request_token_url == oa.request_token_url, request_token_url
    assert access_token_url == oa.access_token_url, access_token_url


def patched_httplib2_request(*args, **kwargs):
    return {'status': '200'},\
        'oauth_callback_confirmed=1&oauth_token=709d434e6b37a25c50e95b0e57d24c46&oauth_token_secret=193ef27f57ab4e37'

@patch('httplib2.Http.request', patched_httplib2_request)
def test_oauth_get_request_token():
    oa = setup_oauth()
    assert oa.get_request_token() == ('709d434e6b37a25c50e95b0e57d24c46',\
                                    '193ef27f57ab4e37')


@patch('httplib2.Http.request', patched_httplib2_request)
def test_oauth_get_authorize_url():
    oa = setup_oauth()
    assert oa.get_authorize_url() ==\
        'https://www.upwork.com/services/api/auth?oauth_token=709d434e6b37a25c50e95b0e57d24c46'
    assert oa.get_authorize_url('http://example.com/oauth/complete') ==\
        'https://www.upwork.com/services/api/auth?oauth_token=709d434e6b37a25c50e95b0e57d24c46&oauth_callback=http%3A%2F%2Fexample.com%2Foauth%2Fcomplete'

def patched_httplib2_access(*args, **kwargs):
    return {'status': '200'},\
        'oauth_token=aedec833d41732a584d1a5b4959f9cd6&oauth_token_secret=9d9cccb363d2b13e'


@patch('httplib2.Http.request', patched_httplib2_access)
def test_oauth_get_access_token():
    oa = setup_oauth()
    oa.request_token = '709d434e6b37a25c50e95b0e57d24c46'
    oa.request_token_secret = '193ef27f57ab4e37'
    assert oa.get_access_token('9cbcbc19f8acc2d85a013e377ddd4118') ==\
     ('aedec833d41732a584d1a5b4959f9cd6', '9d9cccb363d2b13e')


job_profiles_dict = {'profiles': {'profile': [
    {
        u'amount': u'',
        u'as_hrs_per_week': u'0',
        u'as_job_type': u'Hourly',
        u'as_opening_access': u'private',
        u'as_opening_recno': u'111',
        u'as_opening_title': u'Review website and improve copy writing',
        u'as_provider': u'111',
        u'as_rate': u'$10.00',
        u'as_reason': u'Job was cancelled or postponed',
        u'as_reason_api_ref': u'',
        u'as_reason_recno': u'72',
        u'as_recno': u'1',
        u'as_status': u'Closed',
        u'as_to': u'11/2011',
        u'as_total_charge': u'84',
        u'as_total_hours': u'3.00',
        u'op_desc_digest': u'Test job 1.',
        u'op_description': u'Test job 1.',
        u'ciphertext': u'~~111111111',
        u'ui_job_profile_access': u'upwork',
        u'ui_opening_status': u'Active',
        u'version': u'1'
    },
    {
        u'amount': u'',
        u'as_hrs_per_week': u'0',
        u'as_job_type': u'Hourly',
        u'as_opening_access': u'private',
        u'as_opening_recno': u'222',
        u'as_opening_title': u'Review website and improve copy writing',
        u'as_provider': u'222',
        u'as_rate': u'$10.00',
        u'as_reason': u'Job was cancelled or postponed',
        u'as_reason_api_ref': u'',
        u'as_reason_recno': u'72',
        u'as_recno': u'2',
        u'as_status': u'Closed',
        u'as_to': u'11/2011',
        u'as_total_charge': u'84',
        u'as_total_hours': u'3.00',
        u'ciphertext': u'~~222222222',
        u'op_desc_digest': u'Test job 2.',
        u'op_description': u'Test job 2.',
        u'ui_job_profile_access': u'upwork',
        u'ui_opening_status': u'Active',
        u'version': u'1'
    },
]}}

job_profile_dict = {'profile':
    {
        u'amount': u'',
        u'as_hrs_per_week': u'0',
        u'as_job_type': u'Hourly',
        u'as_opening_access': u'private',
        u'as_opening_recno': u'111',
        u'as_opening_title': u'Review website and improve copy writing',
        u'as_provider': u'111',
        u'as_rate': u'$10.00',
        u'as_reason': u'Job was cancelled or postponed',
        u'as_reason_api_ref': u'',
        u'as_reason_recno': u'72',
        u'as_recno': u'1',
        u'as_status': u'Closed',
        u'as_to': u'11/2011',
        u'as_total_charge': u'84',
        u'as_total_hours': u'3.00',
        u'op_desc_digest': u'Test job 1.',
        u'op_description': u'Test job 1.',
        u'ciphertext': u'~~111111111',
        u'ui_job_profile_access': u'upwork',
        u'ui_opening_status': u'Active',
        u'version': u'1'
    }
}


def patched_urlopen_single_job(*args, **kwargs):
    return MicroMock(data=json.dumps(job_profile_dict), status=200)


def patched_urlopen_multiple_jobs(*args, **kwargs):
    return MicroMock(data=json.dumps(job_profiles_dict), status=200)


@patch('urllib3.PoolManager.urlopen', patched_urlopen_single_job)
def test_single_job_profile():
    job = get_client().job

    # Test full_url
    full_url = job.full_url('jobs/111')
    assert full_url == 'https://www.upwork.com/api/profiles/v1/jobs/111', \
        full_url

    # Test input parameters
    try:
        job.get_job_profile({})
        raise Exception('Request should raise ValueError exception.')
    except ValueError as e:
        assert 'Invalid job key' in str(e)
    try:
        job.get_job_profile(['~~{0}'.format(x) for x in range(21)])
        raise Exception('Request should raise ValueError exception.')
    except ValueError as e:
        assert 'Number of keys per request is limited' in str(e)
    try:
        job.get_job_profile(['~~111111', 123456])
        raise Exception('Request should raise ValueError exception.')
    except ValueError as e:
        assert 'List should contain only job keys not recno' in str(e)

    # Get single job profile test
    assert job.get_job_profile('~~111111111') == job_profile_dict['profile'], \
        job.get_job_profile('~~111111111')


@patch('urllib3.PoolManager.urlopen', patched_urlopen_multiple_jobs)
def test_multiple_job_profiles():
    job = get_client().job

    # Test full_url
    full_url = job.full_url('jobs/~~111;~~222')
    assert full_url == \
        'https://www.upwork.com/api/profiles/v1/jobs/~~111;~~222', full_url

    # Get multiple job profiles test
    assert job.get_job_profile(['~~111111111', '~~222222222']) == \
        job_profiles_dict['profiles']['profile'], \
        job.get_job_profile(['~~111111111', '~~222222222'])


#======================
# UTILS TESTS
#======================
def test_decimal_default():
    from upwork.utils import decimal_default

    value = '0.132'

    eq_('{"value": "0.132"}', json.dumps({'value': Decimal(value)},
                                         default=decimal_default))

    value = '0'

    eq_('{"value": "0"}', json.dumps({'value': Decimal(value)},
                                     default=decimal_default))

    value = '10'

    eq_('{"value": "10"}', json.dumps({'value': Decimal(value)},
                                      default=decimal_default))
