# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

from upwork.namespaces import Namespace
from upwork.utils import assert_parameter


class Team(Namespace):

    api_url = 'team/'
    version = 1

    TZ_CHOICES = ('mine', 'user', 'gmt')

    def get_snapshot(self, company_id, user_id, datetime=None):
        """
        Retrieve a company's user snapshots during given time or 'now'.

        *Parameters:*
          :company_id:  The Company ID

          :user_id:     The User ID

          :datetime:    (optional)(default: 'now')
                        Timestamp either a datetime object
                        or a string in ISO 8601 format (in UTC)
                        ``yyyymmddTHHMMSSZ``
                        or a string with UNIX timestamp (number of
                        seconds after epoch)

        """
        url = 'snapshots/{0}/{1}'.format(company_id, user_id)
        if datetime:   # date could be a list or a range also
            url = '{0}/{1}'.format(url, datetime.isoformat())

        result = self.get(url)
        if 'snapshot' in result:
            snapshot = result['snapshot']
        else:
            snapshot = []
        if 'error' in result:
            return result
        return snapshot

    def update_snapshot(self, company_id, user_id, memo, datetime=None):
        """
        Update a company's user snapshot memo at given time or 'now'.

        *Parameters:*
          :company_id:  The Company ID

          :user_id:     The User ID

          :memo:        The Memo text

          :datetime:    (optoinal)(default 'now')
                        Timestamp either a datetime object
                        or a string in ISO 8601 format (in UTC)
                        ``yyyymmddTHHMMSSZ``
                        or a string with UNIX timestamp (number of
                        seconds after epoch)

                        More than one timestamps can be specified either
                        as a range or as a list of values:

                          - range: use the comma character (,) e.g.
                            ``20081205T090351Z,20081205T091853Z``

                          - list: use the semicolon character (;) e.g.
                            ``20081205T090351Z;20081405T090851Z;20081705T091853Z``

        """
        url = 'snapshots/{0}/{1}'.format(company_id, user_id)
        if datetime:
            url = '{0}/{1}'.format(url, datetime.isoformat())
        return self.put(url, {'memo': memo})

    def delete_snapshot(self, company_id, user_id, datetime=None):
        """
        Delete a company's user snapshot memo at given time or 'now'.

        *Parameters:*
          :company_id:  The Company ID

          :user_id:     The User ID

          :datetime:    (optional)(default 'now')
                        Timestamp either a datetime object
                        or a string in ISO 8601 format (in UTC)
                        ``yyyymmddTHHMMSSZ``
                        or a string with UNIX timestamp (number of
                        seconds after epoch)

                        More than one timestamps can be specified either
                        as a range or as a list of values:

                          - range: use the comma character (,) e.g.
                            20081205T090351Z,20081205T091853Z

                          - list: use the semicolon character (;) e.g.
                            20081205T090351Z;20081405T090851Z;20081705T091853Z

        """
        url = 'snapshots/{0}/{1}'.format(company_id, user_id)
        if datetime:
            url = '{0}/{1}'.format(url, datetime.isoformat())
        return self.delete(url)

    def get_workdiaries(self, team_id, username, date=None, tz=None):
        """
        Retrieve a team member's workdiaries for given date or today.

        *Parameters:*

          :team_id:     The Team ID

          :username:    The Team Member's username

          :date:        (optional) A datetime object or a string in yyyymmdd
                        format

          :tz:          (optional) Time zone to use. Possible values:
                          * 'mine' (default)
                          * 'user'
                          * 'gmt'

        """
        url = 'workdiaries/{0}/{1}'.format(team_id, username)
        if date:
            url = '{0}/{1}'.format(url, date)
        result = self.get(url)
        if 'error' in result:
            return result

        data = {}

        if tz:
            assert_parameter('tz', tz, self.TZ_CHOICES)
            data['tz'] = tz

        snapshots = result.get('snapshots', data).get('snapshot', [])
        if not isinstance(snapshots, list):
            snapshots = [snapshots]
        #not sure we need to return user
        return result['snapshots']['user'], snapshots


