import json
import os
import urllib.error
import urllib.request

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-5"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"

REQUEST_TIMEOUT_SECONDS = 20
MAX_TOKENS = 400

SYSTEM_PROMPT = (
    "당신은 PyCoach의 AI 코치입니다. 파이썬을 처음 배우는 학습자를 돕습니다.\n"
    "반드시 지켜야 할 원칙:\n"
    "1. 정답 코드를 통째로 알려주지 마세요. 학습자가 스스로 다음 한 줄을 찾도록 방향과 이유를 설명하세요.\n"
    "2. 학습자의 현재 코드를 보고 어떤 개념에서 막혔는지 짚어주세요.\n"
    "3. 쉬운 말로, 3~5문장 이내로 짧게 답하세요.\n"
    "4. 잘한 부분이 있다면 먼저 칭찬하고, 한 번에 하나의 개선점만 제안하세요.\n"
    "5. 공감하고 격려하는 어조를 유지하세요."
)


class CoachUnavailable(Exception):
    """No API key is configured."""


class CoachRequestFailed(Exception):
    """The API call itself failed (network error, bad key, rate limit, ...)."""


def _build_user_message(prompt: str, code: str, question: str) -> str:
    return (
        f"[문제] {prompt}\n\n"
        f"[학습자가 작성한 코드]\n{code or '(아직 작성하지 않음)'}\n\n"
        f"[학습자의 질문] {question}"
    )


def _post_json(url: str, headers: dict[str, str], body: dict) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as res:
            return json.loads(res.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        raise CoachRequestFailed(str(exc)) from exc


def _ask_anthropic(api_key: str, prompt: str, code: str, question: str) -> str:
    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_ANTHROPIC_MODEL)
    body = {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": _build_user_message(prompt, code, question)}],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
    }
    result = _post_json(ANTHROPIC_API_URL, headers, body)
    try:
        return "".join(block["text"] for block in result["content"] if block.get("type") == "text").strip()
    except (KeyError, IndexError) as exc:
        raise CoachRequestFailed(f"예상치 못한 응답 형식: {result}") from exc


def _ask_openai(api_key: str, prompt: str, code: str, question: str) -> str:
    model = os.environ.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)
    body = {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_message(prompt, code, question)},
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "content-type": "application/json",
    }
    result = _post_json(OPENAI_API_URL, headers, body)
    try:
        return result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as exc:
        raise CoachRequestFailed(f"예상치 못한 응답 형식: {result}") from exc


def ask_coach(prompt: str, code: str, question: str) -> str:
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if anthropic_key:
        return _ask_anthropic(anthropic_key, prompt, code, question)
    if openai_key:
        return _ask_openai(openai_key, prompt, code, question)
    raise CoachUnavailable("ANTHROPIC_API_KEY 또는 OPENAI_API_KEY가 설정되어 있지 않습니다.")
