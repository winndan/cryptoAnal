from textwrap import indent
from traceback import print_exc
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
import os
from dotenv import load_dotenv
import nest_asyncio
import json  # Import the JSON module
from pydantic import BaseModel, Field

nest_asyncio.apply()
load_dotenv()

api_key = os.getenv('API_KEY')

analyst_prompt = """You are a cryptocurrency market analyst and I want you to analyze
                the market and give a summary about the market. Your analysis should be the basis for
                creating or developing strategies for entry and stop loss."""

model = GeminiModel('gemini-1.5-flash', api_key=api_key)
agent = Agent(model=model, system_prompt=analyst_prompt)

question = """Can you find a pattern for me about the market?"""

response = agent.run_sync(question)

# Print the response data and all messages
print(response.data)
print(response.all_messages())


class ResponseModel(BaseModel):
    response: str
    need_escalation: bool
    follow_up_required: bool
    sentiment: str = Field(description="The sentiment of the response")

response2 = agent.run_sync(
    user_prompt="What was my previous question?",
    result_type=ResponseModel,
    message_history=response.all_messages()
)

response3 = agent.run_sync(
    model = model,
    result_type=ResponseModel,
    system_prompt=analyst_prompt

)

print(response2.data)
response1 = response3.run_sync("Analyze the market for me")
print(response1.data.model_dump_json(indent=2))