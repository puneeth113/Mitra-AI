"""
Ask AI - Professional HR Assistance System
Handles: General HR Queries | Salary Text Questions | Payslip Upload & Analysis
Version: 3.0 - With Integrated Payslip Analysis
"""

import streamlit as st
from typing import Tuple

try:
    from groq import Groq
except Exception:
    Groq = None

PDF_IMPORT_ERROR = None
PdfReader = None

try:
    from pypdf import PdfReader
except Exception as e1:
    try:
        from PyPDF2 import PdfReader
    except Exception as e2:
        PDF_IMPORT_ERROR = f"pypdf error: {e1} | PyPDF2 error: {e2}"

try:
    from config import HR_EMAIL
except Exception:
    HR_EMAIL = "payroll2.branch@orchids.edu.in"

HANDBOOK = "handbook_text.txt"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def load_handbook_text() -> str:
    """Load HR handbook for context"""
    try:
        with open(HANDBOOK, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def get_groq_client():
    """Get Groq API client"""
    if Groq is None:
        return None

    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        return None

    if not api_key:
        return None

    return Groq(api_key=api_key)


def get_model_name() -> str:
    """Get Groq model name"""
    try:
        return st.secrets["GROQ_MODEL"]
    except Exception:
        return "llama-3.3-70b-versatile"


def looks_like_code(text: str) -> bool:
    """Check if text looks like code"""
    code_signals = [
        "import ",
        "def ",
        "class ",
        "return ",
        "st.",
        "```python",
        "from groq",
        "from openai",
        "<<",
        ">>",
        "exec(",
        "eval(",
    ]

    lowered = text.lower()
    return any(signal in lowered for signal in code_signals)


def extract_pdf_text(uploaded_pdf) -> Tuple[str, str]:
    """
    Extract text from PDF file.
    Returns: (text, error_message)
    """
    if PdfReader is None:
        return "", (
            "❌ PDF reader is not available in the current environment.\n\n"
            f"Import error details:\n{PDF_IMPORT_ERROR}\n\n"
            "Fix:\n"
            "1. Add `pypdf` and `PyPDF2` to requirements.txt\n"
            "2. Push to GitHub\n"
            "3. Reboot Streamlit app"
        )

    try:
        reader = PdfReader(uploaded_pdf)

        if len(reader.pages) == 0:
            return "", "❌ PDF has no pages. Please upload a valid payslip PDF."

        text = ""

        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text() or ""

            if page_text.strip():
                text += f"--- Page {page_num} ---\n{page_text}\n"

        text = text.strip()

        if not text or len(text) < 50:
            return "", (
                "❌ Could not extract text from PDF. "
                "Please ensure it is a readable payslip PDF, not a scanned image."
            )

        return text, ""

    except Exception as e:
        return "", f"❌ Error reading PDF: {str(e)[:150]}"


# ============================================================================
# PROMPT BUILDERS
# ============================================================================

def build_general_hr_prompt(handbook_text: str) -> str:
    """Build system prompt for general HR queries"""
    return f"""
You are Mitra, a professional HR assistant for employees.

Your role:
- Reply to employee HR questions professionally and accurately.
- Use the HR handbook if available.
- If the handbook does not cover the topic, provide safe general HR guidance.
- Guide employees on what to check before escalating to HR.
- Help reduce unnecessary grievances with helpful guidance.

Important rules:
- Do NOT approve, reject, or promise any action.
- Do NOT promise salary corrections, leave approvals, or exceptions.
- Do NOT make final HR decisions.
- Do NOT blame HR, payroll, management, or employees.
- Do NOT create fake policies.
- If uncertain, recommend contacting HR for official confirmation.
- Always be polite, professional, and empathetic.
- Acknowledge legitimate concerns.

Response format:

### Your Question Answered
Provide a clear, helpful answer.

### Based on Handbook or General HR Practice
State whether the answer comes from handbook or general HR guidance.

### What to Check First
List practical steps employee should take.

### Recommended Next Step
Suggest safest action.

### When to Contact HR
Clearly state when HR involvement is needed.

### Quick Email Draft
Provide a professional email template if appropriate.

HR Email:
{HR_EMAIL}

Handbook:
{handbook_text if handbook_text.strip() else "Not available"}
"""


def build_salary_query_prompt(handbook_text: str) -> str:
    """Build system prompt for salary-related text queries"""
    return f"""
You are Mitra, a payroll specialist HR assistant.

Your expertise:
- Salary structure
- Salary components
- Deductions
- Payslip explanation
- TDS
- PF
- ESI
- LOP

Your role:
- Explain salary components clearly and accurately.
- Help employees understand payslip deductions.
- Guide on common salary issues and solutions.
- Recommend when to contact payroll team.

Important rules:
- Do NOT promise salary corrections or refunds.
- Do NOT make payroll decisions.
- Explain TDS, PF, ESI objectively without guarantees.
- Use employee-friendly language.
- Provide helpful verification steps.
- Recommend payroll escalation when needed.

Response format:

### Salary Explanation
Clear explanation of the salary concept or issue.

### How It Works
Break down relevant components or rules.

### What to Verify
Practical checks employee should do first.

### Common Reasons This Happens
Explain potential causes if applicable.

### When to Escalate to Payroll
Clear guidance on HR/payroll escalation.

### Sample Email to Payroll
Professional email template if needed.

HR Email:
{HR_EMAIL}

Handbook:
{handbook_text if handbook_text.strip() else "Not available"}
"""


def build_payslip_analysis_prompt(handbook_text: str, payslip_text: str) -> str:
    """Build system prompt for payslip PDF analysis"""
    return f"""
You are Mitra, a professional payroll analyst and HR assistant.

Your task:
Analyze uploaded payslips and answer specific employee questions.

Your expertise:
- Payslip components and calculations
- PF, ESI, TDS, Professional Tax, LOP
- Basic, HRA, Allowances, Arrears, Bonus
- Month-to-month salary variations

Your role:
- Explain what each component means.
- Help employees understand deductions.
- Identify possible salary discrepancies.
- Guide verification steps.
- Recommend payroll escalation when needed.

Important rules:
- Do NOT promise corrections or refunds.
- Do NOT make final payroll decisions.
- Acknowledge if payslip data is unclear.
- Provide objective, fact-based explanations.
- Always recommend official confirmation from payroll.
- Use employee-friendly language.
- Protect employee privacy.
- Never expose full PAN, Aadhaar, UAN, or bank account numbers.

Response format:

### Payslip Summary
Summarize key numbers such as total earnings, deductions, net salary, month/year if visible.

### Earnings Breakdown
Explain each visible earning component.

### Deductions Breakdown
Explain each visible deduction:
- What it is
- Why it is deducted
- How it is generally calculated
- Whether it looks normal or needs verification

### Net Salary Calculation
Show: Total Earnings - Total Deductions = Net Salary, only if visible.

### Key Observations
Highlight unusual deductions, LOP, TDS changes, arrears, or missing data.

### What to Verify
List practical checks:
- Compare with previous month
- Check leave/LOP
- Check offer letter/salary structure
- Check ERP/Eduvate records
- Check bank credit

### When to Contact Payroll
Explain when escalation is needed.

### Quick Email to Payroll
Prepare a professional email if escalation is required.

HR Email:
{HR_EMAIL}

Handbook:
{handbook_text if handbook_text.strip() else "Not available"}

Payslip Content to Analyze:
{payslip_text}
"""


# ============================================================================
# AI RESPONSE GENERATORS
# ============================================================================

def generate_general_hr_response(employee_query: str, handbook_text: str) -> str:
    """Generate response for general HR queries"""

    if not handbook_text.strip():
        handbook_text = "Handbook not available. Use safe general HR best practices."

    client = get_groq_client()

    if client is None:
        return f"""
⚠️ **AI Service Not Available**

The AI response feature requires Groq API configuration.

Please contact HR directly:

📧 **HR Email:** {HR_EMAIL}
"""

    try:
        response = client.chat.completions.create(
            model=get_model_name(),
            messages=[
                {"role": "system", "content": build_general_hr_prompt(handbook_text)},
                {"role": "user", "content": employee_query},
            ],
            temperature=0.2,
            max_tokens=1500,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"""
⚠️ **AI Response Error**

Error:
{str(e)[:200]}

Please contact HR directly:

📧 **HR Email:** {HR_EMAIL}
"""


def generate_salary_response(employee_query: str, handbook_text: str) -> str:
    """Generate response for salary-related text queries"""

    if not handbook_text.strip():
        handbook_text = "Handbook not available. Use safe general salary guidance."

    client = get_groq_client()

    if client is None:
        return f"""
⚠️ **AI Service Not Available**

The salary explanation feature requires Groq API configuration.

For salary questions, contact:

📧 **Payroll / HR Email:** {HR_EMAIL}

Prepare:
- Your payslip
- Specific question about deduction/component
- Month/period in question
"""

    try:
        response = client.chat.completions.create(
            model=get_model_name(),
            messages=[
                {"role": "system", "content": build_salary_query_prompt(handbook_text)},
                {"role": "user", "content": employee_query},
            ],
            temperature=0.2,
            max_tokens=1500,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"""
⚠️ **Salary Query Error**

Error:
{str(e)[:200]}

Please contact payroll team directly:

📧 **Payroll Email:** {HR_EMAIL}
"""


def generate_payslip_analysis(
    employee_query: str,
    payslip_text: str,
    handbook_text: str,
) -> str:
    """Generate payslip analysis response"""

    if not handbook_text.strip():
        handbook_text = "Handbook not available. Use safe payslip analysis guidance."

    if not payslip_text or len(payslip_text) < 50:
        return "❌ **Error:** Could not extract payslip content. Please upload again."

    client = get_groq_client()

    if client is None:
        return f"""
⚠️ **AI Service Not Available**

The payslip analysis feature requires Groq API configuration.

For payslip questions, contact:

📧 **Payroll / HR Email:** {HR_EMAIL}

Send:
- Your payslip PDF or screenshot
- Specific question
- Month/year of concern
"""

    try:
        user_message = f"""
Please analyze my payslip and answer this question:

{employee_query if employee_query.strip() else "Please explain all components of my payslip."}

Provide:
1. Summary of my salary
2. Explanation of each earning and deduction
3. Whether anything looks unusual
4. What I should verify
5. When to contact payroll if needed
"""

        response = client.chat.completions.create(
            model=get_model_name(),
            messages=[
                {
                    "role": "system",
                    "content": build_payslip_analysis_prompt(handbook_text, payslip_text),
                },
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
            max_tokens=2000,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"""
⚠️ **Payslip Analysis Error**

Error:
{str(e)[:200]}

Please contact payroll team directly:

📧 **Payroll Email:** {HR_EMAIL}
"""


# ============================================================================
# UI SECTIONS
# ============================================================================

def render_general_hr_section():
    """Render General HR Query Section"""

    st.markdown(
        """
        ### 🤖 General HR Questions

        Ask about policies, leaves, attendance, benefits, career growth, or other HR matters.
        """
    )

    with st.container(border=True):
        st.markdown("**Example Questions:**")
        examples_hr = [
            "How many casual leaves per year?",
            "What should I check if attendance is wrong?",
            "Can I request work-from-home?",
            "What should I do before raising a grievance?",
        ]

        for example in examples_hr:
            st.caption(f"• {example}")

    employee_query = st.text_area(
        "Your HR Question",
        placeholder="Type your HR question here...",
        height=120,
        key="general_hr_query",
    )

    if st.button(
        "🔍 Ask HR Assistant",
        use_container_width=True,
        key="general_hr_button",
        type="primary",
    ):
        if not employee_query or not employee_query.strip():
            st.warning("⚠️ Please enter your HR question.")
            return

        if looks_like_code(employee_query):
            st.warning("⚠️ Please enter an HR question, not code.")
            return

        handbook_text = load_handbook_text()

        with st.spinner("🤔 Analyzing your question..."):
            response = generate_general_hr_response(
                employee_query.strip(),
                handbook_text,
            )

        st.markdown("---")
        st.markdown("## 💬 Mitra's Response")
        st.markdown(response)


def render_salary_query_section():
    """Render Salary Text Query Section"""

    st.markdown(
        """
        ### 💰 Salary Questions

        Ask about salary components, deductions, payslip, TDS, PF, ESI, LOP, or any salary matter.
        """
    )

    with st.container(border=True):
        st.markdown("**Example Questions:**")
        examples_salary = [
            "What is TDS?",
            "How is PF calculated?",
            "What is LOP?",
            "Why is ESI deducted?",
        ]

        for example in examples_salary:
            st.caption(f"• {example}")

    employee_query = st.text_area(
        "Your Salary Question",
        placeholder="Ask about salary components, deductions, or related matters...",
        height=120,
        key="salary_query",
    )

    if st.button(
        "💰 Get Explanation",
        use_container_width=True,
        key="salary_query_button",
        type="primary",
    ):
        if not employee_query or not employee_query.strip():
            st.warning("⚠️ Please enter your salary question.")
            return

        if looks_like_code(employee_query):
            st.warning("⚠️ Please enter a salary question, not code.")
            return

        handbook_text = load_handbook_text()

        with st.spinner("💼 Analyzing salary question..."):
            response = generate_salary_response(
                employee_query.strip(),
                handbook_text,
            )

        st.markdown("---")
        st.markdown("## 💬 Mitra's Response")
        st.markdown(response)


def render_payslip_upload_section():
    """Render Payslip Upload & Analysis Section"""

    st.markdown(
        """
        ### 📄 Payslip Upload & Analysis

        Upload your salary payslip PDF and ask questions about deductions, LOP, TDS, PF, ESI, or net salary.
        """
    )

    with st.container(border=True):
        st.warning(
            """
            🔒 **Your Privacy Matters**

            - Payslip data is not stored by this app.
            - Processing happens only for the current session.
            - Avoid uploading unnecessary sensitive information.
            - For official confirmation, contact payroll.
            """
        )

    st.divider()

    st.markdown("#### Step 1: Upload Your Payslip PDF")

    uploaded_file = st.file_uploader(
        "Choose payslip PDF file",
        type=["pdf"],
        accept_multiple_files=False,
        key="payslip_pdf_upload",
    )

    if uploaded_file is None:
        st.info("👆 Upload a payslip PDF to get started.")

        with st.expander("📖 Common Payslip Components Guide", expanded=False):
            components = {
                "Basic Salary": "Fixed base salary as per employment contract.",
                "HRA": "House Rent Allowance.",
                "Allowances": "Additional salary components.",
                "Arrears": "Salary adjustment from previous months.",
                "Bonus": "Performance or annual bonus.",
                "PF": "Provident Fund contribution.",
                "ESI": "Employee State Insurance, if applicable.",
                "TDS": "Tax Deducted at Source.",
                "Professional Tax": "State-level professional tax.",
                "LOP": "Loss of Pay for unpaid absence.",
            }

            for component, description in components.items():
                st.write(f"**{component}**")
                st.caption(description)

        return

    st.success(f"✅ File uploaded: {uploaded_file.name}")

    with st.spinner("📖 Reading payslip..."):
        payslip_text, error = extract_pdf_text(uploaded_file)

    if error:
        st.error(error)
        return

    if not payslip_text:
        st.error("❌ Could not extract text from payslip.")
        return

    with st.expander("📋 Payslip Preview", expanded=False):
        st.text(payslip_text[:500] + "..." if len(payslip_text) > 500 else payslip_text)

    st.divider()

    st.markdown("#### Step 2: Ask Questions About Your Payslip")

    employee_query = st.text_area(
        "Your Question About Payslip",
        placeholder="Example: Why is my net salary less this month?",
        height=120,
        key="payslip_query",
    )

    analyze_button = st.button(
        "📊 Analyze Payslip",
        use_container_width=True,
        key="payslip_analyze_button",
        type="primary",
    )

    if analyze_button:
        if employee_query and looks_like_code(employee_query):
            st.warning("⚠️ Please enter a payslip question, not code.")
            return

        handbook_text = load_handbook_text()

        with st.spinner("📊 Analyzing your payslip..."):
            response = generate_payslip_analysis(
                employee_query.strip() if employee_query else "",
                payslip_text,
                handbook_text,
            )

        st.markdown("---")
        st.markdown("## 📊 Mitra's Payslip Analysis")
        st.markdown(response)

        st.divider()

        st.markdown("### 📋 Next Steps")

        col1, col2 = st.columns(2)

        with col1:
            st.info(
                """
                📧 **Need Official Answer?**

                Contact payroll with:
                - Payslip
                - Specific question
                - Month/year
                - Any discrepancy noticed
                """
            )

        with col2:
            st.info(
                f"""
                📞 **Payroll Contact**

                Email: {HR_EMAIL}

                Subject: Payslip Clarification - [Month/Year]
                """
            )


# ============================================================================
# MAIN PAGE
# ============================================================================

def ask_ai_page():
    """Main Ask AI Page"""

    st.markdown(
        """
        <div class="page-header">
            <h1>🤖 AI HR Assistant</h1>
            <p>Professional HR & Salary Assistance • Payslip Analysis • Guided by Handbook</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        """
        💡 **Three Ways to Get Help:**

        1. **🤖 General HR Questions** - Policies, leave, attendance, benefits
        2. **💰 Salary Questions** - Deductions, salary components, TDS, PF, ESI
        3. **📄 Payslip Upload** - Upload PDF payslip and ask questions

        AI gives guidance only. For official decisions, contact HR/payroll.
        """
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "🤖 General HR",
            "💰 Salary Q&A",
            "📄 Payslip Upload",
        ]
    )

    with tab1:
        render_general_hr_section()

    with tab2:
        render_salary_query_section()

    with tab3:
        render_payslip_upload_section()

    st.divider()

    st.markdown(
        f"""
        <div style="text-align:center; color:gray; font-size:12px; margin-top:20px;">
            <strong>Need additional help?</strong> Contact HR: {HR_EMAIL}<br>
            Information is based on handbook guidance and general HR practices.
            For official decisions, always contact HR directly.
        </div>
        """,
        unsafe_allow_html=True,
    )
