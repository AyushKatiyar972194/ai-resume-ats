from typing import Any, Dict, List, Tuple
import streamlit as st

SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def _collect_action_items(analysis: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Return list of (severity, source_title, action_text)."""
    items: List[Tuple[str, str, str]] = []

    for issue in analysis.get("detailed_feedback") or []:
        level = (issue.get("severity_level") or "low").lower()
        title = issue.get("issue_title", "")
        for action in issue.get("action_items") or []:
            items.append((level, title, action))

    if not items:
        for suggestion in analysis.get("suggestions") or []:
            items.append(("medium", "General", suggestion))

    items.sort(key=lambda row: SEVERITY_RANK.get(row[0], 99))
    return items

def display_action_items(analysis: Dict[str, Any]) -> None:
    items = _collect_action_items(analysis)
    if not items:
        return

    st.markdown("### ⚡ Prioritized Action Checklist")
    st.caption("Concrete, high-ROI edits to maximize your resume score before applying.")

    color_map = {
        "critical": ("#ef4444", "#fef2f2", "🔴"),
        "high": ("#f97316", "#fff7ed", "🟠"),
        "medium": ("#f59e0b", "#fffbeb", "🟡"),
        "low": ("#10b981", "#ecfdf5", "🟢"),
    }

    for i, (level, source, action) in enumerate(items, 1):
        border_col, bg_col, icon = color_map.get(level, ("#64748b", "#f8fafc", "⚪"))
        st.markdown(
            f"""
            <div style="background:{bg_col}; border-left:4px solid {border_col}; padding:10px 14px;
                        border-radius:6px; margin-bottom:8px; font-size:14px; display:flex; align-items:center;">
                <span style="font-size:16px; margin-right:10px;">{icon}</span>
                <div>
                    <strong style="color:#0f172a;">{source}:</strong>
                    <span style="color:#334155; margin-left:4px;">{action}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
