import streamlit as st
import os
import base64
import re

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def check_auth():
    if not st.session_state.get('logged_in', False):
        st.warning("Please login to access this page.")
        st.stop()

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

def render_sidebar():
    # System Owner Badge
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    owner_img_path = os.path.join(current_dir, "assets", "1234567.jpg")
    
    if os.path.exists(owner_img_path):
        img_base64 = get_base64_image(owner_img_path)
        st.sidebar.markdown(f"""
        <div style='text-align: center; padding: 20px 0 30px 0;'>
            <div style='
                width: 130px; 
                height: 130px; 
                border-radius: 50%; 
                border: 4px solid #0f172a; 
                margin: 0 auto 12px; 
                overflow: hidden;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            '>
                <img src='data:image/jpeg;base64,{img_base64}' style='width: 100%; height: 100%; object-fit: cover;'>
            </div>
            <p style='
                color: #0f172a; 
                font-weight: 800; 
                font-size: 0.9rem; 
                letter-spacing: 1px; 
                margin: 0;
            '>SYSTEM OWNER</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.divider()
    
    # Logo
    logo_path = os.path.join(current_dir, "assets", "logo.png")
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)
        
    st.sidebar.divider()
    
    # Navigation Info
    st.sidebar.markdown("### 👨‍💻 Platform Info")
    
    if st.sidebar.button("👨‍💻 About the Developer", use_container_width=True):
        st.switch_page("pages/6_Developer.py")
        
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 AI Research Paper Generator")

def render_rich_markdown(content):
    """
    Renders markdown and detects Mermaid diagrams to render them properly.
    """
    # Split content by mermaid code blocks
    parts = re.split(r'```mermaid\n(.*?)\n```', content, flags=re.DOTALL)
    
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # Regular markdown
            if part.strip():
                st.markdown(part)
        else:
            # Mermaid diagram
            render_mermaid(part)

def render_mermaid(code):
    """
    Uses Mermaid.js CDN to render diagrams in Streamlit.
    """
    html = f"""
    <div class="mermaid" style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        {code}
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
        }});
    </script>
    """
    st.components.v1.html(html, height=500, scrolling=True)
