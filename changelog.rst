.. _changelog:


***************
Changelog
***************
***************

.. _1.1.1:

Version 1.1.1
-------------
* Drop obsoleted Get Offer API, Get Client/Contractor Offer should be used instead.

.. _1.1.0:

Version 1.1.0
-------------
* Get Categories (V1) is now fully depricated
* Added new Activities API - :py:meth:`Assign to specific engagement the list of activities <upwork.routers.task.Task_V2.assign_to_engagement>`.

.. _1.0.2:

Version 1.0.2
-------------
* os.path.join changed to urlparse.urljoin for supporting Windows systems
* added timeout option for configuring oauth client
* added paging support for Activities API, (!) note: the changes are not backward compatible for get_team_tasks and get_company_tasks

.. _1.0.1:

Version 1.0.1
-------------
* Added new API call - :py:meth:`Get Workdays by Company <upwork.routers.team.Team_V2.get_workdays_by_company>`.
* Added new API call - :py:meth:`Get Workdays by Contract <upwork.routers.team.Team_V2.get_workdays_by_contract>`.

.. _1.0.0:

Version 1.0.0
-------------
* Rebranding, the library moved to ``python-upwork``

.. _0.5.8:

Version 0.5.8
-------------
* Added new API call - :py:meth:`Get Snapshot by Contract <upwork.routers.offers.Offers.get_snapshot_by_contract>`.
* Added new API call - :py:meth:`Update Snapshot memo by Contract <upwork.routers.team.Team_V2.update_snapshot_by_contract>`.
* Added new API call - :py:meth:`Delete Snapshot by Contract <upwork.routers.team.Team_V2.delete_snapshot_by_contract>`.
* Fixed broken API call - :py:meth:`Get Work Diary by Contract <upwork.routers.team.Team_V2.get_workdiaries_by_contract>`.
* Added support of separate parameter ``related_jobcategory2`` in `Send client offer <upwork.routers.offers.Offers.send_client_offer>`
* Fixed issue with wrong name of ``milestones`` parameter in `Send client offer <upwork.routers.offers.Offers.send_client_offer>`
* Fixed issue with passing ``milestones`` and ``context`` parameters in `Send client offer <upwork.routers.offers.Offers.send_client_offer>`

.. _0.5.7:

Version 0.5.7
-------------
* Added new API call - :py:meth:`Accept or decline an offer <upwork.routers.offers.Offers.accept_or_decline>`.
* Added new conditionally required parameter ``category2`` to :py:meth:`Post job <upwork.routers.hr.HR.post_job>` API.

.. _0.5.6:

Version 0.5.6
-------------
* Added new API call - :py:meth:`List categories (v2) <upwork.routers.provider.Provider_V2.get_categories_metadata>`.
* Added new API call - :py:meth:`Get Work Diary by Contract <upwork.routers.team.Team_V2.get_workdiaries_by_contract>`.
* Recent changes from API Changelog - Wednesday, 2015-01-12
* Recent changes from API Changelog - Wednesday, 2014-12-03
* Recent changes from API Changelog - Friday, 2014-11-21
* Recent changes from API Changelog - Friday, 2014-10-31

.. _0.5.5:

Version 0.5.5.1
---------------
Minor maintenance release:

