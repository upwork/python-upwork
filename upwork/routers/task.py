# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

from upwork.compatibility import quote
from upwork.namespaces import Namespace


class Task(Namespace):
    api_url = 'otask/'
    version = 1

    def get_team_tasks(self, company_id, team_id,
                       paging_offset=0, paging_count=1000):
        """
        Retrieve a list of all activities in the given team.

        This call returns both archived and active activities.

        The user authenticated must have been granted the appropriate
        access to the team.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

        """
        if paging_offset or not paging_count == 1000:
            data = {'page': '{0};{1}'.format(paging_offset,
                                             paging_count)}
        else:
            data = {}

        url = 'tasks/companies/{0}/teams/{1}/tasks'.format(company_id,
                                                           team_id)
        return self.get(url, data=data)

    def get_company_tasks(self, company_id,
                          paging_offset=0, paging_count=1000):
        """
        Retrieve a list of all activities within a company.
        It is equivalent to the ``get_team_tasks`` so that
        ``team_id`` is equal to ``company_id`` which is parent
        team ID.

        This call returns both archived and active activities.

        The user authenticated must have been granted the appropriate
        access to the company.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.
        """
        team_id = company_id
        return self.get_team_tasks(
            company_id,
            team_id,
            paging_offset=paging_offset,
            paging_count=paging_count
        )

    def _encode_task_codes(self, task_codes):
        if isinstance(task_codes, (list, tuple)):
            return ';'.join(str(c) for c in task_codes)
        else:
            return str(task_codes)

    def get_team_specific_tasks(self, company_id, team_id, task_codes):
        """
        Return a specific activities within a team.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :task_codes:    Task codes (must be a list, even of 1 item)

        """
        task_codes = self._encode_task_codes(task_codes)
        url = 'tasks/companies/{0}/teams/{1}/tasks/{2}'.format(
            company_id, team_id, quote(task_codes))
        result = self.get(url)
        try:
            return result["tasks"] or []
        except KeyError:
            return result

    def get_company_specific_tasks(self, company_id, task_codes):
        """
        Return a specific activities within a company.
        This is identical to ``get_team_specific_tasks``,
        so that ``team_id`` is the same as ``company_id``.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :task_codes:    Task codes (must be a list, even of 1 item)

        """
        team_id = company_id
        return self.get_team_specific_tasks(
            company_id, team_id, task_codes)

    def post_team_task(self, company_id, team_id, code, description, url,
                       engagements=None, all_in_company=None):
        """
        Create an activity within a team.

        The authenticated user needs to have hiring manager privileges

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :code:          Task code

          :description:   Task description

          :url:           Task URL

          :engagements:   (optional) A list of engagements
                          that are to be assigned to the created activity.
                          It can be a single engagement ID,
                          or an iterable of IDs.

          :all_in_company:  (optional) If ``True``, assign the
                            created activity to all engagements
                            that are exist in the company at
                            the moment.

          If both ``engagements`` and ``all_in_company`` are provided,
          ``engagements`` list will override the ``all_in_company`` setting.

        """
        post_url = 'tasks/companies/{0}/teams/{1}/tasks'.format(
            company_id, team_id)
        data = {'code': code,
                'description': description,
                'url': url}

        if engagements:
            engagements = self._encode_task_codes(engagements)
            data['engagements'] = engagements

        if all_in_company:
            data['all_in_company'] = 1

        result = self.post(post_url, data)
        return result

    def post_company_task(self, company_id, code, description, url,
                          engagements=None, all_in_company=None):
        """
        Create an activity within a company.
        This call is identical to
        ``post_team_task`` so that ``team_id`` is equal
        to ``company_id``.

        The authenticated user needs to have hiring manager privileges.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :code:          Activity ID

          :description:   Activity description

          :url:           Activity URL

          :engagements:   (optional) A list of engagements
                          that are to be assigned to the created activity.
                          It can be a single engagement ID,
                          or an iterable of IDs.

          :all_in_company:  (optional) If ``True``, assign the
                            created activity to all engagements
                            that are exist in the company at
                            the moment.

          If both ``engagements`` and ``all_in_company`` are provided,
          ``engagements`` list will override the ``all_in_company`` setting.

        """
        team_id = company_id
        return self.post_team_task(
            company_id, team_id, code, description,
            url, engagements=engagements, all_in_company=all_in_company)

    def put_team_task(self, company_id, team_id, code, description, url,
                      engagements=None, all_in_company=None):
        """
        Update an activity within a team.

        The authenticated user needs to have hiring manager privileges.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.


          :code:          Task code

          :description:   Task description

          :url:           Task URL

          :engagements:   (optional) A list of engagements
                          that are to be assigned to the created activity.
                          It can be a single engagement ID,
                          or an iterable of IDs.

          :all_in_company:  (optional) If ``True``, assign the
                            updated activity to all engagements
                            that are exist in the company at
                            the moment.

          If both ``engagements`` and ``all_in_company`` are provided,
          ``engagements`` list will override the ``all_in_company`` setting.

        """
        put_url = 'tasks/companies/{0}/teams/{1}/tasks/{2}'.format(
            company_id, team_id, quote(str(code)))
        data = {'code': code,
                'description': description,
                'url': url}

        if engagements:
            engagements = self._encode_task_codes(engagements)
            data['engagements'] = engagements

        if all_in_company:
            data['all_in_company'] = 1

        result = self.put(put_url, data)
        return result

    def put_company_task(self, company_id, code, description, url,
                         engagements=None, all_in_company=None):
        """
        Update an activity within a company.
        This call is identical to ``put_team_task`` so that
        ``team_id`` is equal to ``company_id``.

        The authenticated user needs to have hiring manager privileges.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :code:          Task code

          :description:   Task description

          :url:           Task URL

          :engagements:   (optional) A list of engagements
                          that are to be assigned to the created activity.
                          It can be a single engagement ID,
                          or an iterable of IDs.

          :all_in_company:  (optional) If ``True``, assign the
                            created activity to all engagements
                            that are exist in the company at
                            the moment.

          If both ``engagements`` and ``all_in_company`` are provided,
          ``engagements`` list will override the ``all_in_company`` setting.

        """
        team_id = company_id
        return self.put_team_task(
            company_id, team_id, code,
            description, url, engagements=engagements,
            all_in_company=all_in_company)

    def archive_team_task(self, company_id, team_id, task_code):
        """Archive single activity within a team.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :task_code:     A single Activity ID as a string
                          or a list or tuple of IDs.

        """
        task_code = self._encode_task_codes(task_code)

        url = 'tasks/companies/{0}/teams/{1}/archive/{2}'.format(
            company_id, team_id, quote(task_code))
        return self.put(url, data={})

    def archive_company_task(self, company_id, task_code):
        """Archive single activity within a company.

        This call is identical to ``archive_team_task``, so that
        ``team_id`` is the same as ``company_id``.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :task_code:     A single Activity ID as a string
                          or a list or tuple of IDs.

        """
        team_id = company_id
        return self.archive_team_task(company_id, team_id, task_code)

    def unarchive_team_task(self, company_id, team_id, task_code):
        """Unarchive single activity within a team.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :task_code:     A single Activity ID as a string
                          or a list or tuple of IDs.

        """
        task_code = self._encode_task_codes(task_code)

        url = 'tasks/companies/{0}/teams/{1}/unarchive/{2}'.format(
            company_id, team_id, quote(task_code))
        return self.put(url, data={})

    def unarchive_company_task(self, company_id, task_code):
        """Unarchive single activity within a company.

        This call is identical to ``unarchive_team_task``, so that
        ``team_id`` is the same as ``company_id``.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :task_code:     A single Activity ID as a string
                          or a list or tuple of IDs.

        """
        team_id = company_id
        return self.unarchive_team_task(company_id, team_id, task_code)

    def assign_engagement(self, company_id, team_id,
                          engagement, task_codes=None):
        """Assign an existing engagement to the list of activities.

        Note that activity will appear in contractor's team client
        only if his engagement is assigned to the activity and
        activities are activated for the ongoing contract.

        This will override assigned engagements for the given activities.
        For example, if you pass empty ``task_codes`` or just omit
        this parameter, contractor engagement will be unassigned from
        all Activities.

        *Parameters:*
          :company_id:    Company ID. Use the ``parent_team__id`` value
                          from ``hr.get_team()`` API call.

          :team_id:       Team ID. Use the 'id' value
                          from ``hr.get_team()`` API call.

          :engagement:    Engagement ID that will be assigned/unassigned
                          to the given list of Activities.

          :task_codes:    Task codes (must be a list, even of 1 item)

        """
        task_codes = self._encode_task_codes(task_codes)
        url = 'tasks/companies/{0}/teams/{1}/engagements/{2}/tasks'.format(
            company_id, team_id, engagement)
        data = {'tasks': task_codes}
        result = self.put(url, data)
        return result

    def update_batch_tasks(self, company_id, csv_data):
        """
        Batch update Activities using csv file contents.

        This call is experimental, use it on your own risk.

        *Parameters:*
          :company_id:  Company ID. Use the ``parent_team__id`` value
                        from ``hr.get_team()`` API call.

          :csv_data: Task records in csv format but with "<br>"
                     as line separator -
                     "companyid","teamid","userid","taskid","description","url"
                     Example:
                     "acmeinc","","","T1","A Task","http://example.com"<br>
                     "acmeinc","acmeinc:dev","b42","T2","Task 2",""

        """
        data = {'data': csv_data}
        url = 'tasks/companies/{0}/tasks/batch'.format(company_id)

        return self.put(url, data)


