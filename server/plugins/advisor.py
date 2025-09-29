import logging
from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest

class AzureAdvisorClient:

    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.client = ResourceGraphClient(self.credential)
        self.logger = logging.getLogger(__name__)

    def get_recommendations(self, 
        subscription_id: str,
        resource_group: str = None, 
        resource_name: str = None):

        query = "advisorresources"
        
        if subscription_id:
            query += f"| where subscriptionId=='{subscription_id}' "

        query += """
            | where type == 'microsoft.advisor/recommendations'
            | where properties contains_cs "Right-size" """
        
        if resource_group:
            query += f"| where resourceGroup=='{resource_group}' "

        if resource_name:
            query += f"""
            | extend resourceName = split(id, '/')[8]
            | where resourceName == '{resource_name}' """

        print(query)

        self.logger.info(f"Executing query: {query}")

        # Define the query
        query = QueryRequest(
            subscriptions=[subscription_id],
            query=query
        )

        # Execute the query
        response = self.client.resources(query)
        self.logger.info(f"Query response: {response}")
        return response