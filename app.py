import streamlit as st
from utils import load_all_excels, semantic_search, keyword_search

st.set_page_config(page_title="ФЛ Чат-бот", layout="centered")
st.title("🤖 Чат-бот помощник по фразам")

@st.cache_data
def get_data():
    df = load_all_excels()
    from utils import get_model
    model = get_model()
    df.attrs['phrase_embs'] = model.encode(df['phrase_proc'].tolist(), convert_to_tensor=True)
    return df

df = get_data()

# Инициализация истории чата
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Введи фразу, и я подскажу, к каким тематикам она может относиться."}
    ]

# Вывод истории чата
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ввод пользователя
query = st.chat_input("Напиши фразу для анализа...")

if query:
    # Сохраняем сообщение пользователя
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    try:
        semantic_results = semantic_search(query, df)
        keyword_results = keyword_search(query, df)

        response = ""

        if semantic_results:
            response += "### 🔍 Умный поиск:\n"
            for score, phrase_full, topics, comment in semantic_results:
                response += f"- 🧠 **{phrase_full}** (релевантность: {score:.2f})\n"
                response += f"  🔖 Темы: `{', '.join(topics)}`\n"
                if comment and str(comment).strip().lower() != "nan":
                    response += f"  💬 Комментарий: {comment.strip()}\n"
        else:
            response += "🤔 Ничего не найдено в умном поиске.\n"

        if keyword_results:
            response += "\n### 🧷 Точный поиск:\n"
            for phrase, topics, comment in keyword_results:
                response += f"- 📌 **{phrase}**\n"
                response += f"  🔖 Темы: `{', '.join(topics)}`\n"
                if comment and str(comment).strip().lower() != "nan":
                    response += f"  💬 Комментарий: {comment.strip()}\n"
        else:
            response += "\n🧐 Ничего не найдено в точном поиске."

    except Exception as e:
        response = f"⚠️ Ошибка при обработке запроса: {e}"

    # Сохраняем ответ бота
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
