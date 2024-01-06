import streamlit as st 
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv
load_dotenv() 
import openai

openai.api_key = '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' 



st.title("Dr.Sab") 
st.subheader("By Sytax Scholars")

model = st.selectbox(
    "Select a model", 
    ("gpt-3.5-turbo", "gpt-4")
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = [] 
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Query: ", key="input") 

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()
 
if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        try:
            response = get_chatgpt_response(messages, model)
        except openai.error.AuthenticationError as e:
            st.error(f"AuthenticationError: {str(e)}")
            response = "An error occurred. Please check your API key."
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

        
if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    with st.expander("Show Messages"):
        st.write(messages) 
        