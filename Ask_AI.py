# Ask_AI.py

import streamlit as st

try:
    from groq import Groq
except Exception:
    Groq = None

try:
    from config import HR_EMAIL
except Exception:
    HR_EMAIL = "payroll2.branch@orchids.edu.in"

HANDBOOK = "handbook_text.txt"


def load_handbook_text():
    try:
        with open(HANDBOOK, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def get_groq_client():
    if Groq is None:
        return None

    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        return None

    if not api_key:
        return None

    return Groq(api_key=api_key)


def get_model_name():
    try:
        return st.secrets["GROQ_MODEL"]
    except Exception:
        return "llama-3.3-70b-versatile"


def looks_like_code(text):
    code_signals = [
        "import ",
        "def ",
        "class ",
        "return ",
        "st.",
        "```python",
        "from groq",
        "from openai",
    ]
    lowered = text.lower()
    return any(signal in lowered for signal in code_signals)


def build_prompt(handbook_text):
    return f"""
You are Mitra, a professional HR assistant for Orchids employees.

Your role:
- Reply to employee HR questions.
- First use the HR handbook if the answer is available.
- If the handbook does not clearly mention the issue, provide safe general HR guidance.
- If the issue needs official confirmation, ask the employee to contact HR.
- Help reduce unnecessary grievances by guiding the employee on what to check first.

Important rules:
- Do NOT approve or reject any request.
- Do NOT promise salary correction, leave approval, attendance correction, PF/ESI update, reimbursement, or exception.
- Do NOT say final decision is yours.
- Do NOT blame HR, payroll, manager, school, or employee.
- Do NOT create fake policy.
- If not covered in handbook, clearly say: "This is not clearly mentioned in the handbook and should be confirmed by HR."
- Always be polite and professional.

Reply format:

### Response to your query
Answer the employee clearly.

### Based on handbook / HR guidance
Mention whether the answer is based on handbook or general HR guidance.

### What you should check first
Give practical checks.

### Recommended next step
Give the safest action.

### When to contact HR
Mention when HR escalation is needed.

### HR email draft
If required, provide a short email draft.

HR Email:
{HR_EMAIL}

HR Handbook:
{handbook_text}
"""


def generate_ai_response(employee_query, handbook_text):
    if not handbook_text.strip():
        handbook_text = (
            "Handbook content is not available. "
            "Use only safe general HR guidance and recommend HR confirmation."
        )

    client = get_groq_client()

    if client is None:
        return f"""
⚠️ AI is not configured.

Please configure Groq API in `.streamlit/secrets.toml`.

For now, please contact HR for confirmation:
{HR_EMAIL}
"""

    try:
        response = client.chat.completions.create(
            model=get_model_name(),
            messages=[
                {"role": "system", "content": build_prompt(handbook_text)},
                {"role": "user", "content": employee_query},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"""
⚠️ AI response failed.

Error:
{str(e)}

Please contact HR for confirmation:
{HR_EMAIL}
"""


def ask_ai_page():
    st.markdown(
        """
        <div class="page-header">
            <h1>🤖 AI Mode</h1>
            <p>Ask HR questions · Get handbook or HR-guided response</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "AI Mode replies using the handbook where available. If the handbook does not cover the issue, it gives safe HR guidance and suggests escalation."
    )

    employee_query = st.text_area(
        "Ask your HR question",
        placeholder="Example: My salary is less this month. What should I check before raising a grievance?",
        height=160,
    )

    if st.button("Ask AI", use_container_width=True):
        employee_query = employee_query.strip()

        if not employee_query:
            st.warning("Please enter your HR question.")
            return

        if looks_like_code(employee_query):
            st.warning("Please enter an employee HR question, not code.")
            return

        handbook_text = load_handbook_text()

        with st.spinner("Preparing HR-guided response..."):
            answer = generate_ai_response(employee_query, handbook_text)

        st.markdown("## 🤖 Mitra Response")
        st.markdown(answer)