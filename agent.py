import os

import openai
from dotenv import load_dotenv
from langchain.agents import Tool
from function import web_search
from langchain.agents import AgentExecutor, ConversationalAgent, ZeroShotAgent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from typing import Callable
from langchain.agents import Tool, AgentExecutor
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from utils import zsa_default_executor2

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

prefix = """You are an AI Agent that responds to the Drug and Medication related queries. If you get any query 
related to drugs, medications, or health, you should answer it. If you get any query that is not related to drugs, 
medications, or health, you should respond with "I am DrugChat Agent and I can only answer questions related to 
drugs, medications, or health." You should also respond with "I am DrugChat Agent and I can only answer questions 
related to drugs, medications, or health." If you get query that contains two or more drugs, then run your tools twice
and more times to answer the query."""

suffix = """DO NOT summarize or shorten the Observation. Use relevant emojis.
{history}
Question: {input}
{agent_scratchpad}"""


def get_agent(openai_api_key):
    print("API>>>>", openai_api_key)
    openai.api_key = os.getenv(openai_api_key)
    web_doc_tool = Tool(
        name="Content from Web",
        func=web_search,
        description=f"MUST USE this tool to answer any question related to drugs, medications, or health."
    )

    tools = [web_doc_tool]
    memory = ConversationBufferWindowMemory(memory_key="history", k=2)

    master_agent_user: Callable[[ConversationBufferWindowMemory], AgentExecutor] = lambda \
        user_memory: zsa_default_executor2(prefix=prefix, suffix=suffix, tools=tools, memory=user_memory)

    # Initialize the Master Agent
    master_agent = zsa_default_executor2(prefix=prefix, suffix=suffix, tools=tools, memory=memory)

    return master_agent



