import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    body { font-family: sans-serif; }

    .msg-user {
        display:flex;
        justify-content:flex-end;
        margin:10px 0;
    }

    .msg-bot {
        display:flex;
        margin:10px 0;
    }

    .bubble {
        padding:10px 15px;
        border-radius:12px;
        max-width:70%;
    }

  .msg-bot .bubble {
    background: #e2e8f0;   /* light grey */
    color: #0f172a;        /* dark text ✅ FIX */
}

.msg-user .bubble {
    background: #2563eb;   /* blue */
    color: #ffffff;        /* white text */
}

    .mail-btn {
        background:#2563eb;
        color:white;
        padding:10px 20px;
        border:none;
        border-radius:20px;
        cursor:pointer;
    }
    
    /* =========================
   CHAT BUBBLES
========================= */

.msg-bot, .msg-user {
    display: flex;
    margin: 12px 0;
}

.msg-bot {
    justify-content: flex-start;
}

.msg-user {
    justify-content: flex-end;
}

.bubble {
    padding: 12px 16px;
    border-radius: 16px;
    font-size: 14px;
    line-height: 1.6;
    max-width: 75%;
    word-break: break-word;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: all 0.2s ease;
}

/* BOT */
.msg-bot .bubble {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    color: #0f172a;
    border-top-left-radius: 4px;
}

/* USER */
.msg-user .bubble {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border-top-right-radius: 4px;
}

/* Hover effect */
.bubble:hover {
    transform: translateY(-1px);
}

/* =========================
   CHAT NAME
========================= */

.chat-name {
    font-size: 12px;
    font-weight: 600;
    color: #64748b;
    margin-bottom: 4px;
}

/* =========================
   AVATAR
========================= */

.avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    font-weight: bold;
}

/* =========================
   BUTTONS (MAIN UPGRADE)
========================= */

div[data-testid="stButton"] button {
    border-radius: 999px !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    border: 1px solid #e2e8f0 !important;
    background: #ffffff !important;
    color: #0f172a !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05) !important;
}

/* Hover */
div[data-testid="stButton"] button:hover {
    background: #2563eb !important;
    color: white !important;
    border-color: #2563eb !important;
    transform: translateY(-1px) !important;
}

/* Active click */
div[data-testid="stButton"] button:active {
    transform: scale(0.97) !important;
}

/* =========================
   PRIMARY BUTTON (OPTIONAL)
========================= */

.primary-btn button {
    background: #2563eb !important;
    color: white !important;
    border: none !important;
}

.primary-btn button:hover {
    background: #1d4ed8 !important;
}

/* =========================
   FORM INPUTS
========================= */

input, textarea {
    border-radius: 10px !important;
    border: 1px solid #cbd5f5 !important;
}

input:focus, textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
}
   /* =========================
   SIDEBAR NAVBAR BUTTONS
========================= */

section[data-testid="stSidebar"] div[data-testid="stButton"] button {
    width: 100% !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin-bottom: 6px !important;

    background: #ffffff !important;
    color: #0f172a !important;

    border: 1px solid #e2e8f0 !important;

    font-weight: 600 !important;
    font-size: 14px !important;

    text-align: left !important;

    transition: all 0.2s ease !important;
}

/* Hover */
section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
    background: #eff6ff !important;
    color: #2563eb !important;
    border-color: #2563eb !important;
}

/* Click */
section[data-testid="stSidebar"] div[data-testid="stButton"] button:active {
    transform: scale(0.97);
}
   
   /* =========================
   INPUT TEXT BAR (CHAT + FORMS)
========================= */

/* General input fields */
input, textarea {
    border-radius: 12px !important;
    border: 1px solid #e2e8f0 !important;
    padding: 10px 12px !important;
    font-size: 14px !important;

    background: #ffffff !important;
    color: #0f172a !important;

    transition: all 0.2s ease !important;
}

/* Focus effect */
input:focus, textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
    outline: none !important;
}

/* Placeholder text */
input::placeholder, textarea::placeholder {
    color: #94a3b8 !important;
}

/* =========================
   CHAT INPUT (BOTTOM BAR)
========================= */

/* Streamlit chat input box */
div[data-testid="stChatInput"] textarea {
    border-radius: 20px !important;
    padding: 12px 16px !important;
    border: 1px solid #e2e8f0 !important;

    background: #ffffff !important;
    color: #0f172a !important;
}

/* Chat input focus */
div[data-testid="stChatInput"] textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
}

/* =========================
   INPUT CONTAINER (OPTIONAL POLISH)
========================= */

[data-testid="stTextInput"], 
[data-testid="stTextArea"] {
    margin-bottom: 10px;
}


/* =========================
   CHAT SEND BUTTON
========================= */

/* Target send button */
div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: white !important;

    border-radius: 50% !important;
    width: 40px !important;
    height: 40px !important;

    border: none !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    transition: all 0.2s ease !important;
}

/* Hover effect */
div[data-testid="stChatInput"] button:hover {
    transform: scale(1.08);
    background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
}

/* Click effect */
div[data-testid="stChatInput"] button:active {
    transform: scale(0.95);
}

/* Optional: icon color fix */
div[data-testid="stChatInput"] button svg {
    fill: white !important;
}
   
/* Attendance text inputs */
div[data-testid="stTextInput"] input {
    background: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #334155 !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    font-size: 16px !important;
    box-shadow: none !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.18) !important;
}

/* Remove time input styling conflict if previously added */
div[data-testid="stTimeInput"] input {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}



