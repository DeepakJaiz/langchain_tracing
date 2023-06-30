import os
os.environ["LANGCHAIN_TRACING"] = "true"
os.environ["OPENAI_API_KEY"] = "your api key"


from langchain.llms import OpenAI 
from langchain.chains import LLMMathChain
from langchain.callbacks import tracing_enabled
from langchain.agents import initialize_agent, Tool, load_tools
from langchain.agents import AgentType

tools = load_tools(["llm-math"] , llm = OpenAI(temperature=0))
agent = initialize_agent(tools, OpenAI(temperature=0),agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION , verbose= True)

import asyncio

if "LANGCHAIN_TRACING" in os.environ:
    del os.environ["LANGCHAIN_TRACING"]

questions = [f"What is {i} raised to .123 power?" for i in range(1, 4)]

# start a background task
async def main():
    task = asyncio.create_task(agent.arun(questions[0]))  # this should not be traced
    with tracing_enabled() as session:
        assert session
        tasks = [agent.arun(q) for q in questions[1:3]]  # these should be traced
        await asyncio.gather(*tasks)

    await task
asyncio.run(main())