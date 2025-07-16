import streamlit as st
import requests

st.title("Простой бесплатный чат-бот на HF Spaces")

API_URL = "https://hf.space/embed/multimodalart/ChatGPT/api/predict/"  # пример публичного API (можно поменять)

def ask_hf(prompt):
    payload = {"data": [prompt]}
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        result = response.json()
        # В разных Spaces формат может отличаться, здесь берем первый ответ
        if "data" in result and len(result["data"]) > 0:
            return result["data"][0]
        else:
            return "Ошибка: ответ в неожиданном формате."
    else:
        return f"Ошибка API: {response.status_code} - {response.text}"

chat_history = []

user_input = st.text_input("Введите сообщение:")

if user_input:
    chat_history.append(f"Вы: {user_input}")
    answer = ask_hf(user_input)
    chat_history.append(f"Бот: {answer}")

for msg in chat_history:
    st.write(msg)
