from typing import Any, Dict
import streamlit as st

def display_skill_validation(analysis: Dict[str, Any]) -> None:
    details = analysis.get("skill_validation_details") or {}
    validated = details.get("validated", [])
    unvalidated = details.get("unvalidated", [])
    total = details.get("total", len(validated) + len(unvalidated))
    pct = details.get("validation_pct", 0.0)

    st.markdown("### ✅ Skill Validation & Proof")
    st.caption("ATS algorithms and recruiters verify whether your listed skills are backed by projects or work experience.")

    if total == 0:
        st.info("No skills detected on the resume.")
        return

    # Metric summary cards
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Skills", total)
    c2.metric("Validated with Proof", len(validated), delta=f"{len(validated)} demonstrated")
    c3.metric("Proof Rate", f"{pct:.1f}%", delta=f"{pct - 70:.1f}% vs Target 70%", delta_color="normal" if pct >= 70 else "inverse")

    st.progress(min(max(pct / 100.0, 0.0), 1.0))

    tab1, tab2 = st.tabs([f"✅ Validated Skills ({len(validated)})", f"⚠️ Needs Supporting Evidence ({len(unvalidated)})"])

    with tab1:
        if validated:
            st.markdown(
                "".join([
                    f"<span style='display:inline-block; background-color:#dcfce7; color:#15803d; border:1px solid #bbf7d0; "
                    f"padding:5px 12px; border-radius:16px; margin:4px; font-size:13px; font-weight:600;'>✔ {entry.get('skill', '')}</span>"
                    for entry in validated
                ]),
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🔍 View Project-to-Skill Evidence Mapping", expanded=False):
                for entry in validated:
                    skill = entry.get("skill", "?")
                    projects = entry.get("projects", []) or []
                    similarity = entry.get("similarity")
                    project_text = ", ".join(projects[:3]) if projects else "experience section"
                    sim_text = f" • *{similarity * 100:.0f}% confidence*" if isinstance(similarity, (int, float)) else ""
                    st.markdown(f"- **{skill}** demonstrated in: `{project_text}`{sim_text}")
        else:
            st.info("No skills currently backed by project or experience descriptions.")

    with tab2:
        if unvalidated:
            st.warning(
                "These skills are listed in your skills section but never mentioned in your projects or work experience bullets. "
                "Incorporate them into your project descriptions to boost your score to 90+!"
            )
            st.markdown(
                "".join([
                    f"<span style='display:inline-block; background-color:#fee2e2; color:#b91c1c; border:1px solid #fecaca; "
                    f"padding:5px 12px; border-radius:16px; margin:4px; font-size:13px; font-weight:600;'>⚠️ {skill}</span>"
                    for skill in unvalidated
                ]),
                unsafe_allow_html=True
            )
        else:
            st.success("🎉 Outstanding! 100% of your listed skills are validated with project evidence.")
