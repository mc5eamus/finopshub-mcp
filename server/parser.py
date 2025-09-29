import json
import csv
import os
import sys
import weaviate
from weaviate.classes.config import Property, DataType, Configure
from weaviate.classes.data import DataObject
import dotenv
from plugins.embeddings import EmbeddingsClient
from plugins.completions import CompletionsClient
import asyncio

dotenv.load_dotenv()


embeddings_client = EmbeddingsClient(
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    engine=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", None)
)

completions_client = CompletionsClient(
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    engine=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", None)
)

async def get_embedding(text: str | list[str]):
    """
    Asynchronously retrieves embeddings for the given text using the OpenAI client.
    """
    return await embeddings_client.get_embedding(text)

async def get_completion(prompt: str, text: str, max_tokens: int = 300):
    """
    Asynchronously generates a completion for the given prompt and text using the OpenAI client.
    """
    return await completions_client.generate(prompt, text, max_tokens=max_tokens)


def create_index_entries(items):
    return [DataObject(
        properties={
            "title": i["title"],
            "description":   i["description"],
            "query": i["query"],
        },
        vector=i["vector"], 
    )
    for i in items
    ]

def index_queries(items):
    with weaviate.connect_to_local() as client:

        client.collections.delete("FinOpsHubQueries")

        collection = client.collections.create(
            name="FinOpsHubQueries",
            vectorizer_config=Configure.Vectorizer.none(),
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="description", data_type=DataType.TEXT),
                Property(name="query", data_type=DataType.TEXT)
            ], 
        )

        collection.data.insert_many(items)

        for item in collection.iterator():
            print(item.uuid, item.properties)

async def parse_dashboard():
    
    with open('content/finops_model.md', 'r', encoding='utf-8') as f:
        finops_costs_model = f.read()

    with open('content/query_explainer.md', 'r', encoding='utf-8') as f:
        finops_query_explainer = f.read()

    explainer_prompt = finops_query_explainer.replace("{finops_data_model}", finops_costs_model)

    # Load the dashboard JSON
    with open('content/finops-hub-dashboard.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Build a mapping from queryId to query text
    query_map = {}
    for query in data.get('queries', []):
        query_id = query.get('id')
        query_text = query.get('text')
        # print(f"Processing query: {query_id} - {query_text}")
        if query_id and query_text:
            query_map[query_id] = {"text" : query_text, "usedVariables": query.get('usedVariables', [])}

    base_queries = {}
    for query in data.get('baseQueries', []):
        id = query.get('id')
        query_id = query.get('queryId')
        variable_name = query.get('variableName')
        base_query = query_map.get(query_id)
        base_queries[variable_name] = { 
            "text": base_query.get('text', '') if base_query else '', 
            "usedVariables": base_query.get('usedVariables', []) if base_query else []    
        } 


    # with open('base_queries.json', 'w', encoding='utf-8') as f:
    #     json.dump(base_queries, f, indent=4)

    results = []

    for tile in data.get('tiles', []):
        title = tile.get('title', '')
        query_id = None
        query_ref = tile.get('queryRef', {})
        if isinstance(query_ref, dict):
            query_id = query_ref.get('queryId')
        query_from_map = query_map.get(query_id, '')
        query_text = query_from_map['text'] if query_id else ''
        used_variables = query_from_map['usedVariables'] if query_id else []

        full_query_text = query_text

        # put user variable to stack
        user_variable_stack = []
        for var in used_variables:
            user_variable_stack.append(var)

        # while the stack is not empty, pop the last variable and prepend the query text with the base query
        while user_variable_stack:
            var = user_variable_stack.pop()
            base_query = base_queries.get(var, {}).get('text', '')
            if base_query:
                full_query_text = f"let {var} = {base_query};\n" + full_query_text
                for used_var in base_queries.get(var, {}).get('usedVariables', []):
                    if used_var not in user_variable_stack:
                        user_variable_stack.append(used_var)


        if title and full_query_text:
            query_explanation = await get_completion(
                explainer_prompt,
                full_query_text
            )
            print (f"Query {title}: {query_explanation}")

            embeddings = await get_embedding(f"{title}: {query_explanation}")
            entry = {
                "title": title,
                "description": query_explanation,
                "query": full_query_text,
                "vector": embeddings[0]
            }
            results.append(entry)
    return results


async def inject_to_weaviate(entries):
    with open('content/dashboard_queries_index.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    entries = create_index_entries(results)
    index_queries(entries)

async def dump_dashboard():
    results = await parse_dashboard()

    with open('content/dashboard_queries_index.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Process dashboard queries")
    parser.add_argument("action", choices=["parse","inject"], help="Action to perform")
    args = parser.parse_args()

    if args.action == "inject":
        print("Injecting to index...")
        asyncio.run(inject_to_weaviate(None))
    elif args.action == "parse":
        print("Parsing dashboard...")
        asyncio.run(dump_dashboard())

