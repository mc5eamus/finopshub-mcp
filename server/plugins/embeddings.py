from openai import AsyncAzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

class EmbeddingsClient:
    """
    Calculates embeddings for a given text using the Azure OpenAI embeddings endpoint.
    """
    def __init__(self, endpoint, engine, api_key = None):

        api_version = "2024-07-01-preview"

        if api_key:
            self.client = AsyncAzureOpenAI(
                azure_endpoint=endpoint,
                api_key=api_key,
                api_version=api_version,
                azure_deployment=engine,
            )
        else:
            token_provider = get_bearer_token_provider(
                DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
            )

            self.client = AsyncAzureOpenAI(
                api_version=api_version,
                azure_endpoint=endpoint,
                azure_ad_token_provider=token_provider,
                azure_deployment=engine,
            )
        self.engine = engine

    async def get_embedding(self, text: str | list[str]):
        response = await self.client.embeddings.create(input=text, model=self.engine)
        return list(map(lambda x: x.embedding, response.data))