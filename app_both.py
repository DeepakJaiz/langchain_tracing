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

# Both of the agent runs will be traced because the environment variable is set
output1 = agent.run("What is 3 + 11")
with tracing_enabled() as session:
    output2 = agent.run("What is 590 / 5")

print(output1)
print(output2)