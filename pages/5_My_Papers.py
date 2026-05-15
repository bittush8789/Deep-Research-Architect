import streamlit as st
import os
from utils.helpers import check_auth, load_css, render_sidebar
from database.database import SessionLocal
from database.models import Paper, Section
from exports.pdf_generator import generate_pdf

load_css()
check_auth()
render_sidebar()

# Centering container
_, col_mid, _ = st.columns([1, 4, 1])

with col_mid:
    st.markdown("<h1 style='text-align: center;'>My Research Papers</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>View and download your generated academic papers.</p>", unsafe_allow_html=True)
    
    st.divider()

    db = SessionLocal()
    try:
        papers = db.query(Paper).filter(Paper.user_id == st.session_state['user_id']).order_by(Paper.created_at.desc()).all()
        
        if not papers:
            st.info("You haven't generated any research papers yet.")
        else:
            for paper in papers:
                with st.expander(f"{paper.title} (Generated on {paper.created_at.strftime('%Y-%m-%d')})"):
                    if paper.subtitle:
                        st.write(f"**Subtitle:** {paper.subtitle}")
                    st.write(f"**Target Journal/Domain:** {paper.genre} | **Tone:** {paper.tone}")
                    
                    sections = db.query(Section).filter(Section.paper_id == paper.id).order_by(Section.section_number).all()
                    st.write(f"**Sections:** {len(sections)}")
                    
                    if st.button("Generate PDF", key=f"pdf_{paper.id}", use_container_width=True):
                        with st.spinner("Generating PDF..."):
                            pdf_path = generate_pdf(paper, sections)
                            with open(pdf_path, "rb") as f:
                                st.download_button(
                                    label="Download PDF",
                                    data=f,
                                    file_name=os.path.basename(pdf_path),
                                    mime="application/pdf",
                                    key=f"dl_{paper.id}",
                                    use_container_width=True
                                )
                                
                    st.divider()
                    st.subheader("First Section Preview")
                    if sections:
                        st.markdown(f"### {sections[0].section_title}")
                        from utils.helpers import render_rich_markdown
                        render_rich_markdown(sections[0].content[:800] + "...")
    finally:
        db.close()
