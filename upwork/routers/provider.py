# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

from upwork.namespaces import Namespace


class Provider(Namespace):
    api_url = 'profiles/'
    version = 1

    def get_provider(self, provider_ciphertext):
        """
        Retrieve an exhaustive list of attributes associated with the \
        referenced provider.

        *Parameters:*
          :provider_ciphertext:   The provider's cipher text (key)

        """
        if isinstance(provider_ciphertext, (list, tuple)):
            provider_ciphertext = map(str, provider_ciphertext)
            provider_ciphertext = ';'.join(provider_ciphertext[:20])

        url = 'providers/{0}'.format(provider_ciphertext)
        result = self.get(url)
        return result.get('profile', result)

    def get_provider_brief(self, provider_ciphertext):
        """
        Retrieve an brief list of attributes associated with the \
        referenced provider.

        *Parameters:*
          :provider_ciphertext:   The provider's cipher text (key)

        """
        if isinstance(provider_ciphertext, (list, tuple)):
            provider_ciphertext = map(str, provider_ciphertext)
            provider_ciphertext = ';'.join(provider_ciphertext[:20])

        url = 'providers/{0}/brief'.format(provider_ciphertext)
        result = self.get(url)
        return result.get('profile', result)

    def search_providers(self, data=None, page_offset=0, page_size=20,
                         order_by=None):
        """
        Search Upwork providers.
        NOTE: This call will be deprecated in favor to API V2
        :py:meth:`~upwork.routers.provider.Provider_V2.search_providers`

        *Parameters:*
          :data:       A dict of the following parameters
                     (all parameters are optional):

              :q:     Search query, e.g. "python".
                      Any text that appears in a provider's profile

              :c1:    Category name.
                      Use
                      :py:meth:`~upwork.routers.provider.Provider.get_categories_metadata`
                      to get the list of currently valid categories

              :c2:    Subcategory, which is related to category (c1),
                      please use c2[] to specify a couple subcategories.
                      Use
                      :py:meth:`~upwork.routers.provider.Provider.get_categories_metadata`
                      to get available subcategories.

              :fb:    Feedback (adjusted score),
                      e.g. ``fb='2.0 - 2.9 Stars'``
                      This searches for providers who have an adjusted
                      feedback score equal or greater (up to 5) than the number
                      passed in this parameter (decimals are okay).

              :hrs:     (Total hours) This searches for providers who have
                      a total number of hours equal or greater to the number
                      passed in this parameter.

              :ir:    This boolean parameter is used in combination with
                      the total hours worked parameter, and searches providers
                      who have worked within the last six months.
                      "Yes" or "No" are the only valid searches.
                      Omitting this will default to 'No'.

              :min:   The provider's minimum rate they have charged
                      in the past. Excludes providers with a public rate
                      less than this amount.

              :max:     The provider's maximum rate they have charged
                      in the past. Excludes providers with a public rate
                      greater than this amount.

              :loc:   Country region. Limit your searches to a
                      specific country region. Possible values:
                          * 'Australasia'
                          * 'East Asia'
                          * 'Eastern Europe'
                          * 'North America'
                          * 'South Asia'
                          * 'Western Europe'
                          * 'Misc'

              :pt:    Provider type. Limit your search to independent
                      or affiliate providers. Possible values:
                          * 'Individual'
                          * 'Affiliated'
                      By default both types are returned.

              :last:  Limit your search to providers who were active
                      after the date passed in this parameter.
                      Dates should be formatted like: 07-13-2009

              :test:  Limit your search to providers who have passed
                      a specific test (based on the test id).
                      You can get available tests using
                      :py:meth:`~upwork.routers.provider.Provider.get_tests_metadata`
                      Only singe value is allowed.

              :port:  Limit your search to providers who have at least
                      this number of portfolio items.

              :rdy:   Only return Upwork ready providers.

              :eng:   Limit your results to providers who have
                      at least the rating passed in the parameter.
                      Only the following English levels are available
                      (no decimals): [1,2,3,4,5]

              :ag:    Agency reference. Limit your search to a specific agency.

              :to:    Search the provider profile title text only.
                      Possible values: 'yes'|'no', by default 'no'.

              :g:     Limit your search to a specific group.

              :skills:  Required skills. A name of the skill.
                        Multiple values are allowed as a comma-separated string

          :page_offset: Start of page (number of results to skip) (optional)

          :page_size:   Page size (number of results) (optional: default 20)

          :order_by:  Sorting, in format
                      $field_name1;$field_name2;..$field_nameN;AD...A,
                      where 'A' means ascending, 'D' means descending,
                      the only available sort field as of now is "Date Created"

        """
        url = 'search/providers'
        if data is None:
            data = {}

        data['page'] = '{0};{1}'.format(page_offset, page_size)
        if order_by is not None:
            data['sort'] = order_by
        result = self.get(url, data=data)
        return result.get('providers', result)

    def search_jobs(self, data=None,
                    page_offset=0, page_size=20, order_by=None):
        """
        Search Upwork jobs.
        NOTE: This call will be deprecated in favor to API V2
        :py:meth:`~upwork.routers.provider.Provider_V2.search_jobs`

        *Parameters:*
          :data:        A dict of the following parameters
                        (all parameters are optional):

              :q:       Query, e.g. "python",
                        search the text of the job's description.

              :c1:      Category name. Use Metadata API to get the list
                        of currently valid categories

              :c2:      Subcategory, which is related to category (c1),
                        please use c2[] to specify a couple subcategories

              :qs:      Skill required, single value or comma-separated list

              :fb:      Feedback (adjusted score). Limit your search to buyers
                        with at least a score of the number passed in this
                        parameter. Use the following values to filter by score:
                            * none = '0'
                            * 1 - 4 Scores = '10'
                            * 4 - 4.5 Scores = '40'
                            * 4.5 - 5 Scores = '45'
                            * 5.0 Scores = '50'

              :min:     Minimum budget

              :max:     Maximum budget

              :t:       Job type. Possible values are:
                            * 'Hourly'
                            * 'Fixed'

              :wl:      Hours per week. This parameter can only be used when
                        searching Hourly jobs. These numbers are
                        a little arbitrary, so follow the following parameters
                        in order to successfully use this parameter:
                            * As Needed < 10 Hours/Week = '0'
                            * Part Time: 10-30 hrs/week = '20'
                            * Full Time: 30+ hrs/week = '40'

              :dur:     Engagement duration. This parameter can only be used
                        when searching Hourly jobs. These numbers are
                        a little arbitrary, so follow the following parameters
                        in order to successfully use this parameter:
                            * Ongoing / More than 6 months = '26'
                            * 3 to 6 months = '13'
                            * 1 to 3 months = '4'
                            * Less than 1 month = '1'
                            * Less than 1 week = '0'

              :dp:      Date posted. Search jobs posted according to timeframe.
                        Use the following parameters to specify a timeframe:
                            * Any Timeframe  = empty
                            * Last 24 hours = '0'
                            * Last 24 hours - 3 Days = '1'
                            * Last 3-7 Days = '3'
                            * Last 7-14 Days - '7'
                            * Last 14-30 Days - '14'
                            * > 30 Days - '30'

              :st:      Job status. Search for Canceled jobs, In Progress Jobs
                        and Completed Jobs. Defaults to Open Jobs.
                        Possible values:
                            * Open Jobs = 'Open'
                            * Jobs in Progress = 'In Progress'
                            * Completed Jobs = 'Completed'
                            * Canceled Jobs = 'Cancelled'

              :tba:     Total billed assignments.
                        Limit your search to buyers who completed at least
                        this number of paid assignments. Possible values:
                            * none = '0'
                            * has 1-5 billed assignments = '1'
                            * has 5-10 billed assignments = '5'
                            * has >10 billed assignments = '10'

              :gr:      Preferred group. Limits your search to buyers
                        in a particular group

              :to:        Search the provider profile title text only.
                        Possible values: 'yes'|'no', by default 'no'.

          :page_offset:   Start of page (number of results to skip) (optional)

          :page_size:     Page size (number of results) (optional: default 20)

          :order_by:      Sorting, in format
                        ``$field_name1;$field_name2;..$field_nameN;AD...A``,
                        where A means 'Ascending', D means 'Descending',
                        e.g. ``date_posted;A``

        """
        url = 'search/jobs'
        if data is None:
            data = {}
        data['page'] = '{0};{1}'.format(page_offset, page_size)
        if order_by is not None:
            data['sort'] = order_by
        result = self.get(url, data=data)
        return result.get('jobs', result)

    def get_categories_metadata(self):
        """
        Returns list of all categories available for job/contractor profiles.

        """
        url = 'metadata/categories'
        result = self.get(url)
        return result.get('categories', result)

    def get_skills_metadata(self):
        """
        Returns list of all skills available for job/contractor profiles.

        """
        url = 'metadata/skills'
        result = self.get(url)
        return result.get('skills', result)

    def get_regions_metadata(self):
        """
        Returns list of all region choices available for \
        job/contractor profiles.

        """
        url = 'metadata/regions'
        result = self.get(url)
        return result.get('regions', result)

    def get_tests_metadata(self):
        """
        Returns list of all available tests at Upwork.

        """
        url = 'metadata/tests'
        result = self.get(url)
        return result.get('tests', result)

    def get_reasons_metadata(self, reason_type):
        """
        Returns a list of reasons by specified type.

        *Parameters:*
          :type:    Requested type of the reason. Valid values:
                    ``EmployerEndsNoStartContract``, ``CloseOpening``,
                    ``RejectCandidate``, ``RejectInterviewInvite``,
                    ``CancelCandidacy``, ``EndProviderContract``,
                    ``EndCustomerContract``, ``EndAssignment``

        """
        url = 'metadata/reasons'
        data = {'type': reason_type}
        result = self.get(url, data)
        return result.get('reasons', result)


