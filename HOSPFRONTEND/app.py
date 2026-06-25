import re
import time

import requests
import streamlit as st

from api import BASE_URL

st.set_page_config(
    page_title="AstraClinicAI",
    page_icon="🏥",
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
        radial-gradient(circle at 15% 20%, rgba(0, 255, 220, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(170, 0, 255, 0.10) 0%, transparent 45%),
        linear-gradient(0deg, #000000 0%, #050507 100%);
}

* {
    font-family: 'Rajdhani', sans-serif;
}

.block-container {
    padding-top: 2.5rem;
    max-width: 480px;
}

.brand-wrap {
    text-align: center;
    margin-bottom: 1.8rem;
}

.brand-icon {
    font-size: 2.8rem;
    line-height: 1;
    filter: drop-shadow(0 0 12px rgba(0, 255, 220, 0.6));
}

.brand-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0.4rem 0 0.2rem 0;
    letter-spacing: 0.08em;
    text-shadow: 0 0 10px rgba(0, 255, 220, 0.5), 0 0 22px rgba(170, 0, 255, 0.25);
}

.brand-sub {
    color: #8fa3a8;
    font-size: 0.95rem;
    margin-bottom: 0;
    letter-spacing: 0.02em;
}

.auth-card {
    background: rgba(10, 12, 16, 0.75);
    border: 1px solid rgba(0, 255, 220, 0.25);
    border-radius: 16px;
    padding: 1.8rem 1.8rem 1.4rem 1.8rem;
    box-shadow:
        0 0 0 1px rgba(0, 255, 220, 0.05),
        0 0 30px rgba(0, 255, 220, 0.08),
        0 0 60px rgba(170, 0, 255, 0.06),
        inset 0 0 40px rgba(0, 255, 220, 0.02);
    backdrop-filter: blur(10px);
}

.field-label {
    font-size: 0.78rem;
    font-weight: 700;
    color: #5be8d4;
    margin-bottom: 0.2rem;
    margin-top: 0.7rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea {
    border-radius: 8px !important;
    border: 1.5px solid rgba(0, 255, 220, 0.3) !important;
    padding: 0.55rem 0.8rem !important;
    background: #f5f7f8 !important;
    color: #000000 !important;
    caret-color: #000000 !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: #555c5e !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #00ffdc !important;
    box-shadow: 0 0 0 3px rgba(0, 255, 220, 0.2), 0 0 16px rgba(0, 255, 220, 0.3) !important;
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
    border: 1px solid rgba(0, 255, 220, 0.6);
    padding: 0.6rem 0;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    background: linear-gradient(135deg, rgba(0, 255, 220, 0.15), rgba(170, 0, 255, 0.15));
    color: #ffffff;
    box-shadow: 0 0 18px rgba(0, 255, 220, 0.25), 0 0 30px rgba(170, 0, 255, 0.15);
    transition: transform 0.12s ease, box-shadow 0.15s ease, background 0.15s ease;
    margin-top: 0.9rem;
}

.stButton > button:hover {
    transform: translateY(-1px);
    background: linear-gradient(135deg, rgba(0, 255, 220, 0.28), rgba(170, 0, 255, 0.28));
    box-shadow: 0 0 24px rgba(0, 255, 220, 0.4), 0 0 40px rgba(170, 0, 255, 0.25);
    color: #ffffff;
    border-color: #00ffdc;
}

.stButton > button:active {
    transform: translateY(0px);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(0, 255, 220, 0.15);
    padding: 4px;
    border-radius: 10px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    padding: 0.45rem 0.9rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: #6e8086;
}

.stTabs [aria-selected="true"] {
    background: rgba(0, 255, 220, 0.1) !important;
    color: #00ffdc !important;
    box-shadow: 0 0 12px rgba(0, 255, 220, 0.2);
}

.helper-text {
    font-size: 0.78rem;
    color: #6e8086;
    margin-top: -0.3rem;
}

.strength-weak {color: #ff4d6d; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.04em;}
.strength-medium {color: #ffd166; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.04em;}
.strength-strong {color: #00ffaa; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.04em;}

div[data-testid="stAlert"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(0, 255, 220, 0.2) !important;
    color: #d7e2e4 !important;
}

div[data-baseweb="toggle"] {
    filter: hue-rotate(140deg);
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# HELPERS
# =========================================================
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(value: str) -> bool:
    return bool(EMAIL_RE.match(value.strip()))


def password_strength(pw: str) -> str:
    if len(pw) < 6:
        return "weak"
    score = sum(
        [
            len(pw) >= 8,
            bool(re.search(r"[A-Z]", pw)),
            bool(re.search(r"[0-9]", pw)),
            bool(re.search(r"[^A-Za-z0-9]", pw)),
        ]
    )
    if score >= 3:
        return "strong"
    if score >= 2:
        return "medium"
    return "weak"


def set_session_and_redirect(patient: dict):
    st.session_state["patient_id"] = patient["patient_id"]
    st.session_state["patient_name"] = patient["patient_name"]
    st.switch_page("pages/1_dashboard.py")


# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
<div class="brand-wrap">
    <div class="brand-icon">🏥</div>
    <div class="brand-title">AstraClinicAI</div>
    <p class="brand-sub">AI-powered virtual healthcare — consult, analyze, prescribe.</p>
</div>
""",
    unsafe_allow_html=True,
)

login_tab, register_tab = st.tabs(["🔐 Login", "📝 Register"])

# =========================================================
# LOGIN
# =========================================================
with login_tab:
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    st.markdown('<div class="field-label">Email</div>', unsafe_allow_html=True)
    login_email = st.text_input(
        "Email", key="login_email", placeholder="you@example.com", label_visibility="collapsed"
    )

    st.markdown('<div class="field-label">Password</div>', unsafe_allow_html=True)
    pw_col, toggle_col = st.columns([5, 1])
    show_login_pw = toggle_col.toggle("👁", key="show_login_pw", label_visibility="collapsed")
    login_password = pw_col.text_input(
        "Password",
        type="default" if show_login_pw else "password",
        key="login_password",
        placeholder="Your password",
        label_visibility="collapsed",
    )

    login_clicked = st.button("Login", key="login_btn", use_container_width=True)

    if login_clicked:
        if not login_email or not login_password:
            st.warning("Please enter both email and password.")
        elif not is_valid_email(login_email):
            st.warning("Please enter a valid email address.")
        else:
            with st.spinner("Signing you in..."):
                try:
                    response = requests.get(f"{BASE_URL}patients/", timeout=10)
                    response.raise_for_status()
                    patients = response.json()
                except requests.RequestException:
                    st.error("Could not reach the server. Please try again shortly.")
                    patients = None

            if patients is not None:
                found = next(
                    (
                        p
                        for p in patients
                        if p.get("email") == login_email
                        and p.get("password") == login_password
                    ),
                    None,
                )

                if found:
                    st.success("Welcome back! Redirecting...")
                    time.sleep(0.6)
                    set_session_and_redirect(found)
                else:
                    st.error("Invalid email or password.")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# REGISTER
# =========================================================
with register_tab:
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    st.markdown('<div class="field-label">Full Name</div>', unsafe_allow_html=True)
    name = st.text_input("Full Name", placeholder="Jane Doe", label_visibility="collapsed")

    col_age, col_gender = st.columns(2)
    with col_age:
        st.markdown('<div class="field-label">Age</div>', unsafe_allow_html=True)
        age = st.number_input("Age", min_value=1, max_value=120, label_visibility="collapsed")
    with col_gender:
        st.markdown('<div class="field-label">Gender</div>', unsafe_allow_html=True)
        gender = st.selectbox(
            "Gender", ["male", "female", "other"], label_visibility="collapsed"
        )

    st.markdown('<div class="field-label">Phone Number</div>', unsafe_allow_html=True)
    phone = st.text_input("Phone Number", placeholder="+1 555 123 4567", label_visibility="collapsed")

    st.markdown('<div class="field-label">Email</div>', unsafe_allow_html=True)
    email = st.text_input("Email", placeholder="you@example.com", label_visibility="collapsed")

    st.markdown('<div class="field-label">Password</div>', unsafe_allow_html=True)
    reg_pw_col, reg_toggle_col = st.columns([5, 1])
    show_reg_pw = reg_toggle_col.toggle("👁", key="show_reg_pw", label_visibility="collapsed")
    password = reg_pw_col.text_input(
        "Password",
        type="default" if show_reg_pw else "password",
        placeholder="At least 8 characters",
        label_visibility="collapsed",
    )

    if password:
        strength = password_strength(password)
        st.markdown(
            f'<div class="strength-{strength}">Password strength: {strength.title()}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="field-label">Address</div>', unsafe_allow_html=True)
    address = st.text_area("Address", placeholder="Street, City, State", label_visibility="collapsed")

    register_clicked = st.button("Create Account", key="register_btn", use_container_width=True)

    if register_clicked:
        errors = []
        if not name.strip():
            errors.append("Full name is required.")
        if not is_valid_email(email):
            errors.append("Please enter a valid email address.")
        if not phone.strip():
            errors.append("Phone number is required.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if not address.strip():
            errors.append("Address is required.")

        if errors:
            for err in errors:
                st.warning(err)
        else:
            data = {
                "patient_name": name,
                "age": age,
                "gender": gender,
                "phone_number": phone,
                "email": email,
                "password": password,
                "address": address,
            }

            with st.spinner("Creating your account..."):
                try:
                    response = requests.post(f"{BASE_URL}patients/", json=data, timeout=10)
                except requests.RequestException:
                    st.error("Could not reach the server. Please try again shortly.")
                    response = None

            if response is not None:
                if response.status_code in [200, 201]:
                    patient = response.json()
                    st.success("Account created! Redirecting...")
                    time.sleep(0.6)
                    set_session_and_redirect(patient)
                else:
                    st.error("Registration failed. Please check your details and try again.")

    st.markdown("</div>", unsafe_allow_html=True)