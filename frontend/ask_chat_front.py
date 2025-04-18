import streamlit as st
from backend.ask_chatbot import get_legal_response
import time

# UI Components
def initialize_session():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I assist you with legal cases today?"}
        ]


def load_css():
    with open("style\AMA_chatbot.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    if user_input := st.chat_input("Type your legal query here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get and display response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            for chunk in get_legal_response(user_input):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
                time.sleep(0.005)
            
            # Remove the typing indicator
            response_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})


def main():
    st.markdown(
        """
        <style>
            .centered {
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
            .title {
                font-size: 2.5rem !important;
                margin-bottom: 0.5rem !important;
            }
            .subtitle {
                font-size: 1.2rem !important;
                margin-bottom: 2rem !important;
                color: #7fb3d5 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<h1 class="centered title">⚖️ AMA Legal Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="centered subtitle">Ask me anything about legal cases, statutes, or precedents!</p>', unsafe_allow_html=True)
    load_css()
    initialize_session()
    display_chat_history()
    handle_user_input()