class Provider_V2(Namespace):
    api_url = 'profiles/'
    version = 2

    def get_categories_metadata(self):
        """
        Returns list of all categories (v2) available for job/contractor profiles.

        """
        url = 'metadata/categories'
        result = self.get(url)
        return result.get('categories', result)

    def search_providers(self, data=None, page_offset=0, page_size=20):
        """Search providers.

        The contractor search API allows to third party applications to search
        for any public contractor on Upwork. The search parameters mirror
        the options available on the site plus options to configure
        the format of your results.

        *Parameters:*

         :data:    (optional) A dict of the following parameters
                   (all parameters are optional):

           :q:        The search query.
                      With v2 API we support a subset of the
                      ``lucene query syntax``. In particular we support
                      ``AND``, ``OR``, ``NOT`` and additionally fields
                      exposed are the ones indicated below,
                      e.g ``q=title:php AND category:"Web Development"``

           :title:    Search in title of contractor profile

           :skills:   Search in skills of contractor profile

           :groups:   Search in groups of contractor profile

           :tests:    Search in tests of contractor profile
                      Use
                      :py:meth:`~upwork.routers.provider.Provider.get_tests_metadata`
                      to get available tests

           :tests_top_10:   Search for contractors that are
                            in top 10 for test

           :tests_top_30:   Search for contractors that are
                            in top 30 for test

           :category:    Search for category of contractor profile.
                         Use
                         :py:meth:`~upwork.routers.provider.Provider.get_categories_metadata`
                         to get available categories

           :subcategory: Search for subcategory of contractor profile.
                         Use
                         :py:meth:`~upwork.routers.provider.Provider.get_categories_metadata`
                         to get available categories

           :region:      Search for contractor profile in a region
                         Acceptable values are titles from Metadata Regions API
                         :py:meth:`~upwork.routers.provider.get_regions`,
                         e.g. ``Latin America``

           :feedback:    Search for contractor with feedback score:
                          - single params like ``3`` or ``3,4`` are acceptable
                            (comma - separated values result to OR queries)
                          - also ranges like ``[3 TO 4]`` are acceptable

           :rate:        Search for contractor profile with rate:
                          - single params like ``20`` or ``20,30``
                            are acceptable
                            (comma - separated values result to OR queries)
                          - ranges like ``[20 TO 40]`` are acceptable

           :hours:       Search for contractor profile that has worked
                         this many hours
                          - single params like ``20`` or ``20,30``
                            are acceptable
                            (comma separated values result to OR queries)
                          - ranges like ``[20 TO 40]`` are acceptable

           :recent_hours: Search for contractor profile that has worked
                          this many hours recently:
                           - single params like ``20`` or ``20,30``
                             are acceptable
                             (comma separated values result to OR queries)
                           - ranges like ``[20 TO 40]`` are acceptable

           :last_activity: Date of last time contractor worked
                            - last_activity is searched with ISO 8601
                              Date syntax with hours always set at
                              00:00:00.000 (i.e. ``2013-01-04T00:00:00.000Z``)

           :english_skill: Assessment of contractor on his/her english skills.
                           Value can be set to one of ``0 | 1 | 2 | 3 | 4 | 5``

           :is_upwork_ready: Whether contractor is upwork ready.
                            Value can be set to ``1`` or ``0``

           :profile_type:   Whether contractor is an AC or an IC.
                            Possible values:
                             - ``Independent``
                             - ``Agency``

           :include_entities:   Parameter can be set to ``0`` or ``1``
                                If ``1``: ``data`` in response will contain
                                only profile ids array.

         :page_offset: (optional) Start of page (number of results to skip)

         :page_size:  (optional: default ``20``) Page size (number of results)

        """
        url = 'search/providers'
        search_data = {}

        if data:
            search_data.update(data)

        search_data['paging'] = '{0};{1}'.format(page_offset, page_size)

        result = self.get(url, data=search_data)

        return result.get('providers', result)

    def search_jobs(self, data=None, page_offset=0, page_size=20):
        """Search jobs.

        The Job search API allows to third party applications to search
        for any public job on Upwork. The search parameters mirror the options
        available on the site plus options to configure the format
        of your results.

        *Parameters:*

         :data:    (optional) A dict of the following parameters
                   (all parameters are optional):

           :q:        The search query.
                      With API v2 we support a subset of the
                      ``lucene query syntax``. In particular we support
                      ``AND``, ``OR``, ``NOT`` and additionally fields
                      exposed are the ones indicated below,
                      e.g ``q=title:php AND category:web_development``

           :title:    Search in title of job profile

           :skills:   Search in skills of job profile

           :groups:   Search in groups of job profile

           :tests:    Search in tests of job profile
                      Use
                      :py:meth:`~upwork.routers.provider.Provider.get_tests_metadata`
                      to get available tests

           :tests_top_10:   Search for jobs that require provider to be
                            in top 10 for test

           :tests_top_30:    Search for jobs that require provider to be
                             in top 30 for test

           :category:    Search for category of job profile
                         See full list here:
                         https://developers.upwork.com/?lang=python#metadata_list-categories

           :subcategory: Search for subcategory of job profile
                         See full list here:
                         https://developers.upwork.com/?lang=python#metadata_list-categories
                         in the table "Changes"

           :job_type:     Type of job.
                          Acceptable values are:
                            - ``hourly``
                            - ``fixed``

           :duration:     Indicates job duration.
                          Acceptable values are:
                            - ``week``
                            - ``month``
                            - ``quarter``
                            - ``semester``
                            - ``ongoing``

           :workload:     Indicates workload for the job.
                          Acceptable values are:
                            - ``as_needed``
                            - ``part_time``
                            - ``full_time``

           :client_feedback:  Constrains the search to jobs posted by clients
                              with rating within a range:
                                - If the value is ``None``, then jobs from
                                  clients without rating are returned.
                                - single params like ``1`` or ``2,3``
                                  are acceptable
                                  (comma separated values result to OR queries)
                                - ranges like ``[2 TO 4]`` are acceptable

           :client_hires:   Constrains the search to jobs from clients
                            with range within the given number of past hires:
                              - single params like ``1`` or ``2,3``
                                are acceptable
                                (comma separated values result to OR queries)
                              - ranges like ``[10 TO 20]`` are acceptable

           :budget:   Constrains the search to jobs having the budget
                      within the range given
                        - ranges like ``[100 TO 1000]`` are acceptable

           :job_status:  The status that the job is currently in
                         Acceptable values are:
                           - ``open``
                           - ``completed``
                           - ``cancelled``

           :posted_since:   Number of days since the job was posted.

           :sort:           Field and direction sorting search results.
                            ``create_time`` descending  is used by default.
                            Allowed sorting fields are:
                              - ``create_time``
                              - ``client_rating``
                              - ``client_total_charge``
                              - ``client_total_hours``
                              - ``score``
                              - ``workload``
                              - ``duration``
                            Example: ``sort=create_time%20desc``

         :page_offset: (optional) Start of page (number of results to skip)

         :page_size:  (optional: default ``20``) Page size (number of results)

        """
        url = 'search/jobs'
        search_data = {}

        if data:
            search_data.update(data)

        search_data['paging'] = '{0};{1}'.format(page_offset, page_size)

        result = self.get(url, data=search_data)

        return result.get('jobs', result)
