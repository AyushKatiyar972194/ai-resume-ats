import textwrap
from typing import Any, Dict
import streamlit as st

def display_recommendations(analysis: Dict[str, Any]) -> None:
    suggestions = analysis.get("suggestions") or []
    if not suggestions:
        return

    items_html = "".join([
        f'<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.9rem 1.25rem; margin-bottom:0.6rem; display:flex; align-items:flex-start; gap:0.75rem; box-shadow:0 1px 2px rgba(0,0,0,0.04);"><span style="color:#4F46E5; font-size:1.1rem; line-height:1.4;">💡</span><span style="font-size:0.9rem; color:#334155; line-height:1.5;">{s}</span></div>'
        for s in suggestions
    ])

    full_html = textwrap.dedent(f"""
<div style="margin: 1.5rem 0 1rem 0;">
    <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;">Strategic Advisory</div>
    <h3 style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin: 0;">Long-Term Profile Recommendations</h3>
</div>
{items_html}
""")
    st.markdown(full_html, unsafe_allow_html=True)
