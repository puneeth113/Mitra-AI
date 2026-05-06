import streamlit as st
from Handbook import load_sections
from admin import admin_page
from Ask_AI import ask_ai_page
try:
    from Ask_AI import ask_ai_page
except Exception as e:
    ask_ai_page = None
    ask_ai_error = e

from Handbook import handbook_page

st.set_page_config(
    page_title="Mitra — HR Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    from Handbook import handbook_browser_page
except Exception as e:
    handbook_browser_page = None
    handbook_error = e

try:
    from Tools import tools_page
except Exception as e:
    tools_page = None
    tools_error = e

try:
    from admin import admin_page
except Exception as e:
    admin_page = None
    admin_error = e


def unavailable_page(module_name, error=None):
    st.warning(f"⚠️ {module_name} is not loaded.")
    if error:
        st.code(str(error), language="text")


def logout():
    for key in [
        "authenticated",
        "user_type",
        "user_erp",
        "login_time",
        "page",
        "login_type",
    ]:
        st.session_state.pop(key, None)
    st.rerun()


def render_sidebar():
    with st.sidebar:
        st.markdown("## 🤖 Mitra")
        st.caption("HR Assistant Platform · Orchids")

        st.divider()

        st.success(f"Logged in: {st.session_state.get('user_erp', '')}")
        st.caption(f"Role: {st.session_state.get('user_type', '').title()}")

        st.divider()

        if st.session_state.get("user_type") == "admin":
            pages = [
                "💬 HR Helpdesk",
                "🤖 AI Mode",
                "📖 Handbook Browser",
                "🛡️ Admin",
            ]
        else:
            pages = [
                "💬 HR Helpdesk",
                "🤖 AI Mode",
                "📖 Handbook Browser",
            ]

        page = st.radio(
            "Navigation",
            pages,
            label_visibility="collapsed"
        )

        st.divider()
        st.markdown("### Quick Contact")
        st.info("📧 payroll2.branch@orchids.edu.in")

        if st.button("🚪 Logout", use_container_width=True):
            logout()

        st.caption("Mitra v3.0 · Orchids HR")

    return page


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


    elif page == "📖 Handbook Browser":
     handbook_page()
    
    elif page == "🛡️ Admin":
        if admin_page:
            admin_page()
        else:
            st.error("Admin page failed to load")
            st.code(str(globals().get("admin_error")), language="text")
    
    elif page == "🤖 AI Mode":
        if ask_ai_page:
            ask_ai_page()
        else:
            unavailable_page("Ask_AI.py", globals().get("ask_ai_error"))

if __name__ == "__main__":
    main()