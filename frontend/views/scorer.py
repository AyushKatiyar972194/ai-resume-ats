from typing import Optional
import requests
import streamlit as st

from frontend.services import api_client
from frontend.components.dashboard import display_results_dashboard

def _read_jd(jd_file, jd_text: str) -> str:
    if jd_text:
        return jd_text.strip()
    if jd_file is None:
        return ""
    if jd_file.name.lower().endswith(".txt"):
        return jd_file.getvalue().decode("utf-8", errors="ignore")
    st.warning(
        "Job description files must be `.txt` for now — paste the JD text instead "
        "if you have a PDF or DOCX."
    )
    return ""

def _show_backend_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the backend. Is `uvicorn backend.main:app` running on port 8000?")
    elif isinstance(exc, requests.Timeout):
        st.error("The backend took too long to respond. Try a smaller resume or check the server logs.")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            detail = exc.response.text
        st.error(f"Backend returned {exc.response.status_code}: {detail}")
    else:
        st.error(f"Unexpected error: {exc}")

def _summary_text(analysis: dict) -> str:
    score = analysis.get("ATS_score", analysis.get("ats_score", 0))
    lines = [f"RESUME REVIEW REPORT", f"OVERALL RESUME SCORE: {score:.0f}/100", "="*40, ""]
    
    comp = analysis.get("component_scores") or {}
    if comp:
        lines.append("SCORE BREAKDOWN:")
        for k, v in comp.items():
            lines.append(f"  - {k.replace('_', ' ').title()}: {v}")
        lines.append("")

    if analysis.get("strengths"):
        lines.append("WHAT'S WORKING WELL (STRENGTHS):")
        lines.extend(f"  - {s}" for s in analysis["strengths"])
        lines.append("")
    if analysis.get("critical_issues"):
        lines.append("THINGS TO IMPROVE:")
        lines.extend(f"  - {s}" for s in analysis["critical_issues"])
        lines.append("")
    if analysis.get("suggestions"):
        lines.append("RECOMMENDED FIXES:")
        lines.extend(f"  - {s}" for s in analysis["suggestions"])
    return "\n".join(lines)

