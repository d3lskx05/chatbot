# chat_app.py
import streamlit as st
import requests

st.title("💬 Простой чат без токена")

def ask_openrouter(prompt):
    headers = {
        "HTTP-Referer": "https://test.local",
        "X-Title": "StreamlitTestApp"
    }
    payload = {
        "model": "openchat/openchat-3.5",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
    return res.json()['choices'][0]['message']['content']

if "chat" not in st.session_state:
    st.session_state.chat = []

for role, msg in st.session_state.chat:
    st.chat_message(role).markdown(msg)

prompt = st.chat_input("Задай вопрос")

if prompt:
    st.session_state.chat.append(("user", prompt))
    with st.chat_message("assistant"):
        with st.spinner("Ответ..."):
            answer = ask_openrouter(prompt)
            st.session_state.chat.append(("assistant", answer))
            st.markdown(answer)
