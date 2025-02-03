from typing import Literal, Annotated
from typing_extensions import TypedDict

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)#,filename="app.log")

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from dotenv import load_dotenv
load_dotenv()

from weather import get_weather

from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

import chainlit as cl

class State(TypedDict):
    messages: Annotated[list,add_messages]

tool_belt = [get_weather]
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm = llm.bind_tools(tool_belt)

tool_node = ToolNode(tool_belt)

def call_llm(state):
    logger.debug(f"Calling for: {state['messages']}")
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state) -> Literal["continue", "end"]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "continue"
    
    return "end"

uncompiled_graph = StateGraph(State)
uncompiled_graph.add_node("agent", call_llm)
uncompiled_graph.add_node("action", tool_node)

uncompiled_graph.add_edge(START, "agent")
uncompiled_graph.add_conditional_edges("agent", should_continue,{"continue": "action", "end": END})
uncompiled_graph.add_edge("action", "agent")

compiled_graph = uncompiled_graph.compile()

'''
async def process_graph_updates():
    messages = []
    async for chunk in compiled_graph.astream(inputs, stream_mode="updates"):
        for node, values in chunk.items():
            logger.info(f"Receiving update from node: '{node}'")
            logger.debug(values["messages"])
            messages.append(values["messages"])

    final_llm_response = messages[-1][0].content
    final_llm_metadata = messages[-1][0].response_metadata
'''

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("compiled_graph", compiled_graph)

@cl.on_message
async def on_message(message: cl.Message):
    compiled_graph = cl.user_session.get("compiled_graph")
    msg = cl.Message(content="")
    inputs = {"messages" : [
            SystemMessage(content="You are pickleball expert, get the current weather and find the best time of the day to play the game in city provided by user!"),
            HumanMessage(content=f"{message.content}")
        ]}
    logger.info(f"Inputs: {inputs}")
    messages = []
    await msg.stream_token("Finding the right time, please wait...\n")
    async for chunk in compiled_graph.astream(inputs, stream_mode="updates"):
        for node, values in chunk.items():
            logger.info(f"\nReceiving update from node: '{node}'")
            await msg.stream_token(f"Receiving update from node: '{node}'\n")
            logger.debug(values["messages"])
            messages.append(values["messages"])

    final_llm_response = messages[-1][0].content
    final_llm_metadata = messages[-1][0].response_metadata

    logger.info(f"Response: {final_llm_response}")
    logger.info(f"Metadata: {final_llm_metadata}")

    await msg.stream_token(f"{final_llm_response}\n")

    await msg.send()

#import asyncio
#asyncio.run(process_graph_updates())