import textwrap
import streamlit as st

def render():
    st.markdown(
        """
        <div style="margin-bottom: 2rem;">
            <div style="display:inline-flex; align-items:center; gap:0.4rem; padding:0.25rem 0.75rem; background:#EEF2FF; border:1px solid #C7D2FE; border-radius:9999px; font-size:0.75rem; font-weight:700; color:#4F46E5; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.75rem;">
                <span style="width:6px; height:6px; border-radius:50%; background:#4F46E5;"></span>
                Career Guide // Best Practices
            </div>
            <h1 style="font-size: 2.25rem; font-weight: 800; color: #0F172A; margin: 0 0 0.5rem 0; letter-spacing: -0.025em;">
                Resume & ATS Best Practices Guide
            </h1>
            <p style="font-size: 1rem; color: #64748B; margin: 0; max-width: 720px; line-height: 1.6;">
                Simple, practical advice to help your resume sail through applicant tracking systems and catch the eye of hiring managers.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2-Column DOs vs DONTs Grid
    best_practices_html = textwrap.dedent("""
<div class="comparison-grid" style="margin-bottom: 2rem;">
    <div class="comparison-card">
        <div class="comparison-header">
            <span style="width:28px; height:28px; border-radius:6px; background:#ECFDF5; color:#059669; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.9rem;">✔</span>
            <span class="comparison-title" style="color:#065F46;">What Works Best</span>
        </div>
        <div class="bullet-item">
            <strong style="color:#0F172A; width:130px; flex-shrink:0;">Section Headers:</strong>
            <span>Use standard headings (Work Experience, Education, Skills, Projects). Avoid informal titles like "Where I've Been".</span>
        </div>
        <div class="bullet-item">
            <strong style="color:#0F172A; width:130px; flex-shrink:0;">Quantified Results:</strong>
            <span>Start bullets with strong action verbs and include measurable results (e.g. "reduced loading time by 35%").</span>
        </div>
        <div class="bullet-item">
            <strong style="color:#0F172A; width:130px; flex-shrink:0;">Prove Your Skills:</strong>
            <span>Ensure the core skills you list are backed up with examples in your work experience or project bullets.</span>
        </div>
        <div class="bullet-item">
            <strong style="color:#0F172A; width:130px; flex-shrink:0;">Standard Format:</strong>
            <span>Save as a clean text-based PDF or DOCX file. Make sure you can select and highlight the text with your cursor.</span>
        </div>
        <div class="bullet-item">
            <strong style="color:#0F172A; width:130px; flex-shrink:0;">Clean Typography:</strong>
            <span>Stick to common fonts (Inter, Calibri, Arial, Helvetica, Georgia) at a readable 10–12pt body font size.</span>
        </div>
    </div>
    <div class="comparison-card">
        <div class="comparison-header">
            <span style="width:28px; height:28px; border-radius:6px; background:#FEF2F2; color:#DC2626; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.9rem;">✕</span>
            <span class="comparison-title" style="color:#991B1B;">Common Mistakes to Avoid</span>
        </div>
        <div class="bullet-item">
            <strong style="color:#0F172A; width:130px; flex-shrink:0;">Complex Tables:</strong>
            <span>Avoid nested tables and text boxes. Many automated scanners scramble table text into disordered words.</span>
        </div>
        <div class="bullet-item">
            <strong style="color:#0F172A; width:130px; flex-shrink:0;">Header/Footer Text:</strong>
            <span>Never put contact details in document headers or footers. Many parsers skip margin content completely.</span>
        </div>
        <div class="bullet-item">
            <strong style="color:#0F172A; width:130px; flex-shrink:0;">Icons & Rating Bars:</strong>
            <span>Avoid skill rating stars or progress bars. Scanners cannot read them and treat them as missing skills.</span>
        </div>
        <div class="bullet-item">
            <strong style="color:#0F172A; width:130px; flex-shrink:0;">Keyword Stuffing:</strong>
            <span>Do not hide white text or spam keywords. Modern screening systems easily flag artificial repetition.</span>
        </div>
        <div class="bullet-item">
            <strong style="color:#0F172A; width:130px; flex-shrink:0;">Multi-Column Layouts:</strong>
            <span>Avoid two-column or magazine-style resumes. Parsers read across columns horizontally, jumbling sentences.</span>
        </div>
    </div>
</div>
""")
    st.markdown(best_practices_html, unsafe_allow_html=True)

    # Industry Keyword Taxonomy
    taxonomy_header = textwrap.dedent("""
<div style="margin: 2rem 0 1rem 0;">
    <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;">Popular Keywords</div>
    <h3 style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin: 0;">In-Demand Keywords by Role</h3>
</div>
""")
    st.markdown(taxonomy_header, unsafe_allow_html=True)

    tab_swe, tab_data, tab_lead = st.tabs([
        "💻 Software Engineering",
        "📊 Data & AI",
        "🚀 Product & Leadership"
    ])

    with tab_swe:
        swe_html = textwrap.dedent("""
<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:1.25rem; font-size:0.9rem; line-height:1.7;">
    <div style="margin-bottom:0.75rem;">
        <strong style="color:#0F172A;">Architecture & Systems:</strong><br>
        <span class="keyword-chip chip-neutral">Microservices</span>
        <span class="keyword-chip chip-neutral">Distributed Systems</span>
        <span class="keyword-chip chip-neutral">Event-Driven Architecture</span>
        <span class="keyword-chip chip-neutral">RESTful APIs</span>
        <span class="keyword-chip chip-neutral">gRPC</span>
        <span class="keyword-chip chip-neutral">GraphQL</span>
    </div>
    <div style="margin-bottom:0.75rem;">
        <strong style="color:#0F172A;">Languages & Frameworks:</strong><br>
        <span class="keyword-chip chip-neutral">Python</span>
        <span class="keyword-chip chip-neutral">TypeScript</span>
        <span class="keyword-chip chip-neutral">Go</span>
        <span class="keyword-chip chip-neutral">Rust</span>
        <span class="keyword-chip chip-neutral">React</span>
        <span class="keyword-chip chip-neutral">Next.js</span>
        <span class="keyword-chip chip-neutral">FastAPI</span>
        <span class="keyword-chip chip-neutral">Node.js</span>
    </div>
    <div>
        <strong style="color:#0F172A;">DevOps & Reliability:</strong><br>
        <span class="keyword-chip chip-neutral">Docker</span>
        <span class="keyword-chip chip-neutral">Kubernetes</span>
        <span class="keyword-chip chip-neutral">CI/CD Pipelines</span>
        <span class="keyword-chip chip-neutral">Terraform</span>
        <span class="keyword-chip chip-neutral">Prometheus</span>
        <span class="keyword-chip chip-neutral">High Availability</span>
    </div>
</div>
""")
        st.markdown(swe_html, unsafe_allow_html=True)

    with tab_data:
        data_html = textwrap.dedent("""
<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:1.25rem; font-size:0.9rem; line-height:1.7;">
    <div style="margin-bottom:0.75rem;">
        <strong style="color:#0F172A;">Data Warehousing & ETL:</strong><br>
        <span class="keyword-chip chip-neutral">Snowflake</span>
        <span class="keyword-chip chip-neutral">dbt</span>
        <span class="keyword-chip chip-neutral">Apache Spark</span>
        <span class="keyword-chip chip-neutral">Kafka</span>
        <span class="keyword-chip chip-neutral">Airflow</span>
        <span class="keyword-chip chip-neutral">PostgreSQL</span>
    </div>
    <div>
        <strong style="color:#0F172A;">Machine Learning & AI:</strong><br>
        <span class="keyword-chip chip-neutral">LLM Fine-Tuning</span>
        <span class="keyword-chip chip-neutral">RAG Pipelines</span>
        <span class="keyword-chip chip-neutral">PyTorch</span>
        <span class="keyword-chip chip-neutral">Vector Databases</span>
        <span class="keyword-chip chip-neutral">Hugging Face</span>
        <span class="keyword-chip chip-neutral">MLOps</span>
    </div>
</div>
""")
        st.markdown(data_html, unsafe_allow_html=True)

    with tab_lead:
        lead_html = textwrap.dedent("""
<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:1.25rem; font-size:0.9rem; line-height:1.7;">
    <div style="margin-bottom:0.75rem;">
        <strong style="color:#0F172A;">Product Strategy & Delivery:</strong><br>
        <span class="keyword-chip chip-neutral">Product Discovery</span>
        <span class="keyword-chip chip-neutral">OKRs</span>
        <span class="keyword-chip chip-neutral">Roadmapping</span>
        <span class="keyword-chip chip-neutral">A/B Testing</span>
        <span class="keyword-chip chip-neutral">Customer Journey</span>
        <span class="keyword-chip chip-neutral">KPI Optimization</span>
    </div>
    <div>
        <strong style="color:#0F172A;">Leadership & Process:</strong><br>
        <span class="keyword-chip chip-neutral">Cross-Functional Leadership</span>
        <span class="keyword-chip chip-neutral">Agile / Scrum</span>
        <span class="keyword-chip chip-neutral">Stakeholder Management</span>
        <span class="keyword-chip chip-neutral">Vendor Evaluation</span>
        <span class="keyword-chip chip-neutral">Talent Mentorship</span>
    </div>
</div>
""")
        st.markdown(lead_html, unsafe_allow_html=True)
