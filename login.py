"""
Login Page for Mitra HR System
Handles Employee and Admin Authentication
"""

import streamlit as st
from datetime import datetime
import hashlib

# ============================================================================
# ADMIN CONFIGURATION SECTION - FLEXIBLE ADMIN MANAGEMENT
# ============================================================================
# Admins can be easily added or removed here
ADMIN_CREDENTIALS = {
    "20262002367_OIS": "payroll2@branch",
    # Add more admins like this:
    # "20262001234_OIS": "admin_password@branch",
    # "20262005678_OIS": "another_password@branch",
}
# ============================================================================


def hash_password(password):
    """Hash password for basic security"""
    return hashlib.sha256(password.encode()).hexdigest()


def validate_erp(erp_code):
    """Validate ERP code format: 11 digits + _OIS"""
    import re
    pattern = r'^\d{11}_OIS$'
    if re.match(pattern, erp_code):
        return True, None
    return False, "❌ Invalid ERP format. Expected: 11 digits + _OIS (e.g., 20262002367_OIS)"


def login_page():
    """Main login page with Employee/Admin toggle"""
    st.set_page_config(
        page_title="Mitra HR - Login",
        page_icon="🔐",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for professional look
    st.markdown("""
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .login-container {
                max-width: 450px;
                margin: 60px auto;
                padding: 40px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            }
            .login-header {
                text-align: center;
                margin-bottom: 30px;
            }
            .login-header h1 {
                color: #667eea;
                font-size: 32px;
                margin-bottom: 8px;
            }
            .login-header p {
                color: #666;
                font-size: 14px;
            }
            .toggle-buttons {
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
                justify-content: center;
            }
            .toggle-btn {
                padding: 10px 20px;
                border: 2px solid #667eea;
                background: white;
                border-radius: 5px;
                cursor: pointer;
                font-weight: 500;
                transition: all 0.3s;
            }
            .toggle-btn.active {
                background: #667eea;
                color: white;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #333;
            }
            .form-group input {
                width: 100%;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            .info-box {
                background: #f0f4ff;
                padding: 15px;
                border-left: 4px solid #667eea;
                margin-bottom: 20px;
                border-radius: 4px;
                font-size: 13px;
                color: #555;
            }
            .error-message {
                color: #e74c3c;
                font-weight: 500;
                margin-bottom: 15px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class="login-container">
                <div class="login-header">
                    <h1>🔐 Mitra</h1>
                    <p>HR Management System</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Initialize session state
    if "login_type" not in st.session_state:
        st.session_state.login_type = "employee"
    
    # Toggle between Employee and Admin
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 Employee Login", use_container_width=True, 
                    key="emp_toggle",
                    type="primary" if st.session_state.login_type == "employee" else "secondary"):
            st.session_state.login_type = "employee"
            st.rerun()
    
    with col2:
        if st.button("⚙️ Admin Login", use_container_width=True,
                    key="admin_toggle",
                    type="primary" if st.session_state.login_type == "admin" else "secondary"):
            st.session_state.login_type = "admin"
            st.rerun()
    
    st.divider()
    
    if st.session_state.login_type == "employee":
        _employee_login()
    else:
        _admin_login()


def _employee_login():
    """Employee login form"""
    st.markdown("""
        <div class="info-box">
            <strong>📝 Employee Access</strong><br>
            Enter your ERP Code to access the HR Helpdesk and Grievance Portal.
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("employee_login_form", clear_on_submit=True):
        erp_code = st.text_input(
            "ERP Code",
            placeholder="e.g., 20262002367_OIS",
            help="11 digits followed by _OIS"
        )
        
        submitted = st.form_submit_button("Login", use_container_width=True, type="primary")
        
        if submitted:
            if not erp_code.strip():
                st.error("❌ Please enter your ERP Code")
                return
            
            ok, error = validate_erp(erp_code.strip())
            
            if not ok:
                st.error(error)
                return
            
            # Employee login successful
            st.session_state.authenticated = True
            st.session_state.user_type = "employee"
            st.session_state.user_erp = erp_code.strip()
            st.session_state.login_time = datetime.now()
            
            st.success("✅ Login successful! Redirecting...")
            st.session_state.page = "home"


def _admin_login():
    """Admin login form"""
    st.markdown("""
        <div class="info-box">
            <strong>🔑 Admin Access</strong><br>
            Enter your credentials to access admin dashboard and grievance management.
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("admin_login_form", clear_on_submit=True):
        erp_code = st.text_input(
            "ERP Code (Admin ID)",
            placeholder="e.g., 20262002367_OIS",
            help="Admin ERP Code"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter admin password"
        )
        
        submitted = st.form_submit_button("Login", use_container_width=True, type="primary")
        
        if submitted:
            if not erp_code.strip() or not password.strip():
                st.error("❌ Please enter both ERP Code and Password")
                return
            
            erp_code = erp_code.strip()
            
            # Validate ERP format
            ok, error = validate_erp(erp_code)
            if not ok:
                st.error(error)
                return
            
            # Check admin credentials
            if erp_code in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[erp_code] == password:
                st.session_state.authenticated = True
                st.session_state.user_type = "admin"
                st.session_state.user_erp = erp_code
                st.session_state.login_time = datetime.now()
                
                st.success("✅ Admin login successful! Redirecting...")
                st.session_state.page = "admin_dashboard"
            else:
                st.error("❌ Invalid ERP Code or Password")
                st.info("ℹ️ Please check your credentials and try again.")


if __name__ == "__main__":
    login_page()