# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

from upwork.namespaces import Namespace
from upwork.utils import assert_parameter, ApiValueError


class HR_V1(Namespace):
    """
    HR API version 1
    """
    api_url = 'hr/'
    version = 1

    def invite_to_interview(self, job_id, cover, profile_key=None,
                            provider_reference=None):
        """
        Invite to an interview.

        *Parameters:*
          :job_id:               Job reference ID

          :cover:                Text of the cover letter

          :profile_key:          (optional) Unique contractor's key,
                                 e.g. ~~677961dcd7f65c01

          :provider_reference:   (optional) Developer's unique reference ID,
                                 e.g. 12345. Use it if no profile_key available

        Either one of the parameters ``profile_key`` or ``provider_reference``
        should be provided, otherwise error will be raised.

        """
        data = {}

        if profile_key is None and provider_reference is None:
            raise ApiValueError('Either one of the parameters ``profile_key`` '
                                'or ``provider_reference`` should be provided')

        if profile_key:
            data['profile_key'] = profile_key

        if provider_reference:
            data['provider__reference'] = provider_reference

        data['cover'] = cover

        url = 'jobs/{0}/candidates'.format(job_id)
        return self.post(url, data)


class HR(Namespace):
    """
    HR API version 2
    """
    api_url = 'hr/'
    version = 2

    JOB_TYPES = ('hourly', 'fixed-price')
    JOB_VISIBILITY_OPTIONS = ('public', 'private', 'upwork', 'invite-only')
    JOB_STATUSES = ('open', 'filled', 'cancelled')
    JOB_KEEP_OPEN_OPTIONS = ('yes', 'no')
    CONTRACT_REASON_OPTIONS = (
        'API_REAS_MISREPRESENTED_SKILLS',
        'API_REAS_CONTRACTOR_NOT_RESPONSIVE',
        'API_REAS_HIRED_DIFFERENT',
        'API_REAS_JOB_COMPLETED_SUCCESSFULLY',
        'API_REAS_WORK_NOT_NEEDED',
        'API_REAS_UNPROFESSIONAL_CONDUCT',
    )
    CONTRACT_WOULD_HIRE_AGAIN_OPTONS = ('yes', 'no')

    """userrole api"""

    def get_user_roles(self):
        """
        Retrieve UserRoles object.

        This is a **very important and useful API call**,
        it returns a complete list of privileges the currently
        authorized user has within all the teams and companies
        they have access to.

        """
        url = 'userroles'
        result = self.get(url)
        return result.get('userroles', result)

    """user api"""

    def get_user(self, user_reference):
        """
        Retrieve the user object from the user reference.

        *Parameters:*
          :user_reference:    The user reference

        """
        url = 'users/{0}'.format(user_reference)
        result = self.get(url)
        return result.get('user', result)

    def get_user_me(self):
        """
        Retrieve currently authenticated user object.

        """
        url = 'users/me'
        result = self.get(url)
        return result.get('user', result)

    """company api"""

    def get_companies(self):
        """
        Retrieve the list of companies to which the current authorized user \
        has access.

        """
        url = 'companies'
        result = self.get(url)
        return result['companies']

    def get_company(self, company_referece):
        """
        Retrieve the company object from the company reference.

        *Parameters:*
          :company_reference:     The company reference (can be found using
                                  get_companies method)

        """
        url = 'companies/{0}'.format(company_referece)
        result = self.get(url)
        return result.get('company', result)

    def get_company_teams(self, company_referece):
        """
        Retrieve a list of teams within the company being referenced.

        User has to have access to the referenced company.

        *Parameters:*
          :company_reference:     The company reference (can be found using
                                  get_companies method)

        """
        url = 'companies/{0}/teams'.format(company_referece)
        result = self.get(url)
        return result.get('teams', result)

    def get_company_users(self, company_referece, active=True):
        """
        Retrieve a list of all users within the referenced company.

        Only available for users with hiring privileges for the company.

        *Parameters:*
          :company_reference:     The company reference (can be found using
                                  get_companies method)

          :active:                ``True``/``False`` (default ``True``)

        """
        url = 'companies/{0}/users'.format(company_referece)
        if active:
            data = {'status_in_company': 'active'}
        else:
            data = {'status_in_company': 'inactive'}
        result = self.get(url, data)
        return result.get('users', result)

    """team api"""

    def post_team_adjustment(self, team_reference, engagement_reference,
                             comments, charge_amount, notes=None):
        """
        Add bonus to an engagement.

        *Parameters:*
          :team_reference:        The Team reference ID

          :engagement_reference:  The Engagement reference ID

          :comments:              Comments about this adjustment, e.g.
                                 "Bonus for a good job"

          :charge_amount:         The amount that will be charged to the employer, e.g. 110

          :notes:                 (optional) Notes

        .. note:: You should use either ``amount`` parameter or \
        ``charge_amount``, but not both. Make sure that at least \
        one of them is present.

        """
        url = 'teams/{0}/adjustments'.format(team_reference)
        data = {}

        data['engagement__reference'] = engagement_reference
        data['comments'] = comments
        
        if charge_amount is None or charge_amount == 0:
            raise ApiValueError('Missed obligatory parameter ``charge_amount``')

        data['charge_amount'] = charge_amount

        if notes:
            data['notes'] = notes

        result = self.post(url, data)
        return result.get('adjustment', result)

    def get_teams(self):
        """
        Retrieve a list of all the teams that a user has access to.

        This will return teams across all companies the current
        user has access to.

        """
        url = 'teams'
        result = self.get(url)
        return result.get('teams', result)

    def get_team(self, team_reference, include_users=False):
        """
        Retrieve the team information.

        *Parameters:*
          :team_reference:    The team reference

          :include_users:     Whether to include details of users
                              (default: False)

        """
        url = 'teams/{0}'.format(team_reference)
        result = self.get(url, {'include_users': include_users})
        #TODO: check how included users returned
        return result.get('team', result)

    def get_team_users(self, team_reference, active=True):
        """
        Retrieve users of the team.

        *Parameters:*
          :team_reference:    The team reference

          :active:     Status of the users, If ``True`` - return
                       active users, if ``False`` - return inactive users.
                       Default value is ``True``.

        """
        url = 'teams/{0}/users'.format(team_reference)
        if active:
            data = {'status_in_team': 'active'}
        else:
            data = {'status_in_team': 'inactive'}
        result = self.get(url, data)
        return result.get('users', result)

    """job api"""

    def get_jobs(self, buyer_team_reference,
                 include_sub_teams=False,
                 status=None, created_by=None, created_time_from=None,
                 created_time_to=None, page_offset=0, page_size=20,
                 order_by=None):
        """
        Retrieves all jobs that a user has manage_recruiting access to.
        This API call can be used to find the reference ID of a specific job.

        *Parameters:*
          :buyer_team_reference:  The buyer's team reference ID

          :include_sub_teams:     (optional) <1|0> Whether to include sub-teams

          :status:                (optional) Status of a job

          :created_by:            (optional) Creator's user_id

          :created_time_from:     (optional) timestamp, \
                                  e.g. 2009-01-20T00:00:01

          :created_time_to:       (optional) timestamp, \
                                  e.g. 2009-02-20T11:59:59

          :page_offset:           (optional) Number of entries to skip

          :page_size:             (optional: default 20) Page size in number
                                  of entries

          :order_by:              (optional)

        """
        url = 'jobs'

        data = {}
        data['buyer_team__reference'] = buyer_team_reference

        data['include_sub_teams'] = False
        if include_sub_teams:
            data['include_sub_teams'] = include_sub_teams

        if status:
            data['status'] = status

        if created_by:
            data['created_by'] = created_by

        if created_time_from:
            data['created_time_from'] = created_time_from

        if created_time_to:
            data['created_time_to'] = created_time_to

        data['page'] = '{0};{1}'.format(page_offset, page_size)

        if order_by is not None:
            data['order_by'] = order_by

        result = self.get(url, data)
        return result.get('jobs', result)

    def get_job(self, job_reference):
        """
        Retrieve the complete job object for the referenced job.
        This is only available to users with manage_recruiting
        permissions within the team that the job is posted in.

        *Parameters:*
          :job_reference:     Job reference

        """
        url = 'jobs/{0}'.format(job_reference)
        result = self.get(url)
        return result.get('job', result)

    def post_job(self, buyer_team_reference, title, job_type, description,
                 visibility, budget=None, duration=None, start_date=None,
                 skills=None, category2=None, subcategory2=None):
        """
        Post a job.

        *Parameters:*
          :buyer_team_reference:   Reference ID of the buyer team that is
                                   posting the job, e.g. 34567

          :title:                  Title of the Job

          :job_type:               Type of posted job, e.g. "hourly"
                                   Possible values are:
                                     * 'hourly'
                                     * 'fixed-price'

          :description:            The job's description

          :visibility:             The job's visibility, e.g. 'private'.
                                   Possible values are:
                                     - 'public' jobs are available to all
                                       users who search jobs
                                     - 'private' job is visible to
                                       employer only
                                     - 'upwork' jobs appear in search
                                       results only for Upwork users
                                       who are logged into the service
                                     - 'invite-only' jobs do not appear
                                       in search and are used for jobs
                                       where the buyer wants to control
                                       the potential applicants

          :budget:                 (conditionally optional) The budget of the
                                   Job, e.g. 100. Is used for 'fixed-price'
                                   jobs only.

          :duration:               (conditionally optional) The duration of the
                                   job in hours, e.g. 90. Used for
                                   'hourly-jobs' only.

          :start_date:             (optional) The start date of the Job,
                                   e.g. 06-15-2011. If start_date is not
                                   included the job will default to
                                   starting immediately.

          :skills:                 (optional) Skills required for the job.
                                   Must be a list or tuple even of one item,
                                   e.g. ``['python']``

          :category2:              (conditionally optional) The category (V2) of job, e.g.
                                   'Development'
                                   (where to get? - see Metadata API, List Categories (V2))


          :subcategory2:           (conditionally optional) The subcategory (V2) of job, e.g.
                                   'Web & Mobile Programming'
                                   (where to get? - see Metadata API, List Categories (V2))

        """
        url = 'jobs'
        data = {}

        data['buyer_team__reference'] = buyer_team_reference
        data['title'] = title

        assert_parameter('job_type', job_type, self.JOB_TYPES)
        data['job_type'] = job_type

        data['description'] = description

        assert_parameter('visibility', visibility, self.JOB_VISIBILITY_OPTIONS)
        data['visibility'] = visibility

        if category2 is None or subcategory2 is None:
            raise ApiValueError('sub/category2 parameters must be specified')

        if category2:
            data['category2'] = category2

        if subcategory2:
            data['subcategory2'] = subcategory2

        if budget is None and duration is None:
            raise ApiValueError('Either one of the ``budget``or ``duration`` '
                                'parameters must be specified')

        if budget:
            data['budget'] = budget
        if duration:
            data['duration'] = duration
        if start_date:
            data['start_date'] = start_date
        if skills:
            data['skills'] = ';'.join(skills)

        result = self.post(url, data)
        return result

    def update_job(self, job_id, buyer_team_reference, title, description,
                   visibility, budget=None, duration=None, start_date=None,
                   status=None, category2=None, subcategory2=None):
        """
        Update a job.

        *Parameters:*
          :job_id:                 Job reference ID

          :buyer_team_reference:   Reference ID of the buyer team that is
                                   posting the job, e.g. 34567

          :title:                  Title of the Job

          :description:            The job's description

          :visibility:             The job's visibility, e.g. 'private'.
                                   Possible values are:
                                     - 'public' jobs are available to all
                                       users who search jobs
                                     - 'private' job is visible to
                                       employer only
                                     - 'upwork' jobs appear in search
                                       results only for Upwork users
                                       who are logged into the service
                                     - 'invite-only' jobs do not appear
                                       in search and are used for jobs
                                       where the buyer wants to control
                                       the potential applicants

          :budget:                 (conditionally optional) The budget of the
                                   Job, e.g. 100. Is used for 'fixed-price'
                                   jobs only.

          :duration:               (conditionally optional) The duration of the
                                   job in hours, e.g. 90. Used for
                                   'hourly-jobs' only.

          :start_date:             (optional) The start date of the Job,
                                   e.g. 06-15-2011. If start_date is not
                                   included the job will default to
                                   starting immediately.

          :status:                 (required) The status of the job,
                                   e.g. 'filled'.
                                   Possible values are:
                                   - 'open'
                                   - 'filled'
                                   - 'cancelled'

          :category2:              (conditionally optional) The category (V2) of job, e.g.
                                   'Development'
                                   (where to get? - see Metadata API, List Categories (V2))


          :subcategory2:           (conditionally optional) The subcategory (V2) of job, e.g.
                                   'Web & Mobile Programming'
                                   (where to get? - see Metadata API, List Categories (V2))

        """
        url = 'jobs/{0}'.format(job_id)
        data = {}

        data['buyer_team__reference'] = buyer_team_reference
        data['title'] = title
        data['description'] = description

        assert_parameter('visibility', visibility, self.JOB_VISIBILITY_OPTIONS)
        data['visibility'] = visibility

        data['category2'] = category2
        data['subcategory2'] = subcategory2

        if budget is None and duration is None:
            raise ApiValueError('Either one of the ``budget``or ``duration`` '
                                'parameters must be specified')

        if budget:
            data['budget'] = budget
        if duration:
            data['duration'] = duration
        if start_date:
            data['start_date'] = start_date

        if status:
            assert_parameter('status', status, self.JOB_STATUSES)
            data['status'] = status
        else:
            raise ApiValueError('Missing required parameter "status"')

        return self.put(url, data)

    def delete_job(self, job_id, reason_code):
        """
        Delete a job.

        *Parameters:*
          :job_id:        Job reference ID

          :reason_code:   The reason code to cancel the job, e.g. ``41``.
                          Possible values are:
                            * ``67`` - Accidental opening creation
                            * ``51`` - All positions filled
                            * ``49`` - Filled by alternate source
                            * ``41`` - Project was cancelled
                            * ``34`` - No developer for requested skills

        """
        url = 'jobs/{0}'.format(job_id)
        return self.delete(url, {'reason_code': reason_code})

    """offer api"""

    def get_offers(self, buyer_team_reference, include_sub_teams=None,
                   provider_ref=None, profile_key=None, job_ref=None,
                   agency_ref=None, status=None,
                   created_time_from=None, created_time_to=None,
                   page_offset=0, page_size=20, order_by=None):
        """
        Retrieve a list of all the offers on a specific job or within \
        a specific team.

        *Parameters:*
          :buyer_team_reference:  The buyer's team reference ID

          :include_sub_teams:     (optional) <1|0> Whether to include sub teams

          :provider_ref:          (optional) The provider's reference ID

          :profile_key:           (optional) Unique profile key, used if
                                ``provider_reference`` is absent

          :job_ref:               (optional) The Job's reference ID

          :agency_ref:            (optional) The Agency's reference ID

          :status:                (optional) Engagement status,
                                  e.g., status=active;closed

          :created_time_from:     (optional) timestamp \
                                  e.g.'2008-09-09 00:00:01'

          :created_time_to:       (optional) timestamp \
                                  e.g.'2008-09-09 00:00:01'

          :page_offset:           (optional) Number of entries to skip

          :page_size:             (optional: default 20) Page size in number
                                  of entries

          :order_by:              (optional) Sorting

        """
        url = 'offers'
        data = {}
        data['buyer_team__reference'] = buyer_team_reference

        if include_sub_teams:
            data['include_sub_teams'] = include_sub_teams

        if provider_ref:
            data['provider__reference'] = provider_ref

        if profile_key:
            data['profile_key'] = profile_key

        if job_ref:
            data['job__reference'] = job_ref

        if agency_ref:
            data['agency_team__reference'] = agency_ref

        if status:
            data['status'] = status

        if created_time_from:
            data['created_time_from'] = created_time_from

        if created_time_to:
            data['created_time_to'] = created_time_to

        data['page'] = '{0};{1}'.format(page_offset, page_size)

        if order_by is not None:
            data['order_by'] = order_by

        result = self.get(url, data)
        return result.get('offers', result)

    def get_offer(self, offer_reference):
        """
        Retrieve the referenced offer.

        *Parameters:*
          :offer_reference:   Offer reference ID

        """
        url = 'offers/{0}'.format(offer_reference)
        result = self.get(url)
        return result.get('offer', result)

    def post_offer(self, job_reference, provider_team_reference=None,
                   provider_reference=None, profile_key=None,
                   message_from_buyer=None, engagement_title=None,
                   attached_doc=None, fixed_charge_amount_agreed=None,
                   fixed_pay_amount_agreed=None,
                   fixed_price_upfront_payment=None, hourly_pay_rate=None,
                   weekly_salary_charge_amount=None,
                   weekly_salary_pay_amount=None, weekly_stipend_hours=None,
                   weekly_hours_limit=None, start_date=None, keep_open=None):
        """Make an offer to the provider.

        *Parameters:*
          :job_reference:                  The Job's reference ID

          :provider_team_reference:        (optional) The reference ID
                                           of the provider team. If specified,
                                           the check is performed whether user
                                           you're making offer to belongs
                                           to the team

          :provider_reference:             (conditionally optional)
                                           The provider's reference. Has
                                           the override priority over
                                           ``profile_key`` if both specified.

          :profile_key:                    (conditionally optional)
                                           Unique profile key,
                                           used if ``provider_reference``
                                           is absent

          :message_from_buyer:             (optional) Text message

          :engagement_title:               (optional) The engagement title

          :attached_doc:                   (optional) Attachment

          :fixed_charge_amount_agreed:     (optional) The amount of agreed
                                           charge, required by fixed-price job

          :fixed_pay_amount_agreed:        (optional) The amount of agreed pay

          :fixed_price_upfront_payment:    (optional) The amount of upfront
                                           payment

          :hourly_pay_rate:                (optional) Hourly pay rate

          :weekly_salary_charge_amount:    (optional) Salary charge amount
                                           per week

          :weekly_salary_pay_amount:       (optional) Salary pay amount per
                                           week, required by fixed-price job

          :weekly_stipend_hours:           (optional) Stipend hours per week

          :weekly_hours_limit:             (optional) Limit of hours per week

          :start_date:                     (optional) The offer start date

          :keep_open:                      (optional, default: 'no')
                                           Leave the job opened.
                                           Possible values are: 'yes', 'no'

        When just job and provider reference params are provided in the request
        then an invitation for an interview should be send to the according
        provider. Provider can either choose to accept the invitation and start
        the communication with the user or decline it, in which case
        communication between client and provider stops.

        When additionally engagement title and charge amount params are
        provided in the request, then an actual offer is created for the
        provider. In this case the provider can either accept the offer
        and start working or decline the offer.

        """
        url = 'offers'

        data = {}
        data['job__reference'] = job_reference

        if provider_team_reference:
            data['provider_team__reference'] = provider_team_reference

        if profile_key is None and provider_reference is None:
            raise ApiValueError('Either one of the parameters ``profile_key`` '
                                'or ``provider_reference`` should be provided')

        if provider_reference:
            data['provider__reference'] = provider_reference
        if profile_key:
            data['profile_key'] = profile_key

        if message_from_buyer:
            data['message_from_buyer'] = message_from_buyer

        if engagement_title:
            data['engagement_title'] = engagement_title

        if attached_doc:
            data['attached_doc'] = attached_doc

        if fixed_charge_amount_agreed:
            data['fixed_charge_amount_agreed'] = fixed_charge_amount_agreed

        if fixed_pay_amount_agreed:
            data['fixed_pay_amount_agreed'] = fixed_pay_amount_agreed

        if fixed_price_upfront_payment:
            data['fixed_price_upfront_payment'] = fixed_price_upfront_payment

        if hourly_pay_rate:
            data['hourly_pay_rate'] = hourly_pay_rate

        if weekly_salary_charge_amount:
            data['weekly_salary_charge_amount'] = weekly_salary_charge_amount

        if weekly_salary_pay_amount:
            data['weekly_salary_pay_amount'] = weekly_salary_pay_amount

        if weekly_stipend_hours:
            data['weekly_stipend_hours'] = weekly_stipend_hours

        if weekly_hours_limit:
            data['weekly_hours_limit'] = weekly_hours_limit

        if start_date:
            data['start_date'] = start_date

        if keep_open:
            assert_parameter('keep_open', keep_open,
                             self.JOB_KEEP_OPEN_OPTIONS)
            data['keep_open'] = keep_open

        return self.post(url, data)

    """engagement api"""

    def get_engagements(self, buyer_team_reference=None,
                        include_sub_teams=None, provider_reference=None,
                        profile_key=None, job_reference=None,
                        agency_team_reference=None, status=None,
                        created_time_from=None, created_time_to=None,
                        page_offset=0, page_size=20, order_by=None):
        """
        Retrieve engagements.

        *Parameters:*
          :buyer_team_reference:  (optional) The team reference ID

          :include_sub_teams:     (optional) <0|1> - whether to include info
                                  about sub-teams

          :provider_reference:    (optional)
                                  The provider's reference ID.
                                  Has the override priority over the
                                  ``profile_key`` if both specified.

          :profile_key:           (optional) Unique profile key,
                                  used if ``provider_reference`` is absent

          :job_reference:         (optional) The Job's reference ID

          :agency_team_reference: (optional) The Agency's reference ID

          :status:                (optional) Engagement status, e.g.
                                  ``status=active;closed``

          :created_time_from:     (optional) timestamp \
                                  e.g.'2008-09-09 00:00:01'

          :created_time_to:       (optional) timestamp \
                                  e.g.'2008-09-09 00:00:01'

          :page_offset:           (optional) Number of entries to skip

          :page_size:             (optional: default 20) Page size
                                  in number of entries

          :order_by:           (optional) Sorting, in format
                               $field_name1;$field_name2;..$field_nameN;AD...A,
                               where A means "Ascending", D means "Descending",
                               available fields are:
                                    * 'reference',
                                    * 'created_time',
                                    * 'offer__reference',
                                    * 'job__reference',
                                    * 'buyer_team__reference',
                                    * 'provider__reference',
                                    * 'status',
                                    * 'engagement_start_date',
                                    * 'engagement_end_date'
        """
        url = 'engagements'

        data = {}
        if buyer_team_reference:
            data['buyer_team__reference'] = buyer_team_reference

        if include_sub_teams:
            data['include_sub_teams'] = include_sub_teams

        if profile_key:
            data['profile_key'] = profile_key

        if provider_reference:
            data['provider_reference'] = provider_reference

        if provider_reference:
            data['provider__reference'] = provider_reference
        if profile_key:
            data['profile_key'] = profile_key

        if job_reference:
            data['job__reference'] = job_reference

        if agency_team_reference:
            data['agency_team_reference'] = agency_team_reference

        if status:
            data['status'] = status

        if created_time_from:
            data['created_time_from'] = created_time_from

        if created_time_to:
            data['created_time_to'] = created_time_to

        data['page'] = '{0};{1}'.format(page_offset, page_size)

        if order_by is not None:
            data['order_by'] = order_by

        result = self.get(url, data)
        return result.get('engagements', result)

    def get_engagement(self, engagement_reference):
        """
        Retrieve referenced engagement object.

        *Parameters:*
          :engagement_reference:    Engagement reference ID

        """
        url = 'engagements/{0}'.format(engagement_reference)
        result = self.get(url)
        return result.get('engagement', result)

    """contracts api"""

    def suspend_contract(self, contract_reference, message):
        """
        Suspend the Contract.

        *Parameters:*
          :contract_reference:  The Contract's reference ID

          :message:             A message/reason for contractor

        """
        url = 'contracts/{0}/suspend'.format(contract_reference)
        data = {}

        data['message'] = message

        return self.put(url, data)

    def restart_contract(self, contract_reference, message):
        """
        Restart the Contract.

        *Parameters:*
          :contract_reference:  The Contract's reference ID

          :message:             A message/reason for contractor

        """
        url = 'contracts/{0}/restart'.format(contract_reference)
        data = {}

        data['message'] = message

        return self.put(url, data)

    def end_contract(self, contract_reference, reason, would_hire_again,
                     fb_scores=None, fb_comment=None):
        """
        Close the referenced contract.

        *Parameters:*
          :contract_reference:  The Contract's reference ID

          :reason:              The reason key, e.g.
                                'API_REAS_HIRED_DIFFERENT'.
                                Possible values are:
                                 - 'API_REAS_MISREPRESENTED_SKILLS' -
                                    "Contractor misrepresented his/her skills"
                                 - 'API_REAS_CONTRACTOR_NOT_RESPONSIVE' -
                                    "Contractor not responsive"
                                 - 'API_REAS_HIRED_DIFFERENT' -
                                    "Hired a different contractor"
                                 - 'API_REAS_JOB_COMPLETED_SUCCESSFULLY' -
                                    "Job was completed successfully"
                                 - 'API_REAS_WORK_NOT_NEEDED' -
                                    "No longer need this work completed"
                                 - 'API_REAS_UNPROFESSIONAL_CONDUCT' -
                                    "Unprofessional conduct"

          :would_hire_again:     Whether you would hire a contractor again.
                                 Required if total charge on the contract
                                 is $0.
                                 Possible values are: ['yes', 'no']

          :fb_scores:            (optional) Estimate, a dictionary of
                                 scores, where id is reference to
                                 score description (see example below).
                                 The feedback scores are optional, but if
                                 present they must be complete: all scores.
                                 Below are the possible score reference id
                                 values.

                                 Feedback on contractor:

                                     * ``3`` - "Skills / competency and skills
                                         for the job, understanding of
                                         specifications/instructions"
                                     * ``4`` - "Quality / quality of work
                                         deliveries"
                                     * ``5`` - "Availability / online presence
                                                on a consistent schedule"
                                     * ``6`` - "Deadlines / ability to complete
                                                tasks on time"
                                     * ``7`` - "Communication / communication
                                                skills, frequent
                                                progress updates,
                                                responsiveness"
                                     * ``8`` - "Cooperation / cooperation and
                                         flexibility, suggestions for
                                         improvement"

                                 Feedback on employer:
                                    * ``9`` - "Skills / competency and skills
                                         for the job, understanding of task
                                         complexities"
                                    * ``10`` - "Quality / quality of
                                         specifications/instructions"
                                    * ``11`` - "Availability / online presence
                                         on a consistent schedule"
                                    * ``12`` - "Deadlines / understanding of
                                         complexities and trade-offs"
                                    * ``13`` - "Communication / communication
                                         skills and responsiveness, feedback
                                         and guidance"
                                    * ``14`` - "Cooperation / cooperation and
                                         flexibility, open to suggestions
                                         for improvement"
                                  Example:
                                  {'fb_scores[3]': 5, 'fb_scores[4]': 4, ... ,
                                   'fb_scores[8]': 5}

          :fb_comment:           (optional) Feedback comment, some string
                                 message. It is optional but if present, then
                                 the ``fb_scores`` parameter is also required.

        """
        url = 'contracts/{0}'.format(contract_reference)
        data = {}

        assert_parameter('reason', reason, self.CONTRACT_REASON_OPTIONS)
        data['reason'] = reason

        assert_parameter('would_hire_again', would_hire_again,
                         self.CONTRACT_WOULD_HIRE_AGAIN_OPTONS)
        data['would_hire_again'] = would_hire_again

        if fb_scores:
            for key, value in fb_scores.items():
                data[key] = value

        if fb_comment:
            data['fb_comment'] = fb_comment

        result = self.delete(url, data)
        return result


