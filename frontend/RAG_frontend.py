import streamlit as st
from backend.RAG_chatbot import (
    upload_pdf, 
    retrieve_docs, 
    answer_query, 
    process_pdf
)
import time

def show_legal_chatbot():
    # Streamlit UI
    st.title("🤖 RAG based AI Legal Chatbot")
    st.write("Chat with an AI-powered legal assistant!")

    # Initialize session state variables
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "current_file" not in st.session_state:
        st.session_state.current_file = None
    
    # Document upload section with clear conversation button
    st.markdown("#### Upload Document")
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload PDF", type="pdf", accept_multiple_files=False, key="pdf_uploader")
    with col2:
        if st.button("🧹 Clear Conversation"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Process the uploaded file immediately if it's new
    if uploaded_file:
        if st.session_state.current_file != uploaded_file.name:
            # Create a progress bar
            progress_bar = st.progress(0)
            st.text(f"Processing {uploaded_file.name}...")
            
            # Save the file and get the path
            pdf_path = upload_pdf(uploaded_file)
            progress_bar.progress(25)
            time.sleep(0.1)  # Small delay for visual feedback
            
            # Process the PDF and create vector store
            st.session_state.vector_store = process_pdf(pdf_path)
            progress_bar.progress(90)
            time.sleep(0.1)  # Small delay for visual feedback
            
            # Reset chat history and set current file
            st.session_state.chat_history = []
            st.session_state.current_file = uploaded_file.name
            
            # Complete progress bar
            progress_bar.progress(100)
            
            # Success message
            st.success(f"✅ {uploaded_file.name} has been processed successfully!")
    
    # Display chat messages from history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    user_query = st.chat_input("Ask your legal question...")

    if user_query:
        # Check if vector store exists
        if st.session_state.vector_store:
            # Display user query
            with st.chat_message("user"):
                st.write(user_query)
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            # Retrieve relevant documents with optimized similarity search
            retrieved_docs = retrieve_docs(st.session_state.vector_store, user_query)
            
            # Get the chat history from session state
            chat_history = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in st.session_state.chat_history
            ])
            
            # Stream the response
            with st.chat_message("AI Lawyer", avatar="👨‍⚖️"):  # Added emoji for AI responses
                response_placeholder = st.empty()
                full_response = ""
                for chunk in answer_query(documents=retrieved_docs, query=user_query, chat_history=chat_history):
                    full_response += chunk
                    response_placeholder.markdown(full_response)
                    time.sleep(0.005)  # Slightly faster streaming
                
                # Update chat history with the full response
                st.session_state.chat_history.append({"role": "AI Lawyer", "content": full_response})
        else:
            st.error("Please upload a PDF before asking questions!")