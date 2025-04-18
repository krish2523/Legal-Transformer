import streamlit as st
from backend.analy_risk import LegalDocumentProcessor
import os
import tempfile
import time

def show_document_analyzer():
    with open("style/analy_risk.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.title("📄 Advanced Legal Document Analyzer")
    st.subheader("Analyze and assess risks in legal documents")

    # Initialize session state variables
    if "processor" not in st.session_state:
        st.session_state.processor = LegalDocumentProcessor()
    if "uploaded_file_path" not in st.session_state:
        st.session_state.uploaded_file_path = None
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "risk_assessment" not in st.session_state:
        st.session_state.risk_assessment = None
    if "file_name" not in st.session_state:
        st.session_state.file_name = None
    if "detected_language" not in st.session_state:
        st.session_state.detected_language = None

    # Language selector 
    supported_languages = {
        "en": "English",
        "zh": "Chinese (中文)",
        "es": "Spanish (Español)",
        "ar": "Arabic (العربية)",
        "hi": "Hindi (हिन्दी)",
        "fr": "French (Français)",
        "pt": "Portuguese (Português)",
        "ru": "Russian (Русский)",
        "ja": "Japanese (日本語)",
        "de": "German (Deutsch)",
        "bn": "Bengali (বাংলা)" 
    }

    col_lang1, col_lang2 = st.columns([1, 3])
    with col_lang1:
        st.markdown("### Select language:")
    with col_lang2:
        selected_language = st.selectbox(
            "Select output language",
            options=list(supported_languages.keys()),
            format_func=lambda x: supported_languages[x],
            index=0,
            label_visibility="collapsed"
        )

    # File upload section
    with st.container():
        st.markdown("### Upload your Document")
        col1, col2 = st.columns([3, 1])
        with col1:
            uploaded_file = st.file_uploader(
                "Upload your document in PDF format",
                type=["pdf"],
                help="Support for text PDFs and scanned documents (OCR)"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if uploaded_file is not None:
                with st.spinner("Processing document..."):
                        # Save uploaded file to a temporary location
                        temp_dir = tempfile.mkdtemp()
                        temp_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        st.session_state.uploaded_file_path = temp_path
                        st.session_state.file_name = uploaded_file.name
                        st.success(f"'{uploaded_file.name}' processed successfully!")
                
    # Display document info if uploaded
    if st.session_state.uploaded_file_path:
        st.markdown("---")
        st.markdown(f"## Current Document: {st.session_state.file_name}")
        tab1, tab2, tab3 = st.tabs(["📝 Analysis", "⚠️ Risk Assessment", "📋 Export to Text"])  # Updated tab3 icon and label

        with tab1:
            if "analysis_result" not in st.session_state or not st.session_state.analysis_result:
                if st.button("Generate Document Analysis", key="analyze_button"):
                    with st.spinner("Analyzing document... This may take a few moments."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.1)
                            progress_bar.progress(i + 1)
                        try:
                            result = st.session_state.processor.analyze_document(
                                st.session_state.uploaded_file_path,
                                target_language=selected_language
                            )
                            st.session_state.analysis_result = result
                            st.session_state.detected_language = result["source_language"]
                            st.success("Analysis completed!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Analysis failed: {str(e)}")
            else:
                st.markdown("#### Analysis Results")
                if st.session_state.detected_language:
                    st.info(f"Original document language: {st.session_state.detected_language}")
                st.markdown(st.session_state.analysis_result.get("content", ""))
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Regenerate Analysis", key="regenerate_analysis"):
                        st.session_state.analysis_result = None
                        st.rerun()
                with col2:
                    if st.button("Change Output Language", key="change_lang_analysis"):
                        with st.spinner(f"Translating to {supported_languages[selected_language]}..."):
                            try:
                                result = st.session_state.processor.analyze_document(
                                    st.session_state.uploaded_file_path,
                                    target_language=selected_language
                                )
                                st.session_state.analysis_result = result
                                st.success("Translation completed!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Translation failed: {str(e)}")

        with tab2:
            if not st.session_state.analysis_result:
                st.info("⚠️ Please complete the document analysis first")
            elif "risk_assessment" not in st.session_state or not st.session_state.risk_assessment:
                if st.button("Generate Risk Assessment", key="risk_button"):
                    with st.spinner("Assessing risks... This may take a few moments."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.03)
                            progress_bar.progress(i + 1)
                        try:
                            risk_result = st.session_state.processor.assess_risks(
                                st.session_state.uploaded_file_path,
                                st.session_state.analysis_result,
                                target_language=selected_language
                            )
                            st.session_state.risk_assessment = risk_result
                            st.success("Risk assessment completed!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Risk assessment failed: {str(e)}")
            else:
                st.markdown("#### Risk Assessment Results")
                st.markdown(st.session_state.risk_assessment.get("content", ""))
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Regenerate Risk Assessment", key="regenerate_risk"):
                        st.session_state.risk_assessment = None
                        st.rerun()
                with col2:
                    if st.button("Change Output Language", key="change_lang_risk"):
                        with st.spinner(f"Translating to {supported_languages[selected_language]}..."):
                            try:
                                risk_result = st.session_state.processor.assess_risks(
                                    st.session_state.uploaded_file_path,
                                    st.session_state.analysis_result,
                                    target_language=selected_language
                                )
                                st.session_state.risk_assessment = risk_result
                                st.success("Translation completed!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Translation failed: {str(e)}")

        with tab3:
            st.markdown("### Export to Text")
            export_options = ["Document Analysis", "Risk Assessment", "Both"]
            export_selection = st.selectbox("Select content to export:", export_options)

            if st.button("Export"):
                text_content = ""

                # Ensure session state variables exist before accessing them
                analysis_content = st.session_state.get("analysis_result", {}) or {}
                risk_content = st.session_state.get("risk_assessment", {}) or {}

                if export_selection == "Document Analysis":
                    text_content = f"Analysis:\n{analysis_content.get('content', '[Not yet completed]')}"
                elif export_selection == "Risk Assessment":
                    text_content = f"Risk Assessment:\n{risk_content.get('content', '[Not yet completed]')}"
                elif export_selection == "Both":
                    text_content = f"Analysis:\n{analysis_content.get('content', '[Not yet completed]')}\n\nRisk Assessment:\n{risk_content.get('content', '[Not yet completed]')}"

                st.download_button(
                    label="Download",
                    data=text_content,
                    file_name="exported_results.txt",
                    mime="text/plain"
                )



    # Updated Help section
    with st.expander("ℹ️ Help & Information"):
        st.markdown("""
        ### How to use this tool:
        1. **Upload your document** - Supports both standard and scanned PDFs
        2. **Select your preferred language** - View results in any of the 11 supported languages (including Bengali)
        3. **Generate analysis** - Get a detailed breakdown of the document's key components
        4. **Assess risks** - Identify potential legal and compliance risks
        5. **Export to text** - Save your analysis and risk assessment as a text file
        ### OCR Support
        This tool includes Optical Character Recognition (OCR) for scanned documents.
        For best results, ensure your scanned documents are clear and legible.
        ### Language Support
        The tool can detect the original language of your document and provide analysis in your preferred language.
        """)