* Updated urllib3 requirements to ``urllib3==1.10`
* Use fixed requirements in the ``setup.py``
* Add ``httplib.system-ca-certs-locater`` and update Readme

.. _0.5.5:

Version 0.5.5
-------------
* Added new API call - :py:meth:`Create a new Milestone <upwork.routers.hr.HR_V3.create_milestone>`.
* Added new API call - :py:meth:`Edit the Milestone <upwork.routers.hr.HR_V3.edit_milestone>`.
* Added new API call - :py:meth:`Approve the Milestone <upwork.routers.hr.HR_V3.approve_milestone>`.
* Added new API call - :py:meth:`Activate the Milestone <upwork.routers.hr.HR_V3.activate_milestone>`.
* Added new API call - :py:meth:`Delete the Milestone <upwork.routers.hr.HR_V3.delete_milestone>`.
* Added new API call - :py:meth:`Submit for Approval <upwork.routers.hr.HR_V3.request_submission_approval>`.
* Added new API call - :py:meth:`Approve the Submission <upwork.routers.hr.HR_V3.approve_submission>`.
* Added new API call - :py:meth:`Reject the Submission <upwork.routers.hr.HR_V3.reject_submission>`.
* Added new API call - :py:meth:`Get all Submissions for the Milestone <upwork.routers.hr.HR_V3.get_milestone_submissions>`.
* Added new API call - :py:meth:`Get Active Milestone for the Contract <upwork.routers.hr.HR_V3.get_active_milestone>`.

* ``end_date`` parameter in :py:meth:`Post Job <upwork.routers.hr.HR.post_job>` ad :py:meth:`Update Job <upwork.routers.hr.HR.update_job>` is deprecated, keyword argument still remains for backwards compatibility
  and will be removed in future releases.

.. _0.5.4:

Version 0.5.4
-------------
* Added new API call - :py:meth:`Suspend Contract <upwork.routers.hr.HR.suspend_contract>`.
* Added new API call - :py:meth:`Restart Contract <upwork.routers.hr.HR.restart_contract>`.
* :py:meth:`Archive <upwork.routers.task.Task.archive_team_task>`/:py:meth:`unarchive <upwork.routers.task.Task.unarchive_team_task>` activities calls now support a list of codes.

.. _0.5.3:

Version 0.5.3
-------------
* New API calls added:
    1. Added :py:meth:`List activities for specific engagement<upwork.routers.task.Task_V2.list_engagement_activities>` via ``task_v2`` router.
    2. Added :py:meth:`Reasons metadata<upwork.routers.provider.Provider.get_reasons_metadata>` call.
    3. Added :py:class:`Offers router<upwork.routers.offers.Offers>` with handy number of calls for managing offers as a client and as a freelancer.
    4. Added :py:class:`HR_V3 router<upwork.routers.hr.HR_V3>` with a number of calls for getting job applications  as a client and as a freelancer.
    5. Added :py:meth:`List threads by context <upwork.routers.mc.MC.get_thread_by_context>` call.
* Removed mistakenly documented by Upwork but not working API call for getting team adjustments.

.. _0.5.2:

Version 0.5.2
-------------
* Fixed engagements API call, so that you can call
  ``client.hr.get_engagements()`` without any parameter
  to get all engagements for authorized user.
* oTask API strongly reworked, from now Task Codes are
  renamed to Activities and it's behavior is changed:

    1. Activity now is assigned to the engagement ID.
       It will appear it user's Upwork Team Client only if
       it was assigned to the user's engagement.
    2. You cannot delete activity. You can archive it
       and unarchive if necessary.
    3. Activities are created on the team level,
       you can create a company level activities by
       passing ``team_id`` that is equal to ``company_id``
       (which is ``parent__team_id``). There's a methods
       for this already, please see the reference documentation.
       Note that archived activity has empty engagements list,
       so if you decide to unarchive an activity, you need to
       do an extra update call to assign the activity to someone.
    4. When creating/updating activities you can pass optional
       ``engagements`` parameter, that should be a list of engagements
       that will be assigned to the Activity. Otherwise the activity
       won't be assigned to anyone. If you want to assign created/updated
       activity to all engagements in the company, you can set
       the ``all_in_company`` parameter.
    5. ``update_batch_tasks`` call is marked as experimental,
       use it on your own risk. It will be reworked in future.

.. _0.5.1:

Version 0.5.1
-------------
* Fixed bug preventing update (``PUT`` method) for oTask codes that
  contained non-urlsafe characters, e.g. "space", "colon", etc.

.. _0.5:

Version 0.5
-----------------
*October 2013*

Backwards incompatibility changes:

* Old key-based authorization is completely removed, now the only way
  to authorize is oAuth 1.0
* ``upwork.Client`` class doesn't support ``auth`` keyword argument any more,
  as now there's only one way of doing authorization
* Introduced V2 API calls for
  :py:meth:`Search Providers<upwork.routers.provider.Provider_V2.search_providers>` and
  :py:meth:`Search Jobs<upwork.routers.provider.Provider_V2.search_jobs>`.
  V1 API calls still work but to the end of 2013 will be switched off.
  So we greatly encourage you to use V2 API calls.
* ``examples/`` directory of the repository is updated with new examples for
  web and desktop application

Improvements:

* Clean up API to be consistent with official Upwork API documentation
* Now we use ``urllib3`` and all Http exceptions returned by API have
  meaningful messages
* Real PUT and DELETE json calls
* Some parts of API are fixed with to work correctly. Please refer to the
  method's docstring to see comprehensive description

*Nov 2012*

* Add Metadata Api
* Fixed job posting issue
* Add advanced logging


.. _0.4:

Version 0.4
-----------------
*May 2011*

* *Incompatibility with previous release* Changed name of the otask router to the task
* *Incompatibility with previous release* Chaged name of the oticket router to the ticket ??
* *Incompatibility with previous release* Changed name of the time_report router to the timereport
* *Incompatibility with previous release* Changed name of the finreports router to the finreport
* *Incompatibility with previous release* "from upwork import \*" now import only: "get_version", "Client", "utils"
* All routers moved from the __init__.py to the own files in the routers dir.
* All helper classes moved to own modules
* Added logging inside exceptions
* Added possiblity to switch off unused routers inside client class
* Added oconomy, finance routers
* Added Upwork oAuth support

.. _0.2:

Version 0.2
-----------------
*October 2010*

* All helpers classes moved to the utils.py, added Table helper class
* *Incompatibility with previous release* Changed names of the methods' params to reflect real Upwork params - e.g. company_reference vs company name

.. _0.1.2:

Version 0.1.2
-----------------
*29 September 2010*

Bug fix release

* Fixed check_token method
* Fixed KeyError on empty workdiaries

.. _0.1.1:

Version 0.1.1
-----------------
*15 July 2010*

Bug fix release

* Fixed HR2.get_user_role(user_id=None, team_id=None, sub_teams=False) method to correctly get user roles when both user reference and team reference were submitted - previously only one of them was used in the request
* Documentation fixes

.. _0.1:

Version 0.1
-----------------
*08 July 2010*

First public release
