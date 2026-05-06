# Handbook.py

import re
import streamlit as st
from config import HANDBOOK


def load_sections(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return {}

    sections = {}

    pattern = re.compile(
        r"(Section\s*\d+\s*[:\-]?\s*[^\n]*)(.*?)(?=Section\s*\d+\s*[:\-]?|\Z)",
        re.DOTALL | re.IGNORECASE,
    )

    for match in pattern.finditer(text):
        title = match.group(1).strip()
        content = match.group(2).strip()

        title_match = re.match(r"(Section\s*\d+)\s*[:\-]?\s*(.*)", title, re.IGNORECASE)

        if title_match:
            section_no = title_match.group(1).strip()
            section_name = title_match.group(2).strip()

            display_title = (
                f"{section_no} — {section_name}"
                if section_name
                else section_no
            )
        else:
            display_title = title

        sections[display_title] = content

    return sections


def format_to_bullets(text):
    points = []

    raw_points = re.split(r"\n+|(?<=[.!?])\s+", text)

    for point in raw_points:
        point = point.strip()

        if not point:
            continue

        point = re.sub(r"^[\d\.\-\*\•\s]+", "", point).strip()

        if len(point) > 3:
            points.append(point)

    return points


def handbook_page():
    st.markdown(
        """
        <div class="page-header">
            <h1>📖 Handbook</h1>
            <p>Select a topic to read policy points clearly.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sections = load_sections(HANDBOOK)

    if not sections:
        st.error("Handbook file not found or no valid sections detected.")
        return

    selected = st.selectbox(
        "Select Topic",
        list(sections.keys()),
        key="handbook_topic_select",
    )

    content = sections[selected]
    bullets = format_to_bullets(content)

    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown(f"## {selected}")

    if bullets:
        for point in bullets:
            st.markdown(f"- {point}")
    else:
        st.info("No readable points found for this section.")

    st.markdown("</div>", unsafe_allow_html=True)