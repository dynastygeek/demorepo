import streamlit as st
from chatbot import chatbot
from langchain_core.messages import HumanMessage
 
CONFIG = {'configurable': {'thread_id': '1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []      

# load the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    # add the user message to history and display it
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    # call the chatbot
    # response = chatbot.invoke(
    #     {'messages': [HumanMessage(content=user_input)]},
    #     config=CONFIG
    # )
    # ai_message = response['messages'][-1].content

    # add the assistant message to history and display it
    # st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

        # st.markdown(ai_message)