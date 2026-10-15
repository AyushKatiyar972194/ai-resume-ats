import textwrap
from typing import Any, Dict
import streamlit as st

def display_skill_validation(analysis: Dict[str, Any]) -> None:
    details = analysis.get("skill_validation_details") or {}
    validated = details.get("validated", [])
    unvalidated = details.get("unvalidated", [])
    total = details.get("total", len(validated) + len(unvalidated))
    pct = details.get("validation_pct", 0.0)

    header_html = textwrap.dedent("""
<div style="margin: 1.5rem 0 1rem 0;">
    <div style="font-size: 0.775rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;">Proof-Of-Work Verification</div>
    <h3 style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin: 0;">Contextual Skill Proof Analysis</h3>
</div>
""")
    st.markdown(header_html, unsafe_allow_html=True)

    if total == 0:
        st.info("No technical or domain skills extracted from the resume text.")
        return

    rate_color = "#10B981" if pct >= 70 else "#F59E0B" if pct >= 50 else "#EF4444"
    status_label = "Optimal Evidence" if pct >= 70 else "Moderate Risk" if pct >= 50 else "High Unsubstantiated Risk"
    badge_bg = '#ECFDF5' if pct >= 70 else '#FFFBEB' if pct >= 50 else '#FEF2F2'
    badge_border = '#A7F3D0' if pct >= 70 else '#FDE68A' if pct >= 50 else '#FECACA'

    metrics_html = textwrap.dedent(f"""
<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.25rem 1.75rem; margin-bottom: 1.25rem; display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
    <div>
        <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">Total Skills Extracted</div>
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.75rem; font-weight: 800; color: #0F172A;">{total}</div>
        <div style="font-size: 0.775rem; color: #64748B;">From skills section</div>
    </div>
    <div>
        <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">Demonstrated in Projects</div>
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.75rem; font-weight: 800; color: #10B981;">{len(validated)}</div>
        <div style="font-size: 0.775rem; color: #047857;">Backed by work bullets</div>
    </div>
    <div>
        <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">Proof Rate</div>
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.75rem; font-weight: 800; color: {rate_color};">{pct:.0f}%</div>
        <div style="font-size: 0.775rem; color: #64748B;">Benchmark: 70%+</div>
    </div>
    <div>
        <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">ATS Proof Status</div>
        <div style="margin-top: 6px;">
            <span class="badge-pill" style="background:{badge_bg}; color:{rate_color}; border:1px solid {badge_border};">
                ● {status_label}
            </span>
        </div>
    </div>
</div>
""")
    st.markdown(metrics_html, unsafe_allow_html=True)

    tab1, tab2 = st.tabs([
        f"✔ Validated with Proof ({len(validated)})",
        f"⚠️ Listed Without Proof ({len(unvalidated)})"
    ])

    with tab1:
        if validated:
            chips = "".join([
                f'<span class="keyword-chip chip-match">✔ {entry.get("skill", "")}</span>'
                for entry in validated
            ])
            st.markdown(f'<div class="chips-cloud" style="margin-bottom: 1rem;">{chips}</div>', unsafe_allow_html=True)
            with st.expander("🔍 Inspect Project-to-Skill Semantic Evidence", expanded=False):
                for entry in validated:
                    skill = entry.get("skill", "")
                    projects = entry.get("projects", []) or []
                    similarity = entry.get("similarity")
                    p_text = ", ".join(projects[:3]) if projects else "Experience narrative"
                    sim_str = f" ({similarity*100:.0f}% semantic confidence)" if isinstance(similarity, (int, float)) else ""
                    st.markdown(f"- **{skill}** demonstrated in: `{p_text}`{sim_str}")
        else:
            st.info("No skills are currently validated with explicit project evidence in your resume description bullets.")

    with tab2:
        if unvalidated:
            st.caption("These skills appear in your skills list but lack corresponding proof in your project or experience bullets:")
            chips = "".join([
                f'<span class="keyword-chip chip-missing">⚠️ {skill}</span>'
                for skill in unvalidated
            ])
            st.markdown(f'<div class="chips-cloud" style="margin-bottom: 1rem;">{chips}</div>', unsafe_allow_html=True)
            st.info("💡 **Quick ROI Win:** Choose 3–4 of the above unvalidated skills and explicitly integrate them into your recent work experience or project bullets to increase your ATS proof score.")
        else:
            st.success("🎉 Outstanding! 100% of your listed skills are backed with demonstrable project proof.")
