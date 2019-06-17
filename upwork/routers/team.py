# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2018 Upwork

from upwork.namespaces import Namespace
from upwork.utils import assert_parameter


class Team_V3(Namespace):

    api_url = 'team/'
    version = 3

    def get_workdays_by_company(self, company_id, from_date, till_date, offset=None):
        """
        Retrieve workdays by company

        *Parameters:*
          :company_id:  The Company ID.

          :from_date:   The target start date in `yyyymmdd` format.

          :end_date:    The target end date in `yyyymmdd` format.

          :offset:      (optional) Time zone offset.

        """
        url = 'workdays/companies/{0}/{1},{2}'.format(company_id, from_date, till_date)

        data = {}

        if offset:
            data['offset'] = offset

        result = self.get(url, data)
        if 'error' in result:
            return result

        workdays = result.get('workdays', data)
        if not isinstance(workdays, list):
            workdays = {}

        return workdays

    def get_workdays_by_contract(self, contract_id, from_date, till_date, offset=None):
        """
        Retrieve workdays by contract

        *Parameters:*
          :contract_id: The Contract ID.

          :from_date:   The target start date in `yyyymmdd` format.

          :end_date:    The target end date in `yyyymmdd` format.

          :offset:      (optional) Time zone offset.

        """
        url = 'workdays/contracts/{0}/{1},{2}'.format(contract_id, from_date, till_date)

        data = {}

        if offset:
            data['offset'] = offset

        result = self.get(url, data)
        if 'error' in result:
            return result

        workdays = result.get('workdays', data)
        if not isinstance(workdays, list):
            workdays = {}

        return workdays

    def get_workdiaries(self, team_id, date, sort_by=None, activity=None, freelancer=None, paging=None):
        """
        Retrieve a team member's workdiaries for given date or today.
        *Parameters:*
          :team_id:     The Team ID.

          :date:        A datetime object or a string in yyyymmdd format.

          :sort_by:     (optional) Sort parameter.

          :activity:    (optional) Activity.

          :freelancer:  (optional) Freelancer filter.

          :paging:      (optional) Paging.

        """
        url = 'workdiaries/companies/{0}/{1}'.format(team_id, date)
        data = {}

        if sort_by:
            data['sort_by'] = sort_by

        if activity:
            data['activity'] = activity

        if freelancer:
            data['freelancer'] = freelancer

        if paging:
            data['paging'] = paging

        result = self.get(url, data)
        if 'error' in result:
            return result

        snapshots = result.get('data', data)
        if not isinstance(snapshots, list):
            snapshots = [snapshots]
        #not sure we need to return user
        return snapshots

    def get_workdiaries_by_contract(self, contract_id, date, offset=None):
        """
        Retrieve workdiary snapshots by contract

        *Parameters:*
          :contract_id: The Contract ID.

          :date:        The target date in `yyyymmdd` format.

          :offset:      (optional) Time zone offset.

        """
        url = 'workdiaries/contracts/{0}/{1}'.format(contract_id, date)

        data = {}

        if offset:
            data['offset'] = offset

        result = self.get(url, data)
        if 'error' in result:
            return result

        snapshots = result.get('data', data).get('data', [])
        if not isinstance(snapshots, list):
            snapshots = [snapshots]
        
        return snapshots

    def get_snapshot_by_contract(self, contract_id, datetime):
        """
        Retrieve a company's user snapshots by contract ID during given time.

        *Parameters:*
          :contract_id:  The Contract ID

          :datetime:    Timestamp either a datetime object
                        or a string with UNIX timestamp (number of
                        seconds after epoch)

        """
        url = 'snapshots/contracts/{0}/{1}'.format(contract_id, datetime)

        result = self.get(url)
        if 'snapshot' in result:
            snapshot = result['snapshot']
        else:
            snapshot = []
        if 'error' in result:
            return result
        return snapshot

    def update_snapshot_by_contract(self, contract_id, datetime, memo, task, task_desc):
        """
        Update a company's user snapshot memo by contract ID at given time.

        *Parameters:*
          :contract_id:  The Contract ID

          :datetime:    Timestamp either a datetime object
                        or a string with UNIX timestamp (number of
                        seconds after epoch)

                        More than one timestamps can be specified either
                        as a range or as a list of values:

                          - list: use the semicolon character (;) e.g.
                            ``20081205T090351Z;20081405T090851Z;20081705T091853Z``

          :memo:        The Memo text

          :task:        Task ID

          :task_desc:   Task description

        """
        url = 'snapshots/contracts/{0}/{1}'.format(contract_id, datetime)

        return self.put(url, {'memo': memo, 'task': task, 'task_desc': task_desc})

    def delete_snapshot_by_contract(self, contract_id, datetime, only_webcam=None):
        """
        Delete a company's user snapshot by contract ID at given time.

        *Parameters:*
          :contract_id:  The Contract ID

          :datetime:    Timestamp either a datetime object
                        or a string with UNIX timestamp (number of
                        seconds after epoch)

                        More than one timestamps can be specified either
                        as a range or as a list of values:

                          - list: use the semicolon character (;) e.g.
                            20081205T090351Z;20081405T090851Z;20081705T091853Z

          :only_webcam: Delete only webcam image

        """
        url = 'snapshots/contracts/{0}/{1}'.format(contract_id, datetime)
        if only_webcam:
            url = '{0}/{1}'.format(url, '/webcam')
        return self.delete(url)
