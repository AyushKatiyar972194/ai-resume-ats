import textwrap
from typing import Any, Dict, List
import streamlit as st

def display_strengths_and_issues(analysis: Dict[str, Any]) -> None:
    """Side-by-side comparative layout for Strengths vs Critical Issues."""
    strengths: List[str] = analysis.get("strengths") or []
    critical: List[str] = analysis.get("critical_issues") or []
    summary: List[str] = analysis.get("issues_summary") or []

    # Build Left Column: Strengths
    if strengths:
        strengths_html = "".join([
            f'<div class="bullet-item"><span style="color:#10B981; font-weight:700; font-size:1.1rem; flex-shrink:0;">✔</span><span>{item}</span></div>'
            for item in strengths
        ])
    else:
        strengths_html = '<div style="padding:1.5rem; text-align:center; color:#64748B; font-size:0.9rem;">No clear strengths identified yet. Apply the recommended fixes below to elevate your resume.</div>'

    # Build Right Column: Issues
    combined_issues = list(critical)
    for extra in summary:
        if extra not in combined_issues:
            combined_issues.append(extra)

    if combined_issues:
        issues_html = "".join([
            f'<div class="bullet-item"><span style="color:#EF4444; font-weight:700; font-size:1rem; flex-shrink:0;">⚠️</span><span>{item}</span></div>'
            for item in combined_issues
        ])
    else:
        issues_html = '<div style="padding:1.5rem; text-align:center; color:#059669; font-size:0.9rem; font-weight:600;">🎉 Zero critical ATS bottlenecks detected! Your resume formatting and content structure are clean.</div>'

    html = textwrap.dedent(f"""
<div style="margin: 1.5rem 0 1rem 0;">
    <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;">Diagnostic Balance</div>
    <h3 style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin: 0;">Key Strengths vs Critical Bottlenecks</h3>
</div>
<div class="comparison-grid">
    <div class="comparison-card">
        <div class="comparison-header">
            <span style="width:28px; height:28px; border-radius:6px; background:#ECFDF5; color:#059669; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.9rem;">✔</span>
            <span class="comparison-title" style="color:#065F46;">Competitive Strengths ({len(strengths)})</span>
        </div>
        {strengths_html}
    </div>
    <div class="comparison-card">
        <div class="comparison-header">
            <span style="width:28px; height:28px; border-radius:6px; background:#FEF2F2; color:#DC2626; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.9rem;">!</span>
            <span class="comparison-title" style="color:#991B1B;">Flagged ATS Bottlenecks ({len(combined_issues)})</span>
        </div>
        {issues_html}
    </div>
</div>
""")
    st.markdown(html, unsafe_allow_html=True)

def display_strengths(strengths: List[str]) -> None:
    pass

def display_critical_issues(analysis: Dict[str, Any]) -> None:
    pass
