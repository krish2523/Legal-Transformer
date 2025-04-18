import streamlit as st
import os

def set_page_config():
    st.set_page_config(
        page_title="LegalEase",
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
    css_path = "style\landing.css"  # Adjust path as needed
    
    if not os.path.exists(css_path):
        st.warning(f"CSS file not found at {css_path}. Please create it or adjust the path.")
    else:
        load_css(css_path)

    # Header banner with centered content
    st.markdown(
        """
        <div class="header-banner">
            <div class="header-content">
                <h1 class="landing-title" style="margin-left: 40px;">LegalEase ⚖️</h1>
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

    # Feature section title
    st.markdown(
        """
        <h2 class="section-title">How We Empower Legal Professionals</h2>
        """,
        unsafe_allow_html=True
    )

    # Feature Highlights with three columns
    st.markdown('<div class="feature-section">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <h3>Intelligent Document Analysis</h3>
                <p>Precisely evaluate legal documents to highlight potential liabilities, compliance issues, and strategic advantages with our advanced risk assessment technology.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎙️</div>
                <h3>Legal Transcript</h3>
                <p>Transform legal audio recordings into precise, annotated transcripts with advanced speaker recognition and legal terminology expertise built in.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3>RAG Technology Legal Chatbot</h3>
                <p>Query anything from your documents with minimal latency, highly tuned to answer exclusively from your uploaded materials and established legal matters.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # New centered "Ask Me Anything Chatbot" card
    st.markdown(
        """
        <div class="feature-section" style="display: flex; justify-content: center;">
            <div class="feature-card" style="max-width: 400px;">
                <div class="feature-icon">💬</div>
                <h3>Ask Me Anything Chatbot</h3>
                <p>Ask any legal question and get quick, reliable answers powered by advanced AI, tailored to your needs.</p>
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
                <li><strong>Instant Document Risk Assessment</strong> - Automatically flag potential liabilities, non-compliance issues, and ambiguous clauses in contracts and legal documents</li>
                <li><strong>Multilingual Legal Analysis</strong> - Review documents in 11 languages with accurate legal terminology preservation</li>
                <li><strong>Court-Ready Transcripts</strong> - Convert audio recordings into properly formatted legal transcripts with speaker identification and multi-language summarization in minutes.</li>
                <li><strong>Precision Legal Research</strong> - Get answers from your case documents instantly with our RAG-powered chatbot that cites exact sources</li>
                <li><strong>Standardized Workflows</strong> - Consistent document analysis quality across your entire legal team</li>
                <li><strong>Ask Me Anything Legal Chatbot</strong> - Get immediate answers to general legal questions with web-search capabilities to get latest information</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Call to Action with callback
    def on_start_click():
        st.session_state['page'] = 'main'

    # Centered CTA button using columns for explicit centering
    st.markdown('<div class="cta-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])  # Middle column wider for button
    with col2:  # Place button in the middle column
        st.button(
            "Explore our Prototype",
            key="start_button",
            help="Begin using Legal AI Assistant",
            on_click=on_start_click,
            args=None,
            kwargs=None,
            type="primary"  # Use Streamlit's primary button style as a base
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