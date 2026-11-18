import base64
import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

# Read API_URL from the project's .env file.
load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")

# Keep the interface labels together so the farmer can switch languages.
LANGUAGE_TEXT = {
    "English": {
        "upload_title": "📄 Scheme PDFs", "upload_help": "Upload one or more PDF documents.",
        "choose_files": "Choose PDF files", "index": "Upload and index PDFs",
        "reading": "Reading and indexing PDFs...", "chat_title": "💬 Ask about a scheme",
        "chat_help": "Ask about eligibility, benefits, required documents, or application steps.",
        "question": "Type your question", "searching": "Searching the uploaded PDFs...",
        "sources": "**Retrieved PDF pages:**", "api_error": "I could not reach the local NanjAI API. Please check that it is running.",
        "language": "Language / மொழி", "indexed": "indexed", "chunks": "text chunks",
        "index_failed": "Indexing failed.",
        "brand_caption": "Explore agricultural schemes using your uploaded documents.",
        "kural_english": "Farmers are the world's linchpin, supporting all who cannot till the land.",
    },
    "Tamil": {
        "upload_title": "📄 திட்ட PDF-கள்", "upload_help": "ஒன்று அல்லது அதற்கு மேற்பட்ட PDF ஆவணங்களைப் பதிவேற்றவும்.",
        "choose_files": "PDF கோப்புகளைத் தேர்ந்தெடுக்கவும்", "index": "PDF-களைப் பதிவேற்றி அட்டவணையிடவும்",
        "reading": "PDF-களைப் படித்து அட்டவணையிடுகிறது...", "chat_title": "💬 திட்டத்தைப் பற்றி கேளுங்கள்",
        "chat_help": "தகுதி, நன்மைகள், தேவையான ஆவணங்கள் அல்லது விண்ணப்பிக்கும் முறையைப் பற்றி கேளுங்கள்.",
        "question": "உங்கள் கேள்வியை உள்ளிடவும்", "searching": "பதிவேற்றிய PDF-களில் தேடுகிறது...",
        "sources": "**கண்டறியப்பட்ட PDF பக்கங்கள்:**", "api_error": "உள்ளூர் NanjAI API-ஐ அணுக முடியவில்லை. அது இயங்குகிறதா எனச் சரிபார்க்கவும்.",
        "language": "மொழி / Language", "indexed": "அட்டவணையிடப்பட்டது", "chunks": "உரைப் பகுதிகள்",
        "index_failed": "அட்டவணையிட முடியவில்லை.",
        "brand_caption": "நீங்கள் பதிவேற்றிய ஆவணங்களில் உள்ள வேளாண் திட்டங்களைத் தேடுங்கள்.",
        "kural_english": "உழவர்கள் உலகின் அச்சாணி; உழைக்க இயலாத அனைவரையும் தாங்குபவர்கள்.",
    },
}

st.set_page_config(
    page_title="NanjAI (நஞ்சை)",
    page_icon="🌾",
    layout="wide",
)

# Load the farmer-provided paddy-field photo from the local project assets.
farm_background_path = Path(__file__).resolve().parent.parent / "assets" / "farm_background_madurai.jpg"
farm_art_data = base64.b64encode(farm_background_path.read_bytes()).decode("ascii")

# The state emblem is served from Wikimedia Commons; the app itself remains local.
state_emblem_url = (
    "https://upload.wikimedia.org/wikipedia/commons/7/7c/Seal_of_Tamil_Nadu.svg"
)

