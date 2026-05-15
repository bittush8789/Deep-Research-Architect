import streamlit as st
from utils.helpers import check_auth, load_css, render_sidebar
from database.database import SessionLocal
from database.models import Paper

load_css()
check_auth()
render_sidebar()

# Centering container
_, col_mid, _ = st.columns([1, 2, 1])

with col_mid:
    st.markdown("<h1 style='text-align: center;'>Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1.2rem; color: #64748b;'>Welcome back, <b>{st.session_state['username']}</b>!</p>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("<h3 style='text-align: center;'>Your Statistics</h3>", unsafe_allow_html=True)
    db = SessionLocal()
    try:
        papers_count = db.query(Paper).filter(Paper.user_id == st.session_state['user_id']).count()
        # Metric centering is tricky in Streamlit, using a column hack inside the mid column
        m_col1, m_col2, m_col3 = st.columns([1, 1, 1])
        with m_col2:
            st.metric("Total Papers", papers_count)
    finally:
        db.close()
    
    st.divider()
    
    st.markdown("<h3 style='text-align: center;'>Quick Links</h3>", unsafe_allow_html=True)
    q_col1, q_col2 = st.columns(2)
    with q_col1:
        if st.button("🚀 Generate Paper", use_container_width=True):
            st.switch_page("pages/4_Generate_Paper.py")
    with q_col2:
        if st.button("📚 My Papers", use_container_width=True):
            st.switch_page("pages/5_My_Papers.py")
            
    st.divider()
    
    st.markdown("<h3 style='text-align: center; color: #ef4444;'>Danger Zone</h3>", unsafe_allow_html=True)
    st.warning("This will delete all your generated papers and reset any active form data.")
    
    if st.button("🗑️ Clear Papers & Reset Session", use_container_width=True):
        db = SessionLocal()
        try:
            papers_to_delete = db.query(Paper).filter(Paper.user_id == st.session_state['user_id']).all()
            for p in papers_to_delete:
                db.delete(p)
            db.commit()
        finally:
            db.close()
            
        keys_to_keep = ['logged_in', 'user_id', 'username']
        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                del st.session_state[key]
                
        st.success("All papers and temporary session data cleared successfully!")
        st.rerun()
