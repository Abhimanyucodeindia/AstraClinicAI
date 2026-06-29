import streamlit as st
import requests
from api import BASE_URL
from doctor_utils import resolve_doctor_photo, get_department_name

st.set_page_config(
    page_title="AstraClinicAI — Dashboard",
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
        radial-gradient(circle at 15% 10%, rgba(0, 255, 220, 0.07) 0%, transparent 40%),
        radial-gradient(circle at 90% 85%, rgba(170, 0, 255, 0.09) 0%, transparent 45%),
        linear-gradient(0deg, #000000 0%, #050507 100%);
}

* {
    font-family: 'Rajdhani', sans-serif;
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
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

p, span, div {
    color: #c9d6d8;
}

.welcome-text {
    font-size: 1.05rem;
    color: #8fa3a8;
    letter-spacing: 0.02em;
    margin-top: 0.3rem;
}

/* Doctor card container (Streamlit bordered container) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(10, 12, 16, 0.7);
    border: 1.5px solid rgba(0, 255, 220, 0.2) !important;
    border-radius: 18px;
    padding: 1.4rem 1.2rem 1.2rem 1.2rem;
    overflow: hidden;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    box-shadow: 0 0 12px rgba(0, 255, 220, 0.05);
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-6px);
    border-color: rgba(0, 255, 220, 0.85) !important;
    box-shadow:
        0 0 26px rgba(0, 255, 220, 0.4),
        0 0 46px rgba(170, 0, 255, 0.22),
        inset 0 0 25px rgba(0, 255, 220, 0.05);
}

/* Pulls the photo out past the card's own padding so it fills the
   frame edge-to-edge, while the name/dept/button below keep normal padding. */
.doctor-photo-wrap {
    margin: -1.4rem -1.2rem 1rem -1.2rem;
    width: calc(100% + 2.4rem);
}

.doctor-photo {
    width: 100%;
    height: 260px;
    object-fit: cover;
    display: block;
    border-radius: 18px 18px 0 0;
    border-bottom: 2px solid rgba(0, 255, 220, 0.5);
    box-shadow: 0 4px 24px rgba(0, 255, 220, 0.2);
}

div[data-testid="stVerticalBlockBorderWrapper"] h3 {
    font-size: 1.35rem !important;
    text-align: center;
    margin-top: 0.6rem;
}

.doctor-dept {
    color: #5be8d4;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    text-align: center;
    margin-top: 0.1rem;
    margin-bottom: 1.1rem;
}

.stButton > button {
    width: 100%;
    border-radius: 8px;
    border: 1px solid rgba(0, 255, 220, 0.5);
    padding: 0.65rem 0;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    background: linear-gradient(135deg, rgba(0, 255, 220, 0.12), rgba(170, 0, 255, 0.12));
    color: #ffffff;
    box-shadow: 0 0 12px rgba(0, 255, 220, 0.15);
    transition: transform 0.12s ease, box-shadow 0.15s ease, background 0.15s ease;
    margin-top: 0.5rem;
}

.stButton > button:hover {
    transform: translateY(-1px);
    background: linear-gradient(135deg, rgba(0, 255, 220, 0.25), rgba(170, 0, 255, 0.25));
    box-shadow: 0 0 20px rgba(0, 255, 220, 0.4), 0 0 32px rgba(170, 0, 255, 0.2);
    color: #ffffff;
    border-color: #00ffdc;
}

div[data-testid="stAlert"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(0, 255, 220, 0.2) !important;
    color: #d7e2e4 !important;
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

# =========================================================
# HEADER
# =========================================================
st.title("👨‍⚕️ AI Specialists")

col1, col2 = st.columns([8, 1])

with col1:
    st.markdown(
        f"<div class='welcome-text'>Welcome, {st.session_state['patient_name']}</div>",
        unsafe_allow_html=True,
    )

with col2:
    if st.button("⚙️ Settings"):
        st.switch_page("pages/3_settings.py")

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# FETCH DOCTORS
# =========================================================
try:
    response = requests.get(f"{BASE_URL}doctors/", timeout=10)
    response.raise_for_status()
    doctors = response.json()
except requests.RequestException:
    st.error("Could not load specialists right now. Please try again shortly.")
    doctors = []

# =========================================================
# DOCTOR GRID
# =========================================================
cols = st.columns(3)

for index, doctor in enumerate(doctors):

    with cols[index % 3]:

        with st.container(border=True):

            photo_url = resolve_doctor_photo(doctor)

            st.markdown(
                f"<div class='doctor-photo-wrap'>"
                f"<img class='doctor-photo' src='{photo_url}' />"
                f"</div>",
                unsafe_allow_html=True,
            )

            st.subheader(doctor["doctor_name"])

            st.markdown(
                f"<div class='doctor-dept'>{get_department_name(doctor)}</div>",
                unsafe_allow_html=True,
            )

            if st.button(
                "Start Consultation",
                key=f"doctor_{doctor['doctor_id']}",
                use_container_width=True,
            ):

                consultation_data = {
                    "patient": st.session_state["patient_id"],
                    "doctor": doctor["doctor_id"],
                    "status": "pending",
                }

                try:
                    consultation_response = requests.post(
                        f"{BASE_URL}consultations/",
                        json=consultation_data,
                        timeout=10,
                    )
                    consultation_response.raise_for_status()
                    consultation = consultation_response.json()

                    st.session_state["consultation_id"] = consultation["consultation_id"]
                    st.session_state["doctor_name"] = doctor["doctor_name"]
                    st.session_state["doctor_photo"] = photo_url

                    st.switch_page("pages/2_consultation.py")
                except requests.RequestException:
                    st.error("Could not start consultation. Please try again.")