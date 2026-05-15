import streamlit as st
import os
import base64
from utils.helpers import render_sidebar, load_css

st.set_page_config(page_title="About the Developer", page_icon="👨‍💻", layout="wide")
load_css()
render_sidebar()

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Image path
img_path = os.path.join("assets", "Profile (1).jpg")
if not os.path.exists(img_path):
    img_path = "developer.png"

img_base64 = ""
if os.path.exists(img_path):
    img_base64 = get_base64_image(img_path)

# Build the complete HTML document for the component (White Theme)
html_doc = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
            background-color: transparent;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .dev-container {{
            background: #ffffff;
            color: #1e293b;
            padding: 60px;
            border-radius: 40px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08), 0 5px 15px rgba(0,0,0,0.04);
            max-width: 600px;
            width: 90%;
            text-align: center;
            border: 1px solid #f1f5f9;
        }}
        .profile-img-wrapper {{
            position: relative;
            width: 200px;
            height: 200px;
            margin: 0 auto 30px;
        }}
        .profile-img-wrapper::after {{
            content: '';
            position: absolute;
            top: -8px;
            left: -8px;
            right: -8px;
            bottom: -8px;
            border-radius: 50%;
            background: linear-gradient(135deg, #6366f1, #38bdf8);
            z-index: -1;
            opacity: 0.2;
            filter: blur(10px);
        }}
        .profile-img {{
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 4px solid #ffffff;
            object-fit: cover;
            background-color: #f8fafc;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .dev-name {{
            font-size: 3rem;
            font-weight: 800;
            margin: 0 0 10px;
            color: #0f172a;
            letter-spacing: -1px;
        }}
        .dev-title {{
            font-size: 1.1rem;
            color: #6366f1;
            margin-bottom: 40px;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-weight: 700;
        }}
        .dev-bio {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #64748b;
            margin-bottom: 40px;
            padding: 30px 0;
            border-top: 1px solid #f1f5f9;
            border-bottom: 1px solid #f1f5f9;
        }}
        .dev-bio b {{ color: #1e293b; }}
        .links {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 40px;
        }}
        .link-btn {{
            padding: 14px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 700;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            color: #475569;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
        }}
        .link-btn:hover {{
            background: #ffffff;
            transform: translateY(-4px);
            border-color: #6366f1;
            color: #6366f1;
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.1);
        }}
        .link-btn img {{ width: 18px; }}
        
        .slogan {{
            font-size: 0.95rem;
            color: #94a3b8;
            font-weight: 500;
            margin: 0;
            letter-spacing: 0.5px;
        }}
    </style>
</head>
<body>
    <div class="dev-container">
        <div class="profile-img-wrapper">
            <img class="profile-img" src="data:image/jpeg;base64,{img_base64}" alt="Bittu Sharma">
        </div>
        
        <h1 class="dev-name">Bittu Sharma</h1>
        <p class="dev-title">AI & MLOps Engineer</p>
        
        <div class="dev-bio">
            I am an <b>AI & MLOps Engineer</b> passionate about building scalable AI Infrastructure, 
            Agentic AI Workflows, and Enterprise-grade MLOps pipelines. 
            I specialize in transforming raw data into intelligent, automated business solutions.
        </div>
        
        <div class="links">
            <a href="https://github.com/bittush8789" target="_blank" class="link-btn github">💻 GITHUB</a>
            <a href="https://www.linkedin.com/in/bittu-kumar-54ab13254/" target="_blank" class="link-btn linkedin">🔗 LINKEDIN</a>
            <a href="https://bittullmops.vercel.app/" target="_blank" class="link-btn portfolio">📂 PORTFOLIO</a>
            <a href="https://bittublog.hashnode.dev/" target="_blank" class="link-btn hashnode">✍️ HASHNODE</a>
        </div>
        
        <p class="slogan">Building the future of Autonomous Data Analytics. 🚀</p>
    </div>
</body>
</html>
"""

# Render as an isolated component
st.components.v1.html(html_doc, height=900, scrolling=False)
