import streamlit as st
import requests

# -----------------------------
# API
# -----------------------------
BASE_URL = "http://127.0.0.1:8000"
CHAT_URL = f"{BASE_URL}/chat"

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI STUDY PARTNER",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
    background:#0f172a;
    color:white;
}

section[data-testid="stSidebar"]{
    background:#111827;
}

.stTextInput input{
    background:#1e293b !important;
    color:white !important;
}

.stButton>button{
    width:100%;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:10px;
    height:42px;
}

.stButton>button:hover{
    background:#1d4ed8;
}

.block-container{
    padding-top:1rem;
}

.title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#38bdf8;
}

.subtitle{
    text-align:center;
    color:#94a3b8;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "username" not in st.session_state:
    st.session_state.username = "gokul"

# -----------------------------
# Header
# -----------------------------
st.markdown(
    "<div class='title'>🎓 AI STUDY PARTNER</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Learn • Practice </div>",
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("🎓 Placement Mentor")

    username = st.text_input(
        "Username",
        value=st.session_state.username
    )

    st.session_state.username = username

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):
        st.session_state.session_id = None
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("💬 Recent Chats")

    chats = []

    try:

        response = requests.get(
            f"{BASE_URL}/sessions/{username}"
        )

        if response.status_code == 200:
            chats = response.json()

    except Exception:
        st.warning("Backend Offline")

    if len(chats) == 0:
        st.caption("No recent chats")

    for chat in chats:

        if st.button(
            f"💬 {chat['title']}",
            key=chat["session_id"],
            use_container_width=True
        ):

            history = requests.get(
                f"{BASE_URL}/messages/{chat['session_id']}"
            )

            if history.status_code == 200:

                st.session_state.session_id = chat["session_id"]

                st.session_state.messages = []

                for msg in history.json():

                    st.session_state.messages.append(
                        (
                            msg["role"],
                            msg["message"]
                        )
                    )

            st.rerun()
# ==========================
# MAIN CHAT AREA
# ==========================

st.markdown("<div class='main-title'>🎓 Placement Mentor</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>Learn • Practice • Crack Interviews</div>",
    unsafe_allow_html=True,
)

st.divider()

# Show chat history
for role, message in st.session_state.messages:

    if role == "user":
        with st.chat_message("user"):
            st.markdown(message)

    else:
        with st.chat_message("assistant"):
            st.markdown(message)

# ==========================
# CHAT INPUT
# ==========================

query = st.chat_input("Ask your placement question...")

if query:

    # Show user message immediately
    st.session_state.messages.append(("user", query))

    with st.chat_message("user"):
        st.markdown(query)

    payload = {
        "username": username,
        "session_id": st.session_state.session_id,
        "query": query,
    }

    try:

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                response = requests.post(
                    CHAT_URL,
                    json=payload,
                    timeout=120,
                )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.session_id = data["session_id"]

                    answer = data["response"]

                    st.markdown(answer)

                    st.session_state.messages.append(
                        ("assistant", answer)
                    )

                    st.rerun()

                else:
                    st.error(response.text)

    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to FastAPI server.")

    except Exception as e:
        st.error(str(e))
