from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
import os
from dotenv import load_dotenv
import nest_asyncio
from prompt import question, system_prompt

nest_asyncio.apply()
load_dotenv()



api_key = os.getenv('API_KEY')


model = GeminiModel('gemini-1.5-flash', api_key=api_key)
agent = Agent(model = model,
            system_prompt= system_prompt
            )

test = agent.run_sync(question)

print(test.data)