"""
Admin Grievance Management Dashboard
View, filter, and update employee grievances
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from Grievance_db import get_db
import plotly.express as px
import plotly.graph_objects as go


def admin_page():
    """Main admin grievance management page"""
    
    st.markdown(
        """
        <div class="page-header">
            <h1>📊 Grievance Management Dashboard</h1>
            <p>Manage and track employee grievances</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Logout button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("🚪 Logout", use_container_width=True, key="admin_logout"):
            st.session_state.authenticated = False
            st.session_state.user_type = None
            st.session_state.user_erp = None
            st.session_state.authenticated = False
            st.session_state.user_type = None
            st.session_state.user_erp = None
            st.rerun()

    st.divider()

    db = get_db()

    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 All Grievances",
        "📈 Statistics",
        "🔍 Search & Filter",
        "📥 Export Data"
    ])

    # ========== TAB 1: ALL GRIEVANCES ==========
    with tab1:
        st.subheader("All Grievances")

        # Get all grievances
        grievances = db.get_all_grievances()

        if not grievances:
            st.info("No grievances found.")
        else:
            # Display grievances
            for idx, grev in enumerate(grievances):
                _render_grievance_card(db, grev, idx, "all")

    # ========== TAB 2: STATISTICS ==========
    with tab2:
        st.subheader("Grievance Statistics")

        stats = db.get_statistics()

        if stats['total'] == 0:
            st.info("No data available yet.")
        else:
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Grievances", stats['total'])

            with col2:
                pending = stats['by_status'].get('pending', 0)
                st.metric("Pending", pending)

            with col3:
                in_process = stats['by_status'].get('in_process', 0)
                st.metric("In Process", in_process)

            with col4:
                resolved = stats['by_status'].get('resolved', 0)
                st.metric("Resolved", resolved)

            st.divider()

            # Charts
            col1, col2 = st.columns(2)

            with col1:
                # Status distribution
                if stats['by_status']:
                    fig = px.pie(
                        names=list(stats['by_status'].keys()),
                        values=list(stats['by_status'].values()),
                        title="Grievances by Status",
                        hole=0.3
                    )
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Issue type distribution
                if stats['by_type']:
                    fig = px.bar(
                        x=list(stats['by_type'].keys()),
                        y=list(stats['by_type'].values()),
                        title="Grievances by Issue Type",
                        labels={'x': 'Issue Type', 'y': 'Count'}
                    )
                    st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                # Branch distribution
                if stats['by_branch']:
                    fig = px.bar(
                        x=list(stats['by_branch'].keys()),
                        y=list(stats['by_branch'].values()),
                        title="Grievances by Branch",
                        labels={'x': 'Branch', 'y': 'Count'}
                    )
                    st.plotly_chart(fig, use_container_width=True)

    # ========== TAB 3: SEARCH & FILTER ==========
    with tab3:
        st.subheader("Search & Filter Grievances")

        col1, col2, col3 = st.columns(3)

        filter_type = "all"

        with col1:
            search_by = st.radio("Search By:", ["ERP Code", "Grievance ID", "Employee Name"])

        with col2:
            if search_by == "ERP Code":
                search_value = st.text_input("Enter ERP Code")
                if search_value.strip():
                    grievances = db.get_employee_grievances(search_value.strip())
            elif search_by == "Grievance ID":
                search_value = st.text_input("Enter Grievance ID")
                if search_value.strip():
                    grev = db.get_grievance(search_value.strip())
                    grievances = [grev] if grev else []
            else:  # Employee Name
                search_value = st.text_input("Enter Employee Name")
                if search_value.strip():
                    all_grevs = db.get_all_grievances()
                    grievances = [g for g in all_grevs if search_value.lower() in g['employee_name'].lower()]

        with col3:
            filter_status = st.multiselect(
                "Filter by Status:",
                ["pending", "in_process", "resolved"],
                default=[]
            )

        st.divider()

        # Display filtered results
        if 'grievances' in locals() and grievances:
            if filter_status:
                grievances = [g for g in grievances if g['status'] in filter_status]

            if grievances:
                for grev in grievances:
                    _render_grievance_card(db, grev)
            else:
                st.info("No grievances match the selected filters.")
        else:
            st.info("Enter search criteria to find grievances.")

    # ========== TAB 4: EXPORT DATA ==========
    with tab4:
        st.subheader("Export Grievance Data")

        # Get all grievances as DataFrame
        all_grievances = db.get_all_grievances()

        if all_grievances:
            df = db.export_to_dataframe()

            # Display DataFrame
            st.dataframe(df, use_container_width=True)

            # Export options
            col1, col2, col3 = st.columns(3)

            with col1:
                # CSV export
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"grievances_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            with col2:
                # Excel export
                try:
                    import openpyxl
                    from io import BytesIO

                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Grievances')

                    st.download_button(
                        label="📥 Download as Excel",
                        data=buffer.getvalue(),
                        file_name=f"grievances_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.ms-excel",
                        use_container_width=True
                    )
                except ImportError:
                    st.info("Install openpyxl to export as Excel")

            with col3:
                st.metric("Total Records", len(df))

        else:
            st.info("No grievances to export.")


def _render_grievance_card(db, grev, idx=0, section="main"):
    """Render individual grievance card with update functionality"""
    
    # Status color mapping
    status_colors = {
        "pending": "🔴",
        "in_process": "🟡",
        "resolved": "🟢"
    }

    # Status badge
    status_badge = f"{status_colors.get(grev['status'], '⚪')} {grev['status'].upper()}"

    # Main card
    with st.container(border=True):
        # Header
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            st.markdown(f"### {grev['employee_name']}")
            st.caption(f"ERP: {grev['erp_code']}")

        with col2:
            st.write(f"**ID:** {grev['id']}")
            st.write(f"**Branch:** {grev['branch']}")

        with col3:
            st.write(status_badge)
            created_date = grev['created_at']
            st.caption(f"Created: {created_date[:10]}")

        st.divider()

        # Issue details
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Issue Type:** {grev['issue_type']}")
            st.write(f"**Subject:** {grev['subject']}")

        with col2:
            if grev['shift_start_time'] and grev['shift_end_time']:
                st.write(f"**Shift:** {grev['shift_start_time']} - {grev['shift_end_time']}")
            else:
                st.write("**Shift:** N/A")

        # Description
        st.write("**Description:**")
        st.text(grev['description'][:500] + ("..." if len(grev['description']) > 500 else ""))

        st.divider()

        # Admin update section
        st.markdown("### Update Status")

        col1, col2 = st.columns([1, 2])

        with col1:
            new_status = st.selectbox(
                "New Status:",
                ["pending", "in_process", "resolved"],
                index=["pending", "in_process", "resolved"].index(grev['status']),
                key=f"status_select_{grev['id']}_{idx}_{section}"
            )

        with col2:
            admin_notes = st.text_area(
                "Admin Notes:",
                value=grev.get('admin_notes', ''),
                height=80,
                key=f"notes_area_{grev['id']}_{idx}_{section}"
            )

        # Update button
        if st.button("💾 Update Status", key=f"status_{grev['id']}_{idx}_{section}", use_container_width=True):
            db.update_grievance_status(
                grev['id'],
                new_status,
                st.session_state.get('user_erp', 'ADMIN'),
                admin_notes
            )
            st.success(f"✅ Grievance {grev['id']} updated to {new_status}")
            st.rerun()

        # History
        with st.expander("📜 View History"):
            history = db.get_grievance_history(grev['id'])

            if history:
                hist_df = pd.DataFrame(history)
                st.dataframe(hist_df, use_container_width=True)
            else:
                st.info("No history found.")

