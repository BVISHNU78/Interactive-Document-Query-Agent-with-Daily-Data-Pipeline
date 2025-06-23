import streamlit as st
import requests

st.title("Federal Documents RAG Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about recent federal documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            api_url = "http://127.0.0.1:8000/chat"
            response = requests.post(api_url, json={"query": prompt})
            
            if response.status_code == 200:
                agent_response = response.json().get("response")
                st.markdown(agent_response)
                st.session_state.messages.append({"role": "assistant", "content": agent_response})
            else:
                st.error("Failed to get a response from the agent.")