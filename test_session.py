import os
os.environ["LANGCHAIN_TRACING"] = "true"
os.environ["OPENAI_API_KEY"] = "your api key"
os.environ["LANGCHAIN_SESSION"] = "test_tracing"

from langchain.llms import OpenAI 
from langchain.chains import LLMMathChain
from langchain.callbacks import tracing_enabled
from langchain.agents import initialize_agent, Tool, load_tools
from langchain.agents import AgentType

tools = load_tools(["llm-math"] , llm = OpenAI(temperature=0))
agent = initialize_agent(tools, OpenAI(temperature=0),agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION , verbose= True)

if "LANGCHAIN_TRACING" in os.environ:
    del os.environ["LANGCHAIN_TRACING"]

# here, we are writing traces to "my_test_session"
with tracing_enabled("test_tracing") as session:
    assert session
    output1 = agent.run("What is 33 - 11")  # this should be traced

output2 = agent.run("What is 3 * 11")  # this should not be traced

print(output1)
print(output2)