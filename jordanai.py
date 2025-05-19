import streamlit as st
import openai
import requests

# Setting up my API details from OpenRouter
openai.base_url = "https://openrouter.ai/api/v1"
openai.api_key = st.secrets["OPENROUTER_API_KEY"]

st.title("JordanAI")

# The chat history between user and bot
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are really helpful, Jordan."}]
    

# User input field
user_input = st.text_input("You:", key="input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": st.session_state.messages
            }
        )

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "jordan", "content": reply})
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

# Display messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")





