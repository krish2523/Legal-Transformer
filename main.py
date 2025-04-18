import streamlit as st
import warnings

# Import landing first
from frontend.landing_page import set_page_config, show_landing_page
# Then import feature_page
# from frontend.feature_page import main_app
warnings.filterwarnings("ignore", category=UserWarning)


def main():
    set_page_config()
    if 'page' not in st.session_state:
        st.session_state['page'] = 'landing'
    
    if st.session_state['page'] == 'landing':
        show_landing_page()
    # else:
        # main_app()

if __name__ == "__main__":
    main()