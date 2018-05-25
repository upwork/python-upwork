# Python bindings to Upwork API
# python-upwork
# (C) 2010-2016 Upwork

import urllib

from upwork.namespaces import Namespace


class Messages(Namespace):
    api_url = 'messages/'
    version = 3

    def get_rooms(self, company, params = {}):
        """
        Retrieve rooms information

        *Parameters:*
          :company:          Company ID

          :params:           List of parameters

        """
        url = '{0}/rooms'.format(company)
        result = self.get(url, data=params)
        return result.get(url, result)

    def get_room_details(self, company, room_id, params = {}):
        """
        Get a specific room information

        *Parameters:*
          :company:          Company ID

          :room_id           Room ID

          :params:           List of parameters

        """
        url = '{0}/rooms/{1}'.format(company, room_id)
        result = self.get(url, data=params)
        return result.get(url, result)

    def get_room_by_offer(self, company, offer_id, params = {}):
        """
        Get a specific room by offer ID

        *Parameters:*
          :company:          Company ID

          :offer_id:         Offer ID

          :params:           List of parameters

        """
        url = '{0}/rooms/offers/{1}'.format(company, offer_id)
        result = self.get(url, data=params)
        return result.get(url, result)

    def get_room_by_application(self, company, application_id, params = {}):
        """
        Get a specific room by application ID

        *Parameters:*
          :company:          Company ID

          :application_id:   Application ID

          :params:           List of parameters

        """
        url = '{0}/rooms/applications/{1}'.format(company, application_id)
        result = self.get(url, data=params)
        return result.get(url, result)

    def get_room_by_contract(self, company, contract_id, params = {}):
        """
        Get a specific room by contract ID

        *Parameters:*
          :company:          Company ID

          :contract_id:      Contract ID

          :params:           List of parameters

        """
        url = '{0}/rooms/contracts/{1}'.format(company, contract_id)
        result = self.get(url, data=params)
        return result.get(url, result)

    def create_room(self, company, params = {}):
        """
        Create a new room

        *Parameters:*
          :company:          Company ID

          :params:           List of parameters

        """
        url = '{0}/rooms'.format(company)
        result = self.post(url, data=params)
        return result.get(url, result)

    def send_message_to_room(self, company, room_id, params = {}):
        """
        Send a message to a room

        *Parameters:*
          :company:          Company ID

          :room_id:          Room ID

          :params:           List of parameters

        """
        url = '{0}/rooms/{1}/stories'.format(company, room_id)
        result = self.post(url, data=params)
        return result.get(url, result)

    def update_room_settings(self, company, room_id, username, params = {}):
        """
        Update a room settings

        *Parameters:*
          :company:          Company ID

          :room_id:          Room ID

          :params:           List of parameters

        """
        url = '{0}/rooms/{1}/users/{2}'.format(company, room_id, username)
        result = self.put(url, data=params)
        return result.get(url, result)

    def update_room_metadata(self, company, room_id, params = {}):
        """
        Update the metadata of a room

        *Parameters:*
          :company:          Company ID

          :room_id:          Room ID

          :params:           List of parameters

        """
        url = '{0}/rooms/{1}'.format(company, room_id)
        result = self.put(url, data=params)
        return result.get(url, result)
