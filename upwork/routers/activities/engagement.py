class Api:
    """ """

    client = None

    def __init__(self, client):
        self.client = client

    def get_specific(self, engagement_ref):
        """List activities for specific engagement

        :param engagement_ref: String

        """
        return self.client.get("/tasks/v2/tasks/contracts/{0}".format(engagement_ref))

    def assign(self, company, team, engagement, params):
        """Assign engagements to the list of activities
        
        Parameters:
        :param company: 
        :param team: 
        :param engagement: 
        :param params: 

        """
        return self.client.put(
            "/otask/v1/tasks/companies/{0}/teams/{1}/engagements/{2}/tasks".format(
                company, team, engagement
            ),
            params,
        )

    def assign_to_engagement(self, engagement_ref, params):
        """Assign to specific engagement the list of activities
        
        Parameters:
        :param engagement_ref: 
        :param params: 

        """
        return self.client.put(
            "/tasks/v2/tasks/contracts/{0}".format(engagement_ref), params
        )
