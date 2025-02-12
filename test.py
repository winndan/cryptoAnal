from textwrap import indent
from traceback import print_exc
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
import os
from dotenv import load_dotenv
import nest_asyncio
import json  # Import the JSON module
from pydantic import BaseModel, Field
from system_prompt import analyst_system_prompt, question

nest_asyncio.apply()
load_dotenv()

api_key = os.getenv('API_KEY')

analyst_prompt = analyst_system_prompt

model = GeminiModel('gemini-1.5-flash', api_key=api_key)
agent = Agent(model=model, system_prompt=analyst_prompt)


response = agent.run_sync(question)

# Print the response data and all messages
print(response.data)
#print(response.all_messages())

data = response.data 
# Save to a JSON file
with open("output.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print("Data saved to output.json")