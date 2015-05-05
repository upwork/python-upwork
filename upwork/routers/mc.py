# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

import urllib

from upwork.namespaces import Namespace


class MC(Namespace):
    api_url = 'mc/'
    version = 1

    def get_trays(self, username=None, paging_offset=0, paging_count=20):
        """
        Retrieve a list of all active trays and a message count for each.

        *Parameters:*
          :username:          User name

        """
        url = 'trays'
        if paging_offset or not paging_count == 20:
            data = {'page': '{0};{1}'.format(paging_offset,
                                             paging_count)}
        else:
            data = {}

        if username:
            url = '{0}/{1}'.format(url, username)
        result = self.get(url, data=data)
        return result.get("trays", result)

    def get_tray_content(self, username, tray, paging_offset=None,
                         paging_count=None):
        """
        Retrieve message tray contents.

        *Parameters:*
          :username:          User name

          :tray:              Tray

          :paging_offset:     Start of page (number of results to skip)

          :paging_count:      Page size (number of results)

        """
        url = 'trays/{0}/{1}'.format(username, tray)
        if paging_offset is not None and paging_count is not None:
            data = {'page': '{0};{1}'.format(paging_offset,
                                             paging_count)}
        else:
            data = {}

        result = self.get(url, data=data)
        try:
            current_tray = result.get("current_tray", result)
            return current_tray.get("threads", result)
        except AttributeError:
            return result

    def get_thread_content(self, username, thread_id, paging_offset=0,
                           paging_count=20):
        """
        List details of a specific thread.

        *Parameters:*
          :username:          User name

          :thread_id:         Thread ID

          :paging_offset:     Start of page (number of results to skip)

          :paging_count:      Page size (number of results)

        """
        url = 'threads/{0}/{1}'.format(username, thread_id)
        if paging_offset or not paging_count == 20:
            data = {'page': '{0};{1}'.format(paging_offset,
                                               paging_count)}
        else:
            data = {}

        result = self.get(url, data=data)
        return result.get("thread", result)

    def get_thread_by_context(self, username, job_key, application_id,
                              context='Interviews', last_posts=False):
        """
        List details on a thread given a specific context,
        job key and application ID.

        *Parameters:*
          :username:        User name

          :job_key:         The context job key

          :application_id:  The context application ID.

          :context:         Name of the context. Valid values: Interviews.
                            Default: Interviews

          :last_posts:      If set to True, return the list of the threads
                            for the given context with the content of the last
                            message for each of the threads listed.

        """
        url = 'contexts/{username}/' \
            '{context}:{job_key}:{application_id}'.format(
                username=username, context=context, job_key=job_key,
                application_id=application_id)

        if last_posts:
            url += '/last_posts'

        data = {}

        result = self.get(url, data=data)
        return result.get("thread", result)

    def _generate_many_threads_url(self, url, threads_ids):
        return ';'.join(urllib.quote(str(i)) for i in threads_ids)

    def put_threads_read_unread(self, username, thread_ids, read=True):
        """
        Marks threads as read/unread.

        *Parameters:*
          :username:          User name

          :thread_ids:        must be a list, even of 1 item

          :read:              True/False (optional: default True)

        """
        if isinstance(thread_ids, (list, tuple)):
            thread_ids = ';'.join(map(str, thread_ids))
        url = 'threads/{0}/{1}'.format(username, thread_ids)

        if read:
            data = {'read': 'true'}
        else:
            data = {'read': 'false'}

        return self.put(url, data=data)

    def put_threads_read(self, username, thread_ids):
        """
        Marks threads as read.

        *Parameters:*
          :username:          User name

          :thread_ids:        must be a list, even of 1 item

        """
        return self.put_threads_read_unread(username, thread_ids, read=True)

    def put_threads_unread(self, username, thread_ids):
        """
        Marks threads as unread.

        *Parameters:*
          :username:          User name

          :thread_ids:        must be a list, even of 1 item

        """
        return self.put_threads_read_unread(username, thread_ids, read=False)

    def put_threads_starred_or_unstarred(self, username, thread_ids,
                                         starred=True):
        """
        Marks threads as starred/not starred.

        *Parameters:*
          :username:          User name

          :thread_ids:        must be a list, even of 1 item

          :starred:           True/False (optional: default True)

        """
        if isinstance(thread_ids, (list, tuple)):
            thread_ids = ';'.join(map(str, thread_ids))
        url = 'threads/{0}/{1}'.format(username, thread_ids)

        if starred:
            data = {'starred': 'true'}
        else:
            data = {'starred': 'false'}

        return self.put(url, data=data)

    def put_threads_starred(self, username, thread_ids):
        """
        Marks threads as starred.

        *Parameters:*
          :username:          User name

          :thread_ids:        must be a list, even of 1 item

        """
        return self.put_threads_starred_or_unstarred(username,
                                            thread_ids, starred=True)

    def put_threads_unstarred(self, username, thread_ids):
        """
        Marks threads as unstarred.

        *Parameters:*
          :username:          User name

          :thread_ids:        must be a list, even of 1 item

        """
        return self.put_threads_starred_or_unstarred(username,
                                            thread_ids, starred=False)

    def put_threads_deleted_or_undeleted(self, username, thread_ids,
                                         deleted=True):
        """
        Marks threads as deleted/not deleted.

        *Parameters:*
          :username:          User name

          :thread_ids:        must be a list, even of 1 item

          :deleted:           True/False (optional: default True)

        """
        if isinstance(thread_ids, (list, tuple)):
            thread_ids = ';'.join(map(str, thread_ids))
        url = 'threads/{0}/{1}'.format(username, thread_ids)

        if deleted:
            data = {'deleted': 'true'}
        else:
            data = {'deleted': 'false'}

        return self.put(url, data=data)

    def put_threads_deleted(self, username, thread_ids):
        """
        Marks threads as deleted.

        *Parameters:*
          :username:          User name

          :thread_ids:        must be a list, even of 1 item

        """
        return self.put_threads_deleted_or_undeleted(username, thread_ids,
                                                     deleted=True)

    def put_threads_undeleted(self, username, thread_ids):
        """
        Marks threads as not deleted

        *Parameters:*
          :username:          User name

          :thread_ids:        must be a list, even of 1 item

        """
        return self.put_threads_deleted_or_undeleted(username, thread_ids,
                                                     deleted=False)

    def post_message(self, username, recipients, subject, body,
                     thread_id=None, bcc=None, attachment_key=None):
        """
        Send a new message (creating a new thread) or reply to an existing \
        thread.

        *Parameters:*
          :username:        User name (of sender)

          :recipients:      Recipient(s)  (a single string or a list/tuple)

          :subject:         Message subject

          :body:            Message text

          :thread_id:       (optional) The thread id if replying
                            to an existing thread

          :bcc:             (optional) List of BCC recipients,
                            use comma (",") to separate ids in list

          :attachment_key:  (optional) The unique private key of any attachment
                            associated with the thread

        """
        url = 'threads/{0}'.format(username)
        if not isinstance(recipients, (list, tuple)):
            recipients = [recipients]
        recipients = ','.join(map(str, recipients))
        if thread_id:
            url = '{0}/{1}'.format(url, thread_id)

        data = {'recipients': recipients,
                'subject': subject,
                'body': body}

        if bcc:
            data['bcc'] = bcc

        if attachment_key:
            data['attachment-key'] = attachment_key

        return self.post(url, data=data)
