import logging
import os
from typing import List
from azure.search.documents.aio import SearchClient
from azure.search.documents.models import VectorizedQuery 
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from plugins.embeddings import EmbeddingsClient
from plugins.model import DashboardQuery
    
class QueryLibraryPlugin:
    
    def __init__(self,  embeddings_client: EmbeddingsClient):
          
        # get credentials from environment variables, if not present, use DefaultAzureCredential
        if os.getenv("AZURE_SEARCH_API_KEY"):
            self.credential = AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))
        else:
            self.credential = DefaultAzureCredential()
        
        self.embeddings_client = embeddings_client

        self.logger = logging.getLogger(__name__)

    async def get_query_suggestions(
        self,
        query_purpose: str,
        keywords: List[str]
    ) -> List[DashboardQuery]:
        
        """
        Provides samples of queries for a specific task.
        
        Args:
            query_purpose: Purpose of the query
            keywords: Keywords extracted from the query
            
        Returns:
            List of DashboardQuery objects
        """
        self.logger.info(f"Searching for queries matching: '{query_purpose}', keywords: {', '.join(keywords)}")
        
        try:
            # Generate embedding for the query purpose
            embedded_question = await self.embeddings_client.get_embedding(query_purpose)

            keyword_query = ' OR '.join([f'"{keyword}"' for keyword in keywords]) if keywords else None

            vector_query = VectorizedQuery(vector=embedded_question[0], k_nearest_neighbors=5, fields="vector")

            async with SearchClient(
                endpoint=os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT"),
                index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
                credential=self.credential
            ) as search_client:
                response = await search_client.search(
                    search_text=keyword_query,
                    vector_queries=[vector_query],
                    top=3,
                    select=["id", "title", "description", "query"])
                
                queries = []
                async for result in response:
                    dashboard_query = DashboardQuery(
                        id=result.get("id", ""),
                        title=result.get("title", ""),
                        description=result.get("description", ""),
                        query=result.get("query", "")
                    )
                    queries.append(dashboard_query)
                    
                    self.logger.info(f"Found query candidate: {dashboard_query.title} - {dashboard_query.description}")
                
                return queries
            
        except Exception as e:
            self.logger.error(f"Error while searching for queries: {e}")
            return []
