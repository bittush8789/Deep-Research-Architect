from langchain_core.prompts import PromptTemplate

TITLE_PROMPT = PromptTemplate(
    input_variables=["topic", "target_conference", "audience"],
    template="""You are an expert academic researcher.
Generate a compelling research paper title and an optional subtitle based on the following information:
Research Topic: {topic}
Target Journal/Conference: {target_conference}
Audience: {audience}

Format your response exactly like this:
Title: [Main Title]
Subtitle: [Subtitle or leave blank]
"""
)

OUTLINE_PROMPT = PromptTemplate(
    input_variables=["title", "subtitle", "topic", "target_conference", "audience", "num_sections"],
    template="""You are a senior academic researcher outlining a paper.
Create a detailed outline for a research paper with the following details:
Title: {title}
Subtitle: {subtitle}
Topic: {topic}
Journal/Domain Style: {target_conference}
Target Audience: {audience}
Number of Sections: {num_sections}

Typically, sections should include: Abstract, Introduction, Literature Review, Methodology/Approach, Results/Analysis, Discussion, and Conclusion. Adapt this depending on the specific domain (e.g., Medical papers need Clinical Trials/Methods, Humanities papers need Theoretical Framework).

Format the output EXACTLY like this for each section:
Section 1: [Section Name] - [Brief description of what will be covered]
Section 2: [Section Name] - [Brief description]
...
"""
)

CHAPTER_PROMPT = PromptTemplate(
    input_variables=["title", "section_title", "section_description", "tone", "previous_summary"],
    template="""You are writing a section for an academic research paper.
Paper Title: {title}
Current Section: {section_title}
Section Objective: {section_description}
Writing Tone: {tone} (e.g., Academic, Objective, Analytical)

Previous Section Context:
{previous_summary}

Write the full content for this section. Use superior academic language, deep theoretical foundations, and highly structured arguments. 

CRITICAL: Provide the 'best possible explanation' for all technical concepts, including mathematical formulas (in LaTeX if needed), step-by-step logic, and deep analytical insight. Avoid brief summaries; strive for the depth found in top-tier publications like Nature, IEEE Transactions, or Harvard Law Review. Use markdown formatting for subheadings, bold text for key terms, and lists for clarity. Do NOT output "Section X:" at the start, just write the high-quality content.
"""
)

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["section_content"],
    template="""Summarize the following academic paper section in 2-3 sentences. This summary will be used to maintain context for writing the next section.
Section Content:
{section_content}

Summary:"""
)

ONE_CLICK_PAPER_PROMPT = PromptTemplate(
    input_variables=["topic", "institution"],
    template="""Generate a complete professional research paper in the domain of {institution} on the topic:

"{topic}"

The research paper should be highly detailed, structured, and written in a professional academic writing style suitable for:
- journal publication
- conference submission
- thesis / dissertation chapter
- research portfolio

The paper must contain the following structural elements in detail, appropriately adapted to the '{institution}' domain (e.g., Tech, Medical, Business, Humanities):

1. Title & Subtitle
- Generate a professional, domain-appropriate title and subtitle.

2. Abstract
- Write a detailed abstract (200-300 words).
- Include: background, problem statement, methodology, key findings, and conclusion.

3. Keywords
- Generate 8-15 professional academic keywords.

4. Introduction
- Explain the background and context.
- Explain current challenges in the field.
- Explain the research objectives and significance of this study.

5. Literature Review / Related Work
- Discuss existing theories, research papers, and approaches.
- Identify the gap in the current literature.

6. Theoretical Framework / Problem Statement
- Clearly define the problem or theoretical foundation.
- For tech/science, detail the exact problem/limitations.
- For humanities/business, detail the conceptual framework.

7. Methodology / Research Design
- Explain the research methodology.
- E.g., for Tech: System architecture and algorithms. 
- E.g., for Medical: Clinical study design, patient cohorts. 
- E.g., for Business: Survey design, financial models.
- E.g., for Humanities: Archival research, textual analysis.

8. Implementation / Data Collection
- Explain how the methodology was executed or how data was gathered.

9. Results / Findings
- Present the main findings. Generate realistic data, trends, or analytical observations.

10. Discussion & Analysis
- Interpret the results.
- Compare findings with traditional systems/previous literature.

11. Advantages & Practical Applications
- Explain the real-world impact and applications of this research.

12. Limitations
- Provide a realistic assessment of the study's limitations (e.g., sample size, model bias, scope constraints).

13. Future Scope / Directions
- Suggest what future researchers should focus on next.

14. Conclusion
- Write a strong professional conclusion summarizing the contribution and impact.

15. References
- Generate realistic academic references in standard format (APA, IEEE, or MLA depending on domain). Include realistic papers, journals, and books.

Additional Requirements:
- Maintain a strict professional and academic tone suitable for '{institution}'.
- Use structured headings and subheadings.
- Incorporate markdown tables to present data, comparisons, or literature summaries.
- Add elite-level explanations, deep technical insight, and maximum academic depth.
- CRITICAL: Provide the 'best explanation' for all complex topics. Include detailed mathematical equations (in LaTeX), architecture diagrams (in Mermaid.js syntax), or complex statistical models.
- Include **Detailed Numerical Examples** and **Step-by-Step Case Studies** to demonstrate practical application.
- For technical papers, generate **Mermaid.js** code blocks for:
    * Architecture Diagrams
    * Flowcharts
    * Process Sequences
- For data-heavy papers, generate **detailed benchmark tables** and **performance graphs** (in markdown table format).
- Generate the entire paper in markdown format.
"""
)
