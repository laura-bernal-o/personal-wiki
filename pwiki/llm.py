"""Thin client for the local Ollama server (stdlib only).

Gemma never reads files on its own: everything it sees is passed in `messages`
by the harness. This module only moves JSON to and from 127.0.0.1.
"""
import json
import time
import urllib.error
import urllib.request

from . import config


class ModelUnavailable(RuntimeError):
    """Ollama isn't running or the model isn't pulled."""


def _post(path, payload, timeout=config.REQUEST_TIMEOUT):
    req = urllib.request.Request(
        config.OLLAMA_URL + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        if e.code == 404 and "not found" in body:
            model = payload.get("model", "?")
            raise ModelUnavailable(
                f"Model '{model}' is not downloaded. Run (while online): ollama pull {model}"
            ) from None
        raise RuntimeError(f"Ollama returned HTTP {e.code}: {body[:300]}") from None
    except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
        raise ModelUnavailable(
            f"Can't reach Ollama at {config.OLLAMA_URL} ({e}). Start it with: ollama serve"
        ) from None


def chat(messages, model=None, tools=None, fmt=None, temperature=0.2, num_ctx=None):
    """One non-streaming chat call. Returns (message_dict, stats_dict)."""
    payload = {
        "model": model or config.CHAT_MODEL,
        "messages": messages,
        "stream": False,
        "think": False,
        "options": {"temperature": temperature, "num_ctx": num_ctx or config.NUM_CTX},
    }
    if tools:
        payload["tools"] = tools
    if fmt:
        payload["format"] = fmt
    t0 = time.perf_counter()
    data = _post("/api/chat", payload)
    stats = {
        "model": data.get("model"),
        "wall_s": round(time.perf_counter() - t0, 2),
        "load_s": round(data.get("load_duration", 0) / 1e9, 2),
        "prompt_tokens": data.get("prompt_eval_count"),
        "output_tokens": data.get("eval_count"),
        "tokens_per_s": round(data["eval_count"] / (data["eval_duration"] / 1e9), 1)
        if data.get("eval_duration") else None,
    }
    return data["message"], stats


def embed(texts, model=None):
    """Embed a list of strings locally. Returns list[list[float]]."""
    out = []
    for i in range(0, len(texts), 32):
        data = _post("/api/embed", {"model": model or config.EMBED_MODEL, "input": texts[i:i + 32]})
        out.extend(data["embeddings"])
    return out


def model_info(model=None):
    """Exact identity for evidence cards: name, digest, quantization, params."""
    model = model or config.CHAT_MODEL
    info = {"model": model, "runtime": "ollama", "mode": "local"}
    try:
        show = _post("/api/show", {"model": model}, timeout=30)
        details = show.get("details", {})
        info.update(
            quantization=details.get("quantization_level"),
            parameter_size=details.get("parameter_size"),
            family=details.get("family"),
            format=details.get("format"),
        )
        with urllib.request.urlopen(config.OLLAMA_URL + "/api/tags", timeout=10) as r:
            for m in json.loads(r.read())["models"]:
                if m["name"] == model or m["model"] == model:
                    info["digest"] = m["digest"][:12]
        with urllib.request.urlopen(config.OLLAMA_URL + "/api/version", timeout=10) as r:
            info["ollama_version"] = json.loads(r.read())["version"]
    except Exception as e:  # identity is best-effort; never block an answer on it
        info["error"] = str(e)
    return info


def loaded_memory():
    """Memory Ollama reports for currently loaded models (GB)."""
    try:
        with urllib.request.urlopen(config.OLLAMA_URL + "/api/ps", timeout=10) as r:
            return {m["name"]: round(m["size"] / 1e9, 2) for m in json.loads(r.read())["models"]}
    except Exception:
        return {}
