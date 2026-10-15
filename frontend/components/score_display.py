import math
import textwrap
from typing import Any, Dict
import streamlit as st

COMPONENTS = [
    ("Layout & Formatting", "formatting", 20, "📐", "How clearly sections, headings, and fonts are organized."),
    ("Keywords & Skills", "keywords", 25, "🔑", "Relevant industry terms and technologies found in your resume."),
    ("Impact & Action Verbs", "content", 25, "📈", "Clear bullet points with measurable results and active language."),
    ("Skills Backed by Projects", "skill_validation", 15, "🛡️", "Whether listed skills are supported by real project examples."),
    ("ATS Readability", "ats_compatibility", 15, "🤖", "Ensures your resume won't get scrambled by hiring software."),
]

def _get_tier_info(score: float):
    if score >= 85:
        return {
            "tier": "Interview Ready!",
            "color": "#10B981",
            "bg": "#ECFDF5",
            "border": "#A7F3D0",
            "percentile": "Top 10% Candidate",
            "desc": "Your resume looks great! It is easy for ATS scanners to read, includes strong keywords, and highlights measurable results."
        }
    elif score >= 70:
        return {
            "tier": "Competitive Profile",
            "color": "#4F46E5",
            "bg": "#EEF2FF",
            "border": "#C7D2FE",
            "percentile": "Good Foundation",
            "desc": "Solid foundation! You're in good shape for most job applications. Making a few recommended tweaks can help you reach the top tier."
        }
    elif score >= 50:
        return {
            "tier": "Needs Some Polish",
            "color": "#F59E0B",
            "bg": "#FFFBEB",
            "border": "#FDE68A",
            "percentile": "Moderate Match",
            "desc": "Your resume may get overlooked by automated filters. Adding more specific keywords and measurable achievements will help it stand out."
        }
    else:
        return {
            "tier": "Needs Attention",
            "color": "#EF4444",
            "bg": "#FEF2F2",
            "border": "#FECACA",
            "percentile": "Action Recommended",
            "desc": "Your resume is missing important keywords or has formatting issues that could prevent recruiters from seeing your full potential."
        }

def display_overall_score(analysis: Dict[str, Any]) -> None:
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    score_clamped = max(0.0, min(100.0, score))
    tier = _get_tier_info(score_clamped)
    
    radius = 72
    circumference = 2 * math.pi * radius
    dash_offset = circumference - (circumference * (score_clamped / 100.0))
    interpretation = analysis.get("interpretation") or tier["desc"]

    html = textwrap.dedent(f"""
<div class="score-hero-card">
    <div class="score-radial-wrapper">
        <svg class="score-radial-svg" viewBox="0 0 180 180">
            <circle class="score-radial-bg" cx="90" cy="90" r="{radius}" />
            <circle class="score-radial-fill" cx="90" cy="90" r="{radius}"
                    stroke="{tier['color']}"
                    stroke-dasharray="{circumference:.2f}"
                    stroke-dashoffset="{dash_offset:.2f}" />
        </svg>
        <div class="score-radial-text">
            <div class="score-radial-number" style="color: {tier['color']};">{score_clamped:.0f}</div>
            <div class="score-radial-denominator">/ 100</div>
        </div>
    </div>
    <div class="score-details-col">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
            <span class="badge-pill" style="background:{tier['bg']}; color:{tier['color']}; border:1px solid {tier['border']};">
                ● {tier['tier']}
            </span>
            <span style="font-size: 0.8rem; font-weight: 600; color: #64748B;">
                {tier['percentile']}
            </span>
        </div>
        <div class="score-tier-headline">Overall Resume Strength: {score_clamped:.0f} / 100</div>
        <div class="score-interpretation-text">{interpretation}</div>
        <div style="display: flex; gap: 1rem; font-size: 0.8rem; color: #64748B;">
            <span>📐 5 Core Areas Checked</span>
            <span>•</span>
            <span>🎯 Recruiter Friendly</span>
            <span>•</span>
            <span>💡 Actionable Feedback</span>
        </div>
    </div>
</div>
""")
    st.markdown(html, unsafe_allow_html=True)

def display_score_breakdown(analysis: Dict[str, Any]) -> None:
    component_scores = analysis.get("component_scores") or {}
    
    cards_html = []
    for label, key, max_score, icon, desc in COMPONENTS:
        val = float(component_scores.get(key, 0))
        val_clamped = max(0.0, min(float(max_score), val))
        pct = (val_clamped / max_score) * 100.0 if max_score else 0

        if pct >= 80:
            status_chip = '<span class="badge-pill badge-emerald">GREAT</span>'
            bar_color = "linear-gradient(90deg, #10B981, #34D399)"
        elif pct >= 60:
            status_chip = '<span class="badge-pill badge-amber">GOOD</span>'
            bar_color = "linear-gradient(90deg, #F59E0B, #FBBF24)"
        else:
            status_chip = '<span class="badge-pill badge-rose">NEEDS WORK</span>'
            bar_color = "linear-gradient(90deg, #EF4444, #F87171)"

        cards_html.append(textwrap.dedent(f"""
<div class="breakdown-item-card">
    <div class="breakdown-item-top">
        <div style="display:flex; align-items:center; gap:0.5rem;">
            <span style="font-size: 1.1rem;">{icon}</span>
            <span class="breakdown-item-label">{label}</span>
        </div>
        <div style="display:flex; align-items:center; gap:0.5rem;">
            <span class="breakdown-item-val" style="color: #0F172A;">{val_clamped:.0f}/{max_score}</span>
            {status_chip}
        </div>
    </div>
    <div class="breakdown-track">
        <div class="breakdown-bar" style="width: {pct:.1f}%; background: {bar_color};"></div>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.35rem;">
        <span class="breakdown-item-sub">{desc}</span>
        <span style="font-size:0.75rem; font-weight:700; color:#64748B;">{pct:.0f}%</span>
    </div>
</div>
""").strip())

    full_html = textwrap.dedent(f"""
<div style="margin: 1.5rem 0 1rem 0;">
    <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;">Score Breakdown</div>
    <h3 style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin: 0;">How You Scored Across 5 Key Areas</h3>
</div>
<div class="breakdown-grid">
    {''.join(cards_html)}
</div>
""")
    st.markdown(full_html, unsafe_allow_html=True)
