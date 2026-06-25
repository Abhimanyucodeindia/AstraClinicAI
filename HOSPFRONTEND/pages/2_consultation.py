import streamlit as st
import requests
from api import BASE_URL

st.set_page_config(
    page_title="AstraClinicAI — Consultation",
    page_icon="💬",
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
        radial-gradient(circle at 12% 8%, rgba(0, 255, 220, 0.06) 0%, transparent 40%),
        radial-gradient(circle at 92% 90%, rgba(170, 0, 255, 0.08) 0%, transparent 45%),
        linear-gradient(0deg, #000000 0%, #050507 100%);
}

* {
    font-family: 'Rajdhani', sans-serif;
}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 6rem;
    max-width: 820px;
}

h1 {
    font-family: 'Orbitron', sans-serif !important;
    color: #ffffff !important;
    font-size: 1.6rem !important;
    letter-spacing: 0.05em;
    text-shadow: 0 0 10px rgba(0, 255, 220, 0.5), 0 0 20px rgba(170, 0, 255, 0.2);
    margin-bottom: 0 !important;
}

/* Top bar */
.chat-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(10, 12, 16, 0.7);
    border: 1px solid rgba(0, 255, 220, 0.2);
    border-radius: 14px;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 0 16px rgba(0, 255, 220, 0.06);
}

.doctor-tag {
    color: #5be8d4;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 0.03em;
}

.doctor-status {
    color: #6e8086;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* Chat bubbles */
div[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.4rem 0 !important;
}

div[data-testid="stChatMessageAvatarUser"],
div[data-testid="stChatMessageAvatarAssistant"] {
    background: rgba(0, 255, 220, 0.12) !important;
    border: 1px solid rgba(0, 255, 220, 0.4) !important;
    box-shadow: 0 0 10px rgba(0, 255, 220, 0.25);
}

div[data-testid="stChatMessageContent"] {
    color: #d7e2e4 !important;
}

div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    background: rgba(0, 255, 220, 0.04) !important;
    border: 1px solid rgba(0, 255, 220, 0.15) !important;
    border-radius: 14px !important;
    padding: 0.6rem 1rem !important;
}

div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
    background: rgba(170, 0, 255, 0.04) !important;
    border: 1px solid rgba(170, 0, 255, 0.18) !important;
    border-radius: 14px !important;
    padding: 0.6rem 1rem !important;
}

/* Chat input bar (this is what gives the Claude-style pill with embedded icons) */
[data-testid="stChatInput"] {
    background: rgba(10, 12, 16, 0.85) !important;
    border: 1.5px solid rgba(0, 255, 220, 0.35) !important;
    border-radius: 16px !important;
    box-shadow: 0 0 20px rgba(0, 255, 220, 0.15), 0 0 36px rgba(170, 0, 255, 0.08) !important;
}

[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    caret-color: #00ffdc !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #6e8086 !important;
}

[data-testid="stChatInput"] button {
    color: #00ffdc !important;
}

[data-testid="stChatInputFileAttachButton"] svg,
[data-testid="stBaseButton-headerNoPadding"] svg {
    color: #00ffdc !important;
}

.stButton > button {
    border-radius: 8px;
    border: 1px solid rgba(0, 255, 220, 0.5);
    font-weight: 700;
    font-size: 0.82rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    background: linear-gradient(135deg, rgba(0, 255, 220, 0.12), rgba(170, 0, 255, 0.12));
    color: #ffffff;
    box-shadow: 0 0 10px rgba(0, 255, 220, 0.15);
    transition: transform 0.12s ease, box-shadow 0.15s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 0 18px rgba(0, 255, 220, 0.35), 0 0 28px rgba(170, 0, 255, 0.18);
    border-color: #00ffdc;
    color: #ffffff;
}

div[data-testid="stAlert"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(0, 255, 220, 0.2) !important;
    color: #d7e2e4 !important;
}

[data-testid="stDialog"] {
    background: #050507 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# AUTH / CONSULTATION GUARD
# =========================================================
if "consultation_id" not in st.session_state:
    st.switch_page("pages/1_dashboard.py")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# =========================================================
# PRESCRIPTION DIALOG
# =========================================================
@st.dialog("📋 Prescription")
def show_prescription():
    data = st.session_state["prescription"]
    st.markdown(f"**Diagnosis**\n\n{data.get('diagnosis', '—')}")
    st.markdown(f"**Medicines**\n\n{data.get('medicines', '—')}")
    st.markdown(f"**Instructions**\n\n{data.get('instructions', '—')}")
    st.success("Prescription generated successfully")


# =========================================================
# TOP BAR
# =========================================================
st.title("💬 Consultation")

top_col1, top_col2, top_col3 = st.columns([6, 2, 2])

with top_col1:
    st.markdown(
        f"""
        <div class="chat-topbar">
            <div>
                <div class="doctor-tag">🤖 {st.session_state['doctor_name']}</div>
                <div class="doctor-status">● Online — AI Specialist</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_col2:
    if st.button("📋 Prescription", use_container_width=True):
        try:
            response = requests.post(
                f"{BASE_URL}consultations/"
                f"{st.session_state['consultation_id']}"
                f"/generate_prescription/",
                timeout=15,
            )
            response.raise_for_status()
            st.session_state["prescription"] = response.json()
            show_prescription()
        except requests.RequestException:
            st.error("Could not generate prescription.")

with top_col3:
    if st.button("🔴 End Chat", use_container_width=True):
        st.session_state.pop("consultation_id", None)
        st.session_state.pop("doctor_name", None)
        st.session_state.pop("messages", None)
        st.session_state.pop("prescription", None)
        st.switch_page("pages/1_dashboard.py")

if "prescription" in st.session_state:
    if st.button("View last prescription", key="reopen_prescription"):
        show_prescription()

# =========================================================
# CHAT HISTORY
# =========================================================
for msg in st.session_state["messages"]:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        if msg.get("image"):
            st.image(msg["image"], width=220)
        if msg.get("content"):
            st.write(msg["content"])

# =========================================================
# CHAT INPUT (text + attach icon, Claude-style)
# =========================================================
prompt = st.chat_input(
    "Message your AI doctor, or attach a medical image...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)

if prompt:
    user_text = prompt.text.strip() if prompt.text else ""
    attached_files = prompt["files"] if prompt.files else []

    # --- Handle image upload first (if any) ---
    if attached_files:
        for img_file in attached_files:
            try:
                files = {"image": img_file}
                data = {"consultation": st.session_state["consultation_id"]}
                upload_response = requests.post(
                    f"{BASE_URL}medicalimages/", files=files, data=data, timeout=20
                )
                upload_response.raise_for_status()
                image_data = upload_response.json()
                st.session_state["image_id"] = image_data["image_id"]

                st.session_state["messages"].append(
                    {"role": "user", "content": "📷 Uploaded a medical image", "image": img_file}
                )
            except requests.RequestException:
                st.session_state["messages"].append(
                    {"role": "assistant", "content": "⚠️ Failed to upload the image. Please try again."}
                )

    # --- Handle text message ---
    if user_text:
        st.session_state["messages"].append({"role": "user", "content": user_text})

        try:
            response = requests.post(
                f"{BASE_URL}consultations/"
                f"{st.session_state['consultation_id']}"
                f"/send_message/",
                json={"message": user_text},
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
            st.session_state["messages"].append(
                {"role": "assistant", "content": data.get("response", "")}
            )
        except requests.RequestException:
            st.session_state["messages"].append(
                {"role": "assistant", "content": "⚠️ Failed to get a response. Please try again."}
            )

    st.rerun()