# The language choice controls interface labels and the answer language.
selected_language = st.selectbox(
    "Language / மொழி", ["English", "Tamil"], format_func=lambda value: "English" if value == "English" else "தமிழ்"
)
text = LANGUAGE_TEXT[selected_language]

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: #f4f7f1; font-size: 18px; }}
    .hero {{
        background: linear-gradient(110deg, #174c36, #347b50);
        color: white; padding: 20px 28px; border-radius: 16px; margin-bottom: 20px;
    }}
    .hero-grid {{
        display: grid; grid-template-columns: minmax(0, 1fr) 116px minmax(0, 1fr);
        align-items: center; gap: 26px;
    }}
    .brand-title {{ margin: 0; color: white; font-size: 2.25rem; line-height: 1.2; }}
    .brand-tamil {{ color: #f5d98a; font-size: 1.7rem; white-space: nowrap; }}
    .brand-caption {{ color: #e2f0e4; font-size: 1.06rem; margin: 8px 0 0; }}
    .emblem-wrap {{ display: flex; justify-content: center; align-items: center;
                    width: 116px; height: 122px; background: #fff; border-radius: 14px;
                    padding: 9px; box-sizing: border-box; }}
    .emblem-wrap img {{ width: 94px; height: 104px; object-fit: contain; }}
    .kural {{ text-align: right; color: #fff8e8; }}
    .kural-label {{ color: #f5d98a; font-weight: 750; font-size: 1.12rem; margin-bottom: 5px; }}
    .kural-tamil {{ font-family: 'Latha', 'Nirmala UI', 'Noto Sans Tamil', sans-serif;
                    font-size: 1.16rem; line-height: 1.55; font-weight: 650; }}
    .kural-line {{ display: block; }}
    .kural-english {{ color: #e0eedf; font-size: .94rem; line-height: 1.4;
                      margin-top: 7px; font-style: italic; }}
    /* Stretch the divider and artwork to the full height of both work areas. */
    div[data-testid="stHorizontalBlock"] > div:first-child {{
        border-right: 3px solid #39764e; padding-right: 1rem;
        min-height: 100vh;
    }}
    div[data-testid="stHorizontalBlock"] > div:last-child {{
        padding: 1rem 1.15rem; min-height: 100vh; border-radius: 18px;
        background-color: #f4f8f1 !important;
        background-image: linear-gradient(rgba(255,255,255,.78), rgba(255,255,255,.78)),
                          url('data:image/jpeg;base64,{farm_art_data}') !important;
        background-size: cover; background-position: center;
    }}
    div[data-testid="stHorizontalBlock"] > div:last-child div[data-testid="stChatMessage"] {{
        background: rgba(255,255,255,.84); border-radius: 12px; padding: .35rem .55rem;
    }}
    /* Increase contrast and type weight for the main app controls and copy. */
    div[data-testid="stMarkdownContainer"] p:not(.brand-caption) {{
        color: #183a29 !important; font-size: 1.2rem !important;
        font-weight: 650 !important; line-height: 1.6 !important;
    }}
    div[data-testid="stCaptionContainer"] {{
        color: #173b29 !important; font-size: 1.08rem !important;
        font-weight: 650 !important;
    }}
    div[data-testid="stCaptionContainer"] p {{
        color: #173b29 !important; font-size: 1.08rem !important;
        font-weight: 650 !important;
    }}
    div[data-testid="stHeading"] h1,
    div[data-testid="stHeading"] h2,
    div[data-testid="stHeading"] h3 {{
        color: #173b29 !important; font-weight: 800 !important;
    }}
    div[data-testid="stChatMessage"] p {{
        color: #172f21 !important; font-size: 1.22rem !important;
        font-weight: 700 !important; line-height: 1.65 !important;
    }}
    div[data-testid="stFileUploader"] label,
    div[data-testid="stChatInput"] textarea {{
        color: #173b29 !important; font-size: 1.15rem !important;
        font-weight: 650 !important;
    }}
    div[data-testid="stAlert"] p {{
        color: #17452f !important; font-size: 1.08rem !important;
        font-weight: 700 !important;
    }}
    .stButton button {{
        color: #fff !important; font-size: 1.12rem !important;
        font-weight: 800 !important; min-height: 3rem;
    }}
    .hero .brand-caption {{ color: #eaf5eb !important; font-size: 1.12rem !important; }}
    .kural-tamil {{ font-size: 1.25rem; font-weight: 750; }}
    .kural-english {{ color: #f0f5e8; font-size: 1.02rem; font-weight: 650; }}
    @media (max-width: 850px) {{
        .hero-grid {{ grid-template-columns: 1fr; gap: 14px; text-align: center; }}
        .emblem-wrap {{ margin: 0 auto; }}
        .kural {{ text-align: center; }}
        div[data-testid="stHorizontalBlock"] > div:first-child {{
            border-right: 0; border-bottom: 3px solid #39764e; padding: 0 0 1rem; min-height: unset;
        }}
        div[data-testid="stHorizontalBlock"] > div:last-child {{ padding: 1rem; min-height: 70vh; }}
    }}
    </style>
    <div class="hero">
      <div class="hero-grid">
        <div>
          <h1 class="brand-title">🌾 NanjAI <span class="brand-tamil">(நஞ்சை)</span></h1>
          <p class="brand-caption">{text['brand_caption']}</p>
        </div>
        <div class="emblem-wrap">
          <img src="{state_emblem_url}" alt="Tamil Nadu Government state emblem" />
        </div>
        <div class="kural">
          <div class="kural-label">குறள் 1032</div>
          <div class="kural-tamil">
            <span class="kural-line">உழுவார் உலகத்தார்க்கு ஆணிஅஃ தாற்றாது</span>
            <span class="kural-line">எழுவாரை எல்லாம் பொறுத்து</span>
          </div>
          <div class="kural-english">{text['kural_english']}</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Give the chat more room than the upload panel, with a visible divider.
upload_column, chat_column = st.columns([0.72, 1.68], gap=None)

with upload_column:
    st.subheader(text["upload_title"])
    st.write(text["upload_help"])

    pdf_files = st.file_uploader(
        text["choose_files"],
        type=["pdf"],
        accept_multiple_files=True,
    )

    if st.button(
        text["index"],
        type="primary",
        use_container_width=True,
        disabled=not pdf_files,
    ):
        # Send each selected PDF to the FastAPI /upload endpoint.
        files_to_send = [
            ("files", (pdf.name, pdf.getvalue(), "application/pdf"))
            for pdf in pdf_files
        ]

        try:
            with st.spinner(text["reading"]):
                response = requests.post(
                    f"{API_URL}/upload",
                    files=files_to_send,
                    timeout=600,
                )
            response.raise_for_status()

            # Show whether each PDF was indexed or why it failed.
            for result in response.json()["results"]:
                if result["status"] == "indexed":
                    st.success(
                        f"{result['filename']}: {text['indexed']} "
                        f"({result['chunks']} {text['chunks']})"
                    )
                else:
                    st.error(
                        f"{result['filename']}: "
                        f"{result.get('error', text['index_failed'])}"
                    )
        except requests.RequestException as error:
            st.error(f"NanjAI API-ஐ அணுக முடியவில்லை / Could not reach the NanjAI API: {error}")

with chat_column:
    with st.container(key="chat_panel"):
        st.subheader(text["chat_title"])
        st.caption(text["chat_help"])

        # Keep the conversation visible while Streamlit refreshes the page.
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input(text["question"])

        if question:
            st.session_state.messages.append(
                {"role": "user", "content": question}
            )

            try:
                with st.spinner(text["searching"]):
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"question": question, "language": selected_language},
                        timeout=120,
                    )
                response.raise_for_status()
                result = response.json()

                # Display the answer and the retrieved PDF pages.
                answer = result["answer"]
                sources = result.get("sources", [])
                if sources:
                    source_lines = [
                        f"- {source['filename']}, page {source['page']}"
                        for source in sources
                    ]
                    answer += "\n\n" + text["sources"] + "\n" + "\n".join(source_lines)

            except requests.RequestException as error:
                answer = (
                    text["api_error"] + " "
                    f"Please check that it is running. ({error})"
                )

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
            st.rerun()
