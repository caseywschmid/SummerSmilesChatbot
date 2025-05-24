from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)

vector_stores = client.vector_stores.list()
print(vector_stores)

