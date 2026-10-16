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

    st.markdown("""
        <div class="sidebar-section-divider"></div>
        <div class="sidebar-auth-header">
            <div class="sidebar-auth-badge">
                <span class="auth-dot"></span>
                <span>ACCOUNT ACCESS</span>
            </div>
            <div class="sidebar-auth-title">Your Account</div>
            <div class="sidebar-auth-subtitle">Sign in to sync reviews & scores</div>
        </div>
    """, unsafe_allow_html=True)

    from frontend.services import supabase_client

    if st.session_state.access_token:
        # Signed-in state
        email_str = str(st.session_state.user_email or "User")
        initial = email_str[0].upper()
        st.markdown(
            f"""
            <div class="sidebar-user-card">
                <div class="sidebar-user-avatar">{initial}</div>
                <div class="sidebar-user-details">
                    <div class="sidebar-user-email" title="{email_str}">{email_str}</div>
                    <div class="sidebar-user-status"><span class="user-status-dot"></span> Signed In</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Sign Out", use_container_width=True, key="sidebar_signout_btn"):
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

        tab_in, tab_up = st.tabs(["Sign In", "Create Account"])

        with tab_in:
            with st.form("signin_form", clear_on_submit=False):
                email = st.text_input("Email Address", placeholder="name@domain.com", key="signin_email")
                password = st.text_input("Password", type="password", placeholder="••••••••", key="signin_pw")
                submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")
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
                email_up = st.text_input("Email Address", placeholder="name@domain.com", key="signup_email")
                password_up = st.text_input("Password (min 6 chars)", type="password", placeholder="At least 6 characters", key="signup_pw")
                submitted_up = st.form_submit_button("Create Free Account →", use_container_width=True, type="primary")
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

        st.markdown(
            """
            <div class="sidebar-auth-divider">
                <div class="auth-divider-line"></div>
                <span class="auth-divider-text">OR CONTINUE WITH</span>
                <div class="auth-divider-line"></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        oauth = supabase_client.google_oauth_url()
        if "error" in oauth:
            st.caption(f"Google sign-in unavailable: {oauth['error']}")
        else:
            st.markdown(
                f"""
                <a href="{oauth['url']}" target="_self" class="sidebar-google-btn">
                    <svg width="18" height="18" viewBox="0 0 24 24" style="flex-shrink:0;">
                        <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                        <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
                    </svg>
                    <span>Continue with Google</span>
                </a>
                """,
                unsafe_allow_html=True
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
