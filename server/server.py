import os
import dotenv
from typing import List
import pandas as pd
import logging
from fastmcp import FastMCP
from plugins.model import QuerySuggestionResponse
from plugins.advisor import AzureAdvisorClient
from plugins.weaviate import QueryLibraryPlugin
from plugins.kusto import KustoQueryExecutor
from plugins.metrics import VmMetricsClient
from plugins.embeddings import EmbeddingsClient

dotenv.load_dotenv()

embeddings_client = EmbeddingsClient(
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    engine=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", None)
)

mcp = FastMCP(name="FinOpsHubMCP")

query_library_plugin = QueryLibraryPlugin(embeddings_client=embeddings_client)
query_executor_plugin = KustoQueryExecutor(os.getenv("FINOPS_HUB_CLUSTER", None), "Hub")
advisor_plugin = AzureAdvisorClient()

@mcp.tool()
async def get_query_suggestions(
    purpose: str, 
    keywords: List[str]) -> QuerySuggestionResponse:
    """Makes FinOps query suggestions based on a given purpose and keywords.
    
    Args:
        purpose: what is the concern of the request
        keywords: keywords associated with the purpose
    """

    # Call the QueryLibraryPlugin to get query suggestions
    result = await query_library_plugin.get_query_suggestions(purpose, keywords)
    return result

@mcp.tool()
def execute_finops_query(
    query: str) -> pd.DataFrame:
    """Executes a FinOps Kusto Query.
    
    Args:
        query: KQL query to execute
    """
    try:
        if not query:
            raise ValueError("Query cannot be empty")

        # Execute the query using the KustoQueryExecutor
        return query_executor_plugin.execute_query(query)
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        raise ValueError(f"Failed to execute query: {e}")
    
@mcp.tool()
def vm_cpu_utilization(
    subscription_id: str,
    resource_group: str,
    vm_name: str
) -> pd.DataFrame:
    """Fetches VM CPU utilization metrics.
    Args:
        subscription_id: Azure subscription ID
        resource_group: Azure resource group name
        vm_name: Name of the virtual machine
    """
    try:
        vm_metrics_client = VmMetricsClient()
        metrics = vm_metrics_client.get_vm_metrics(subscription_id, resource_group, vm_name)
        return metrics
    
    except Exception as e:
        logging.error(f"Error retrieving data for {vm_name}: {e}")
        raise ValueError(f"Error retrieving data for {vm_name}: {e}")

@mcp.tool()
async def retrieve_advisor_recommendations(
        subscription_id: str,
        resource_group: str = None,
        resource_name: str = None):
    """Retrieves Azure Advisor recommendations for a specific resource.

    Args:
        subscription_id: Azure subscription ID
        resource_group: Azure resource group name or None for all resource groups
        resource_name: Name of the resource or None for all resources
    """
    try:
        recommendations = advisor_plugin.get_recommendations(subscription_id, resource_group, resource_name)
        return recommendations

    except Exception as e:
        logging.error(f"Error retrieving recommendations: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    print("Starting FinOps Server…")
    mcp.run(transport="http")