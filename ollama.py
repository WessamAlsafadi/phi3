import streamlit as st
import requests
import json

st.set_page_config(page_title="My Agent", page_icon="🔥")
st.title("🔥 My Custom AI Agent (Powered by Ollama)")

# Session state to store the full conversation
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You're a helpful assistant."}]

# Show the conversation
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.spinner("Thinking..."):
        url = "https://q2mdykuo7xnfhy-11434.proxy.runpod.net/api/chat"
        payload = {
            "model": "phi3",
            "messages": st.session_state.messages
        }

        response = requests.post(url, json=payload, stream=True)
        result = ""

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        result += data["message"]["content"]
                        message_placeholder.markdown(result + "▌")
                    except:
                        pass

            message_placeholder.markdown(result)

        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": result})
