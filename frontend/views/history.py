import requests
import streamlit as st

from frontend.services import api_client
from frontend.components.dashboard import display_results_dashboard

def _show_backend_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the backend. Is it running on port 8000?")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        st.error(f"Backend returned {exc.response.status_code}: {exc.response.text}")
    else:
        st.error(f"Unexpected error: {exc}")

def render() -> None:
    st.markdown(
        """
        <div style="margin-bottom: 2rem;">
            <div style="display:inline-flex; align-items:center; gap:0.4rem; padding:0.25rem 0.75rem; background:#EEF2FF; border:1px solid #C7D2FE; border-radius:9999px; font-size:0.75rem; font-weight:700; color:#4F46E5; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.75rem;">
                <span style="width:6px; height:6px; border-radius:50%; background:#4F46E5;"></span>
                Saved Reviews // Track Your Progress
            </div>
            <h1 style="font-size: 2.25rem; font-weight: 800; color: #0F172A; margin: 0 0 0.5rem 0; letter-spacing: -0.025em;">
                My Saved Resume Reviews
            </h1>
            <p style="font-size: 1rem; color: #64748B; margin: 0; max-width: 720px; line-height: 1.6;">
                Review your past resume scores, track your progress as you edit, and revisit previous recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    access_token = st.session_state.get("access_token")
    if not access_token and st.query_params.get("preview") == "sample":
        history = [{
            "id": "sample-1",
            "filename": "Arg (3).pdf",
            "ats_score": 77.2,
            "created_at": "2026-10-15 18:30:00",
            "analysis_result": st.session_state.get("scorer_analysis", {})
        }]
    elif not access_token:
        st.markdown(
            """
            <div style="background:#FFFBEB; border:1px solid #FDE68A; border-radius:12px; padding:1.5rem; text-align:center;">
                <div style="font-size:1.8rem; margin-bottom:0.5rem;">🔒</div>
                <div style="font-weight:700; font-size:1.1rem; color:#92400E; margin-bottom:0.35rem;">Sign In to View Past Reviews</div>
                <div style="color:#78350F; font-size:0.9rem; max-width:480px; margin:0 auto 1rem auto;">
                    Sign in via the left sidebar to access your past resume reviews and track your improvements over time.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return
    else:
        try:
            history = api_client.get_history(access_token)
        except requests.RequestException as exc:
            _show_backend_error(exc)
            return

    if not history:
        st.markdown(
            """
            <div style="background:#FFFFFF; border:1px dashed #CBD5E1; border-radius:16px; padding:3.5rem 2rem; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
                <div style="font-size:2.5rem; margin-bottom:0.75rem;">📊</div>
                <h3 style="font-size:1.25rem; font-weight:800; color:#0F172A; margin:0 0 0.5rem 0;">No Saved Reviews Yet</h3>
                <p style="color:#64748B; font-size:0.95rem; max-width:460px; margin:0 auto 1.5rem auto;">
                    You haven't reviewed any resumes on this account yet. Upload a resume to get your first score and personalized suggestions!
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("🎯  Check a Resume Now", use_container_width=True, type="primary"):
                st.session_state.current_view = "scorer"
                st.query_params["view"] = "scorer"
                st.rerun()
        return

    # Calculate Summary Metrics
    scores = [float(entry.get("ats_score", 0)) for entry in history]
    avg_score = sum(scores) / len(scores) if scores else 0
    max_score = max(scores) if scores else 0

    st.markdown(
        f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:1.25rem 1.75rem; margin-bottom:1.5rem; display:grid; grid-template-columns:repeat(3, 1fr); gap:1.5rem; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <div>
                <div style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.05em;">Resumes Reviewed</div>
                <div style="font-family:'Plus Jakarta Sans', sans-serif; font-size:1.75rem; font-weight:800; color:#0F172A;">{len(history)}</div>
            </div>
            <div>
                <div style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.05em;">Average Score</div>
                <div style="font-family:'Plus Jakarta Sans', sans-serif; font-size:1.75rem; font-weight:800; color:#4F46E5;">{avg_score:.0f} / 100</div>
            </div>
            <div>
                <div style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.05em;">Highest Score</div>
                <div style="font-family:'Plus Jakarta Sans', sans-serif; font-size:1.75rem; font-weight:800; color:#10B981;">{max_score:.0f} / 100</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Render History Cards
    for idx, entry in enumerate(history):
        filename = entry.get("filename", "resume.pdf")
        ats_score = float(entry.get("ats_score", 0))
        created_at = str(entry.get("created_at", ""))[:19].replace("T", " ")
        analysis = entry.get("analysis_result", {}) or {}
        component_scores = analysis.get("component_scores", {}) or {}
        jd_comparison = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")

        score_color = "#10B981" if ats_score >= 85 else "#4F46E5" if ats_score >= 70 else "#F59E0B" if ats_score >= 50 else "#EF4444"

        with st.expander(f"📄  {filename}  •  Score: {ats_score:.0f}/100  •  {created_at}"):
            # Top card row inside expander
            c_score, c_breakdown = st.columns([1, 2])
            with c_score:
                st.markdown(
                    f"""
                    <div style="text-align:center; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.25rem;">
                        <div style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase;">Overall Score</div>
                        <div style="font-family:'Plus Jakarta Sans', sans-serif; font-size:3rem; font-weight:800; color:{score_color}; line-height:1.1;">{ats_score:.0f}</div>
                        <div style="font-size:0.75rem; color:#64748B;">/ 100</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with c_breakdown:
                st.markdown(
                    f"""
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; font-size:0.85rem;">
                        <div style="background:#F8FAFC; padding:8px; border-radius:6px; border:1px solid #E2E8F0;">
                            Formatting: <strong>{component_scores.get('formatting', 0):.0f}/20</strong>
                        </div>
                        <div style="background:#F8FAFC; padding:8px; border-radius:6px; border:1px solid #E2E8F0;">
                            Keywords: <strong>{component_scores.get('keywords', 0):.0f}/25</strong>
                        </div>
                        <div style="background:#F8FAFC; padding:8px; border-radius:6px; border:1px solid #E2E8F0;">
                            Content: <strong>{component_scores.get('content', 0):.0f}/25</strong>
                        </div>
                        <div style="background:#F8FAFC; padding:8px; border-radius:6px; border:1px solid #E2E8F0;">
                            Skill Proof: <strong>{component_scores.get('skill_validation', 0):.0f}/15</strong>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if jd_comparison:
                    match_p = float(jd_comparison.get("match_percentage", 0))
                    st.markdown(f"<div style='margin-top:6px; font-size:0.85rem;'>🎯 <strong>Target Job Match:</strong> {match_p:.0f}%</div>", unsafe_allow_html=True)

            c_act1, c_act2 = st.columns([3, 1])
            with c_act1:
                if st.button("🔍 View Full Report", key=f"load_{idx}"):
                    st.session_state["scorer_analysis"] = analysis
                    st.session_state.current_view = "scorer"
                    st.query_params["view"] = "scorer"
                    st.rerun()
            with c_act2:
                entry_id = entry.get("id")
                if entry_id:
                    if st.button("🗑️ Delete", key=f"del_{idx}"):
                        try:
                            api_client.delete_history_entry(str(entry_id), access_token)
                            st.success("Entry removed.")
                            st.rerun()
                        except requests.RequestException as exc:
                            _show_backend_error(exc)
