import streamlit as st
from backend.contr_gen_agent import generate_legal_document, download_legal_document
import time

def get_input_fields(doc_type):
    inputs = {}
    if doc_type == "Contracts/Agreements":
        inputs["Parties Involved"] = st.text_input("Names of Parties", key="parties_involved")
        inputs["Contract Purpose"] = st.text_area("Brief Description of Agreement", key="contract_purpose")
        inputs["Key Terms"] = st.text_area("Specific Terms or Conditions", key="key_terms")
    
    elif doc_type == "Wills and Testaments":
        inputs["Testator Name"] = st.text_input("Full Name of Will Creator", key="testator_name")
        inputs["Beneficiaries"] = st.text_area("List of Beneficiaries", key="beneficiaries")
        inputs["Asset Details"] = st.text_area("Assets to be Distributed", key="asset_details")
    
    elif doc_type == "Deeds":
        inputs["Property Description"] = st.text_area("Detailed Property Description", key="property_description")
        inputs["Current Owner"] = st.text_input("Current Property Owner", key="current_owner")
        inputs["New Owner"] = st.text_input("New Property Owner", key="new_owner")
    
    elif doc_type == "Power of Attorney":
        inputs["Principal Name"] = st.text_input("Name of Person Granting Power", key="principal_name")
        inputs["Attorney Name"] = st.text_input("Name of Appointed Attorney", key="attorney_name")
        inputs["Powers Granted"] = st.multiselect(
            "Specific Powers",
            ["Financial Decisions", "Medical Decisions", "Property Management", "Legal Representation"],
            key="powers_granted"
        )
    
    elif doc_type == "Court Orders/Judgments":
        inputs["Case Number"] = st.text_input("Court Case Number", key="case_number")
        inputs["Parties Involved"] = st.text_input("Names of Parties", key="court_parties")
        inputs["Order Type"] = st.selectbox(
            "Type of Order",
            ["Divorce Decree", "Child Custody", "Restraining Order", "Other"],
            key="order_type"
        )
    
    return inputs

def reset_document_state():
    """Function to reset document generation state when document type changes"""
    st.session_state.document_generated = False
    st.session_state.document_text = ""
    st.session_state.is_generating = False
    st.session_state.progress_message = ""

def show_legal_document_generator():
    # Initialize session state variables if they don't exist
    if 'document_generated' not in st.session_state:
        st.session_state.document_generated = False
    if 'document_text' not in st.session_state:
        st.session_state.document_text = ""
    if 'document_type' not in st.session_state:
        st.session_state.document_type = "Contracts/Agreements"
    if 'progress_message' not in st.session_state:
        st.session_state.progress_message = ""
    if 'is_generating' not in st.session_state:
        st.session_state.is_generating = False
    if 'previous_doc_type' not in st.session_state:
        st.session_state.previous_doc_type = st.session_state.document_type
    if 'document_language' not in st.session_state:
        st.session_state.document_language = "English"
    
    st.title("📜 Smart Legal Doc Builder")
    
    # Use session state for document type selection
    document_type = st.selectbox(
        "Select Document Type",
        [
            "Contracts/Agreements",
            "Wills and Testaments",
            "Deeds",
            "Power of Attorney",
            "Court Orders/Judgments"
        ],
        key="document_type",
        on_change=reset_document_state
    )
    
    # Language selector
    document_language = st.selectbox(
        "Select Document Language",
        [
            "English",
            "Spanish",
            "Mandarin Chinese",
            "Hindi"
        ],
        key="document_language",
        on_change=reset_document_state
    )
    
    # Check if document type has changed and reset output
    if st.session_state.previous_doc_type != document_type:
        st.session_state.previous_doc_type = document_type
    
    user_inputs = get_input_fields(document_type)
    user_details = "\n".join([f"{k}: {v}" for k, v in user_inputs.items() if v])
    
    def generate_doc():
        """Callback function for the Generate Document button"""
        st.session_state.is_generating = True
        st.session_state.document_generated = False
    
    generate_button = st.button("Generate Document", on_click=generate_doc, disabled=st.session_state.is_generating)
    
    # Show progress bar when generation is in progress
    if st.session_state.is_generating and user_details:
        # Create a placeholder for the progress bar
        progress_placeholder = st.empty()
        progress_bar = progress_placeholder.progress(0)
        
        # Status message placeholder
        status_message = st.empty()
        
        # Update progress bar to show activity
        for i in range(101):
            # Update progress bar every 1%
            progress_bar.progress(i)
            
            # Update status message based on progress
            if i < 30:
                st.session_state.progress_message = "Researching legal requirements..."
            elif i < 70:
                st.session_state.progress_message = "Drafting document..."
            else:
                st.session_state.progress_message = "Finalizing document..."
                
            # Display the current status message
            status_message.info(st.session_state.progress_message)
            
            # Generate document when progress bar reaches 30%
            if i == 30:
                try:
                    st.session_state.document_text = generate_legal_document(
                        document_type, 
                        user_details,
                        document_language
                    )
                except Exception as e:
                    st.error(f"Error generating document: {e}")
                    st.session_state.is_generating = False
                    break
            
            # Adjust sleep time to match actual generation time
            time.sleep(0.05)
        
        # Clear the progress elements
        progress_placeholder.empty()
        status_message.empty()
        
        # Update session state after completion
        st.session_state.is_generating = False
        st.session_state.document_generated = True
        
        # Force a rerun to refresh the UI
        st.rerun()
    
    # Display the generated document if available
    if st.session_state.document_generated and st.session_state.document_text:
        st.success("Document Generated!")
        st.write("### Generated Document")
        st.write(st.session_state.document_text)
        download_legal_document(st.session_state.document_text, document_type)