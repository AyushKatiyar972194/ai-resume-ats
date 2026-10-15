import textwrap
from typing import Any, Dict, List, Tuple
import streamlit as st

SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def _normalize_level(raw_level: str) -> str:
    level = (raw_level or "low").lower().strip()
    if level in ("critical", "urgent", "blocker"):
        return "critical"
    if level in ("high", "major", "warning"):
        return "high"
    if level in ("moderate", "medium", "normal"):
        return "medium"
    return "low"

def _collect_action_items(analysis: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    items: List[Tuple[str, str, str]] = []

    for issue in analysis.get("detailed_feedback") or []:
        norm = _normalize_level(issue.get("severity_level", ""))
        title = issue.get("issue_title", "General")
        for action in issue.get("action_items") or []:
            items.append((norm, title, action))

    if not items:
        for suggestion in analysis.get("suggestions") or []:
            items.append(("medium", "Optimization", suggestion))

    items.sort(key=lambda row: SEVERITY_RANK.get(row[0], 99))
    return items

def display_action_items(analysis: Dict[str, Any]) -> None:
    items = _collect_action_items(analysis)
    if not items:
        return

    tag_styles = {
        "critical": ("background:#FEF2F2; color:#991B1B; border:1px solid #FECACA;", "🔴 CRITICAL"),
        "high":     ("background:#FFF7ED; color:#9A3412; border:1px solid #FED7AA;", "🟠 HIGH"),
        "medium":   ("background:#FFFBEB; color:#92400E; border:1px solid #FDE68A;", "🟡 MODERATE"),
        "low":      ("background:#ECFDF5; color:#065F46; border:1px solid #A7F3D0;", "🟢 LOW"),
    }

    cards_html = []
    for i, (level, source, action) in enumerate(items[:8], 1):
        style, label = tag_styles.get(level, tag_styles["low"])
        card = f'<div class="action-item-card"><span class="action-priority-tag" style="{style}">{label}</span><div style="flex:1;"><div style="font-size:0.85rem; font-weight:700; color:#0F172A; margin-bottom:2px;">{source}</div><div style="font-size:0.875rem; color:#334155; line-height:1.5;">{action}</div></div></div>'
        cards_html.append(card)

    full_html = textwrap.dedent(f"""
<div style="margin: 1.5rem 0 1rem 0;">
    <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;">Tactical Edits</div>
    <h3 style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin: 0;">Prioritized Action Checklist</h3>
</div>
{''.join(cards_html)}
""")
    st.markdown(full_html, unsafe_allow_html=True)
