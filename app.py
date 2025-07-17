import streamlit as st
import gradio as gr
from utils import load_all_excels, semantic_search  # твой utils.py должен быть рядом
import requests

# Загружаем данные один раз при старте
try:
    df = load_all_excels()
except Exception as e:
    print(f"Ошибка загрузки данных: {e}")
    df = None

# Функция обращения к бесплатной онлайн модели Hugging Face без токена (пример с Falcon 7B - публичный)
def query_llm_online(prompt):
    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    # Можно менять на любую другую публичную модель из Hugging Face (без токена)
    
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True, "use_cache": False}
    }
    headers = {
        "Accept": "application/json",
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code != 200:
        return f"Ошибка от модели: {response.status_code}"
    
    try:
        result = response.json()
        # Обычно результат: list с одним элементом dict с ключом generated_text
        return result[0]["generated_text"]
    except Exception as e:
        return f"Ошибка обработки ответа модели: {e}"

# Функция для обработки вопроса пользователя и формирование ответа с контекстом
def chatbot(user_message, chat_history):
    if df is None:
        return "Данные не загружены, бот не может отвечать.", chat_history
    
    # Ищем подходящие фразы из твоей базы по смыслу
    search_results = semantic_search(user_message, df, top_k=3, threshold=0.5)
    
    # Формируем контекст из найденных фраз (можно брать топ 3)
    context = "\n".join([f"- {res[1]} (темы: {res[2]})" for res in search_results])
    
    # Текст запроса для LLM включает вопрос и найденные фразы (контекст)
    prompt = f"Вот контекст из базы знаний:\n{context}\n\nОтветь на вопрос пользователя:\n{user_message}"
    
    # Запрос к онлайн-модели
    answer = query_llm_online(prompt)
    
    # Добавляем в историю и возвращаем обновленную
    chat
