import streamlit as st
from ai_main import INITIAL_PROMPT , graph , config
from pathlib import Path 
import logging
from langchain_core.messages import AIMessage

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Research AI Agent")
st.title("Research AI Agent")

# Initialization of session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized Chat History")

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None 

# Chat Interface
user_input = st.chat_input("What research topic would you like to explore")

if user_input:
    logger.info(f"User input : {user_input}")
    st.session_state.chat_history.append({"role" : "user"  , "content" : user_input})
    st.chat_message("user").write(user_input)

    chat_input = {"messages" : [{'role' : 'system' , 'content' : INITIAL_PROMPT}] + st.session_state.chat_history}
    logger.info("Starting agent processing")

    full_response = ""
    for s in graph.stream(chat_input , config , stream_mode="values"):
        message = s['messages'][-1]

        if getattr(message , "tool_calls" , None):
            for tool_call in message.tool_calls:
                logger.info(f"Tool Call : {tool_call['name']}")

        if isinstance(message , AIMessage) and message.content:
            text_content = message.content if isinstance(message.content , str) else str(message.content)
            full_response += text_content + " "
            st.chat_message("assistant").write(full_response)
        
    if full_response:
        st.session_state.chat_history.append({'role' : 'assistant' , 'content' : full_response})
    