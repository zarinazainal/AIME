import json
import uuid
from typing import Optional
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import KnowledgeBaseEntry, ConversationMessage

def home_view(request):
    return render(request, "index.html")

def _get_session_id(request: HttpRequest) -> str:
    sid = request.session.get("aime_session_id")
    if not sid:
        sid = uuid.uuid4().hex
        request.session["aime_session_id"] = sid
    return sid


def _kb_reply(user_text: str) -> str:
    if not user_text:
        return "Sila taip soalan anda."
    # Naive search across question/answer/tags
    qs = KnowledgeBaseEntry.objects.filter(is_active=True)
    terms = [t.strip() for t in user_text.lower().split() if t.strip()]
    if not terms:
        return "Maaf, saya belum pasti. Cuba taip semula atau rujuk FAQ. (EPIC 1 mod luar talian)"
    query = Q()
    for t in terms:
        query |= Q(question__icontains=t) | Q(answer__icontains=t) | Q(tags__icontains=t)
    hit = qs.filter(query).first()
    if hit:
        return hit.answer
    return "Maaf, saya belum pasti. Cuba taip semula atau rujuk FAQ. (EPIC 1 mod luar talian)"


def _ask_fastapi(session_id: str, message: str, timeout: float = 15.0) -> Optional[str]:
    """Call FastAPI /chat if configured; return reply or None on error."""
    try:
        import requests  # lazy import so migrations don’t crash if package missing
    except Exception:
        return None

    base = getattr(settings, "FASTAPI_INTERNAL_URL", None)
    if not base:
        port = getattr(settings, "FASTAPI_PORT", 8001)
        base = f"http://fastapi:{port}"
    try:
        r = requests.post(
            f"{base}/chat",
            json={"session_id": session_id, "message": message},
            timeout=timeout,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("reply")
    except Exception:
        return None


@require_http_methods(["GET", "POST"])
def chat_view(request: HttpRequest):
    """
    GET  -> render chat page with conversation history for this session
    POST -> save user msg, try FastAPI; if unavailable, fallback to KB reply
            returns HTML page (your current template) or JSON if requested
    """
    sid = _get_session_id(request)

    if request.method == "POST":
        # accept form-encoded or JSON
        user_text = request.POST.get("message")
        if user_text is None:
            try:
                data = json.loads(request.body.decode("utf-8"))
                user_text = (data.get("message") or "").strip()
            except Exception:
                user_text = ""
        else:
            user_text = user_text.strip()

        if not user_text:
            return HttpResponseBadRequest("Message is required")

        # Save user message
        ConversationMessage.objects.create(session_id=sid, role="user", text=user_text)

        # Try FastAPI first; fallback to KB
        reply = _ask_fastapi(sid, user_text)
        if not reply:
            reply = _kb_reply(user_text)

        # Save assistant reply
        ConversationMessage.objects.create(session_id=sid, role="assistant", text=reply)

        # If the request expects JSON (e.g., fetch/ajax), return JSON
        if request.headers.get("x-requested-with") == "XMLHttpRequest" or \
           request.headers.get("accept", "").lower().find("application/json") >= 0:
            return JsonResponse({"reply": reply})

    # GET or POST (non-ajax) -> render page with history
    messages = ConversationMessage.objects.filter(session_id=sid).order_by("created_at", "id")
    return render(request, "chat/chat.html", {"messages": messages})


@require_http_methods(["GET"])
def kb_search(request: HttpRequest):
    """
    Simple KB search API used by your UI (?q=...).
    Returns JSON: { answer: "...", source: "kb" }
    """
    q = (request.GET.get("q") or "").strip()
    answer = _kb_reply(q)
    return JsonResponse({"answer": answer, "source": "kb"})
