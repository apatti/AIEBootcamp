from typing import Literal, Annotated
from typing_extensions import TypedDict

from langchain_core.tools import tool  
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.runnables.graph import MermaidDrawMethod

from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
load_dotenv()

from weather import get_weather, WeatherData

from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

from IPython.display import Image, display

import chainlit as cl


tavilTool = TavilySearchResults(max_results=3)
tool_belt = [tavilTool]


llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
llm.bind_tools(tool_belt)


class State(TypedDict):
    messages: Annotated[list,add_messages]

def call_llm(state):
    print(f"Calling for: {state['messages']}")
    messages = state["messages"]
    response = llm.invoke(messages)
    print(f"Response: {response}")
    return {"messages": [response]}

def should_continue(state) -> Literal["continue", "end"]:
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "continue"
    
    return "end"

tool_node = ToolNode(tool_belt)

uncompiled_graph = StateGraph(State)
uncompiled_graph.add_node("agent", call_llm)
uncompiled_graph.add_node("action", tool_node)

#uncompiled_graph.add_edge(START, "agent")
uncompiled_graph.set_entry_point("agent")
uncompiled_graph.add_conditional_edges("agent", should_continue,{"continue": "action", "end": END})
uncompiled_graph.add_edge("action", "agent")

compiled_graph = uncompiled_graph.compile()

def display_graph(app):
    display(
        Image(
            app.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API
            )
        )
    )
    app.get_graph().print_ascii()

inputs = {"messages" : [HumanMessage(content="Who is the current captain of the Winnipeg Jets?")]}


async def process_graph_updates():
    async for chunk in compiled_graph.astream(inputs, stream_mode="updates"):
        for node, values in chunk.items():
            print(f"Receiving update from node: '{node}'")
            print(values["messages"])
            print("\n\n")

import asyncio
display_graph(compiled_graph)
asyncio.run(process_graph_updates())