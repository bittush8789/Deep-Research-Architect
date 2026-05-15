# 🔬 Aristotle AI: Universal Research Paper Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Groq AI](https://img.shields.io/badge/AI-Groq%20Llama--3-orange.svg)](https://groq.com/)

**Aristotle AI** is an industry-grade, domain-agnostic research paper generation platform. It leverages advanced Generative AI to author professional, high-fidelity academic papers across any field, including Engineering (IEEE), Science (MIT/IIT), Medicine, Law, and Business.

---

## 🌟 Core Capabilities

- **Institutional Publication Engines**: Dedicated workflows for IEEE, MIT, IIT, and Oxford publication standards.
- **Deep Technical Reasoning**: Generates detailed mathematical derivations, numerical examples, and case studies.
- **Visual Intelligence**: Automatically generates and renders **Mermaid.js** architecture diagrams and flowcharts.
- **Multimodal Context**: Support for image and audio uploads to guide research focus.
- **Section-by-Section Control**: Fine-grained manual generation mode for expert researchers.
- **Premium PDF Export**: Instantly compile research into perfectly formatted PDF documents.
- **Secure Infrastructure**: Encrypted authentication and persistent SQLite storage.

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Premium customized White Theme)
- **AI Orchestration**: LangChain & Groq (Llama-3.3-70B)
- **Data Engine**: SQLAlchemy & SQLite
- **Security**: Bcrypt Password Encryption
- **Graphics**: Mermaid.js (Real-time diagram rendering)
- **Exports**: ReportLab PDF Engine

---

## 🚀 Getting Started

### 1. Repository Setup
```bash
git clone https://github.com/bittush8789/aristotle-ai.git
cd aristotle-ai
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_actual_groq_api_key
```

### 3. Dependency Installation
```bash
pip install -r requirements.txt
```

### 4. Launch Platform
```bash
streamlit run app.py
```

---

## 📂 Architecture Overview

```text
ai-book-generator/
├── app.py                      # Hero Landing Page
├── auth/                       # Security & Encryption
├── chains/                     # AI Pipeline Logic
├── database/                   # Persistent Schema
├── exports/                    # PDF Processing Engine
├── pages/                      # Platform Sub-systems
│   ├── 1_Register.py           # User Onboarding
│   ├── 2_Login.py              # Identity Access
│   ├── 3_Dashboard.py          # User Analytics
│   ├── 4_Generate_Paper.py     # Core Generation Engine
│   ├── 5_My_Papers.py          # Document Repository
│   └── 6_Developer.py          # Developer Portfolio
├── prompts/                    # Advanced Academic Prompts
├── utils/                      # UI Helpers & Custom CSS
└── assets/                     # Professional Branding
```

---

## 🔒 Production & Security

This application is pre-hardened for production environments:
- **Zero Leakage**: All Streamlit headers, toolbars, and "Share" menus are restricted.
- **Connection Safety**: Automatic database session pooling and cleanup.
- **UI Integrity**: Global CSS overrides prevent theme flickering and ensure high contrast.

---

## 👨‍💻 Developed By

**Bittu Sharma**  
*AI & MLOps Specialist*

- 🌐 [Portfolio](https://bittullmops.vercel.app/)
- 💼 [LinkedIn](https://www.linkedin.com/in/bittu-kumar-54ab13254/)
- 🐙 [GitHub](https://github.com/bittush8789)
- ✍️ [Blog](https://bittublog.hashnode.dev/)

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

*Empowering the global research community through Intelligent Automation.*
