# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

from upwork.namespaces import Namespace
from upwork.compatibility import quote


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
            provider_ciphertext = quote(';').join(provider_ciphertext[:20])

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

           :category2:   Search for category of contractor profile.
                         Use
                         :py:meth:`~upwork.routers.provider.Provider.get_categories_metadata`
                         to get available categories

           :subcategory2: Search for subcategory of contractor profile.
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

           :category2:   Search for category of job profile
                         See full list here:
                         https://developers.upwork.com/?lang=python#metadata_list-categories

           :subcategory2: Search for subcategory of job profile
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
