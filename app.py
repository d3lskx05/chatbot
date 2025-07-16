import streamlit as st
from utils import load_all_excels, semantic_search  # импортируем из твоего utils.py
import functools

@functools.lru_cache(maxsize=1)
def load_data():
    st.info("Загружаем и обрабатываем данные (может занять время)...")
    df = load_all_excels()
    st.success("Данные загружены!")
    return df

def main():
    st.title("Чат-бот с семантическим поиском")

    df = load_data()

    user_input = st.text_input("Введите вопрос:")

    if user_input:
        with st.spinner("Ищем ответы..."):
            results = semantic_search(user_input, df, top_k=5, threshold=0.5)
        
        if results:
            st.markdown("### Результаты поиска:")
            for score, phrase, topics, comment in results:
                st.write(f"**Фраза:** {phrase}")
                st.write(f"**Темы:** {topics}")
                if comment:
                    st.write(f"**Комментарий:** {comment}")
                st.write(f"**Похожесть:** {score:.3f}")
                st.write("---")
        else:
            st.warning("Ничего не найдено по вашему запросу.")

if __name__ == "__main__":
    main()
