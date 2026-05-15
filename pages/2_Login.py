import streamlit as st
from auth.auth import login_user
from utils.helpers import load_css, render_sidebar

load_css()
render_sidebar()

if st.session_state.get('logged_in'):
    st.success(f"You are already logged in as {st.session_state.get('username')}.")
    st.info("Please navigate to the Dashboard from the sidebar.")
    st.stop()

col1, col2, col3 = st.columns([1, 1.5, 1])

with col2:
    st.title("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username and password:
                success, msg = login_user(username, password)
                if success:
                    st.switch_page("pages/3_Dashboard.py")
                else:
                    st.error(msg)
            else:
                st.error("Please fill in all fields.")

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #475569;'>Don't have an account?</p>", unsafe_allow_html=True)
    if st.button("📝 Create Account", use_container_width=True):
        st.switch_page("pages/1_Register.py")
