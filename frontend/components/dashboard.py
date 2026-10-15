import textwrap
from typing import Any, Dict
import streamlit as st

from frontend.components.score_display import display_overall_score, display_score_breakdown
from frontend.components.strengths_issues import display_strengths_and_issues
from frontend.components.skill_validation import display_skill_validation
from frontend.components.jd_comparison import display_jd_comparison
from frontend.components.detailed_feedback import display_detailed_feedback
from frontend.components.action_items import display_action_items
from frontend.components.recommendations import display_recommendations

def display_results_dashboard(analysis: Dict[str, Any]) -> None:
    """
    Render the comprehensive ATS results dashboard.
    """
    # Top Header Bar
    header_html = textwrap.dedent("""
<div class="results-header-bar">
    <div>
        <div class="results-meta-title">Resume Review Report</div>
        <div class="results-meta-subtitle">Detailed feedback and suggestions based on standard recruiter screening criteria</div>
    </div>
    <div style="display:flex; align-items:center; gap:0.75rem;">
        <span class="badge-pill badge-emerald">✔ Review Complete</span>
        <span style="font-size:0.8rem; font-weight:600; color:#64748B;">AI Assistant Ready</span>
    </div>
</div>
""")
    st.markdown(header_html, unsafe_allow_html=True)

    # 1. Executive Overall Score Gauge
    display_overall_score(analysis)

    # 2. 5-Vector Component Scores
    display_score_breakdown(analysis)

    # 3. Strengths vs Bottlenecks Comparative Grid
    display_strengths_and_issues(analysis)

    # 4. Contextual Skill Proofing
    display_skill_validation(analysis)

    # 5. Targeted JD Comparison (if provided)
    jd_comparison = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
    if jd_comparison:
        display_jd_comparison(jd_comparison)

    # 6. Prioritized Action Checklist
    display_action_items(analysis)

    # 7. Deep Diagnostic Audit
    display_detailed_feedback(analysis)

    # 8. Strategic Long-Term Advisory
    display_recommendations(analysis)
