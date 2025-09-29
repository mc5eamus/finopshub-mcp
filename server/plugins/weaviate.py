import logging
from dataclasses import dataclass
from typing import List
from weaviate import connect_to_local
from weaviate.classes.query import MetadataQuery
from plugins.embeddings import EmbeddingsClient
from plugins.model import DashboardQuery, QuerySuggestionResponse
from plugins.config import COLLECTION_NAME

class QueryLibraryPlugin:
    
    def __init__(self,  embeddings_client: EmbeddingsClient):
        self.embeddings_client = embeddings_client
        self.logger = logging.getLogger(__name__)

    async def get_query_suggestions(
        self,
        query_purpose: str,
        keywords: List[str]
    ) -> QuerySuggestionResponse:
        
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

            # Connect to Weaviate and perform vector search
            with connect_to_local() as client:

                if not client.collections.exists(COLLECTION_NAME):
                    return {
                        "error": f"Collection '{COLLECTION_NAME}' does not exist, please make sure to populate it with query examples.",
                        "queries": []
                    }

                queries_collection = client.collections.get(COLLECTION_NAME)
                
                # Perform vector search
                result = queries_collection.query.near_vector(
                    near_vector=embedded_question[0],
                    limit=3,
                    return_metadata=MetadataQuery(distance=True)
                )
                
                queries = []
                for obj in result.objects:
                    properties = obj.properties
                    dashboard_query = DashboardQuery(
                        id=properties.get("id", ""),
                        title=properties.get("title", ""),
                        description=properties.get("description", ""),
                        query=properties.get("query", "")
                    )
                    queries.append(dashboard_query)

                    self.logger.info(f"Found query candidate: {dashboard_query.title} - {dashboard_query.description} (distance: {obj.metadata.distance})")

                return {"queries": queries}
            
        except Exception as e:
            self.logger.error(f"Error while searching for queries: {e}")
            return {
                "error": str(e),
                "queries": []
            }
