from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.rag import UPLOAD_DIR, add_pdf_to_faiss, answer_question

from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(title="NanjAI API")
class QuestionRequest(BaseModel):
    """Validate the length of a question sent to the chat endpoint."""
    question: str = Field(min_length=3, max_length=1000)
    language: Literal["English", "Tamil"] = "English"

@app.get("/health")
def health():
    """Let us check that the local API is running."""
    return {"status": "ok"}


@app.post("/upload")
def upload_pdfs(files: list[UploadFile] = File(...)):
    """Save uploaded PDFs locally and add their text to the FAISS index."""

    results = []

    for uploaded_file in files:
        filename = Path(uploaded_file.filename or "document.pdf").name

        # Accept PDFs only.
        if not filename.lower().endswith(".pdf"):
            results.append({"filename": filename, "status": "failed",
                            "error": "Only PDF files are accepted."})
            continue

        # Read at most 25 MB plus one byte, so oversized files can be rejected.
        pdf_bytes = uploaded_file.file.read(25 * 1024 * 1024 + 1)

        if len(pdf_bytes) > 25 * 1024 * 1024:
            results.append({"filename": filename, "status": "failed",
                            "error": "The file exceeds the 25 MB limit."})
            continue

        # Check that the file starts with the PDF signature.
        if not pdf_bytes.startswith(b"%PDF-"):
            results.append({"filename": filename, "status": "failed",
                            "error": "This file does not appear to be a valid PDF."})
            continue

        # Add a unique prefix so two PDFs with the same name don't overwrite.
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        saved_path = UPLOAD_DIR / f"{uuid4().hex[:8]}_{filename}"
        saved_path.write_bytes(pdf_bytes)

        try:
            chunk_count = add_pdf_to_faiss(str(saved_path))
            results.append({
                "filename": filename,
                "status": "indexed",
                "chunks": chunk_count,
            })
        except Exception as error:
            # Remove the local copy if reading or indexing failed.
            saved_path.unlink(missing_ok=True)
            results.append({
                "filename": filename,
                "status": "failed",
                "error": str(error),
            })

    return {"results": results}
@app.post("/chat")
def chat(request: QuestionRequest):
    """Retrieve PDF passages and return a grounded answer with sources."""
    try:
        return answer_question(request.question.strip(), request.language)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"Could not answer right now: {error}",
        ) from error
