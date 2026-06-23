import streamlit as st
from huggingface_hub import InferenceClient

# ================================
# 🤖 AI CHATBOT
# ================================

st.title("🤖 My AI Chatbot")
st.markdown("Ask me anything!")

# ================================
# 🔑 Hugging Face Token
# ================================
API_TOKEN = "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"

client = InferenceClient(token=API_TOKEN)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
user_input = st.chat_input("Type your question...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=st.session_state.messages,
            max_tokens=500,
        )

        ai_reply = response.choices[0].message.content

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_reply}
        )

        with st.chat_message("assistant"):
            st.write(ai_reply)

    except Exception as e:
        st.error(f"❌ Error: {e}")

# ================================
# 💾 Save Chat
# ================================
if st.button("💾 Save Chat to File"):
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        for msg in st.session_state.messages:
            f.write(f"{msg['role']}: {msg['content']}\n")

    st.success("✅ Chat saved to chat_history.txt!")