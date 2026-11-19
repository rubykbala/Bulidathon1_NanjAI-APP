# NanjAI (நஞ்சை)

NanjAI is a bilingual (English and Tamil) retrieval-augmented generation (RAG) application that helps farmers ask questions about agricultural schemes described in uploaded PDF documents. Answers are grounded in retrieved PDF text and include the source PDF name and page number.

## Features

- Upload one or more PDF documents from the Streamlit interface.
- Extract PDF text page by page, split it into overlapping chunks, and create embeddings.
- Store the vectors, text, and source metadata in a persistent local FAISS index.
- Ask scheme questions in the chat interface and select English or Tamil for the answer.
- Show source PDF filenames and page numbers with answers.
- Validate uploaded file type, PDF signature, and file size (25 MB maximum per PDF).
- Keep uploaded PDFs and the FAISS index in the local `data/` folder.

## Technology

- **Frontend:** Streamlit
- **API:** FastAPI
- **Document loading:** LangChain `PyPDFLoader`
- **Text splitting:** LangChain `RecursiveCharacterTextSplitter` (900-character chunks, 150-character overlap)
- **Vector database:** FAISS (`faiss-cpu`)
- **Embeddings and answer generation:** OpenAI API through LangChain

> **Data and privacy note:** The app stores uploaded PDFs and the FAISS index under `data/`. This repository currently includes PDFs in `Uploaded_PDF/`, copies of uploaded PDFs under `data/uploads/`, and a saved FAISS index under `data/faiss_index/`. New uploads on a user's computer are not automatically sent to GitHub. OpenAI is used to create embeddings and generate answers, so document text sent for embedding, retrieved excerpts, and questions are sent to the OpenAI API. This version is not fully offline or fully on-premises. Keep the API key private and do not commit `.env`.

## Requirements

- Windows with Python installed
- An OpenAI API key with access to the configured embedding and chat models
- The project PDF files you want to index

## Setup in Windows CMD

Make sure Git and Python are installed. Open CMD and run these commands to clone this public repository into a folder named `NanjAI` under your Windows user folder:

```cmd
cd /d "%USERPROFILE%"
git clone https://github.com/rubykbala/Bulidathon1_NanjAI-APP.git NanjAI
cd NanjAI
```

Create and activate a virtual environment dedicated to this project:

```cmd
py -m venv .venv
.venv\Scripts\activate
```

Install the packages listed for NanjAI:

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file in the `NanjAI` project folder. Add your own OpenAI API key without quotation marks. Do not share or commit this file:

```text
OPENAI_API_KEY=your_openai_api_key
```

The application defaults to `text-embedding-3-small` for embeddings and `gpt-4o-mini` for chat. Optional overrides are `OPENAI_EMBEDDING_MODEL`, `OPENAI_CHAT_MODEL`, and `API_URL` (default: `http://127.0.0.1:8000`).

## Run NanjAI

Keep both CMD windows open while using the app. In **CMD window 1**, go to the cloned project folder, activate its virtual environment, and start the FastAPI backend:

```cmd
cd /d "%USERPROFILE%\NanjAI"
.venv\Scripts\activate
uvicorn app.main:app --reload
```

In **CMD window 2**, go to the same project folder, activate its virtual environment, and start the Streamlit interface:

```cmd
cd /d "%USERPROFILE%\NanjAI"
.venv\Scripts\activate
streamlit run app/ui.py
```

Open the Streamlit URL shown in CMD (usually `http://localhost:8501`). FastAPI's interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Use the app

1. Choose **English** or **தமிழ்** from the language selector.
2. In **Scheme PDFs**, select one or more PDFs and choose **Upload and index PDFs**.
3. Wait for the per-file indexing status and chunk count.
4. In **Ask about a scheme**, ask about details present in the uploaded PDFs.
5. Review the answer and its cited PDF pages. Choose a language before asking to receive the new answer in that language.

The FAISS index is saved under `data/faiss_index/`; uploaded PDFs are saved under `data/uploads/`. The repository currently includes a saved index and uploaded PDFs in these locations. New uploads persist on the computer running the app; they are not automatically committed to GitHub. If the local `data/` folder is removed, upload and index the PDFs again.

## RAG flow

```text
PDF upload
  -> PDF text extraction with page metadata
  -> text splitting with overlap
  -> OpenAI embeddings
  -> persistent local FAISS index

Farmer question + selected language
  -> question embedding and FAISS similarity search (up to 5 chunks)
  -> grounded answer from retrieved excerpts
  -> answer with source PDF names and page numbers
```

## Grounding and guardrails

- The answer prompt instructs the model to use only retrieved PDF excerpts and not to follow instructions that may appear inside those excerpts.
- The model is instructed not to invent scheme details and to say when the PDFs do not support an answer.
- Source filenames and page numbers are retained as metadata and displayed with the answer.
- Chat requests require a question between 3 and 1,000 characters and accept only English or Tamil as the selected output language.
- Uploads are restricted to PDF files, checked for the PDF signature, and limited to 25 MB each.

These are application-level safeguards; they do not guarantee that every generated answer is correct. Confirm important scheme details against the cited source PDF and the relevant official department.

## Project layout

```text
NanjAI/
├── app/
│   ├── main.py       # FastAPI upload and chat endpoints
│   ├── rag.py        # PDF ingestion, chunking, FAISS, retrieval, and answers
│   └── ui.py         # Streamlit interface
├── assets/           # Local UI image assets and photo credit
├── Uploaded_PDF/    # Source scheme PDFs included in the repository
├── data/
│   ├── uploads/      # Uploaded PDF copies (currently included in this repository)
│   └── faiss_index/  # Persisted FAISS files (currently included in this repository)
├── requirements.txt
├── .env              # Create locally with your API key; do not commit
└── README.md
```

## Current limitations

- Scanned/image-only PDFs may not provide extractable text; OCR is not currently included.
- Tamil answers depend on the text available in the PDFs and the language model; check the cited pages for critical information.
- The app uses the OpenAI API for embeddings and answer generation, so internet access is required for those steps.
- Playwright-based website browsing or scheme scraping is not implemented in this version; the knowledge base comes from PDFs uploaded by the user.
