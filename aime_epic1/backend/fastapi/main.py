# backend/fastapi/main.py
import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment (works in Docker and local)
load_dotenv()

app = FastAPI(title="AIME FastAPI", version="1.0.0")

# ---------------- CORS (for optional direct browser calls) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Optional Ollama (offline LLM) via LangChain -------------
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma:2b")
# If FastAPI is in Docker and Ollama runs on your host, this URL works on Docker Desktop:
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")

_llm = None
_ollama_ok = False
try:
    # Lazy import so the app still runs if langchain/ollama aren't installed
    from langchain_community.llms import Ollama  # type: ignore
    _llm = Ollama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
    _ollama_ok = True
except Exception:
    _ollama_ok = False

# ---------------- Models (original + local prompt) ----------------
class Ask(BaseModel):
    text: str

class ChatIn(BaseModel):
    session_id: str | None = None
    message: str

class ChatOut(BaseModel):
    reply: str
    timestamp: str

class LocalAsk(BaseModel):
    prompt: str

# ---------------- Endpoints ----------------
@app.get("/health")
def health():
    return {"status": "ok", "ollama": _ollama_ok, "model": OLLAMA_MODEL if _ollama_ok else None}

@app.post("/echo")
def echo(body: Ask):
    # Original echo endpoint stays as-is
    return {"reply": body.text}

@app.post("/chat-local")
def chat_local(body: LocalAsk):
    """
    Simple local method: { "prompt": "..." } -> { "response": "..." }
    Useful if you want to call FastAPI directly from a static page.
    """
    if _ollama_ok:
        try:
            out = _llm.invoke(body.prompt.strip())
            return {"response": out}
        except Exception as e:
            return {"response": f"(ollama error) {e}"}
    # Fallback: mimic echo-style behavior
    return {"response": body.prompt}

@app.post("/chat", response_model=ChatOut)
def chat(payload: ChatIn):
    """
    Django-compatible endpoint (chat_view -> _ask_fastapi).
    If Ollama is available, replies from the local model; otherwise uses your original stub.
    """
    text = payload.message.strip()
    if _ollama_ok:
        try:
            out = _llm.invoke(text)
            return ChatOut(reply=out, timestamp=datetime.utcnow().isoformat() + "Z")
        except Exception as e:
            # Graceful fallback
            fallback = f"(ollama error) I heard: '{text}'. AIME (EPIC 1) is alive! ✅"
            return ChatOut(reply=fallback, timestamp=datetime.utcnow().isoformat() + "Z")

    # Original behavior (no Ollama)
    reply_text = f"I heard: '{text}'. AIME (EPIC 1) is alive! ✅"
    return ChatOut(reply=reply_text, timestamp=datetime.utcnow().isoformat() + "Z")
