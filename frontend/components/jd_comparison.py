from typing import Any, Dict, Optional
import streamlit as st

def display_jd_comparison(jd_comparison: Optional[Dict[str, Any]]) -> None:
    if not jd_comparison:
        return

    st.markdown(
        """
        <div style="margin: 1.5rem 0 1rem 0;">
            <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;">Job Match</div>
            <h3 style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin: 0;">How Well Your Resume Fits This Job Posting</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    match_pct = float(jd_comparison.get("match_percentage", 0))
    semantic = float(jd_comparison.get("semantic_similarity", 0))
    matched = jd_comparison.get("matched_keywords", []) or []
    missing = jd_comparison.get("missing_keywords", []) or []
    gap = jd_comparison.get("skills_gap", []) or []

    match_color = "#10B981" if match_pct >= 75 else "#4F46E5" if match_pct >= 55 else "#EF4444"
    match_status = "Strong Match" if match_pct >= 75 else "Moderate Match" if match_pct >= 55 else "Low Alignment"

    # Top Metrics Banner
    st.markdown(
        f"""
        <div class="jd-metrics-banner">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.85rem; font-weight: 700; color: #0F172A;">Matching Keywords</span>
                    <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.5rem; font-weight: 800; color: {match_color};">{match_pct:.0f}%</span>
                </div>
                <div class="breakdown-track">
                    <div class="breakdown-bar" style="width: {min(100.0, match_pct):.1f}%; background: {match_color};"></div>
                </div>
                <div style="font-size: 0.775rem; color: #64748B; margin-top: 0.35rem;">
                    Exact skills, tools, and terms from the job posting found in your resume.
                </div>
            </div>
            <div>
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.85rem; font-weight: 700; color: #0F172A;">Experience Match</span>
                    <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.5rem; font-weight: 800; color: #6366F1;">{semantic * 100:.0f}%</span>
                </div>
                <div class="breakdown-track">
                    <div class="breakdown-bar" style="width: {min(100.0, semantic * 100):.1f}%; background: linear-gradient(90deg, #4F46E5, #06B6D4);"></div>
                </div>
                <div style="font-size: 0.775rem; color: #64748B; margin-top: 0.35rem;">
                    How closely your overall work experience aligns with the job requirements.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Keywords Columns
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.25rem 1.5rem; height: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #F1F5F9;">
                    <span style="font-weight: 700; font-size: 0.95rem; color: #065F46;">✔ Matching Keywords ({len(matched)})</span>
                    <span class="badge-pill badge-emerald">In Resume</span>
                </div>
                <div class="chips-cloud">
                    {''.join([f'<span class="keyword-chip chip-match">✔ {kw}</span>' for kw in matched[:20]]) if matched else '<span style="color:#64748B; font-size:0.85rem;">No exact keyword matches found.</span>'}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_r:
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.25rem 1.5rem; height: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid #F1F5F9;">
                    <span style="font-weight: 700; font-size: 0.95rem; color: #991B1B;">⚠️ Missing Keywords ({len(missing)})</span>
                    <span class="badge-pill badge-rose">Recommended to Add</span>
                </div>
                <div class="chips-cloud">
                    {''.join([f'<span class="keyword-chip chip-missing">❌ {kw}</span>' for kw in missing[:20]]) if missing else '<span style="color:#059669; font-size:0.85rem;">All primary job keywords are included in your resume!</span>'}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if gap:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 10px; padding: 1rem 1.25rem; font-size: 0.875rem;">
                <strong style="color: #92400E;">💡 Recommended Skills to Add:</strong>
                <span style="color: #78350F; margin-left: 6px;">The job posting emphasizes: <strong>{', '.join(gap[:8])}</strong>. If you have experience with these, try adding them to your resume summary or bullet points.</span>
            </div>
            """,
            unsafe_allow_html=True
        )
