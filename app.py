import streamlit as st
import requests
from utils import load_all_excels, semantic_search

# ----------------------------------------------
# 👇 СЮДА ВСТАВЬ СВОЙ API-токен Hugging Face
HUGGINGFACE_TOKEN = "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"  # 🔐 ВСТАВЬ СЮДА свой токен Hugging Face
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
# ----------------------------------------------

st.set_page_config(page_title="🤖 Ассистент + Поиск", layout="centered")
st.title("💬 Чат-помощник с умным поиском")

@st.cache_data
def get_data():
    df = load_all_excels()
    from utils import get_model
    model = get_model()
    df.attrs['phrase_embs'] = model.encode(df['phrase_proc'].tolist(), convert_to_tensor=True)
    return df

@st.cache_resource
def query_llm(prompt):
    payload = {"inputs": prompt}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()[0]["generated_text"]
    except Exception as e:
        return f"⚠️ Ошибка при обращении к модели: {e}"

df = get_data()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Показать историю
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_prompt = st.chat_input("Введите ваш вопрос или фразу...")

if user_prompt:
    # Отображаем ввод
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Ответ бота
    with st.chat_message("assistant"):
        with st.spinner("Генерация ответа..."):
            reply = query_llm(user_prompt)
            st.markdown(f"**GPT-бот:** {reply}")
            st.session_state.messages.append({"role": "assistant", "content": f"GPT-бот: {reply}"})

        # Поиск похожих фраз
        with st.spinner("Поиск релевантных фраз..."):
            results = semantic_search(user_prompt, df)
            if results:
                st.markdown("### 🔍 Похожие фразы из базы:")
                for score, phrase_full, topics, comment in results:
                    st.markdown(
                        f"""
                        <div style="border:1px solid #ddd; border-radius:10px; padding:10px; margin:10px 0; background:#f9f9f9;">
                        <strong>{phrase_full}</strong><br>
                        🔖 <i>{", ".join(topics)}</i><br>
                        🎯 Релевантность: {score:.2f}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("Совпадений в базе не найдено.")
