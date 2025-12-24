import streamlit as st
import requests
import json

st.title("🤖 AI Customer Support")
st.caption("Powered by n8n + Ollama")

# Historique des conversations
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "agent" in msg:
            st.caption(f"Agent: {msg['agent']}")

# Input utilisateur
if prompt := st.chat_input("How can we help you today?"):
    # Ajouter message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Appeler le workflow n8n
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:5678/webhook-test/customer",
                    json={
                        "message": prompt,
                        "user_id": st.session_state.get("user_id", "anonymous")
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    reply = data.get("reply", "No response")
                    
                    # Afficher la réponse
                    st.markdown(reply)
                    
                    # Ajouter à l'historique
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": reply,
                        "agent": data.get("agent", "unknown")
                    })
                    
                    # Afficher des métadonnées
                    if data.get("needs_human"):
                        st.warning("⚠️ This case will be escalated to a human agent")
                else:
                    st.error("Error contacting support system")
                    
            except Exception as e:
                st.error(f"Connection error: {e}")