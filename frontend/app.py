import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Awadhi Chatbot",
    page_icon="💬",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f4f6fb;
}

.chat-container {
    max-width: 700px;
    margin: auto;
}

.user-bubble {
    background: #4f46e5;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0;
    text-align: right;
    font-size: 16px;
}

.bot-bubble {
    background: white;
    color: #111827;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    font-size: 16px;
}

.header {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    color: #111827;
}

.subheader {
    text-align: center;
    color: #6b7280;
    margin-bottom: 20px;
}

button {
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='header'>💬 Awadhi Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Text • Voice • English → Awadhi Support</div>", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "text_query" not in st.session_state:
    st.session_state.text_query = ""

# ---------------- TEXT TO SPEECH ----------------
engine = pyttsx3.init()
engine.setProperty("rate", 155)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------------- BACKEND CALL ----------------
def ask_backend(question):
    try:
        res = requests.get(
            "http://127.0.0.1:8000/chat",
            params={"query": question},
            timeout=60
        )
        if res.status_code == 200:
            return res.json().get("answer", "कोई उत्तर नहीं मिला")
        else:
            return "Backend error"
    except Exception as e:
        return f"Server error: {e}"

# ---------------- TEXT SEND ----------------
def send_text():
    q = st.session_state.text_query.strip()
    if q == "":
        return

    answer = ask_backend(q)

    st.session_state.chat_history.append({
        "q": q,
        "a": answer
    })

    speak(answer)
    st.session_state.text_query = ""

# ---------------- VOICE INPUT ----------------
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ बोलिए (Hindi / simple शब्द)")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="hi-IN")
        answer = ask_backend(text)

        st.session_state.chat_history.append({
            "q": text,
            "a": answer
        })

        speak(answer)

    except sr.UnknownValueError:
        st.error("❌ आवाज़ समझ नहीं आई")
    except sr.RequestError:
        st.error("❌ Voice service उपलब्ध नहीं है")

# ---------------- INPUT AREA ----------------
st.text_input(
    "अपना प्रश्न लिखिए (Enter दबाएँ)",
    key="text_query",
    on_change=send_text
)

# ---------------- BUTTONS ----------------
col1, col2 = st.columns(2)

with col1:
    st.button("🎙️ बोलकर पूछें", on_click=voice_input)

with col2:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []

# ---------------- CHAT AREA ----------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for chat in st.session_state.chat_history:
    st.markdown(
        f"<div class='user-bubble'>🧑 {chat['q']}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div class='bot-bubble'>🤖 {chat['a']}</div>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)
