import os
from langchain_groq import ChatGroq
from prompts.prompts import TITLE_PROMPT, OUTLINE_PROMPT, CHAPTER_PROMPT, SUMMARY_PROMPT, ONE_CLICK_PAPER_PROMPT

def get_llm(model_name="llama-3.3-70b-versatile"):
    return ChatGroq(temperature=0.7, model_name=model_name, groq_api_key=os.getenv("GROQ_API_KEY"))

def generate_title_and_subtitle(llm, topic, target_conference, audience):
    chain = TITLE_PROMPT | llm
    result = chain.invoke({"topic": topic, "target_conference": target_conference, "audience": audience}).content
    
    title = ""
    subtitle = ""
    for line in result.split('\n'):
        if line.startswith("Title:"):
            title = line.replace("Title:", "").strip()
        elif line.startswith("Subtitle:"):
            subtitle = line.replace("Subtitle:", "").strip()
            
    return title, subtitle

def generate_outline(llm, title, subtitle, topic, target_conference, audience, num_sections):
    chain = OUTLINE_PROMPT | llm
    result = chain.invoke({
        "title": title, "subtitle": subtitle, "topic": topic, 
        "target_conference": target_conference, "audience": audience, "num_sections": num_sections
    }).content
    
    sections = []
    for line in result.split('\n'):
        if line.startswith("Section"):
            parts = line.split('-', 1)
            if len(parts) == 2:
                section_title = parts[0].split(':', 1)[1].strip() if ':' in parts[0] else parts[0].strip()
                description = parts[1].strip()
                sections.append({"title": section_title, "description": description})
    return sections

def generate_chapter(llm, title, section_title, section_description, tone, previous_summary):
    chain = CHAPTER_PROMPT | llm
    return chain.invoke({
        "title": title, "section_title": section_title, 
        "section_description": section_description, "tone": tone, 
        "previous_summary": previous_summary
    }).content

def generate_summary(llm, section_content):
    chain = SUMMARY_PROMPT | llm
    return chain.invoke({"section_content": section_content}).content

def generate_one_click_paper_full(llm, topic, institution):
    chain = ONE_CLICK_PAPER_PROMPT | llm
    return chain.invoke({"topic": topic, "institution": institution}).content
