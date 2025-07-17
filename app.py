import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

@st.cache_resource(show_spinner=False)
def load_model():
    model_name = "gpt2"  # простая маленькая модель, без токенов
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

def generate_response(tokenizer, model, prompt, chat_history_ids=None):
    input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors='pt')
    if chat_history_ids is not None:
        input_ids = torch.cat([chat_history_ids, input_ids], dim=-1)
    chat_history_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response, chat_history_ids

def main():
    st.title("Простой чат-бот на GPT2 в Streamlit")

    tokenizer, model = load_model()

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None
        st.session_state.past = []
        st.session_state.generated = []

    user_input = st.text_input("Ваш вопрос:", key="input")

    if user_input:
        # Добавляем вопрос пользователя к истории
        prompt = user_input

        # Генерируем ответ
        response, chat_history_ids = generate_response(tokenizer, model, prompt, st.session_state.chat_history)

        st.session_state.chat_history = chat_history_ids
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state.generated:
        for i in range(len(st.session_state.generated)):
            st.markdown(f"**Вы:** {st.session_state.past[i]}")
            st.markdown(f"**Бот:** {st.session_state.generated[i]}")

if __name__ == "__main__":
    main()
