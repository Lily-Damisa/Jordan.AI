import streamlit as st
import openai
import requests

# Setting up my API details from OpenRouter
openai.base_url = "https://openrouter.ai/api/v1"
openai.api_key = st.secrets["OPENROUTER_API_KEY"]

st.title("WellMama")

st.markdown(
    """
    <style>
    /* Main title */
    .title {
        font-size: 32px;
        font-weight: bold;
        color: #C2185B;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Chat bubbles */
    .user-bubble {
        background-color: #E1F5FE;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        color: #01579B;
        width: fit-content;
        max-width: 80%;
    }

    .bot-bubble {
        background-color: #F8BBD0;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        color: #880E4F;
        width: fit-content;
        max-width: 80%;
    }

    /* Center the bot messages on the left and user messages on the right */
    .bot-container {
        display: flex;
        justify-content: flex-start;
    }
    .user-container {
        display: flex;
        justify-content: flex-end;
    }

    /* Input box styling */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #C2185B;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# The chat history between user and bot
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are really helpful, WellMama."}]
    

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
            st.session_state.messages.append({"role": "wellmama", "content": reply})
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

# Display messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")





