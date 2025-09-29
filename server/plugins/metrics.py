import requests
import logging
from azure.identity import DefaultAzureCredential

class VmMetricsClient:
    def __init__(self):
        self.credentials = DefaultAzureCredential()
        self.token = self.credentials.get_token("https://management.azure.com/.default").token
        self.logger = logging.getLogger(__name__)

    def get_vm_metrics(self, subscription_id: str, resource_group: str, vm_name: str):
        # Implementation for fetching VM metrics
        metric_namespace = 'Microsoft.Compute/virtualMachines' # resource provider name
        metric_name = 'Percentage CPU'
        time_grain = 'PT1H'  # 1 hour time grain
        time_span = 'P30D'  # 30 days timespan

        # build request URL
        url = f'https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/{metric_namespace}/{vm_name}/providers/Microsoft.Insights/metrics?api-version=2023-10-01'
        
        # prepare headers
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }    

        payload = {
            'timespan': time_span,
            'interval': time_grain,
            'metricnames': metric_name,
            'aggregation': 'Maximum'
        }

        self.logger.info(f"Performing API request for {url} with payload {payload}")
        response = requests.get(url, headers=headers, params=payload).json()
        return response
