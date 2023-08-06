import os
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, ZeroShotAgent
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

DEFAULT_TOKENS = 1280
DEFAULT_TEMPERATURE = 0


def openai_llm(temperature: int = 0, max_tokens: int = DEFAULT_TOKENS):
    return ChatOpenAI(model_name="gpt-4", temperature=temperature, max_tokens=max_tokens)


def llm_chain_default(prompt, temperature: int = 0, max_tokens: int = DEFAULT_TOKENS):
    return LLMChain(llm=openai_llm(temperature=temperature, max_tokens=max_tokens), prompt=prompt)


def zsa_default_executor(prompt, tools, memory, verbose: bool = True):
    agent = ZeroShotAgent(llm_chain=llm_chain_default(prompt))
    return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools,
                                              verbose=verbose, memory=memory)


def zsa_default_executor2(prefix: str, suffix: str, tools: list, memory, verbose: bool = True):
    prompt = ZeroShotAgent.create_prompt(tools, prefix=prefix, suffix=suffix,
                                         input_variables=["input", "history", "agent_scratchpad"])
    agent = ZeroShotAgent(llm_chain=llm_chain_default(prompt))
    return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools,
                                              verbose=verbose, memory=memory)



