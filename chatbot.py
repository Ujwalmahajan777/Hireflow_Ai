from langgraph.graph import StateGraph, START, MessagesState
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode , tools_condition
from langchain_core import tools
import os
from langchain_core.messages import HumanMessage, SystemMessage ,BaseMessage 
from tools import extract_text_from_pdf
from typing import Annotated,TypedDict
from langgraph.graph.message import add_messages


load_dotenv()

# --- model and tools ---
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

def chat_node(state: ChatState ):
    """LLM node that may answer or request a tool call."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


tools = [extract_text_from_pdf]
llm_with_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)

# --- build graph ---
builder = StateGraph(MessagesState)
builder.add_node("chat_node",chat_node )
builder.add_node("tools", tool_node)

builder.add_edge(START, "chat_node")
builder.add_conditional_edges("chat_node",tools_condition)
builder.add_edge("tools","chat_node")


DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres"

def run_stream_in_terminal():
    # # open Postgres saver for this whole CLI session
    # with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    #     # 1) create tables ONCE
    #     checkpointer.setup()

    checkpointer = MemorySaver()

        # 2) compile graph with this checkpointer
    graph = builder.compile(checkpointer=checkpointer)

    print("HR Assistant CLI (type 'exit' to quit)")
    thread_config = {"configurable": {"thread_id": "thread-1"}}

    while True:
            user_text = input("HR: ")
            if user_text.lower() == "exit":
                break

            input_payload = {
                "messages": 
                    [SystemMessage(content="""You are HR Assistant, an agentic AI automating HR workflows as per human command
                    use the given path of resumes files located in resume text extract tool"""),
                    HumanMessage(content= user_text)]
                  
            }

            try:
                result = graph.invoke(input_payload, thread_config)
                messages = result.get("messages", [])
                text = messages[-1].content if messages else "Sorry, no response."
                print("Assistant:", text)
            except Exception as e:
                print("Assistant: Error:", e)

if __name__ == "__main__":
    run_stream_in_terminal()
