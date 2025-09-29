from openai import AsyncAzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

class CompletionsClient:
    def __init__(self, endpoint, engine, api_key = None):

        api_version = "2024-12-01-preview"

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

    async def aclose(self):
        await self.client.aclose()


    async def generate(self, prompt: str, content: str, max_tokens: int = 300):

        response = await self.client.chat.completions.create(
            model=self.engine,
            messages=[
                {
                "role": "system",
                "content": [ {"type": "text", "text": prompt} ],
                },
                {
                "role": "user",
                "content": [ {"type": "text", "text": content} ],
                },                
            ],
            max_completion_tokens=max_tokens,
            )
        return response.choices[0].message.content