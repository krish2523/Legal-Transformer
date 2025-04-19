import streamlit as st
import os

def set_page_config():
    st.set_page_config(
        page_title="Legal-Transformer",
        page_icon="⚖️", 
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_css(css_file):
    """Load CSS styles from a file."""
    with open(css_file, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def show_landing_page():
    """Display the enhanced landing page."""
    # Load custom CSS
    css_path = "style\\landing.css"  # Adjust path as needed

    if not os.path.exists(css_path):
        st.warning(f"CSS file not found at {css_path}. Please create it or adjust the path.")
    else:
        load_css(css_path)

    # Header banner
    st.markdown(
        """
        <div class="header-banner">
            <div class="header-content">
                <h1 class="landing-title" style="margin-left: 40px;">Legal-Transformer ⚖️</h1>
                <p class="landing-subtitle" style="margin-left: -40px;">Transforming legal workflows with artificial intelligence</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Intro text
    st.markdown(
        """
        <div class="intro-text">
            Streamline your legal practice with our AI-powered suite of tools designed specifically for legal professionals. 
            Save hours on routine tasks, reduce errors, and focus on what truly matters: providing excellent legal counsel to your clients.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Section title
    st.markdown(
        """
        <h2 class="section-title">How We Empower Legal Professionals</h2>
        """,
        unsafe_allow_html=True
    )

    # Feature Highlights with 3 cards
    st.markdown('<div class="feature-section">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <h3>Document Analysis and Risk Assessment</h3>
                <p>Automatically flag liabilities, non-compliance issues, and ambiguous clauses using advanced document analysis tailored for legal professionals.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎙️</div>
                <h3>AI-Powered Legal Transcript</h3>
                <p>Convert legal recordings into court-ready transcripts with multilingual support and speaker identification—fast, reliable, and accurate.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3>Secure RAG Chatbot</h3>
                <p>Ask questions based on your documents with zero data leakage. Our on-device RAG chatbot ensures contextual replies while protecting privacy.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Ask Me Anything + Contract Generator cards side by side
    st.markdown(
        """
        <div class="feature-section" style="display: flex; justify-content: center; gap: 40px;">
            <div class="feature-card" style="max-width: 400px;">
                <div class="feature-icon">💬</div>
                <h3>Ask Me Anything Chatbot</h3>
                <p>Engage in natural conversations on legal topics. It remembers past queries, allowing context-aware follow-ups—like your personal legal associate.</p>
            </div>
            <div class="feature-card" style="max-width: 400px;">
                <div class="feature-icon">📝</div>
                <h3>AI Contract Generator</h3>
                <p>Create compliant, ready-to-sign contracts in minutes using agentic AI. Supports four major languages—English, Hindi, Spanish, and Mandarin.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Productivity section
    st.markdown(
        """
        <div class="productivity-banner">
            <h2 class="productivity-title">Boost Your Productivity</h2>
            <p class="productivity-text">Leverage the power of top LLMs to transform your legal practice. Our AI assistant combines state-of-the-art language models with legal expertise to deliver unprecedented efficiency and accuracy in your daily workflows.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Benefits section
    st.markdown(
        """
        <h2 class="section-title">Benefits</h2>
        <div class="intro-text" style="margin-top:0">   
            <ul class="benefits-list">
                <li><strong>Instant Document Risk Assessment</strong> – Automatically flag potential liabilities, non-compliance issues, and ambiguous clauses in contracts and legal documents.</li>
                <li><strong>Multilingual Legal Analysis</strong> – Review documents in 11 languages with accurate legal terminology preservation.</li>
                <li><strong>Court-Ready Transcripts</strong> – Convert audio recordings into properly formatted transcripts with speaker and multi-language summarization in minutes.</li>
                <li><strong>Secure Legal Intelligence Chatbot</strong> – Instantly retrieve answers from your private legal documents using on-device Retrieval-Augmented Generation (RAG). Your data stays local—no document is ever transmitted to external servers and guess what? the chatbot has the context-aware discussions capabilities.</li>
                <li><strong>Ask Me Anything Legal Chatbot</strong> – Get immediate answers to general legal questions in a natural, conversational style. The chatbot remembers your previous queries, enabling context-aware discussions and follow-ups—just like speaking to a legal associate who never forgets.</li>
                <li><strong>AI Contract Generation (India Compliant)</strong> – Draft highly tailored, legally sound contracts in minutes using an <em>Agentic AI approach</em>. It ensures the inclusion of the latest clauses, regulatory requirements, and compliance mandates specific to the Indian legal ecosystem. Contracts can be generated in four major global languages—English, Hindi, Spanish, and Mandarin—enabling cross-border legal collaboration without barriers.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # CTA button
    def on_start_click():
        st.session_state['page'] = 'main'

    st.markdown('<div class="cta-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button(
            "Explore our Prototype",
            key="start_button",
            help="Begin using Legal AI Assistant",
            on_click=on_start_click,
            type="primary"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown(
        """
        <div class="footer">
            © 2025 Legal AI Assistant | Empowering legal professionals with cutting-edge AI technology
        </div>
        """,
        unsafe_allow_html=True
    )
