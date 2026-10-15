import streamlit as st
import sys
from pathlib import Path

# Put the repo root on sys.path so `from frontend.views import ...` resolves
# regardless of the directory streamlit was launched from.
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure page
st.set_page_config(
    page_title="ATS Resume Scorer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auth state. Populated by Supabase sign-in / sign-up / OAuth.
# All four are None when signed out, all four are set when signed in.
for key, default in [
    ("access_token", None),
    ("refresh_token", None),
    ("user_id", None),       # Supabase auth user id (uuid); also used by api_client
    ("user_email", None),
    ("auth_error", None),
    ("auth_info", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# If we just came back from Google OAuth, Supabase appends `?code=<authcode>`
# to the redirect URL. Exchange it for a session before rendering anything.
if (
    not st.session_state.access_token
    and "code" in st.query_params
):
    from frontend.services import supabase_client
    result = supabase_client.exchange_code_for_session(st.query_params["code"])

    # Always clear the ?code= param so a refresh doesn't try to re-exchange.
    st.query_params.clear()
    if "error" in result:
        st.session_state.auth_error = f"Google sign-in failed: {result['error']}"
    else:
        st.session_state.access_token  = result["access_token"]
        st.session_state.refresh_token = result["refresh_token"]
        st.session_state.user_id       = result["user_id"]
        st.session_state.user_email    = result["email"]
        st.query_params["auth_token"]  = result["refresh_token"]
        st.rerun()

# Automatically restore session on browser refresh if token is present
elif (
    not st.session_state.access_token
    and "auth_token" in st.query_params
):
    from frontend.services import supabase_client
    refreshed = supabase_client.refresh_user_session(st.query_params["auth_token"])
    if "error" not in refreshed and refreshed.get("access_token"):
        st.session_state.access_token  = refreshed["access_token"]
        st.session_state.refresh_token = refreshed["refresh_token"]
        st.session_state.user_id       = refreshed["user_id"]
        st.session_state.user_email    = refreshed["email"]
        st.query_params["auth_token"]  = refreshed["refresh_token"]
    else:
        st.query_params.pop("auth_token", None)

# Check for direct view deep linking in query params
if "view" in st.query_params and st.query_params["view"] in ("landing", "scorer", "history", "resources"):
    st.session_state.current_view = st.query_params["view"]

# Developer / test preview support for visual verification
if st.query_params.get("preview") == "sample":
    import json
    sample_path = Path("C:/Users/Ayush/.gemini/antigravity/brain/c8387dfb-cd88-41e7-8e26-10a7415efbab/sample_analysis.json")
    if sample_path.exists():
        try:
            st.session_state["scorer_analysis"] = json.loads(sample_path.read_text(encoding="utf-8"))
            if "view" not in st.query_params:
                st.session_state.current_view = "scorer"
        except Exception:
            pass

# Load custom CSS
def load_css():
    try:
        css_path = Path(__file__).parent / 'assets' / 'styles.css'
        with open(css_path, 'r', encoding='utf-8') as f:
            return f'<style>{f.read()}</style>'
    except Exception:
        return ''

st.markdown(load_css(), unsafe_allow_html=True)

# Initialize session state for view management
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'landing'

# Sidebar navigation
with st.sidebar:
    # Sleek Brand Header
    st.markdown(
        """
        <div class="brand-sidebar-header">
            <div class="brand-icon-sq">🎯</div>
            <div class="brand-text-col">
                <span class="brand-title-text">Resume ATS Checker</span>
                <span class="brand-version-badge">AI Assistant</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## Navigation")

    cur = st.session_state.current_view
    
    # Styled Navigation buttons
    if st.button("🏠  Home", use_container_width=True, type="primary" if cur == 'landing' else "secondary", key="nav_home"):
        st.session_state.current_view = 'landing'
        st.query_params["view"] = 'landing'
        st.rerun()

    if st.button("🎯  Check Resume", use_container_width=True, type="primary" if cur == 'scorer' else "secondary", key="nav_scorer"):
        st.session_state.current_view = 'scorer'
        st.query_params["view"] = 'scorer'
        st.rerun()

    if st.button("📊  Past Reviews", use_container_width=True, type="primary" if cur == 'history' else "secondary", key="nav_history"):
        st.session_state.current_view = 'history'
        st.query_params["view"] = 'history'
        st.rerun()

    if st.button("💡  Tips & Guides", use_container_width=True, type="primary" if cur == 'resources' else "secondary", key="nav_resources"):
        st.session_state.current_view = 'resources'
        st.query_params["view"] = 'resources'
        st.rerun()

    st.markdown("---")
    st.markdown("## Your Account")

    from frontend.services import supabase_client

    if st.session_state.access_token:
        # Signed-in state
        email_str = str(st.session_state.user_email or "User")
        initial = email_str[0].upper()
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:10px; padding:10px 12px; display:flex; align-items:center; gap:10px; margin-bottom:12px;">
                <div style="width:32px; height:32px; border-radius:50%; background:#4F46E5; color:white; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:14px;">
                    {initial}
                </div>
                <div style="overflow:hidden; text-overflow:ellipsis;">
                    <div style="color:#F8FAFC; font-size:12px; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{email_str}</div>
                    <div style="color:#10B981; font-size:11px; font-weight:500;">● Signed In</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Sign out", use_container_width=True):
            supabase_client.sign_out()
            for k in ("access_token", "refresh_token", "user_id", "user_email"):
                st.session_state[k] = None
            st.query_params.pop("auth_token", None)
            st.rerun()
    else:
        # Signed-out state
        if st.session_state.auth_error:
            st.error(st.session_state.auth_error)
            st.session_state.auth_error = None
        if st.session_state.auth_info:
            st.info(st.session_state.auth_info)
            st.session_state.auth_info = None

        tab_in, tab_up = st.tabs(["Sign in", "Sign up"])

        with tab_in:
            with st.form("signin_form", clear_on_submit=False):
                email = st.text_input("Email", key="signin_email")
                password = st.text_input("Password", type="password", key="signin_pw")
                submitted = st.form_submit_button("Sign in", use_container_width=True)
            if submitted:
                result = supabase_client.sign_in_with_password(email, password)
                if "error" in result:
                    st.session_state.auth_error = result["error"]
                else:
                    st.session_state.access_token  = result["access_token"]
                    st.session_state.refresh_token = result["refresh_token"]
                    st.session_state.user_id       = result["user_id"]
                    st.session_state.user_email    = result["email"]
                    st.query_params["auth_token"]  = result["refresh_token"]
                st.rerun()

        with tab_up:
            with st.form("signup_form", clear_on_submit=False):
                email_up = st.text_input("Email", key="signup_email")
                password_up = st.text_input("Password (min 6 chars)", type="password", key="signup_pw")
                submitted_up = st.form_submit_button("Create account", use_container_width=True)
            if submitted_up:
                result = supabase_client.sign_up_with_password(email_up, password_up)
                if "error" in result:
                    st.session_state.auth_error = result["error"]
                elif result.get("pending_confirmation"):
                    st.session_state.auth_info = (
                        f"Check your inbox — confirmation email sent to {result['email']}."
                    )
                else:
                    st.session_state.access_token  = result["access_token"]
                    st.session_state.refresh_token = result["refresh_token"]
                    st.session_state.user_id       = result["user_id"]
                    st.session_state.user_email    = result["email"]
                    st.query_params["auth_token"]  = result["refresh_token"]
                st.rerun()

        st.markdown("<div style='text-align:center; margin: 10px 0; color:#64748B; font-size:12px;'>— OR CONTINUE WITH —</div>",
                    unsafe_allow_html=True)

        oauth = supabase_client.google_oauth_url()
        if "error" in oauth:
            st.caption(f"Google sign-in unavailable: {oauth['error']}")
        else:
            st.link_button(
                "Continue with Google",
                url=oauth["url"],
                use_container_width=True,
            )

# Main content area - render based on current view
if st.session_state.current_view == 'landing':
    # Import and render landing page
    from frontend.views import landing
    landing.render()

elif st.session_state.current_view == 'scorer':
    # Import and render scorer page
    from frontend.views import scorer
    scorer.render()

elif st.session_state.current_view == 'history':
    # Import and render history page
    from frontend.views import history
    history.render()

elif st.session_state.current_view == 'resources':
    # Import and render resources page
    from frontend.views import resources
    resources.render()
