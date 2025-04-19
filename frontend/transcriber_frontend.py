import streamlit as st
import os
from backend.transcription_agent import summarize_meeting, transcribe_audio

def load_css():
    """Loads external CSS for styling."""
    try:
        with open("style/whisper.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Style file not found. Ensure 'whisper.css' exists in the 'style' folder.")

def initialize_session_state():
    """Initializes session state variables."""
    for key in ["file_path", "transcript", "summary", "file_saved", "summarization_done"]:
        if key not in st.session_state:
            st.session_state[key] = None if key != "file_saved" and key != "summarization_done" else False

def upload_audio():
    """Handles file upload and saving."""
    uploaded_audio = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"], help="Supported formats: MP3, WAV, OGG")
    if uploaded_audio:
        audio_dir = "audio"
        os.makedirs(audio_dir, exist_ok=True)
        file_path = os.path.join(audio_dir, uploaded_audio.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_audio.getbuffer())
        st.session_state.file_path = file_path
        st.session_state.file_saved = True
        st.success(f"File saved successfully at {file_path}")

def perform_summarization(selected_language):
    """Handles transcription and summarization of audio."""
    if not st.session_state.get("file_saved", False):
        st.warning("⚠️ Please upload an audio file first.")
        return
    
    with st.spinner(f"Processing audio and preparing summary in {selected_language}..."):
        try:
            transcript = transcribe_audio(st.session_state.file_path)
            st.session_state.transcript = transcript
            
            with st.expander("View Transcript"):
                st.text(transcript)
            
            st.write(f"### Summary in {selected_language}:")
            summary_stream = summarize_meeting(st.session_state.file_path, selected_language)
            summary_placeholder = st.empty()
            
            full_summary = []
            for chunk in summary_stream:
                full_summary.append(chunk)
                summary_placeholder.markdown("".join(full_summary))
            
            st.session_state.summary = "".join(full_summary)
            st.session_state.summarization_done = True
            st.success("Summarization completed!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def download_section():
    """Handles transcript and summary downloads."""
    if st.session_state.get("summarization_done", False):
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download Transcript",
                data=st.session_state.transcript,
                file_name="transcript.txt",
                mime="text/plain"
            )
        with col2:
            st.download_button(
                label="Download Summary",
                data=st.session_state.summary,
                file_name="summary.txt",
                mime="text/plain"
            )
    else:
        st.info("Complete summarization in the first tab to enable downloads.")

def show_transcriber():
    """Main function to display the transcriber interface."""
    load_css()
    st.title("🎙️ Legal-Whisper")
    initialize_session_state()
    
    languages = ["English", "Mandarin Chinese", "Hindi", "Spanish", "French", "Arabic", "Bengali", "Portuguese", "Russian", "Japanese"]
    
    tab1, tab2 = st.tabs(["Summarization", "Downloads"])
    
    with tab1:
        selected_language = st.selectbox("Select output language", languages, index=0, help="Choose the language for your summary")
        upload_audio()
        if st.button("Perform Summarization"):
            perform_summarization(selected_language)
    
    with tab2:
        st.subheader("Download Files")
        download_section()

