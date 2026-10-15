import streamlit as st

def render():
    # Hero Section
    st.markdown(
        """
        <div class="hero-wrapper">
            <div class="hero-pill">
                <span class="hero-pill-dot"></span>
                ✨ AI-Powered Resume Checker
            </div>
            <h1 class="hero-title">
                Turn Your Resume Into an <br><span class="gradient-text">Interview Magnet</span>
            </h1>
            <p class="hero-subtitle">
                See exactly how hiring managers and applicant tracking systems (like Workday, Taleo & Greenhouse) read your resume.
                Find missing keywords, fix formatting glitches, and get easy tips to land more interviews.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Primary Action Row
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        if st.button("🚀  Check My Resume Free", use_container_width=True, type="primary"):
            st.session_state.current_view = 'scorer'
            st.query_params["view"] = 'scorer'
            st.rerun()

    # Hero Metrics Bar
    st.markdown(
        """
        <div class="hero-stats-row" style="max-width: 800px; margin: 1.5rem auto 3rem auto;">
            <div class="hero-stat-item">
                <div class="hero-stat-num">95%</div>
                <div class="hero-stat-label">ATS Match Accuracy</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-num">5 Areas</div>
                <div class="hero-stat-label">Complete Resume Review</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-num">100%</div>
                <div class="hero-stat-label">Private & Confidential</div>
            </div>
            <div class="hero-stat-item">
                <div class="hero-stat-num">&lt; 15s</div>
                <div class="hero-stat-label">Instant Results</div>
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
                <span class="window-title">sample-resume-review.pdf — Preview</span>
            </div>
            <div style="display: grid; grid-template-columns: 200px 1fr; gap: 2rem; align-items: center; padding: 0.5rem 1rem;">
                <div style="text-align: center; border-right: 1px solid #E2E8F0; padding-right: 1.5rem;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">Overall Resume Score</div>
                    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 3.5rem; font-weight: 800; color: #10B981; line-height: 1;">88</div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: #047857; margin-top: 0.5rem; background: #ECFDF5; border: 1px solid #A7F3D0; padding: 2px 8px; border-radius: 9999px; display: inline-block;">Top 10% Candidate</div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <span style="font-weight: 700; font-size: 0.95rem; color: #0F172A;">How Your Resume Performs</span>
                        <span class="badge-pill badge-emerald">✔ Ready for Recruiters</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; font-size: 0.825rem;">
                        <div style="background: #F8FAFC; padding: 8px 12px; border-radius: 8px; border: 1px solid #E2E8F0;">
                            <span style="color: #64748B;">Keywords & Terms:</span> <strong style="color: #0F172A;">24/25 (96%)</strong>
                        </div>
                        <div style="background: #F8FAFC; padding: 8px 12px; border-radius: 8px; border: 1px solid #E2E8F0;">
                            <span style="color: #64748B;">Layout & Readability:</span> <strong style="color: #0F172A;">15/15 (100%)</strong>
                        </div>
                        <div style="background: #F8FAFC; padding: 8px 12px; border-radius: 8px; border: 1px solid #E2E8F0;">
                            <span style="color: #64748B;">Impact & Results:</span> <strong style="color: #0F172A;">22/25 (88%)</strong>
                        </div>
                        <div style="background: #F8FAFC; padding: 8px 12px; border-radius: 8px; border: 1px solid #E2E8F0;">
                            <span style="color: #64748B;">Skills Backed by Projects:</span> <strong style="color: #0F172A;">14/15 (93%)</strong>
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
            <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">How It Works</div>
            <h2 style="font-size: 2rem; font-weight: 800; color: #0F172A; margin: 0;">Simple 3-Step Review Process</h2>
        </div>
        <div class="flow-step-container">
            <div class="flow-step-card">
                <span class="flow-step-badge">STEP 01</span>
                <div class="card-icon-box icon-box-indigo">📥</div>
                <div class="card-title">1. Upload Your Resume</div>
                <div class="card-desc">
                    Drop your resume in PDF or Word format. We quickly read your experience, projects, skills, and layout — just like a real hiring system.
                </div>
            </div>
            <div class="flow-step-card">
                <span class="flow-step-badge">STEP 02</span>
                <div class="card-icon-box icon-box-cyan">🧠</div>
                <div class="card-title">2. Instant 5-Point Check</div>
                <div class="card-desc">
                    We review your resume across 5 key areas: keywords, clean formatting, impactful bullet points, verified skills, and ATS readability.
                </div>
            </div>
            <div class="flow-step-card">
                <span class="flow-step-badge">STEP 03</span>
                <div class="card-icon-box icon-box-emerald">⚡</div>
                <div class="card-title">3. Get Clear, Actionable Tips</div>
                <div class="card-desc">
                    Receive simple, step-by-step suggestions and ready-to-use bullet point rewrites so you can apply with complete confidence.
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
            <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">Key Features</div>
            <h2 style="font-size: 2rem; font-weight: 800; color: #0F172A; margin: 0;">Everything You Need to Land More Interviews</h2>
        </div>
        <div class="features-grid">
            <div class="saas-card">
                <div class="card-icon-box icon-box-indigo">🎯</div>
                <div class="card-title">Pass ATS Filters Easily</div>
                <div class="card-desc">
                    Find and fix hidden formatting traps like complex tables, unusual columns, and unreadable fonts before you apply.
                </div>
            </div>
            <div class="saas-card">
                <div class="card-icon-box icon-box-cyan">🔍</div>
                <div class="card-title">Prove Your Skills with Evidence</div>
                <div class="card-desc">
                    Ensure the skills you list are backed up with clear project achievements and real work examples that recruiters love.
                </div>
            </div>
            <div class="saas-card">
                <div class="card-icon-box icon-box-emerald">📋</div>
                <div class="card-title">Match Any Job Description</div>
                <div class="card-desc">
                    Paste any job description to instantly see which keywords, tools, and requirements you're missing, so you can tailor your resume in minutes.
                </div>
            </div>
            <div class="saas-card">
                <div class="card-icon-box icon-box-indigo">📊</div>
                <div class="card-title">Clear & Honest Scoring</div>
                <div class="card-desc">
                    Get a transparent score out of 100 with clear breakdowns, so you always know where you stand and what to improve next.
                </div>
            </div>
            <div class="saas-card">
                <div class="card-icon-box icon-box-cyan">📑</div>
                <div class="card-title">Download & Share Reports</div>
                <div class="card-desc">
                    Export a clean, professional PDF summary of your review to keep handy as you refine your job applications.
                </div>
            </div>
            <div class="saas-card">
                <div class="card-icon-box icon-box-emerald">🔒</div>
                <div class="card-title">100% Private & Safe</div>
                <div class="card-desc">
                    Your personal information and career history stay completely confidential. Your data is never shared or sold.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Bottom Call to Action Card
    st.markdown(
        """
        <div class="cta-dark-card">
            <h2 class="cta-heading" style="color: #FFFFFF !important;">Ready to Supercharge Your Applications?</h2>
            <p class="cta-desc" style="color: #94A3B8 !important;">
                Upload your resume now to uncover blind spots and get personalized feedback before recruiters look at your profile.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col_x, col_y, col_z = st.columns([1, 2, 1])
    with col_y:
        st.markdown("<div style='margin-top: -30px;'>", unsafe_allow_html=True)
        if st.button("🚀  Check Your Resume Now", use_container_width=True, type="primary", key="cta_bottom"):
            st.session_state.current_view = 'scorer'
            st.query_params["view"] = 'scorer'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
