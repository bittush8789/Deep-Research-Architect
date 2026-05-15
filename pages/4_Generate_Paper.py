import streamlit as st
import os
import uuid
from utils.helpers import check_auth, load_css, render_sidebar
from chains.book_generator import get_llm, generate_title_and_subtitle, generate_outline, generate_chapter, generate_summary, generate_one_click_paper_full
from database.database import SessionLocal
from database.models import Paper, Section

# Optional audio recording component
try:
    from streamlit_webrtc import webrtc_streamer
except ImportError:
    webrtc_streamer = None

load_css()
check_auth()
render_sidebar()

# Centering Title
st.markdown("<h1 style='text-align: center;'>Generate a New Research Paper</h1>", unsafe_allow_html=True)

def render_one_click_form(key_prefix, institution_name, description):
    st.markdown(f"<div style='background: white; padding: 2rem; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{institution_name} Publication Engine</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #64748b;'>{description}</p>", unsafe_allow_html=True)
    
    topic = st.text_area("Research Topic", height=100, placeholder="Enter your research topic...", key=f"{key_prefix}_topic")
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded_image = st.file_uploader("Upload Image (Optional)", type=["png","jpg","jpeg"], key=f"{key_prefix}_img")
    with col2:
        uploaded_audio = st.file_uploader("Upload Audio (Optional)", type=["wav","mp3","m4a"], key=f"{key_prefix}_aud")
    
    # Model selection for one-click too
    model_name = st.selectbox("LLM Model", ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "llama3-70b-8192"], key=f"{key_prefix}_model")
    
    if st.button(f"Generate {institution_name} Paper ⚡", use_container_width=True, key=f"{key_prefix}_btn"):
        if not topic:
            st.error("Please enter a research topic.")
        else:
            extra = handle_uploads(uploaded_image, uploaded_audio)
            generate_one_click_paper(topic + extra, institution_name, model_name)
    st.markdown("</div>", unsafe_allow_html=True)

def generate_one_click_paper(topic, domain_style, model_name="llama-3.3-70b-versatile"):
    try:
        llm = get_llm(model_name)
    except Exception as e:
        st.error(f"Error initializing LLM: {str(e)}. Check your API keys in .env")
        return

    progress_placeholder = st.empty()
    with progress_placeholder.container():
        st.info(f"🚀 Initiating {domain_style} Academic Pipeline...")
        st.spinner(f"Generating full {domain_style} Research Paper... This may take 1-3 minutes.")
        
        try:
            full_paper_content = generate_one_click_paper_full(llm, topic, domain_style)
            
            db = SessionLocal()
            try:
                short_title = topic[:40] + "..." if len(topic) > 40 else topic
                
                paper = Paper(
                    user_id=st.session_state['user_id'],
                    title=f"{domain_style} Paper: {short_title}",
                    subtitle=f"Generated via One-Click {domain_style} Tool",
                    genre=f"{domain_style} Publication",
                    tone="Academic & Professional"
                )
                db.add(paper)
                db.commit()
                db.refresh(paper)
                
                db_section = Section(
                    paper_id=paper.id,
                    section_number=1,
                    section_title="Full Research Paper",
                    content=full_paper_content,
                    summary="Full monolithic paper."
                )
                db.add(db_section)
                db.commit()
            finally:
                db.close()
            
            progress_placeholder.empty()
            st.success(f"✅ Successfully generated your {domain_style} Research Paper!")
            
            with st.expander("Preview Generated Paper", expanded=True):
                from utils.helpers import render_rich_markdown
                render_rich_markdown(full_paper_content)
                
        except Exception as e:
            progress_placeholder.empty()
            st.error(f"❌ An error occurred during generation: {str(e)}")

def handle_uploads(img, aud):
    extra = ""
    if img:
        img_path = os.path.join("uploads", f"{uuid.uuid4()}_{img.name}")
        os.makedirs("uploads", exist_ok=True)
        with open(img_path, "wb") as f:
            f.write(img.getbuffer())
        extra += f"\n[Image: {os.path.basename(img_path)}]"
    if aud:
        aud_path = os.path.join("uploads", f"{uuid.uuid4()}_{aud.name}")
        os.makedirs("uploads", exist_ok=True)
        with open(aud_path, "wb") as f:
            f.write(aud.getbuffer())
        extra += f"\n[Audio: {os.path.basename(aud_path)}]"
    return extra

# Centering Tabs
_, col_mid, _ = st.columns([1, 6, 1])