def _render_export_buttons(analysis: dict) -> None:
    st.markdown(
        """
        <div style="margin: 2.5rem 0 1.25rem 0; padding-top: 1.5rem; border-top: 1px solid #E2E8F0;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;">Save & Share</div>
                    <h3 style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin: 0;">Download Your Resume Report</h3>
                    <p style="font-size: 0.875rem; color: #64748B; margin: 0.25rem 0 0 0;">Save your full review as a PDF or download a quick action checklist to guide your edits.</p>
                </div>
                <span class="badge-pill badge-indigo">PDF + TXT</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📑 Generate PDF Report", use_container_width=True, type="primary"):
            try:
                with st.spinner("Generating your full PDF report..."):
                    pdf_bytes = api_client.generate_pdf(
                        analysis,
                        access_token=st.session_state.get("access_token"),
                    )
                st.session_state["scorer_pdf_bytes"] = pdf_bytes
            except requests.RequestException as exc:
                _show_backend_error(exc)

        if "scorer_pdf_bytes" in st.session_state:
            st.download_button(
                "⬇️ Download PDF Report",
                data=st.session_state["scorer_pdf_bytes"],
                file_name="resume_review_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_pdf_report",
            )

    with c2:
        st.download_button(
            "📄 Download Action Checklist (.txt)",
            data=_summary_text(analysis),
            file_name="resume_action_checklist.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_summary",
        )

def render() -> None:
    # Workspace Header
    st.markdown(
        """
        <div style="margin-bottom: 2rem;">
            <div style="display:inline-flex; align-items:center; gap:0.4rem; padding:0.25rem 0.75rem; background:#EEF2FF; border:1px solid #C7D2FE; border-radius:9999px; font-size:0.75rem; font-weight:700; color:#4F46E5; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.75rem;">
                <span style="width:6px; height:6px; border-radius:50%; background:#4F46E5;"></span>
                Instant Resume Review // 5-Point Check
            </div>
            <h1 style="font-size: 2.25rem; font-weight: 800; color: #0F172A; margin: 0 0 0.5rem 0; letter-spacing: -0.025em;">
                Resume Checker & Job Matcher
            </h1>
            <p style="font-size: 1rem; color: #64748B; margin: 0; max-width: 720px; line-height: 1.6;">
                Upload your resume to see your overall score and get personalized recommendations, or compare your resume against a specific job description to find missing keywords.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Mode Selector
    st.markdown(
        """
        <div style="font-size:0.8rem; font-weight:700; color:#0F172A; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.4rem;">
            Choose your review type:
        </div>
        """,
        unsafe_allow_html=True
    )
    analysis_mode = st.radio(
        "Choose your review type",
        ["General Resume Review", "Match with a Job Description"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # Guided Upload Container
    col_resume, col_jd = st.columns(2)

    with col_resume:
        st.markdown(
            """
            <div style="font-weight: 700; font-size: 0.95rem; color: #0F172A; margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: space-between;">
                <span>📄 Your Resume</span>
                <span class="badge-pill badge-indigo">PDF, DOC, DOCX</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        resume_file = st.file_uploader(
            "Upload Your Resume File",
            type=["pdf", "doc", "docx"],
            help="Supports PDF, DOC, and DOCX files up to 5 MB",
            key="resume_upload",
            label_visibility="collapsed"
        )
        if resume_file:
            st.markdown(
                f"""
                <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:8px; padding:0.6rem 0.9rem; margin-top:0.5rem; display:flex; align-items:center; justify-content:space-between; font-size:0.85rem;">
                    <span style="color:#065F46; font-weight:600;">✔ {resume_file.name}</span>
                    <span style="color:#047857; font-size:0.75rem;">{resume_file.size / 1024:.1f} KB</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    jd_file: Optional[object] = None
    jd_text = ""

    with col_jd:
        if analysis_mode == "Match with a Job Description":
            st.markdown(
                """
                <div style="font-weight: 700; font-size: 0.95rem; color: #0F172A; margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: space-between;">
                    <span>📋 Target Job Description</span>
                    <span class="badge-pill badge-emerald">Compare & Tailor</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            jd_method = st.radio(
                "JD Method",
                ["Paste Text", "Upload .txt File"],
                horizontal=True,
                key="jd_input_method",
                label_visibility="collapsed"
            )
            if jd_method == "Upload .txt File":
                jd_file = st.file_uploader(
                    "JD File",
                    type=["txt"],
                    key="jd_upload",
                    label_visibility="collapsed"
                )
                if jd_file:
                    st.success(f"✔ {jd_file.name}")
            else:
                jd_text = st.text_area(
                    "Job Description Text",
                    height=130,
                    placeholder="Paste the job description or role requirements here to check how well your resume matches...",
                    key="jd_text",
                    label_visibility="collapsed"
                )
                if jd_text:
                    st.caption(f"✔ {len(jd_text):,} characters entered")
        else:
            st.markdown(
                """
                <div style="font-weight: 700; font-size: 0.95rem; color: #0F172A; margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: space-between;">
                    <span>📋 What We Review</span>
                    <span class="badge-pill badge-indigo">5 Key Areas</span>
                </div>
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:1.25rem; font-size:0.875rem; color:#475569; line-height:1.6; min-height:152px; height:auto; display:flex; flex-direction:column; justify-content:center;">
                    <div style="font-weight:600; color:#334155;">Scoring standard recruitment criteria:</div>
                    <div style="margin-top:0.4rem; font-size:0.8rem; color:#64748B; line-height:1.65;">
                        • Layout & Formatting (20%) — Clean structure that scanners can easily parse<br>
                        • Keywords & Terms (25%) — In-demand skills and industry terminology<br>
                        • Impact & Measurable Results (25%) — Strong action verbs with clear metrics<br>
                        • Skills Backed by Projects (15%) — Real proof for listed skills<br>
                        • ATS Compatibility (15%) — Standard fonts, headers, and file format
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Action Execution Card
    access_token = st.session_state.get("access_token")

    if not resume_file:
        st.markdown(
            """
            <div style="background:#F8FAFC; border:1px dashed #CBD5E1; border-radius:12px; padding:1.75rem; text-align:center; color:#64748B;">
                <div style="font-size:1.5rem; margin-bottom:0.25rem;">📄</div>
                <div style="font-weight:600; font-size:0.95rem; color:#334155;">Upload your resume above to get your instant score and recommendations</div>
                <div style="font-size:0.8rem; color:#94A3B8; margin-top:2px;">Supports PDF and Word documents up to 5 MB</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.session_state.get("scorer_analysis"):
            st.markdown("---")
            display_results_dashboard(st.session_state["scorer_analysis"])
            _render_export_buttons(st.session_state["scorer_analysis"])
        return

    if not access_token:
        st.markdown(
            """
            <div style="background:#FFFBEB; border:1px solid #FDE68A; border-radius:12px; padding:1.25rem 1.5rem; margin-bottom:1rem; display:flex; align-items:center; justify-content:space-between;">
                <div>
                    <strong style="color:#92400E; font-size:0.95rem;">Please Sign In to Review</strong>
                    <div style="color:#78350F; font-size:0.85rem; margin-top:2px;">
                        Sign in via the left sidebar to analyze your resume and save it to your history.
                    </div>
                </div>
                <span class="badge-pill badge-amber">Sign In on Sidebar</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # Trigger Button
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        analyze = st.button("⚡  Analyze My Resume", use_container_width=True, type="primary")

    if not analyze:
        if st.session_state.get("scorer_analysis"):
            st.markdown("---")
            display_results_dashboard(st.session_state["scorer_analysis"])
            _render_export_buttons(st.session_state["scorer_analysis"])
        return

    # Fresh Run
    st.session_state.pop("scorer_pdf_bytes", None)
    st.session_state.pop("scorer_analysis", None)

    job_description = _read_jd(jd_file, jd_text) if analysis_mode == "Match with a Job Description" else ""

    try:
        with st.spinner("Reviewing your resume and checking ATS compatibility... (takes ~10 seconds)"):
            analysis = api_client.analyze_resume(
                resume_file=resume_file,
                access_token=access_token,
                job_description=job_description,
            )
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    st.session_state["scorer_analysis"] = analysis
    st.success("✔ Review complete! Here is your personalized feedback report below.")
    display_results_dashboard(analysis)
    _render_export_buttons(analysis)
