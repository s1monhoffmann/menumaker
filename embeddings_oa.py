from openai import OpenAI
import os

client = OpenAI(api_key="YOUR_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_embeddings(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )

    return response.data[0].embedding