with col_mid:
    tabs = st.tabs([
        "One-Click IEEE", 
        "One-Click MIT", 
        "One-Click IIT", 
        "One-Click Oxford", 
        "Other Domains",
        "Section-by-Section"
    ])

    with tabs[0]:
        render_one_click_form("ieee", "IEEE", "Generate a massive professional **IEEE-style** research paper.")

    with tabs[1]:
        render_one_click_form("mit", "MIT", "Generate a massive professional **MIT-style** research paper.")

    with tabs[2]:
        render_one_click_form("iit", "IIT", "Generate a massive professional **IIT-style** research paper.")

    with tabs[3]:
        render_one_click_form("oxford", "Oxford", "Generate a massive professional **Oxford-style** research paper.")

    with tabs[4]:
        st.markdown("<p style='text-align: center;'>Generate research papers for other specific industries.</p>", unsafe_allow_html=True)
        with st.form("domain_form"):
            selected_domain = st.selectbox("Select Domain", ["Science & Medical", "Business & Finance", "Humanities & Arts", "Law & Policy"])
            domain_topic = st.text_area("Research Topic", height=100, placeholder="Enter your research topic...")
            col1, col2 = st.columns(2)
            with col1:
                uploaded_image = st.file_uploader("Upload Image", type=["png","jpg","jpeg"], key="domain_img")
            with col2:
                uploaded_audio = st.file_uploader("Upload Audio", type=["wav","mp3","m4a"], key="domain_aud")
            
            if st.form_submit_button("Generate Domain Paper ⚡", use_container_width=True):
                extra = handle_uploads(uploaded_image, uploaded_audio)
                generate_one_click_paper(domain_topic + extra, selected_domain)

    with tabs[5]:
        st.markdown("<p style='text-align: center;'>Generate a paper section-by-section with fine-grained control.</p>", unsafe_allow_html=True)
        with st.form("paper_params"):
            topic = st.text_area("Research Topic", height=100, placeholder="Enter your research topic or prompt here...")
            
            with st.expander("Advanced Settings", expanded=False):
                target_journal = st.selectbox("Target Journal/Style", ["IEEE", "MIT", "Oxford", "Nature", "General Academic"])
                tone = st.selectbox("Tone", ["Academic", "Analytical", "Objective", "Survey Review", "Persuasive"])
                audience = st.text_input("Target Audience", value="Domain Experts")
                num_sections = st.number_input("Number of Sections", min_value=1, max_value=20, value=6)
                model_name = st.selectbox("LLM Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
            
            submit_custom = st.form_submit_button("Start Manual Generation", use_container_width=True)

        if submit_custom:
            if not topic or not audience:
                st.error("Please provide all required fields.")
                st.stop()
                
            try:
                llm = get_llm(model_name)
            except Exception as e:
                st.error(f"Error initializing LLM: {str(e)}")
                st.stop()

            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Generating title...")
            title, subtitle = generate_title_and_subtitle(llm, topic, target_journal, audience)
            st.write(f"**Title:** {title}")
            progress_bar.progress(10)
            
            db = SessionLocal()
            try:
                paper = Paper(
                    user_id=st.session_state['user_id'],
                    title=title,
                    subtitle=subtitle,
                    genre=target_journal,
                    tone=tone
                )
                db.add(paper)
                db.commit()
                db.refresh(paper)
                
                status_text.text("Generating outline...")
                outline = generate_outline(llm, title, subtitle, topic, target_journal, audience, num_sections)
                
                st.subheader("Paper Outline")
                for idx, sec in enumerate(outline, 1):
                    st.write(f"**Section {idx}:** {sec['title']}")
                
                progress_bar.progress(20)
                
                prev_sum = ""
                step = 80 / max(1, len(outline))
                prog = 20
                
                for idx, sec in enumerate(outline, 1):
                    status_text.text(f"Generating Section {idx}: {sec['title']}...")
                    content = generate_chapter(llm, title, sec['title'], sec['description'], tone, prev_sum)
                    prev_sum = generate_summary(llm, content)
                    
                    db_section = Section(
                        paper_id=paper.id,
                        section_number=idx,
                        section_title=sec['title'],
                        content=content,
                        summary=prev_sum
                    )
                    db.add(db_section)
                    db.commit()
                    
                    prog += step
                    progress_bar.progress(min(int(prog), 100))
            finally:
                db.close()
            status_text.text("Paper generation complete!")
            progress_bar.progress(100)
            st.success("Paper generated! Go to 'My Papers' to view.")
