import math
import textwrap
from typing import Any, Dict
import streamlit as st

COMPONENTS = [
    ("Formatting & Structure", "formatting", 20, "📐", "Evaluates layout, font choice, sections, and parseability."),
    ("Keywords & Industry Terms", "keywords", 25, "🔑", "Assesses technical depth, hard skills, and domain taxonomy."),
    ("Content Quality & Impact", "content", 25, "📈", "Measures action verbs, metrics, business results, and clarity."),
    ("Skill Proof Validation", "skill_validation", 15, "🛡️", "Verifies claimed skills against real experience bullets."),
    ("ATS Filter Compliance", "ats_compatibility", 15, "🤖", "Tests against table traps, unreadable glyphs, and column bugs."),
]

def _get_tier_info(score: float):
    if score >= 85:
        return {
            "tier": "Top 10% Candidate (Interview Ready)",
            "color": "#10B981",
            "bg": "#ECFDF5",
            "border": "#A7F3D0",
            "percentile": "Top 8th Percentile",
            "desc": "Your resume displays superior ATS compatibility, strong keyword density, and clear impact metrics."
        }
    elif score >= 70:
        return {
            "tier": "Competitive Profile (Minor Polish Needed)",
            "color": "#4F46E5",
            "bg": "#EEF2FF",
            "border": "#C7D2FE",
            "percentile": "Top 28th Percentile",
            "desc": "Solid foundation that passes most automated filters. Address the flagged items to reach the 90+ interview tier."
        }
    elif score >= 50:
        return {
            "tier": "Average Profile (Significant Filter Risk)",
            "color": "#F59E0B",
            "bg": "#FFFBEB",
            "border": "#FDE68A",
            "percentile": "50th Percentile",
            "desc": "At risk of automated rejection by strict ATS systems (Workday, Taleo). Key technical terms and quantified results are missing."
        }
    else:
        return {
            "tier": "Critical Hazard (Overhaul Required)",
            "color": "#EF4444",
            "bg": "#FEF2F2",
            "border": "#FECACA",
            "percentile": "Bottom 20th Percentile",
            "desc": "Major formatting or keyword deficiencies detected. Automated screeners will likely reject this resume before a human sees it."
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
        <div class="score-tier-headline">ATS Pass Probability: {score_clamped:.0f}%</div>
        <div class="score-interpretation-text">{interpretation}</div>
        <div style="display: flex; gap: 1rem; font-size: 0.8rem; color: #64748B;">
            <span>📐 5 Vectors Evaluated</span>
            <span>•</span>
            <span>🤖 Fortune 500 Calibrated</span>
            <span>•</span>
            <span>⚡ Deterministic Weights</span>
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
            status_chip = '<span class="badge-pill badge-emerald">OPTIMIZED</span>'
            bar_color = "linear-gradient(90deg, #10B981, #34D399)"
        elif pct >= 60:
            status_chip = '<span class="badge-pill badge-amber">ACCEPTABLE</span>'
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
    <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;">Dimension Analysis</div>
    <h3 style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin: 0;">5-Vector Component Breakdown</h3>
</div>
<div class="breakdown-grid">
    {''.join(cards_html)}
</div>
""")
    st.markdown(full_html, unsafe_allow_html=True)
