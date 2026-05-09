"""
Updated HR Helpdesk with Shift Selection, Professional Email, and Grievance Management
"""

import urllib.parse
from datetime import datetime, time
import streamlit as st
import re
from Grievance_db import get_db


HR_EMAIL = "payroll@company.com"

# Shift templates for quick selection
SHIFT_TEMPLATES = {
    "Morning (9:00 AM - 5:30 PM)": ("09:00", "17:30"),
    "Morning with Buffer (8:45 AM - 5:45 PM)": ("08:45", "17:45"),
    "Evening (1:00 PM - 9:30 PM)": ("13:00", "21:30"),
    "Evening with Buffer (12:45 PM - 9:45 PM)": ("12:45", "21:45"),
    "Night (10:00 PM - 6:30 AM)": ("22:00", "06:30"),
    "Night with Buffer (9:45 PM - 6:45 AM)": ("21:45", "06:45"),
}


FAQ = {
    "Salary & Payslip": {
        "Salary not credited": {
            "policy_note": "Salaries are released on or before the 10th of the following month.",
            "explanation": (
                "As per HR policy, salaries are released on or before the 10th of every month.\n\n"
                "Please check your bank account, verify your registered bank details, "
                "and raise a request with payroll if the salary is still not credited after the 10th."
            ),
            "subject": "Salary Not Credited – {month} – {erp}",
            "body_template": (
                "Dear HR / Payroll Team,\n\n"
                "I am writing to formally request your assistance regarding my salary payment for {month}.\n\n"
                "Issue Details:\n"
                "- Month: {month}\n"
                "- Expected Credit Date: On or before 10th of {month}\n"
                "- Current Status: Not Yet Credited\n\n"
                "Employee Information:\n"
                "- Full Name: {name}\n"
                "- ERP Code: {erp}\n"
                "- Bank Account: [Your Registered Bank Account]\n"
                "- Grievance ID: {grievance_id}\n\n"
                "I have verified my registered bank details and confirm that the salary has not been credited to my account as of {date}.\n\n"
                "Request: Kindly investigate the issue and confirm the expected credit date. If there are any discrepancies in my records, please communicate the same so we can resolve it promptly.\n\n"
                "Thank you for your prompt attention to this matter.\n\n"
                "Best Regards,\n{name}\nERP: {erp}"
            ),
        },
        "Wrong salary amount credited": {
            "policy_note": "Salary discrepancies may happen due to LOP, arrears, or payroll corrections.",
            "explanation": (
                "A salary discrepancy may occur due to incorrect LOP, joining-date arrears, "
                "component mismatch, or payroll revision delay.\n\n"
                "Please compare your payslip with your expected salary breakup before raising the issue."
            ),
            "subject": "Salary Discrepancy Report – {month} – {erp}",
            "body_template": (
                "Dear HR / Payroll Team,\n\n"
                "I am writing to bring to your attention a discrepancy in my salary credited for {month}.\n\n"
                "Issue Details:\n"
                "- Month: {month}\n"
                "- Grievance ID: {grievance_id}\n\n"
                "Salary Information:\n"
                "- Expected Amount: ₹__________\n"
                "- Amount Actually Received: ₹__________\n"
                "- Difference: ₹__________\n\n"
                "Employee Information:\n"
                "- Full Name: {name}\n"
                "- ERP Code: {erp}\n\n"
                "Breakdown of Expected vs Received:\n"
                "[Please attach or paste your expected salary breakup]\n\n"
                "Request: I kindly request you to review my payslip and provide a detailed explanation for the discrepancy. If it is an error, please process the correction at the earliest.\n\n"
                "Thank you for your attention to this urgent matter.\n\n"
                "Best Regards,\n{name}\nERP: {erp}"
            ),
        },
        "Payslip not received": {
            "policy_note": "Payslips are usually available after salary processing.",
            "explanation": (
                "Payslips are usually shared through registered email or ERP after salary processing.\n\n"
                "Please check your inbox, spam folder, and Eduvate ERP portal."
            ),
            "subject": "Payslip Access Request – {month} – {erp}",
            "body_template": (
                "Dear HR / Payroll Team,\n\n"
                "I am writing to request the payslip for {month}, which I have not received.\n\n"
                "Issue Details:\n"
                "- Month: {month}\n"
                "- Date Salary Processed: Approx. 10th of {month}\n"
                "- Grievance ID: {grievance_id}\n\n"
                "Employee Information:\n"
                "- Full Name: {name}\n"
                "- ERP Code: {erp}\n"
                "- Registered Email: [Your Email]\n\n"
                "Actions Taken:\n"
                "- Checked primary email inbox\n"
                "- Checked spam/junk folder\n"
                "- Checked ERP portal\n\n"
                "Request: Could you please either resend the payslip to my registered email or provide me with access to retrieve it from the ERP portal?\n\n"
                "Thank you for your assistance.\n\n"
                "Best Regards,\n{name}\nERP: {erp}"
            ),
        },
    },
    "Attendance & Leave": {
        "Leave not credited": {
            "policy_note": "Casual Leaves are credited as per the annual leave cycle.",
            "explanation": (
                "Casual Leaves are credited as per the company leave cycle. "
                "If your leave is not credited, please check your joining date, leave cycle, "
                "and ERP leave balance."
            ),
            "subject": "Leave Balance Not Credited – {erp}",
            "body_template": (
                "Dear HR / Leave Management Team,\n\n"
                "I am writing to report that my Casual Leave balance has not been credited as per the expected leave cycle.\n\n"
                "Issue Details:\n"
                "- Leave Type: Casual Leave (CL)\n"
                "- Expected Credit Date: [Mention your leave cycle date]\n"
                "- Current Balance: 0 (or lower than expected)\n"
                "- Grievance ID: {grievance_id}\n\n"
                "Employee Information:\n"
                "- Full Name: {name}\n"
                "- ERP Code: {erp}\n"
                "- Date of Joining: [Your Joining Date]\n"
                "- Current Leave Cycle: [Your Cycle]\n\n"
                "Request: Please verify my leave eligibility based on my joining date and current leave cycle. If there is an error in the system, kindly update my leave balance accordingly.\n\n"
                "Thank you for your prompt action.\n\n"
                "Best Regards,\n{name}\nERP: {erp}"
            ),
        },
        "Attendance regularization": {
            "policy_note": "Only two attendance regularizations are allowed per month.",
            "explanation": (
                "Attendance regularization is allowed for genuine missed punch or biometric issues. "
                "As per policy, only two regularizations are allowed per month."
            ),
            "subject": "Attendance Regularization Request – {erp}",
            "body_template": (
                "Dear HR / Attendance Team,\n\n"
                "I am writing to request attendance regularization for a missed punch due to technical or genuine issues.\n\n"
                "Issue Details:\n"
                "- Grievance ID: {grievance_id}\n"
                "- Date(s) Requiring Regularization: __________\n"
                "- Reason: __________\n"
                "- Shift Timing: {shift_start} to {shift_end}\n\n"
                "Employee Information:\n"
                "- Full Name: {name}\n"
                "- ERP Code: {erp}\n\n"
                "Details:\n"
                "- Work was completed on the mentioned date(s)\n"
                "- Missed punch was due to: [Biometric malfunction / System issue / Other]\n"
                "- Manager Approval: [Will be obtained if required]\n\n"
                "Request: I kindly request you to process this attendance regularization as per company policy. This is within the allowed limit of 2 regularizations per month.\n\n"
                "Thank you for your assistance.\n\n"
                "Best Regards,\n{name}\nERP: {erp}"
            ),
        },
        "LOP dispute": {
            "policy_note": "LOP is applied when leave balance is exhausted or attendance is incomplete.",
            "explanation": (
                "LOP may be applied due to exhausted leave balance, unapproved leave, "
                "attendance shortage, or missed punch not regularized."
            ),
            "subject": "LOP Deduction Dispute – {month} – {erp}",
            "body_template": (
                "Dear HR / Payroll Team,\n\n"
                "I am writing to formally dispute the Loss of Pay (LOP) deduction applied to my salary for {month}.\n\n"
                "Issue Details:\n"
                "- Month: {month}\n"
                "- LOP Days Deducted: __________\n"
                "- LOP Amount Deducted: ₹__________\n"
                "- Grievance ID: {grievance_id}\n\n"
                "Employee Information:\n"
                "- Full Name: {name}\n"
                "- ERP Code: {erp}\n\n"
                "Reason for Dispute:\n"
                "- Leave balance was available [Attach proof]\n"
                "- Attendance was regularized [Mention dates]\n"
                "- Leave was properly approved [Mention approval details]\n\n"
                "Request: I kindly request you to review the LOP deduction in light of the above details and revert with a detailed explanation or correction.\n\n"
                "Thank you for your attention to this matter.\n\n"
                "Best Regards,\n{name}\nERP: {erp}"
            ),
        },
    },
    "PF / ESI / Tax": {
        "PF not reflecting": {
            "policy_note": "PF contributions may take time to reflect on the EPFO portal.",
            "explanation": (
                "PF contributions generally take time to reflect after payroll processing. "
                "Please verify your UAN, Aadhaar, PAN, and bank KYC details."
            ),
            "subject": "PF Contribution Not Reflecting – {erp}",
            "body_template": (
                "Dear HR / PF Administration Team,\n\n"
                "I am writing to report that my PF (Provident Fund) contribution for {month} is not reflecting on the EPFO portal.\n\n"
                "Issue Details:\n"
                "- Month: {month}\n"
                "- Expected Contribution: ₹__________\n"
                "- Grievance ID: {grievance_id}\n\n"
                "Employee Information:\n"
                "- Full Name: {name}\n"
                "- ERP Code: {erp}\n"
                "- UAN Number: __________\n"
                "- PAN: __________\n"
                "- Aadhaar: __________\n\n"
                "Verification Status:\n"
                "- UAN is active and linked to EPFO portal\n"
                "- KYC details are up-to-date\n"
                "- Bank account is verified\n\n"
                "Request: Could you please verify that the PF contribution was processed from your end and provide an update on when it will reflect on the EPFO portal? If there is a mismatch in my records, please advise on the rectification process.\n\n"
                "Thank you for your assistance.\n\n"
                "Best Regards,\n{name}\nERP: {erp}"
            ),
        },
        "Wrong TDS deducted": {
            "policy_note": "TDS is based on annual income projection and declared investments.",
            "explanation": (
                "Wrong TDS may happen if investment declarations, rent receipts, or previous employer "
                "details were not submitted or updated."
            ),
            "subject": "TDS Deduction Review – {month} – {erp}",
            "body_template": (
                "Dear HR / Tax Administration Team,\n\n"
                "I am writing to request a review of the Tax Deducted at Source (TDS) applied to my salary for {month}.\n\n"
                "Issue Details:\n"
                "- Month: {month}\n"
                "- TDS Deducted: ₹__________\n"
                "- Expected TDS: ₹__________\n"
                "- Difference: ₹__________\n"
                "- Grievance ID: {grievance_id}\n\n"
                "Employee Information:\n"
                "- Full Name: {name}\n"
                "- ERP Code: {erp}\n"
                "- PAN: __________\n"
                "- Annual Gross Income: ₹__________\n\n"
                "Declarations Submitted:\n"
                "- Investment declarations under Section 80C: Yes / No\n"
                "- Rent receipts (if applicable): Yes / No\n"
                "- Previous employer TDS certificate: Yes / No\n\n"
                "Request: I have submitted all necessary declarations and supporting documents. Could you please review the TDS calculation and adjust if there is an error? Please provide a detailed breakdown of the TDS computation.\n\n"
                "Thank you for your attention to this matter.\n\n"
                "Best Regards,\n{name}\nERP: {erp}"
            ),
        },
    },
    "Policy & General": {
        "Probation period query": {
            "policy_note": "Probation period depends on employee category.",
            "explanation": (
                "Probation period may vary by role or department. "
                "Please contact HR with your joining date and role for exact confirmation status."
            ),
            "subject": "Probation Status Confirmation – {erp}",
            "body_template": (
                "Dear HR / Employee Relations Team,\n\n"
                "I am writing to inquire about my probation status and request formal confirmation of completion if applicable.\n\n"
                "Employee Information:\n"
                "- Full Name: {name}\n"
                "- ERP Code: {erp}\n"
                "- Date of Joining: __________\n"
                "- Staff Category: __________\n"
                "- Grievance ID: {grievance_id}\n\n"
                "Details:\n"
                "- Expected Probation End Date: __________\n"
                "- Current Status: Pending / Completed\n\n"
                "Request: Could you please confirm my probation status based on my joining date and staff category? If my probation period has been completed, I would appreciate a formal confirmation of the same.\n\n"
                "Thank you for your assistance.\n\n"
                "Best Regards,\n{name}\nERP: {erp}"
            ),
        },
        "Reimbursement claim": {
            "policy_note": "Reimbursements require proper approval and bills.",
            "explanation": (
                "Reimbursement claims generally require manager approval, original bills, "
                "and correct claim details."
            ),
            "subject": "Reimbursement Claim Submission – {erp}",
            "body_template": (
                "Dear HR / Finance Team,\n\n"
                "I am writing to submit a reimbursement claim for expenses incurred in the course of business.\n\n"
                "Employee Information:\n"
                "- Full Name: {name}\n"
                "- ERP Code: {erp}\n"
                "- Grievance ID: {grievance_id}\n\n"
                "Expense Details:\n"
                "- Expense Type: __________\n"
                "- Category: Travel / Meals / Office / Other\n"
                "- Amount Claimed: ₹__________\n"
                "- Date of Expense: __________\n"
                "- Project / Purpose: __________\n\n"
                "Supporting Documents:\n"
                "- Original bills/invoices: Attached\n"
                "- Manager approval: Obtained\n"
                "- Description of expense: [Provide brief details]\n\n"
                "Request: Please process this reimbursement claim as per company policy. All supporting documents and approvals are in order.\n\n"
                "Thank you for your prompt processing.\n\n"
                "Best Regards,\n{name}\nERP: {erp}"
            ),
        },
    },
}


