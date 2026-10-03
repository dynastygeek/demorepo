from langgraph.graph import START,END,StateGraph
from typing import List, Dict,TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage,SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
load_dotenv()
from langgraph.checkpoint.memory import InMemorySaver

# Define a TypedDict for the chatbot state
class ChatbotGraph(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# Define a function to handle the chat node
def chat_node(state: ChatbotGraph) -> ChatbotGraph:
    # Create a chat model
    chat_model = ChatOpenAI()

    # Get the messages from the state
    messages = state["messages"]

    # Generate a response using the chat model
    response = chat_model.invoke(messages)

    # Append the AI's response to the messages
    messages.append(AIMessage(content=response.content))

    # Return the updated state
    return {"messages": messages}

# Create an in-memory checkpoint saver
checkpoint = InMemorySaver()

# Create a state graph for the chatbot
graph = StateGraph(ChatbotGraph)

# add a start node
graph.add_node("chat_node", chat_node)

# add edges to define the flow of the graph
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile the graph into a chatbot
chatbot = graph.compile(checkpointer=checkpoint)
chatbot

# # Stream a response from the chatbot
# for message_chunks, metadata in chatbot.stream({"messages": [HumanMessage(content="Write an essay about Python programming")]},
#                config={"configurable" :{"thread_id": "1"}}, stream_mode ='messages'):
#     if message_chunks.content:
#             print(f"AI: {message_chunks.content}", end='', flush=True)

