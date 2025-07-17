import streamlit as st
import requests

# Хранилище истории
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Ты полезный AI-ассистент. Отвечай четко и дружелюбно."}
    ]

# Отображаем историю сообщений
st.title("💬 Онлайн GPT-бот без токенов")

for msg in st.session_state.messages[1:]:  # не показываем system
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ввод пользователя
prompt = st.chat_input("Напиши что-нибудь...")

# === ФУНКЦИЯ ЗАПРОСА К ОНЛАЙН LLM ===
def ask_online_llm(messages):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": messages,
            "max_tokens": 300,
        },
    )

    if response.status_code != 200:
        return f"⚠️ Ошибка: {response.status_code}"

    return response.json()["choices"][0]["message"]["content"]

# === Обработка нового сообщения ===
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Пишу ответ..."):
            reply = ask_online_llm(st.session_state.messages)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