def _init_helpdesk_state():
    """Initialize helpdesk session state"""
    defaults = {
        "hd_messages": [],
        "hd_stage": "greeting",
        "hd_category": None,
        "hd_issue": None,
        "hd_user_info": {},
        "hd_info_step": 0,
        "hd_draft_subject": None,
        "hd_draft_body": None,
        "hd_grievance_id": None,
        "hd_shift_start": None,
        "hd_shift_end": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _bot(text, buttons=None):
    """Add bot message"""
    st.session_state.hd_messages.append({
        "role": "bot",
        "text": text,
        "buttons": buttons or [],
    })


def _user(text):
    """Add user message"""
    st.session_state.hd_messages.append({
        "role": "user",
        "text": text,
    })


def _reset_helpdesk():
    """Reset helpdesk state"""
    for key in list(st.session_state.keys()):
        if key.startswith("hd_"):
            del st.session_state[key]


def _validate_description(text):
    """Validate description is at least 50 words"""
    word_count = len(text.split())
    return word_count >= 50, word_count


def _start_chat():
    """Start helpdesk chat"""
    _bot(
        "👋 Hi! I'm Mitra, your HR Helpdesk Assistant.\n\n"
        "I'll help you understand your HR issue and create a formal grievance.\n\n"
        "What is your full name?"
    )
    st.session_state.hd_stage = "collect_info"
    st.session_state.hd_info_step = 0


def _show_categories():
    """Show issue categories"""
    st.session_state.hd_stage = "category"
    _bot(
        "Thank you. Please select the category of your issue:",
        buttons=list(FAQ.keys()) + ["Describe my own issue"],
    )


def _handle_collect_info(value):
    """Handle info collection (name, ERP, branch)"""
    step = st.session_state.hd_info_step
    user_info = st.session_state.hd_user_info

    if step == 0:
        user_info["name"] = value.strip()
        _user(value.strip())

        _bot(
            "Got it. Please enter your ERP Code.\n\n"
            "Format: 11 digits followed by `_OIS`\n"
            "Example: `20262002367_OIS`"
        )
        st.session_state.hd_info_step = 1
        return

    if step == 1:
        ok, error = _validate_erp(value)
        _user(value.strip())

        if not ok:
            _bot(f"{error}\n\nPlease re-enter your ERP Code:")
            return

        user_info["erp"] = value.strip()
        
        _bot("Please enter your Branch name (e.g., Makali, Kadugodi, Mysore Road")
        st.session_state.hd_info_step = 2
        return

    if step == 2:
        user_info["branch"] = value.strip()
        _user(value.strip())
        _show_categories()


def _validate_erp(erp_code):
    """Validate ERP code format"""
    pattern = r'^\d{11}_OIS$'
    if re.match(pattern, erp_code.strip()):
        return True, None
    return False, "❌ Invalid ERP format. Expected: 11 digits + _OIS (e.g., 20262002367_OIS)"


def _handle_category(category):
    """Handle category selection"""
    _user(category)

    if category == "Describe my own issue":
        st.session_state.hd_stage = "custom_input"
        _bot("Please describe your issue in detail (minimum 50 words required):")
        return

    st.session_state.hd_category = category
    st.session_state.hd_stage = "sub_issue"

    _bot(
        f"You selected **{category}**.\n\nPlease choose your specific issue:",
        buttons=list(FAQ[category].keys()) + ["Back to categories"],
    )


def _create_draft(subject_template, body_template, grievance_id):
    """Create professional email draft"""
    user_info = st.session_state.hd_user_info

    today = datetime.now().strftime("%d %B %Y")
    month = datetime.now().strftime("%B %Y")

    subject = subject_template.format(
        erp=user_info.get("erp", "[ERP]"),
        month=month,
    )

    shift_start = st.session_state.hd_shift_start or "HH:MM"
    shift_end = st.session_state.hd_shift_end or "HH:MM"

    body = body_template.format(
        name=user_info.get("name", "[Name]"),
        erp=user_info.get("erp", "[ERP]"),
        month=month,
        date=today,
        grievance_id=grievance_id,
        shift_start=shift_start,
        shift_end=shift_end,
    )

    st.session_state.hd_draft_subject = subject
    st.session_state.hd_draft_body = body


def _handle_sub_issue(issue):
    """Handle sub-issue selection"""
    if issue == "Back to categories":
        _user(issue)
        st.session_state.hd_category = None
        st.session_state.hd_issue = None
        _show_categories()
        return

    _user(issue)

    category = st.session_state.hd_category
    data = FAQ[category][issue]

    st.session_state.hd_issue = issue
    st.session_state.hd_stage = "shift_selection"

    _bot(f"**{issue}**\n\n{data['explanation']}")

    _bot(
        "If this issue is related to attendance, please select your shift timing "
        "(or leave blank if not applicable):",
        buttons=list(SHIFT_TEMPLATES.keys()) + ["Custom shift", "Not applicable"],
    )


def _handle_shift_selection(choice):
    """Handle shift selection"""
    _user(choice)

    if choice == "Not applicable":
        st.session_state.hd_shift_start = None
        st.session_state.hd_shift_end = None
        _finalize_grievance()
    elif choice == "Custom shift":
        st.session_state.hd_stage = "custom_shift"
        _bot("Enter your shift start time (HH:MM format, e.g., 09:00):")
    else:
        st.session_state.hd_shift_start, st.session_state.hd_shift_end = SHIFT_TEMPLATES[choice]
        _finalize_grievance()


def _finalize_grievance():
    """Finalize and create grievance"""
    db = get_db()

    category = st.session_state.get("hd_category")
    issue = st.session_state.get("hd_issue")
    user_info = st.session_state.hd_user_info

    is_custom_issue = not category or not issue

    if is_custom_issue:
        description = st.session_state.get("hd_custom_description", "Custom HR issue")
        subject_template = "Custom HR Grievance – {erp}"
        body_template = (
            "Dear HR Team,\n\n"
            "I am writing to raise the following HR grievance:\n\n"
            "{description}\n\n"
            "Employee Information:\n"
            "- Full Name: {name}\n"
            "- ERP Code: {erp}\n"
            "- Branch: {branch}\n"
            "- Grievance ID: {grievance_id}\n\n"
            "Shift Details:\n"
            "- Shift Start: {shift_start}\n"
            "- Shift End: {shift_end}\n\n"
            "Kindly review this issue and guide me on the next steps.\n\n"
            "Thank you,\n"
            "{name}\n"
            "ERP: {erp}"
        )
        issue_type = "Custom Issue"

    else:
        data = FAQ[category][issue]
        description = f"{issue}: {data['explanation']}"
        subject_template = data["subject"]
        body_template = data["body_template"]
        issue_type = category

    grievance_id = db.create_grievance(
        erp_code=user_info.get("erp"),
        employee_name=user_info.get("name"),
        branch=user_info.get("branch"),
        issue_type=issue_type,
        description=description,
        subject=subject_template,
        shift_start=st.session_state.get("hd_shift_start"),
        shift_end=st.session_state.get("hd_shift_end"),
    )

    st.session_state.hd_grievance_id = grievance_id
    st.session_state.hd_stage = "resolution"

    if is_custom_issue:
        today = datetime.now().strftime("%d %B %Y")

        subject = subject_template.format(
            erp=user_info.get("erp", "[ERP]")
        )

        body = body_template.format(
            name=user_info.get("name", "[Name]"),
            erp=user_info.get("erp", "[ERP]"),
            branch=user_info.get("branch", "[Branch]"),
            grievance_id=grievance_id,
            description=description,
            shift_start=st.session_state.get("hd_shift_start") or "Not applicable",
            shift_end=st.session_state.get("hd_shift_end") or "Not applicable",
            date=today,
        )

        st.session_state.hd_draft_subject = subject
        st.session_state.hd_draft_body = body

    else:
        _create_draft(subject_template, body_template, grievance_id)

    _bot(
        f"✅ **Grievance Created**\n\n"
        f"**Grievance ID:** {grievance_id}\n\n"
        f"Your draft email is ready below. Fill in any blanks and send it to **{HR_EMAIL}**.\n\n"
        f"You can track the status of this grievance in your dashboard.",
        buttons=["Issue resolved", "Need more clarity", "I have another issue", "Close chat"],
    )

def _handle_custom_issue(issue_text):
    """Handle custom issue input"""
    issue_text = issue_text.strip()
    valid, word_count = _validate_description(issue_text)

    _user(issue_text[:100] + "..." if len(issue_text) > 100 else issue_text)

    if not valid:
        _bot(
            f"❌ Your description is too short ({word_count} words). "
            f"Please provide at least 50 words describing your issue:\n\n"
            f"Current: {word_count} words | Required: 50 words"
        )
        return

    st.session_state.hd_custom_description = issue_text
    st.session_state.hd_stage = "shift_selection"
    
    _bot(
        "Thank you. If this issue is related to attendance, please select your shift timing "
        "(or leave blank if not applicable):",
        buttons=list(SHIFT_TEMPLATES.keys()) + ["Custom shift", "Not applicable"],
    )


def _handle_custom_shift(time_input):
    """Handle custom shift time input"""
    _user(time_input)

    # Validate time format
    try:
        datetime.strptime(time_input.strip(), "%H:%M")
        if not st.session_state.get("hd_shift_start"):
            st.session_state.hd_shift_start = time_input.strip()
            _bot("Enter your shift end time (HH:MM format, e.g., 17:30):")
        else:
            st.session_state.hd_shift_end = time_input.strip()
            
            # Add 15 min buffer
            end_time = datetime.strptime(time_input.strip(), "%H:%M")
            buffered_end = (end_time.hour * 60 + end_time.minute + 15) % (24 * 60)
            st.session_state.hd_shift_end = f"{buffered_end // 60:02d}:{buffered_end % 60:02d}"
            
            _bot(f"✅ Shift time recorded with 15-minute buffer:\n\n"
                 f"Start: {st.session_state.hd_shift_start}\n"
                 f"End: {st.session_state.hd_shift_end}")
            
            _finalize_grievance()
    except ValueError:
        _bot("❌ Invalid time format. Please use HH:MM format (e.g., 09:00)")


def _handle_resolution(choice):
    """Handle resolution options"""
    _user(choice)

    if choice == "Issue resolved":
        st.session_state.hd_stage = "closed"
        grievance_id = st.session_state.hd_grievance_id
        _bot(
            f"Great! 🎉\n\n"
            f"Your grievance (ID: **{grievance_id}**) has been registered.\n\n"
            f"You can track its status in your dashboard.\n\n"
            f"Thank you for using Mitra HR!"
        )
        return

    if choice == "Need more clarity":
        category = st.session_state.hd_category
        issue = st.session_state.hd_issue

        if category and issue:
            data = FAQ[category][issue]
            _bot(
                f"Here is more detail on **{issue}**:\n\n"
                f"{data['explanation']}\n\n"
                f"**Policy note:** {data.get('policy_note', '')}\n\n"
                "Feel free to send the drafted email to HR or contact your manager for additional support.",
                buttons=["Issue resolved", "I have another issue", "Close chat"],
            )
        else:
            _bot(
                "For custom issues, the best next step is to send the drafted email to HR.",
                buttons=["Issue resolved", "I have another issue", "Close chat"],
            )
        return

    if choice == "I have another issue":
        st.session_state.hd_stage = "category"
        st.session_state.hd_category = None
        st.session_state.hd_issue = None
        st.session_state.hd_draft_subject = None
        st.session_state.hd_draft_body = None
        st.session_state.hd_grievance_id = None
        st.session_state.hd_shift_start = None
        st.session_state.hd_shift_end = None
        st.session_state.hd_custom_description = ""
        _show_categories()
        return

    if choice == "Close chat":
        st.session_state.hd_stage = "closed"
        _bot("Thank you for using Mitra HR Helpdesk. Goodbye! 👋")
        return


def _render_message(message):
    """Render chat message"""
    text = message["text"].replace("\n", "<br>")

    if message["role"] == "bot":
        st.markdown(
            f"""
            <div class="msg-bot">
                <div class="avatar">M</div>
                <div>
                    <div class="chat-name">Mitra</div>
                    <div class="bubble">{text}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="msg-user">
                <div class="bubble">{text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_draft_box():
    """Render email draft"""
    subject = st.session_state.get("hd_draft_subject")
    body = st.session_state.get("hd_draft_body")

    if not subject or not body:
        return

    st.markdown("---")
    st.markdown("### 📧 Your Draft Email")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("### 📧 Email Draft")

        st.markdown(f"**To:** {HR_EMAIL}")
        st.markdown(f"**Subject:** {subject}")

        st.text_area(
            "Email Body",
            value=body,
            height=300
)

    # with col2:
    #     st.markdown("### Actions")
        
    #     # Copy button
    #     st.code(f"To: {HR_EMAIL}\nSubject: {subject}\n\n{body}", language="text")

        mailto = (
            f"mailto:{HR_EMAIL}"
            f"?subject={urllib.parse.quote(subject)}"
            f"&body={urllib.parse.quote(body)}"
        )

        st.markdown(
            f'<a href="{mailto}" target="_blank" style="display: inline-block; padding: 10px 20px; '
            f'background-color: #667eea; color: white; text-decoration: none; border-radius: 5px;">'
            f'📧 Open in Mail</a>',
            unsafe_allow_html=True
        )


def _render_buttons(last_bot, stage):
    """Render action buttons"""
    buttons = last_bot.get("buttons", [])

    if not buttons:
        return

    st.write("**Choose an option:**")

    cols = st.columns(min(3, len(buttons)))

    for index, button_text in enumerate(buttons):
        with cols[index % len(cols)]:
            if st.button(button_text, key=f"hd_{stage}_{index}_{button_text}", use_container_width=True):
                if stage == "category":
                    _handle_category(button_text)
                elif stage == "sub_issue":
                    _handle_sub_issue(button_text)
                elif stage == "shift_selection":
                    _handle_shift_selection(button_text)
                elif stage == "resolution":
                    _handle_resolution(button_text)

                st.rerun()


def helpdesk_page():
    """Main helpdesk page"""
    _init_helpdesk_state()

    st.markdown(
        """
        <div class="page-header">
            <h1>💼 HR Helpdesk — Mitra</h1>
            <p>Create and track your HR grievances with professional emails</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 New Chat", use_container_width=True, key="hd_new_chat"):
            _reset_helpdesk()
            st.rerun()

    if not st.session_state.hd_messages:
        _start_chat()

    for message in st.session_state.hd_messages:
        _render_message(message)

    if st.session_state.get("hd_draft_subject"):
        _render_draft_box()

    if st.session_state.hd_stage == "closed":
        st.success("✅ Conversation closed.")
        return

    stage = st.session_state.hd_stage

    last_bot = next(
        (msg for msg in reversed(st.session_state.hd_messages) if msg["role"] == "bot"),
        None,
    )

    if last_bot and last_bot.get("buttons"):
        _render_buttons(last_bot, stage)

    elif stage == "collect_info":
        with st.form("hd_info_form", clear_on_submit=True):
            value = st.text_input("Your response", key="hd_collect_info_input")
            submitted = st.form_submit_button("Send", use_container_width=True)

            if submitted and value.strip():
                _handle_collect_info(value.strip())
                st.rerun()

    elif stage == "custom_input":
        with st.form("hd_custom_form", clear_on_submit=True):
            value = st.text_area("Describe your issue", height=150, key="hd_custom_input")
            word_count = len(value.split())
            st.caption(f"Word count: {word_count} / 50 (minimum)")

            submitted = st.form_submit_button("Send", use_container_width=True)

            if submitted and value.strip():
                _handle_custom_issue(value.strip())
                st.rerun()

    elif stage == "custom_shift":
        with st.form("hd_custom_shift_form", clear_on_submit=True):
            value = st.text_input("Time (HH:MM format)", key="hd_custom_shift_input")
            submitted = st.form_submit_button("Send", use_container_width=True)

            if submitted and value.strip():
                _handle_custom_shift(value.strip())
                st.rerun()