class HR_V3(Namespace):
    """
    HR API version 3.
    """
    api_url = 'hr/'
    version = 3

    def create_milestone(self, contract_reference, milestone_description, deposit_amount, due_date=None):
        """
        Create a milestone.

        *Parameters:*
          :contract_reference:      Contract reference. Contracts info are available in the Engagements API.
          :milestone_description:   Name of the milestone.
          :deposit_amount:          Amount to deposit for this milestone.
          :due_date:                (optional) Expected date of finalization. Format mm-dd-yyyy.

        """
        data = {}
        data['contract_reference'] = contract_reference
        data['milestone_description'] = milestone_description
        data['deposit_amount'] = deposit_amount

        if due_date:
            data['due_date'] = due_date

        url = 'fp/milestones'
        return self.post(url, data)

    def edit_milestone(self, milestone_id, milestone_description=None, deposit_amount=None, due_date=None, message=None):
        """
        Edit an existing milestone.

        *Parameters:*
          :milestone_id:            Milestone reference.
          :milestone_description:   (optional) Name of the milestone.
          :deposit_amount:          (optional) Amount to deposit for this milestone.
          :due_date:                (optional) Expected date of finalization. Format mm-dd-yyyy.
          :message:                 (optional) Message from the client to the freelancer.

        """
        data = {}
        data['milestone_id'] = milestone_id

        if milestone_description:
            data['milestone_description'] = milestone_description

        if deposit_amount:
            data['deposit_amount'] = deposit_amount

        if due_date:
            data['due_date'] = due_date

        if message:
            data['message'] = message

        url = 'fp/milestones/{0}'.format(milestone_id)
        return self.put(url, data)

    def activate_milestone(self, milestone_id, message=None):
        """
        Activates a milestone that has not been funded.

        *Parameters:*
          :milestone_id:            Milestone reference.
          :message:                 (optional) Message from the client to the freelancer.

        """
        data = {}
        data['milestone_id'] = milestone_id

        if message:
            data['message'] = message

        url = 'fp/milestones/{0}/activate'.format(milestone_id)
        return self.put(url, data)

    def approve_milestone(self, milestone_id, amount=None, bonus=None, pay_comments=None, underpayment_reason=None, note2contractor=None):
        """
        Approve the milestone.

        *Parameters:*
          :milestone_id:            Milestone reference.
          :amount:                  (optional) Amount of money to be paid. If none provided, the full deposit_amount is paid.
          :bonus:                   (optional) Amount of money paid as bonus.
          :pay_comments:            (optional) Comments on the payment.
          :underpayment_reason:     (optional) Reason for a smaller payment than the one agreed.
                                    Valid values: `329`, `330`, `331`, `332`
          :note2contractor:         (optional) Notes from the client to the freelancer.

        """
        data = {}
        data['milestone_id'] = milestone_id

        if amount:
            data['amount'] = amount

        if bonus:
            data['bonus'] = bonus

        if pay_comments:
            data['pay_comments'] = pay_comments

        if underpayment_reason:
            data['underpayment_reason'] = underpayment_reason

        if note2contractor:
            data['note2contractor'] = note2contractor

        url = 'fp/milestones/{0}/approve'.format(milestone_id)
        return self.put(url, data)

    def delete_milestone(self, milestone_id):
        """
        Delete the milestone.

        *Parameters:*
          :milestone_id:            Milestone reference.

        """
        data = {}

        url = 'fp/milestones/{0}'.format(milestone_id)
        return self.delete(url, data)

    def request_submission_approval(self, milestone_id, note2client, amount):
        """
        Freelancer submits work for the client to approve.

        *Parameters:*
          :milestone_id:    Milestone reference.
          :note2client:     Notes from freelancer to client about work that was done.
          :amount:          Amount requested by the freelancer.

        """
        data = {}
        data['milestone_id'] = milestone_id
        data['note2client'] = note2client
        data['amount'] = amount

        url = 'fp/submissions'
        return self.post(url, data)

    def approve_submission(self, submission_id, amount, bonus=None, pay_comments=None, underpayment_reason=None, note2contractor=None):
        """
        Approve the submission.

        *Parameters:*
          :submission_id:           Submission reference.
          :amount:                  Amount of money to be paid. If none provided, the full deposit_amount is paid.
          :bonus:                   (optional) Amount of money paid as bonus.
          :pay_comments:            (optional) Comments on the payment.
          :underpayment_reason:     (optional) Reason for a smaller payment than the one agreed.
                                    Valid values: `329`, `330`, `331`, `332`
          :note2contractor:         (optional) Notes from the client to the freelancer.

        """
        data = {}
        data['submission_id'] = submission_id
        data['amount'] = amount

        if bonus:
            data['bonus'] = bonus

        if pay_comments:
            data['pay_comments'] = pay_comments

        if underpayment_reason:
            data['underpayment_reason'] = underpayment_reason

        if note2contractor:
            data['note2contractor'] = note2contractor

        url = 'fp/submissions/{0}/approve'.format(submission_id)
        return self.put(url, data)

    def reject_submission(self, submission_id, note2contractor):
        """
        Reject the submission.

        *Parameters:*
          :submission_id:           Submission reference.
          :note2contractor:         Notes from the client to the freelancer.

        """
        data = {}
        data['submission_id'] = submission_id
        data['note2contractor'] = note2contractor

        url = 'fp/submissions/{0}/reject'.format(submission_id)
        return self.put(url, data)

    def get_milestone_submissions(self, milestone_id):
        """
        Get all submissions for specific milestone.

        *Parameters:*
          :milestone_id:           Milestone reference ID.

        """
        data = {}

        url = 'fp/milestones/{0}/submissions'.format(milestone_id)
        return self.get(url, data)

    def get_active_milestone(self, contract_reference):
        """
        Get active milestone for specific contract.

        *Parameters:*
          :contract_reference:           Contract reference. Contracts info are available in the Engagements API.

        """
        data = {}

        url = 'fp/milestones/statuses/active/contracts/{0}'.format(contract_reference)
        return self.get(url, data)


