import streamlit as st

def render():
    # Hero Section
    st.markdown(
        """
        <div class="hero-wrapper">
            <div class="hero-pill">
                <span class="hero-pill-dot"></span>
                AI-Powered Resume Intelligence Platform
            </div>
            <h1 class="hero-title">
                Turn Your Resume Into an <br><span class="gradient-text">Interview Magnet</span>
            </h1>
            <p class="hero-subtitle">
                Engineered to reverse-engineer Fortune 500 ATS algorithms (Workday, Taleo, Greenhouse).
                Instantly diagnose formatting traps, keyword voids, and unproven skill claims before submitting.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Primary Action Row
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        if st.button("🚀  Start Resume Assessment", use_container_width=True, type="primary"):
            st.session_state.current_view = 'scorer'
            st.query_params["view"] = 'scorer'
            st.rerun()

    # Hero Metrics Bar
    st.markdown(
        """
        <div class="hero-stats-row" style="max-width: 800px; margin: 1.5rem auto 3rem auto;">
            <div class="hero-stat-item">
                <div class="hero-stat-num">94.8%</div>
                <div class="hero-stat-label">ATS Accuracy Rate</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-num">5 Vectors</div>
                <div class="hero-stat-label">Comprehensive Scoring</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-num">100%</div>
                <div class="hero-stat-label">Private & Local Parsing</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-num">&lt; 15s</div>
                <div class="hero-stat-label">Deep Diagnostic Speed</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Interactive Product Preview Mockup
    st.markdown(
        """
        <div class="preview-window">
            <div class="window-header">
                <span class="window-dot dot-red"></span>
                <span class="window-dot dot-yellow"></span>
                <span class="window-dot dot-green"></span>
                <span class="window-title">diagnostic-telemetry // report-preview.ats</span>
            </div>
            <div style="display: grid; grid-template-columns: 200px 1fr; gap: 2rem; align-items: center; padding: 0.5rem 1rem;">
                <div style="text-align: center; border-right: 1px solid #E2E8F0; padding-right: 1.5rem;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">Overall ATS Score</div>
                    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 3.5rem; font-weight: 800; color: #10B981; line-height: 1;">88</div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: #047857; margin-top: 0.5rem; background: #ECFDF5; border: 1px solid #A7F3D0; padding: 2px 8px; border-radius: 9999px; display: inline-block;">Top 10% Candidate</div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <span style="font-weight: 700; font-size: 0.95rem; color: #0F172A;">Multi-Dimensional Analysis Breakdown</span>
                        <span class="badge-pill badge-emerald">✔ Ready for Human Screen</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; font-size: 0.825rem;">
                        <div style="background: #F8FAFC; padding: 8px 12px; border-radius: 8px; border: 1px solid #E2E8F0;">
                            <span style="color: #64748B;">Keywords & Taxonomy:</span> <strong style="color: #0F172A;">24/25 (96%)</strong>
                        </div>
                        <div style="background: #F8FAFC; padding: 8px 12px; border-radius: 8px; border: 1px solid #E2E8F0;">
                            <span style="color: #64748B;">Layout & ATS Compatibility:</span> <strong style="color: #0F172A;">15/15 (100%)</strong>
                        </div>
                        <div style="background: #F8FAFC; padding: 8px 12px; border-radius: 8px; border: 1px solid #E2E8F0;">
                            <span style="color: #64748B;">Content Impact & Metrics:</span> <strong style="color: #0F172A;">22/25 (88%)</strong>
                        </div>
                        <div style="background: #F8FAFC; padding: 8px 12px; border-radius: 8px; border: 1px solid #E2E8F0;">
                            <span style="color: #64748B;">Skill Proof Verification:</span> <strong style="color: #0F172A;">14/15 (93%)</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3-Step Guided Methodology
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">Methodology</div>
            <h2 style="font-size: 2rem; font-weight: 800; color: #0F172A; margin: 0;">How The Intelligence Engine Works</h2>
        </div>
        <div class="flow-step-container">
            <div class="flow-step-card">
                <span class="flow-step-badge">STEP 01</span>
                <div class="card-icon-box icon-box-indigo">📥</div>
                <div class="card-title">Ingest & Semantic Parse</div>
                <div class="card-desc">
                    Extracts unstructured text from PDF and DOCX documents while preserving layout hierarchy, section tags, and contact metadata.
                </div>
            </div>
            <div class="flow-step-card">
                <span class="flow-step-badge">STEP 02</span>
                <div class="card-icon-box icon-box-cyan">🧠</div>
                <div class="card-title">5-Vector Evaluation</div>
                <div class="card-desc">
                    Weights content quality (25%), keyword density (25%), structural formatting (20%), skill validation (15%), and ATS compliance (15%).
                </div>
            </div>
            <div class="flow-step-card">
                <span class="flow-step-badge">STEP 03</span>
                <div class="card-icon-box icon-box-emerald">⚡</div>
                <div class="card-title">Prioritized Action Playbook</div>
                <div class="card-desc">
                    Generates line-by-line edit recommendations and exact before-and-after bullet rewrites to boost your interview callback rate.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Key Features Grid
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">Core Architecture</div>
            <h2 style="font-size: 2rem; font-weight: 800; color: #0F172A; margin: 0;">Built for Modern Technical & Enterprise Recruiting</h2>
        </div>
        <div class="features-grid">
            <div class="saas-card">
                <div class="card-icon-box icon-box-indigo">🎯</div>
                <div class="card-title">ATS Filter Emulation</div>
                <div class="card-desc">
                    Detects table headers, multi-column traps, unreadable glyphs, and font issues that cause 75% of resumes to get discarded.
                </div>
            </div>
            <div class="saas-card">
                <div class="card-icon-box icon-box-cyan">🔍</div>
                <div class="card-title">Contextual Skill Proofing</div>
                <div class="card-desc">
                    Matches listed technical proficiencies directly against project descriptions to ensure every claim is substantiated with proof.
                </div>
            </div>
            <div class="saas-card">
                <div class="card-icon-box icon-box-emerald">📋</div>
                <div class="card-title">Targeted JD Gap Analysis</div>
                <div class="card-desc">
                    Compares your resume against specific job descriptions to highlight exact missing keywords, frameworks, and domain credentials.
                </div>
            </div>
            <div class="saas-card">
                <div class="card-icon-box icon-box-indigo">📊</div>
                <div class="card-title">Deterministic Scoring</div>
                <div class="card-desc">
                    Transparent, mathematically weighted metrics calibrated against thousands of verified successful candidate submissions.
                </div>
            </div>
            <div class="saas-card">
                <div class="card-icon-box icon-box-cyan">📑</div>
                <div class="card-title">Executive PDF Export</div>
                <div class="card-desc">
                    Download a comprehensive audit report with detailed findings, component scorecards, and step-by-step revision suggestions.
                </div>
            </div>
            <div class="saas-card">
                <div class="card-icon-box icon-box-emerald">🔒</div>
                <div class="card-title">Strict Privacy Standards</div>
                <div class="card-desc">
                    Your resume data is processed securely and never sold, shared, or used to train third-party public models.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Bottom Call to Action Card
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #090D1A 0%, #1E293B 100%); border-radius: 16px; padding: 3rem 2rem; text-align: center; color: white; margin-top: 1rem; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 10px 25px rgba(15,23,42,0.15);">
            <h2 style="color: #FFFFFF !important; font-size: 2rem; font-weight: 800; margin-bottom: 0.75rem;">Ready to Supercharge Your Applications?</h2>
            <p style="color: #94A3B8; font-size: 1rem; max-width: 580px; margin: 0 auto 1.75rem auto;">
                Upload your resume now to uncover blind spots and get actionable feedback before recruiters look at your profile.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col_x, col_y, col_z = st.columns([1, 2, 1])
    with col_y:
        st.markdown("<div style='margin-top: -30px;'>", unsafe_allow_html=True)
        if st.button("🚀  Scan Your Resume Free", use_container_width=True, type="primary", key="cta_bottom"):
            st.session_state.current_view = 'scorer'
            st.query_params["view"] = 'scorer'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
