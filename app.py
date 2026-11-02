Python
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="WM Internship Tracker", page_icon="💼", layout="centered"
)

# Initialize Session State for Data Persistence during the session
if "tracker_data" not in st.session_state:
  st.session_state.tracker_data = pd.DataFrame([
      {
          "Firm Name": "Morgan Stanley",
          "Tier": "Wirehouse",
          "Role": "PWM Summer Analyst",
          "Status": "Networking",
          "Contact": "Jane Doe (VP)",
          "Next Action": "Follow up on coffee chat",
      },
      {
          "Firm Name": "Fisher Investments",
          "Tier": "Independent RIA",
          "Role": "Private Client Group",
          "Status": "Applied",
          "Contact": "John Smith (Recruiter)",
          "Next Action": "Wait for HireVue invite",
      },
  ])

if "networking_data" not in st.session_state:
  st.session_state.networking_data = pd.DataFrame([{
      "Alumni / Advisor": "Jane Doe",
      "Firm": "Morgan Stanley",
      "Date": "2026-03-01",
      "Topic": "Discussed wealth advisory path",
      "Status": "Completed",
  }])

# App Header
st.title("💼 WM Internship Command Center")
st.markdown(
    "Target top wealth management firms, track your networking, and land your"
    " sophomore role."
)

# Navigation Sidebar
tab1, tab2, tab3 = st.tabs(
    ["📊 Internship Tracker", "🤝 Networking Log", "✉️ Email Generator"]
)

# --- TAB 1: INTERNSHIP TRACKER ---
with tab1:
  st.subheader("Target Firms Dashboard")

  # Metrics overview
  df = st.session_state.tracker_data
  col1, col2, col3 = st.columns(3)
  col1.metric("Total Tracked", len(df))
  col2.metric("Networking", len(df[df["Status"] == "Networking"]))
  col3.metric("Applied / Interviewing", len(df[df["Status"].isin(["Applied", "Interviewing"])]))

  st.divider()

  # Interactive Table
  edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
  st.session_state.tracker_data = edited_df

  with st.expander("➕ Add New Target Firm"):
    with st.form("firm_form"):
      f_name = st.text_input("Firm Name")
      f_tier = st.selectbox(
          "Firm Tier",
          [
              "Wirehouse / Bulge Bracket",
              "Regional Boutique",
              "Independent RIA",
              "Private Bank",
          ],
      )
      f_role = st.text_input("Role Title", value="Wealth Management Intern")
      f_status = st.selectbox(
          "Status",
          [
              "Not Applied",
              "Networking",
              "Applied",
              "Interviewing",
              "Offer",
              "Rejected",
          ],
      )
      f_contact = st.text_input("Key Contact / Alumni Name")
      f_action = st.text_input("Next Action Item")

      submit_firm = st.form_submit_button("Save Firm")
      if submit_firm and f_name:
        new_row = pd.DataFrame([{
            "Firm Name": f_name,
            "Tier": f_tier,
            "Role": f_role,
            "Status": f_status,
            "Contact": f_contact,
            "Next Action": f_action,
        }])
        st.session_state.tracker_data = pd.concat(
            [st.session_state.tracker_data, new_row], ignore_index=True
        )
        st.success(f"Added {f_name} to tracker!")
        st.rerun()

# --- TAB 2: NETWORKING LOG ---
with tab2:
  st.subheader("Coffee Chat & Alumni Tracker")
  net_df = st.session_state.networking_data
  edited_net = st.data_editor(
      net_df, num_rows="dynamic", use_container_width=True
  )
  st.session_state.networking_data = edited_net

  with st.expander("➕ Log New Connection"):
    with st.form("net_form"):
      n_name = st.text_input("Advisor / Alum Name & Title")
      n_firm = st.text_input("Firm")
      n_date = st.date_input("Chat Date")
      n_topic = st.text_input("Key Takeaway / Notes")
      n_status = st.selectbox(
          "Follow-up Status",
          ["Scheduled", "Completed - Needs Thank You", "Done"],
      )

      submit_net = st.form_submit_button("Log Connection")
      if submit_net and n_name:
        new_net_row = pd.DataFrame([{
            "Alumni / Advisor": n_name,
            "Firm": n_firm,
            "Date": str(n_date),
            "Topic": n_topic,
            "Status": n_status,
        }])
        st.session_state.networking_data = pd.concat(
            [st.session_state.networking_data, new_net_row], ignore_index=True
        )
        st.success(f"Logged chat with {n_name}!")
        st.rerun()

# --- TAB 3: COLD EMAIL GENERATOR ---
with tab3:
  st.subheader("Quick Cold Outreach Generator")
  st.markdown(
      "Select your outreach angle, fill in the details, and copy the template"
      " to use on LinkedIn or via email."
  )

  template_type = st.selectbox(
      "Outreach Goal",
      [
          "Alumni Informational Interview",
          "Independent RIA Cold Outreach",
          "Post-Interview Thank You Note",
      ],
  )

  target_name = st.text_input("Contact's First Name", value="Alex")
  target_firm = st.text_input("Firm Name", value="Morgan Stanley Private Wealth")
  my_university = st.text_input("Your University", value="State University")

  if template_type == "Alumni Informational Interview":
    message = f"""Hi {target_name},\n\nI hope you're having a great week. I’m a sophomore finance major at {my_university} exploring career paths in wealth management.\n\nI’ve been following {target_firm}’s approach to holistic planning and noticed your background as an alum. I’d love to ask you 2-3 quick questions about your transition from campus to advisory work.\n\nDo you have 10 minutes for a brief call next week? No worries if your schedule is packed.\n\nBest,\n[Your Name]"""

  elif template_type == "Independent RIA Cold Outreach":
    message = f"""Hi {target_name},\n\nI’m a sophomore at {my_university} building a career in private wealth management. I admire how independent firms like {target_firm} focus deeply on personalized client stewardship.\n\nI am actively seeking sophomore internship opportunities where I can support client service models and portfolio operations. Would you be open to a brief 10-minute introduction call to discuss your team's work?\n\nBest regards,\n[Your Name]"""

  else:
    message = f"""Hi {target_name},\n\nThank you so much for taking the time to speak with me today. I really enjoyed hearing your perspective on how {target_firm} manages client relationships during market shifts.\n\nI'm more excited than ever about the opportunity to contribute to your team. Please let me know if there's any additional information I can provide.\n\nBest,\n[Your Name]"""

  st.text_area("Generated Message (Ready to Copy)", value=message, height=220)
