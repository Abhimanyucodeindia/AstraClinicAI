import streamlit as st
import requests
from api import BASE_URL

st.set_page_config(
    page_title="AstraClinicAI — Settings",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# STYLES
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Rajdhani:wght@500;600;700&display=swap');

[data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none;
}

#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background: #000000;
    background-image:
        radial-gradient(circle at 12% 8%, rgba(0, 255, 220, 0.07) 0%, transparent 40%),
        radial-gradient(circle at 92% 90%, rgba(170, 0, 255, 0.09) 0%, transparent 45%),
        linear-gradient(0deg, #000000 0%, #050507 100%);
}

* {
    font-family: 'Rajdhani', sans-serif;
}

.block-container {
    padding-top: 2rem;
    max-width: 720px;
}

h1 {
    font-family: 'Orbitron', sans-serif !important;
    color: #ffffff !important;
    font-size: 1.9rem !important;
    letter-spacing: 0.06em;
    text-shadow: 0 0 10px rgba(0, 255, 220, 0.5), 0 0 22px rgba(170, 0, 255, 0.2);
}

h3 {
    color: #ffffff !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.03em;
}

.section-card {
    background: rgba(10, 12, 16, 0.7);
    border: 1.5px solid rgba(0, 255, 220, 0.2);
    border-radius: 16px;
    padding: 1.4rem 1.4rem 1rem 1.4rem;
    margin-bottom: 1.3rem;
    box-shadow: 0 0 16px rgba(0, 255, 220, 0.06);
}

.profile-row {
    display: flex;
    justify-content: space-between;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.profile-row:last-child {
    border-bottom: none;
}

.profile-label {
    color: #5be8d4;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.profile-value {
    color: #e6eef0;
    font-size: 0.95rem;
    text-align: right;
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea {
    border-radius: 8px !important;
    border: 1.5px solid rgba(0, 255, 220, 0.3) !important;
    padding: 0.5rem 0.75rem !important;
    background: #f5f7f8 !important;
    color: #000000 !important;
    caret-color: #000000 !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #00ffdc !important;
    box-shadow: 0 0 0 3px rgba(0, 255, 220, 0.2) !important;
}

div[data-testid="stSelectbox"] > div > div {
    border-radius: 8px !important;
    border: 1.5px solid rgba(0, 255, 220, 0.3) !important;
    background: #f5f7f8 !important;
    color: #000000 !important;
}

div[data-testid="stSelectbox"] span {
    color: #000000 !important;
}

.stButton > button {
    width: 100%;
    border-radius: 8px;
    border: 1px solid rgba(0, 255, 220, 0.5);
    padding: 0.55rem 0;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    background: linear-gradient(135deg, rgba(0, 255, 220, 0.12), rgba(170, 0, 255, 0.12));
    color: #ffffff;
    box-shadow: 0 0 12px rgba(0, 255, 220, 0.15);
    transition: transform 0.12s ease, box-shadow 0.15s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 0 20px rgba(0, 255, 220, 0.35), 0 0 32px rgba(170, 0, 255, 0.2);
    border-color: #00ffdc;
    color: #ffffff;
}

div[data-testid="stAlert"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(0, 255, 220, 0.2) !important;
    color: #d7e2e4 !important;
}

div[data-testid="stExpander"] {
    background: rgba(10, 12, 16, 0.7) !important;
    border: 1.5px solid rgba(0, 255, 220, 0.2) !important;
    border-radius: 14px !important;
}

div[data-testid="stExpander"] summary {
    color: #ffffff !important;
    font-weight: 700 !important;
}

.danger-btn button {
    border-color: rgba(255, 77, 109, 0.6) !important;
    background: linear-gradient(135deg, rgba(255, 77, 109, 0.12), rgba(170, 0, 255, 0.08)) !important;
}

.danger-btn button:hover {
    border-color: #ff4d6d !important;
    box-shadow: 0 0 20px rgba(255, 77, 109, 0.35) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# AUTH GUARD
# =========================================================
if "patient_id" not in st.session_state:
    st.switch_page("app.py")

st.title("⚙️ Settings")

# =========================================================
# FETCH PROFILE
# =========================================================
try:
    response = requests.get(
        f"{BASE_URL}patients/{st.session_state['patient_id']}/", timeout=10
    )
    response.raise_for_status()
    patient = response.json()
except requests.RequestException:
    st.error("Could not load your profile right now. Please try again shortly.")
    patient = None

# =========================================================
# PROFILE (inside an expander, editable)
# =========================================================
if patient:
    with st.expander("👤  View / Edit Profile", expanded=False):

        if "edit_mode" not in st.session_state:
            st.session_state["edit_mode"] = False

        if not st.session_state["edit_mode"]:

            st.markdown(
                f"""
                <div class="profile-row"><span class="profile-label">Name</span><span class="profile-value">{patient['patient_name']}</span></div>
                <div class="profile-row"><span class="profile-label">Age</span><span class="profile-value">{patient['age']}</span></div>
                <div class="profile-row"><span class="profile-label">Email</span><span class="profile-value">{patient['email']}</span></div>
                <div class="profile-row"><span class="profile-label">Phone</span><span class="profile-value">{patient['phone_number']}</span></div>
                <div class="profile-row"><span class="profile-label">Gender</span><span class="profile-value">{patient['gender'].title()}</span></div>
                <div class="profile-row"><span class="profile-label">Address</span><span class="profile-value">{patient['address']}</span></div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("✏️ Edit Profile", key="enter_edit"):
                st.session_state["edit_mode"] = True
                st.rerun()

        else:
            # ---- Editable form ----
            edit_name = st.text_input("Full Name", value=patient["patient_name"])
            edit_age = st.number_input(
                "Age", min_value=1, max_value=120, value=int(patient["age"])
            )
            edit_email = st.text_input("Email", value=patient["email"])
            edit_phone = st.text_input("Phone Number", value=patient["phone_number"])
            edit_gender = st.selectbox(
                "Gender",
                ["male", "female", "other"],
                index=["male", "female", "other"].index(patient["gender"].lower())
                if patient["gender"].lower() in ["male", "female", "other"]
                else 0,
            )
            edit_address = st.text_area("Address", value=patient["address"])

            save_col, cancel_col = st.columns(2)

            with save_col:
                if st.button("💾 Save Changes", key="save_profile"):
                    updated_data = {
                        "patient_name": edit_name,
                        "age": edit_age,
                        "email": edit_email,
                        "phone_number": edit_phone,
                        "gender": edit_gender,
                        "address": edit_address,
                    }
                    try:
                        update_response = requests.patch(
                            f"{BASE_URL}patients/{st.session_state['patient_id']}/",
                            json=updated_data,
                            timeout=10,
                        )
                        update_response.raise_for_status()
                        st.session_state["patient_name"] = edit_name
                        st.session_state["edit_mode"] = False
                        st.success("Profile updated successfully")
                        st.rerun()
                    except requests.RequestException:
                        st.error("Failed to update profile. Please try again.")

            with cancel_col:
                if st.button("✖️ Cancel", key="cancel_edit"):
                    st.session_state["edit_mode"] = False
                    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# NAVIGATION (aligned)
# =========================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🧭 Navigation")

nav_col1, nav_col2 = st.columns(2, gap="medium")

with nav_col1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/1_dashboard.py")

with nav_col2:
    has_consultation = "consultation_id" in st.session_state
    if st.button(
        "💬 Consultation" if has_consultation else "💬 No Active Consultation",
        use_container_width=True,
        disabled=not has_consultation,
    ):
        st.switch_page("pages/2_consultation.py")

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ACCOUNT ACTIONS
# =========================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🔐 Account")

acc_col1, acc_col2 = st.columns(2, gap="medium")

with acc_col1:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

with acc_col2:
    st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
    delete_clicked = st.button("🗑️ Delete Account", use_container_width=True, key="delete_account_btn")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Confirm before actually deleting
if delete_clicked:
    st.session_state["confirm_delete"] = True

if st.session_state.get("confirm_delete"):
    st.warning("This will permanently delete your account. This cannot be undone.")
    confirm_col1, confirm_col2 = st.columns(2, gap="medium")

    with confirm_col1:
        if st.button("✅ Yes, delete my account", use_container_width=True, key="confirm_delete_yes"):
            try:
                delete_response = requests.delete(
                    f"{BASE_URL}patients/{st.session_state['patient_id']}/", timeout=10
                )
                if delete_response.status_code in [200, 204]:
                    st.session_state.clear()
                    st.success("Account deleted.")
                    st.switch_page("app.py")
                else:
                    st.error("Failed to delete account.")
            except requests.RequestException:
                st.error("Could not reach the server. Please try again.")

    with confirm_col2:
        if st.button("Cancel", use_container_width=True, key="confirm_delete_no"):
            st.session_state["confirm_delete"] = False
            st.rerun()