class HR_V4(Namespace):
    """
    HR API version 4.
    """
    api_url = 'hr/'
    version = 4

    def list_client_applications(self, buyer_team__reference, job_key,
                                 status=None, profile_key=None,
                                 agency_team__reference=None,
                                 order_by=None, page_offset=None,
                                 page_size=None):
        """
        List job applications as a client.

        *Parameters:*
          :buyer_team__reference:  The reference ID of the client's team.
                                   It allows getting applications for a
                                   specific team. Example: ``34567``.
                                   Use 'List Teams' API call to get it.

          :job_key:                The job key. It allows getting applications
                                   for a specific job. Example: ``~01d54a7xxxxx125731``.

          :status:                 (optional) The current status of the job application.
                                   Valid values: ``shortlisted``, ``messaged``,
                                   ``hired``, ``offered``, ``declined``, ``hidden``.

          :profile_key:            (optional) Filters by a specific freelancer's profile key.

          :agency_team__reference: (optional) The reference ID of the agency.

          :order_by:               (optional) Sorts results in format ``$field_name1;$field_name2;..$field_nameN;AD...A``.
                                    Here ``A`` resebles ascending order, ``D`` - descending order. Example: ``order_by=created_time;D``.

          :page_offset:            (optional) Number of entries to skip

          :page_size:              (optional: default 20) Page size
                                   in number of entries

        """
        data = {}

        data['buyer_team__reference'] = buyer_team__reference
        data['job_key'] = job_key

        if status:
            data['status'] = status

        if profile_key:
            data['profile_key'] = profile_key

        if agency_team__reference:
            data['agency_team__reference'] = agency_team__reference

        if order_by:
            data['order_by'] = order_by

        data['page'] = '{0};{1}'.format(page_offset, page_size)

        url = 'clients/applications'
        return self.get(url, data)

    def get_client_application(self, application_id, buyer_team__reference):
        """
        Get specific job application as a client.

        *Parameters:*
          :application_id:    Job application reference ID.

          :buyer_team__reference:  The reference ID of the client's team.
                                   It allows getting applications for a
                                   specific team. Example: ``34567``.
                                   Use 'List Teams' API call to get it.

        """
        data = {}

        data['buyer_team__reference'] = buyer_team__reference

        url = 'clients/applications/{0}'.format(application_id)
        return self.get(url, data)

    def list_freelancer_applications(self, status=None, page_offset=None, page_size=None):
        """
        List job applications as a freelancer.

        *Parameters:*
          :status:                 (optional) The current status of the job application.
                                   Valid values: ``interviews``, ``invites``, ``active``.

          :page_offset:            (optional) Number of entries to skip

          :page_size:              (optional: default 20) Page size
                                   in number of entries

        """
        data = {}

        if status:
            data['status'] = status

        if page_offset and page_size:
            data['page'] = '{0};{1}'.format(page_offset, page_size)

        url = 'contractors/applications'
        return self.get(url, data)

    def get_freelancer_application(self, application_id):
        """
        Get specific job application as a freelancer.

        *Parameters:*
          :application_id:    Job application reference ID.

        """
        data = {}

        url = 'contractors/applications/{0}'.format(application_id)
        return self.get(url, data)
