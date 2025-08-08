import streamlit as st
import requests

st.set_page_config(page_title="WellMama", page_icon="🤱", layout="centered")

# Sidebar
with st.sidebar:
    st.title("🤱 WellMama")
    st.markdown("""
    Your supportive AI companion for postpartum mothers in Nigeria.  
    💬 Ask questions, share feelings, or get tips.
    """)
    st.markdown("---")
    st.markdown("**Powered by OpenRouter + GPT-3.5**")

# Title
st.markdown("<h1 style='text-align: center;'>🤱 WellMama</h1>", unsafe_allow_html=True)

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are WellMama, a supportive AI assistant for postpartum mothers in Nigeria."}
    ]

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI reply
    with st.chat_message("assistant"):
        with st.spinner("WellMama is thinking..."):
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
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
