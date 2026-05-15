import streamlit as st
from auth.auth import register_user
from utils.helpers import load_css, render_sidebar

load_css()
render_sidebar()

col1, col2, col3 = st.columns([1, 1.5, 1])

with col2:
    st.title("Register")
    
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")
        
        if submit:
            if username and email and password:
                success, msg = register_user(username, email, password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.error("Please fill in all fields.")

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #475569;'>Already have an account?</p>", unsafe_allow_html=True)
    if st.button("🔑 Go to Login", use_container_width=True):
        st.switch_page("pages/2_Login.py")