class Task_V2(Namespace):
    api_url = 'tasks/'
    version = 2

    def _encode_task_codes(self, task_codes):
        if isinstance(task_codes, (list, tuple)):
            return ';'.join(str(c) for c in task_codes)
        else:
            return str(task_codes)

    def list_engagement_activities(self, engagement_ref):
        """
        Retrieve list of all activities assigned to the specific engagement.

        The user authenticated must have been granted the appropriate
        hiring manager permissions.

        *Parameters:*
          :engagement_ref:    Engagement reference ID. You can get it using
                              'List engagemnets' API call. Example: `1234`.

        """
        url = 'tasks/contracts/{0}'.format(engagement_ref)
        result = self.get(url)
        return result

    def assign_to_engagement(self, engagement_ref, task_codes=None):
        """Assign a list of activities to the existing engagement.

        Note that activity will appear in contractor's team client
        only if his engagement is assigned to the activity and
        activities are activated for the ongoing contract.

        This will override assigned engagements for the given activities.
        For example, if you pass empty ``task_codes`` or just omit
        this parameter, contractor engagement will be unassigned from
        all Activities.

        *Parameters:*
          :engagement_ref: Engagement ID that will be assigned/unassigned
                           to the given list of Activities.

          :task_codes:    Task codes (must be a list, even of 1 item)

        """
        task_codes = self._encode_task_codes(task_codes)
        url = 'tasks/contracts/{0}'.format(engagement_ref)
        data = {'tasks': task_codes}
        result = self.put(url, data)
        return result
