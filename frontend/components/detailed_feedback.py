import textwrap
from typing import Any, Dict, List
import streamlit as st

SEVERITY_ORDER = ["critical", "high", "medium", "low"]

SEVERITY_META = {
    "critical": {"label": "High Priority Fixes", "icon": "🚨", "bg": "#FEF2F2", "color": "#991B1B", "border": "#FECACA"},
    "high":     {"label": "Recommended Improvements", "icon": "⚠️", "bg": "#FFF7ED", "color": "#9A3412", "border": "#FED7AA"},
    "medium":   {"label": "Helpful Suggestions", "icon": "💡", "bg": "#FFFBEB", "color": "#92400E", "border": "#FDE68A"},
    "low":      {"label": "Minor Touchups", "icon": "✨", "bg": "#ECFDF5", "color": "#065F46", "border": "#A7F3D0"},
}

def _normalize_level(raw_level: str) -> str:
    level = (raw_level or "low").lower().strip()
    if level in ("critical", "urgent", "blocker"):
        return "critical"
    if level in ("high", "major", "warning"):
        return "high"
    if level in ("moderate", "medium", "normal"):
        return "medium"
    return "low"

def _group_by_severity(issues: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {level: [] for level in SEVERITY_ORDER}
    for issue in issues:
        norm = _normalize_level(issue.get("severity_level", ""))
        grouped[norm].append(issue)
    return grouped

def _render_issue(issue: Dict[str, Any]) -> None:
    level = _normalize_level(issue.get("severity_level", ""))
    meta = SEVERITY_META.get(level, SEVERITY_META["low"])
    title = issue.get("issue_title", "Suggestion")
    impact = issue.get("ats_impact", "")
    explanation = issue.get("explanation", "")
    where = issue.get("where_it_appears", "")
    how_to_fix = issue.get("how_to_fix", "")
    action_items = issue.get("action_items") or []
    example = issue.get("example_improvement", "")

    impact_badge = f'<span style="font-size:0.775rem; color:#64748B; font-weight:500;">Why it matters: {impact}</span>' if impact else ''
    banner = textwrap.dedent(f"""
<div style="background:{meta['bg']}; border-left:4px solid {meta['color']}; border:1px solid {meta['border']}; border-left-width:4px; border-radius:8px; padding:0.85rem 1.15rem; margin-bottom:0.5rem; display:flex; justify-content:space-between; align-items:center;">
    <div style="display:flex; align-items:center; gap:0.6rem;">
        <span style="font-size:1.1rem;">{meta['icon']}</span>
        <span style="font-weight:700; font-size:0.95rem; color:{meta['color']};">{title}</span>
    </div>
    {impact_badge}
</div>
""")
    st.markdown(banner, unsafe_allow_html=True)

    with st.expander("💡 How to fix this & example rewrite", expanded=False):
        if explanation:
            st.markdown(f"**Why this matters:** {explanation}")
        if where:
            st.markdown(f"**Where we found it:** `{where}`")
        if how_to_fix:
            st.markdown(f"**How to fix it:** {how_to_fix}")
        if action_items:
            st.markdown("**Steps to take:**")
            for item in action_items:
                st.markdown(f"- {item}")
        if example:
            st.markdown("**Example rewrite (Before & After):**")
            st.code(example, language="text")

def display_detailed_feedback(analysis: Dict[str, Any]) -> None:
    issues = analysis.get("detailed_feedback") or []
    if not issues:
        return

    header_html = textwrap.dedent("""
<div style="margin: 1.5rem 0 1rem 0;">
    <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;">In-Depth Feedback</div>
    <h3 style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin: 0;">Step-by-Step Fixes for Each Issue</h3>
</div>
""")
    st.markdown(header_html, unsafe_allow_html=True)

    grouped = _group_by_severity(issues)
    for level in SEVERITY_ORDER:
        items = grouped.get(level, [])
        if not items:
            continue
        meta = SEVERITY_META.get(level, SEVERITY_META["low"])
        category_header = textwrap.dedent(f"""
<div style="display:flex; align-items:center; gap:0.5rem; margin:1.25rem 0 0.5rem 0;">
    <span style="font-weight:800; font-size:0.9rem; color:{meta['color']}; text-transform:uppercase; letter-spacing:0.05em;">
        {meta['label']}
    </span>
    <span class="badge-pill" style="background:{meta['bg']}; color:{meta['color']}; border:1px solid {meta['border']};">
        {len(items)} Issue{'s' if len(items) > 1 else ''}
    </span>
</div>
""")
        st.markdown(category_header, unsafe_allow_html=True)
        for issue in items:
            _render_issue(issue)