class Team_V2(Namespace):

    api_url = 'team/'
    version = 2

    ONLINE_CHOICES = ('now', 'last_24h', 'all')
    DISABLED_CHOICES = ('yes', 'no')

    def get_teamrooms(self):
        """
        Retrieve all teamrooms accessible to the authenticated user.

        """
        url = 'teamrooms'

        result = self.get(url)

        if 'error' in result:
            return result

        if 'teamrooms' in result and 'teamroom' in result['teamrooms']:
            teamrooms = result['teamrooms']['teamroom']
        else:
            teamrooms = []
        if not isinstance(teamrooms, list):
            teamrooms = [teamrooms]

        return teamrooms

    def get_snapshots(self, company_or_team_id, online=None, disabled=None):
        """
        Retrieve team member snapshots.

        *Parameters:*
          :company_or_team_id: The Company ID or Team ID

          :online:             (optional) Filter user by work hours.
                               Possible values are (default):
                                 * 'now' (default)
                                 * 'last_24h'
                                 * 'all'

          :disabled:           (optional) Whether disabled users
                               need to be returned in response.
                               Possible values are (default):
                                 * 'no' (default)
                                 * 'yes'

        """
        url = 'teamrooms/{0}'.format(company_or_team_id)

        data = {}

        if online:
            assert_parameter('online', online, self.ONLINE_CHOICES)
            data['online'] = online

        if disabled:
            assert_parameter('disabled', disabled, self.ONLINE_CHOICES)
            data['disabled'] = disabled

        result = self.get(url, data)
        if 'error' in result:
            return result

        if 'teamroom' in result and 'snapshot' in result['teamroom']:
            snapshots = result['teamroom']['snapshot']
        else:
            snapshots = []
        if not isinstance(snapshots, list):
            snapshots = [snapshots]

        return snapshots

    def get_workdays_by_company(self, company_id, from_date, till_date, tz=None):
        """
        Retrieve workdays by company

        *Parameters:*
          :company_id:  The Company ID.

          :from_date:   The target start date in `yyyymmdd` format.

          :end_date:    The target end date in `yyyymmdd` format.

          :tz:          (optional) Time zone to use. Possible values:
                          * 'mine' (default)
                          * 'user'
                          * 'gmt'

        """
        url = 'workdays/companies/{0}/{1},{2}'.format(company_id, from_date, till_date)

        data = {}

        if tz:
            assert_parameter('tz', tz, self.TZ_CHOICES)
            data['tz'] = tz

        result = self.get(url, data)
        if 'error' in result:
            return result

        workdays = result.get('workdays', data)
        if not isinstance(workdays, list):
            workdays = {}

        return workdays

    def get_workdays_by_contract(self, contract_id, from_date, till_date, tz=None):
        """
        Retrieve workdays by contract

        *Parameters:*
          :contract_id: The Contract ID.

          :from_date:   The target start date in `yyyymmdd` format.

          :end_date:    The target end date in `yyyymmdd` format.

          :tz:          (optional) Time zone to use. Possible values:
                          * 'mine' (default)
                          * 'user'
                          * 'gmt'

        """
        url = 'workdays/contracts/{0}/{1},{2}'.format(contract_id, from_date, till_date)

        data = {}

        if tz:
            assert_parameter('tz', tz, self.TZ_CHOICES)
            data['tz'] = tz

        result = self.get(url, data)
        if 'error' in result:
            return result

        workdays = result.get('workdays', data)
        if not isinstance(workdays, list):
            workdays = {}

        return workdays

    def get_workdiaries_by_contract(self, contract_id, date, tz=None):
        """
        Retrieve workdiary snapshots by contract

        *Parameters:*
          :contract_id: The Contract ID.

          :date:        The target date in `yyyymmdd` format.

          :tz:          (optional) Time zone to use. Possible values:
                          * 'mine' (default)
                          * 'user'
                          * 'gmt'

        """
        url = 'workdiaries/contracts/{0}/{1}'.format(contract_id, date)

        data = {}

        if tz:
            assert_parameter('tz', tz, self.TZ_CHOICES)
            data['tz'] = tz

        result = self.get(url, data)
        if 'error' in result:
            return result

        snapshots = result.get('snapshots', data).get('snapshot', [])
        if not isinstance(snapshots, list):
            snapshots = [snapshots]
        
        return result['snapshots']['user'], snapshots

    def get_snapshot_by_contract(self, contract_id, datetime=None):
        """
        Retrieve a company's user snapshots by contract ID during given time or 'now'.

        *Parameters:*
          :contract_id:  The Contract ID

          :datetime:    (optional)(default: 'now')
                        Timestamp either a datetime object
                        or a string in ISO 8601 format (in UTC)
                        ``yyyymmddTHHMMSSZ``
                        or a string with UNIX timestamp (number of
                        seconds after epoch)

        """
        url = 'snapshots/contracts/{0}'.format(contract_id)
        if datetime:   # date could be a list or a range also
            url = '{0}/{1}'.format(url, datetime.isoformat())

        result = self.get(url)
        if 'snapshot' in result:
            snapshot = result['snapshot']
        else:
            snapshot = []
        if 'error' in result:
            return result
        return snapshot

    def update_snapshot_by_contract(self, contract_id, memo, datetime=None):
        """
        Update a company's user snapshot memo by contract ID at given time or 'now'.

        *Parameters:*
          :contract_id:  The Contract ID

          :memo:        The Memo text

          :datetime:    (optoinal)(default 'now')
                        Timestamp either a datetime object
                        or a string in ISO 8601 format (in UTC)
                        ``yyyymmddTHHMMSSZ``
                        or a string with UNIX timestamp (number of
                        seconds after epoch)

                        More than one timestamps can be specified either
                        as a range or as a list of values:

                          - range: use the comma character (,) e.g.
                            ``20081205T090351Z,20081205T091853Z``

                          - list: use the semicolon character (;) e.g.
                            ``20081205T090351Z;20081405T090851Z;20081705T091853Z``

        """
        url = 'snapshots/contracts/{0}'.format(contract_id)
        if datetime:
            url = '{0}/{1}'.format(url, datetime.isoformat())
        return self.put(url, {'memo': memo})

    def delete_snapshot_by_contract(self, contract_id, datetime=None):
        """
        Delete a company's user snapshot by contract ID at given time or 'now'.

        *Parameters:*
          :contract_id:  The Contract ID

          :datetime:    (optional)(default 'now')
                        Timestamp either a datetime object
                        or a string in ISO 8601 format (in UTC)
                        ``yyyymmddTHHMMSSZ``
                        or a string with UNIX timestamp (number of
                        seconds after epoch)

                        More than one timestamps can be specified either
                        as a range or as a list of values:

                          - range: use the comma character (,) e.g.
                            20081205T090351Z,20081205T091853Z

                          - list: use the semicolon character (;) e.g.
                            20081205T090351Z;20081405T090851Z;20081705T091853Z

        """
        url = 'snapshots/contracts/{0}'.format(contract_id)
        if datetime:
            url = '{0}/{1}'.format(url, datetime.isoformat())
        return self.delete(url)
