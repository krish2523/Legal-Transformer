import streamlit as st
from frontend.analy_risk_frontend import show_document_analyzer
from frontend.transcriber_frontend import show_transcriber
from frontend.RAG_frontend import show_legal_chatbot
from frontend.ask_chat_front import main
from frontend.contr_gen_frontend import show_legal_document_generator

# Function to load CSS file
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main_app():
    """Main application with improved sidebar UI and radio button navigation."""
    
    # Load the CSS file
    load_css("style/feature.css")  # Ensure this points to your CSS file
    
    # Sidebar layout
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>⚖️ JuriScriptor</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>Your AI Legal Companion</p>", unsafe_allow_html=True)

        st.markdown("---")  # Separator

        # Feature Selection (Radio Button)
        feature = st.radio(
            "Select Feature",
            [
                "📄 Document Analyzer & Risk Detector",
                "🎙️ Legal Proceeding Transcriber & Summarizer",
                "📝 Contract Generator",
                "🤖 RAG Legal Chatbot",
                "💬 Ask Me Anything Chatbot"
                
            ],
            index=0
        )

        st.markdown("---")

        # About Section
        with st.expander("ℹ️ About This Tool"):
            st.markdown(
                "This AI-powered assistant helps legal professionals with document analysis, "
                "transcription, a ChatBot on RAG technology, and an Ask Me Anything feature."
            )

        # Home Button
        def on_back_click():
            st.session_state['page'] = 'landing'

        st.button("🏠 Return to Home", key="back_button", on_click=on_back_click)

        # Footer
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; font-size: 12px; color: gray;'>
                © 2025 Legal AI Assistant | Designed for Legal Excellence
            </div>
            """,
            unsafe_allow_html=True
        )
    
    if feature == "📄 Document Analyzer & Risk Detector":
        show_document_analyzer()
    elif feature == "🎙️ Legal Proceeding Transcriber & Summarizer":
        show_transcriber()
    elif feature == "🤖 RAG Legal Chatbot":
        show_legal_chatbot()
    elif feature == "📝 Contract Generator":
        show_legal_document_generator()
    elif feature == "💬 Ask Me Anything Chatbot":
        main()