/* =========================================================
   FINAL SELECTBOX WHITE BLOCK FIX
   Fixes white cursor/block inside st.selectbox
========================================================= */

/* Main selectbox wrapper */
div[data-baseweb="select"] {
    background: transparent !important;
}

/* Selectbox visible container */
div[data-baseweb="select"] > div {
    background: #27272f !important;
    border: 1px solid #374151 !important;
    border-radius: 14px !important;
    min-height: 58px !important;
    box-shadow: none !important;
}

/* Text inside selectbox */
div[data-baseweb="select"] span {
    color: #f8fafc !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}

/* Dropdown arrow */
div[data-baseweb="select"] svg {
    fill: #f8fafc !important;
}

/* CRITICAL: remove white input/caret block */
div[data-baseweb="select"] input {
    width: 1px !important;
    min-width: 1px !important;
    max-width: 1px !important;

    opacity: 0 !important;
    color: transparent !important;
    caret-color: transparent !important;
    background: transparent !important;

    border: none !important;
    outline: none !important;
    box-shadow: none !important;

    padding: 0 !important;
    margin: 0 !important;
}

/* Remove input selection highlight */
div[data-baseweb="select"] input::selection {
    background: transparent !important;
    color: transparent !important;
}

/* Remove focus ring from internal select input */
div[data-baseweb="select"] input:focus {
    outline: none !important;
    border: none !important;
    box-shadow: none !important;
}

/* Dropdown menu background */
div[data-baseweb="popover"] {
    background: #27272f !important;
    border-radius: 14px !important;
}

/* Dropdown list */
ul[role="listbox"] {
    background: #27272f !important;
    border: 1px solid #374151 !important;
    border-radius: 14px !important;
    padding: 6px !important;
}

/* Dropdown options */
li[role="option"] {
    background: #27272f !important;
    color: #f8fafc !important;
    border-radius: 10px !important;
    padding: 10px 12px !important;
}

/* Option hover */
li[role="option"]:hover {
    background: #2563eb !important;
    color: #ffffff !important;
}

/* =========================================================
   SIDEBAR STYLING — MITRA
========================================================= */

/* Sidebar background */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    border-right: 1px solid #334155 !important;
}

/* Sidebar default text */
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Logo */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 24px;
    font-weight: 800;
    color: #38bdf8 !important;
    margin-bottom: 4px;
}

/* Subtitle */
.sidebar-subtitle {
    font-size: 12px;
    color: #94a3b8 !important;
    margin-bottom: 18px;
}

/* Section title */
.sidebar-section-title {
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #64748b !important;
    margin: 18px 0 10px 0;
}

/* User card */
.sidebar-user-card {
    display: flex;
    flex-direction: column;
    gap: 4px;
    background: rgba(30, 58, 138, 0.35);
    border: 1px solid rgba(59, 130, 246, 0.35);
    border-radius: 14px;
    padding: 12px 14px;
    margin: 14px 0 18px 0;
}

.sidebar-user-card p {
    margin: 0;
    font-size: 12px;
    color: #bfdbfe !important;
}

/* Divider */
.sidebar-divider {
    margin: 18px 0 12px 0;
    border-top: 1px solid rgba(148, 163, 184, 0.25);
}

/* Contact card */
.sidebar-contact-card {
    display: flex;
    flex-direction: column;
    gap: 4px;
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 14px;
    padding: 12px 14px;
    margin-top: 10px;
}

.sidebar-contact-card p {
    margin: 0;
    font-size: 12px;
    color: #cbd5e1 !important;
}

/* Footer */
.sidebar-footer {
    font-size: 11px;
    color: #64748b !important;
    text-align: center;
    margin-top: 18px;
}

/* =========================================================
   SIDEBAR BUTTONS — BLACK TEXT
========================================================= */

/* Button wrapper */
section[data-testid="stSidebar"] div[data-testid="stButton"] {
    margin-bottom: 8px !important;
}

/* Normal sidebar buttons */
section[data-testid="stSidebar"] div[data-testid="stButton"] button {
    width: 100% !important;

    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 10px !important;

    background: #ffffff !important;
    color: #0f172a !important;

    border: 1px solid rgba(148, 163, 184, 0.35) !important;
    border-radius: 12px !important;

    padding: 12px 14px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    text-align: left !important;

    transition: all 0.18s ease !important;
    box-shadow: none !important;
}

/* Force button text black */
section[data-testid="stSidebar"] div[data-testid="stButton"] button *,
section[data-testid="stSidebar"] button,
section[data-testid="stSidebar"] button * {
    color: #0f172a !important;
}

/* Hover effect */
section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
    background: #eff6ff !important;
    color: #0f172a !important;
    border-color: #2563eb !important;
    transform: translateX(3px) !important;
    box-shadow: 0 6px 18px rgba(37, 99, 235, 0.18) !important;
}

/* Click effect */
section[data-testid="stSidebar"] div[data-testid="stButton"] button:active {
    transform: scale(0.98) !important;
}

/* Active selected navigation button */
.active-nav-btn {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 10px;

    background: #ffffff !important;
    border: 2px solid #2563eb !important;
    border-radius: 12px;

    padding: 12px 14px;
    margin-bottom: 8px;

    font-size: 14px;
    font-weight: 800;
    color: #0f172a !important;

    box-shadow: 0 8px 22px rgba(37, 99, 235, 0.25);
}


    </style>
    """, unsafe_allow_html=True)
