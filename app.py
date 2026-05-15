import streamlit as st
from utils.helpers import init_session_state, load_css, render_sidebar
from database.database import engine, Base
import database.models  # Import models so Base knows about them before create_all
from dotenv import load_dotenv
import os

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

st.set_page_config(page_title="AI Research Paper Generator", page_icon="🔬", layout="wide")
load_css()

init_session_state()
render_sidebar()

# Layout with 3 columns (adjusted to center the main content better)
col1, col2, col3 = st.columns([0.5, 3, 0.5])

with col2:
    # Logo and Title
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.image(logo_path, width=150)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 0;'>AI Research Paper Generator 🔬</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #64748b; margin-bottom: 2rem;'>Write, outline, and export complete academic research papers across any domain or industry in minutes.</p>", unsafe_allow_html=True)
    
    st.info("✨ **Features:**\n\n- Generate full papers with structured academic formatting\n- Target specific fields (Medical, Tech, Humanities, Business)\n- Export to beautifully formatted PDFs automatically")
    
    st.write("") # Add spacing
    
    if st.session_state.get('logged_in'):
        st.markdown(f"<h3 style='text-align: center;'>Welcome back, <b>{st.session_state.get('username')}</b>!</h3>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 Go to Dashboard", use_container_width=True):
                st.switch_page("pages/3_Dashboard.py")
        with c2:
            from auth.auth import logout_user
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
                st.rerun()
    else:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔑 Login", use_container_width=True):
                st.switch_page("pages/2_Login.py")
        with c2:
            if st.button("📝 Register", use_container_width=True):
                st.switch_page("pages/1_Register.py")
