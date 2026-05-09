import streamlit as st

st.set_page_config(
    page_title="Mitra — HR Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# SAFE IMPORTS
# ─────────────────────────────────────────────────────────────

try:
    from styles import inject_css
except Exception:
    def inject_css():
        pass


try:
    from login import login_page
except Exception as e:
    login_page = None
    login_error = e


try:
    from Helpdesk import helpdesk_page
except Exception as e:
    helpdesk_page = None
    helpdesk_error = e


try:
    from Ask_AI import ask_ai_page
except Exception as e:
    ask_ai_page = None
    ask_ai_error = e


try:
    from Handbook import handbook_page
except Exception as e:
    handbook_page = None
    handbook_error = e


try:
    from admin import admin_page
except Exception:
    try:
        from admin import admin_grievance_page as admin_page
    except Exception as e:
        admin_page = None
        admin_error = e


# ─────────────────────────────────────────────────────────────
# FALLBACK PAGE
# ─────────────────────────────────────────────────────────────

def unavailable_page(module_name, error=None):
    st.warning(f"⚠️ {module_name} is not loaded.")
    if error:
        st.code(str(error), language="text")


# ─────────────────────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────────────────────

def logout():
    for key in [
        "authenticated",
        "user_type",
        "user_erp",
        "login_time",
        "page",
        "login_type",
        "active_page",
    ]:
        st.session_state.pop(key, None)

    st.rerun()


# ─────────────────────────────────────────────────────────────
# SIDEBAR — BUTTON NAVIGATION
# ─────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-logo">🤖 Mitra</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-subtitle">HR Assistant Platform · Orchids</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="sidebar-user-card">
                <p><strong>Logged in:</strong> {st.session_state.get("user_erp", "")}</p>
                <p><strong>Role:</strong> {st.session_state.get("user_type", "").title()}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Page list based on role
        if st.session_state.get("user_type") == "admin":
            pages = [
                "💬 HR Helpdesk",
                "🤖 AI Mode",
                "📖 Handbook Browser",
                "🛡️ Admin",
            ]
            default_page = "🛡️ Admin"
        else:
            pages = [
                "💬 HR Helpdesk",
                "🤖 AI Mode",
                "📖 Handbook Browser",
            ]
            default_page = "💬 HR Helpdesk"

        # Initialize active page
        if "active_page" not in st.session_state:
            st.session_state.active_page = default_page

        # Reset if role/page changes
        if st.session_state.active_page not in pages:
            st.session_state.active_page = default_page

        st.markdown(
            '<div class="sidebar-section-title">Navigation</div>',
            unsafe_allow_html=True,
        )

        # Button navigation instead of radio
        for page_name in pages:
            if st.session_state.active_page == page_name:
                st.markdown(
                    f'<div class="active-nav-btn">{page_name}</div>',
                    unsafe_allow_html=True,
                )
            else:
                if st.button(
                    page_name,
                    key=f"nav_button_{page_name}",
                    use_container_width=True,
                ):
                    st.session_state.active_page = page_name
                    st.rerun()

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="sidebar-section-title">Quick Contact</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="sidebar-contact-card">
                <p><strong>Payroll & Leave Issues</strong></p>
                <p>📧 payroll2.branch@orchids.edu.in</p>
                <br>
                <p><strong>Eduvate ERP Portal</strong></p>
                <p>🌐 Attendance · Leave · Payslips</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        if st.button("🚪 Logout", key="logout_button", use_container_width=True):
            logout()

        st.markdown(
            '<div class="sidebar-footer">Mitra v3.0 · Orchids HR</div>',
            unsafe_allow_html=True,
        )

    return st.session_state.active_page


# ─────────────────────────────────────────────────────────────
# MAIN ROUTING
# ─────────────────────────────────────────────────────────────

def main():
    inject_css()

    if not st.session_state.get("authenticated"):
        if login_page:
            login_page()
        else:
            unavailable_page("login.py", globals().get("login_error"))
        return

    page = render_sidebar()

    if page == "💬 HR Helpdesk":
        if helpdesk_page:
            helpdesk_page()
        else:
            unavailable_page("Helpdesk.py", globals().get("helpdesk_error"))

    elif page == "🤖 AI Mode":
        if ask_ai_page:
            ask_ai_page()
        else:
            unavailable_page("Ask_AI.py", globals().get("ask_ai_error"))

    elif page == "📖 Handbook Browser":
        if handbook_page:
            handbook_page()
        else:
            unavailable_page("Handbook.py", globals().get("handbook_error"))

    elif page == "🛡️ Admin":
        if st.session_state.get("user_type") != "admin":
            st.error("❌ Unauthorized access.")
            return

        if admin_page:
            admin_page()
        else:
            unavailable_page("admin.py", globals().get("admin_error"))


if __name__ == "__main__":
    main()
