#!/usr/bin/env python3
"""Batch scan DGWay model availability across OpenAI, Gemini and Antigravity."""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import dataclasses
import datetime as dt
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict, defaultdict
from typing import Any


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PRICING_JSON = REPO_ROOT / "backend/resources/model-pricing/model_prices_and_context_window.json"

MANDATORY = {
    "openai": [
        "gpt-image-1",
        "gpt-image-2",
    ],
    "gemini": [
        "gemini-2.5-flash-image",
        "gemini-2.5-flash-image-preview",
        "gemini-3.1-flash-image",
        "gemini-3.1-flash-image-preview",
        "gemini-3-pro-image",
        "gemini-3-pro-image-preview",
        "nanobananapro",
        "nanobanana2",
    ],
    "antigravity": [
        "claude-sonnet-4-6",
        "claude-opus-4-6",
        "claude-opus-4-6-thinking",
        "claude-opus-4-8",
        "gemini-2.5-flash-image",
        "gemini-2.5-flash-image-preview",
        "gemini-3.1-flash-image",
        "gemini-3.1-flash-image-preview",
        "gemini-3-pro-image",
        "gemini-3-pro-image-preview",
        "nanobananapro",
        "nanobanana2",
    ],
}

PLATFORM_LABEL = {
    "openai": "GPT / OpenAI",
    "gemini": "Gemini OAuth",
    "antigravity": "Antigravity OAuth",
}

GROUP_LABEL = {
    "openai": "GPT / OpenAI 分组",
    "gemini": "Gemini 分组",
    "antigravity": "Antigravity 分组",
}

TEXT_PROMPT_OPENAI = "用中文简短回复：DGWay OpenAI model test ok"
TEXT_PROMPT_GEMINI = "用中文简短回复：DGWay Gemini text model test ok"
TEXT_PROMPT_ANTIGRAVITY = "用中文简短回复：DGWay Antigravity model test ok"
IMAGE_PROMPT = "Create a simple 1:1 blue letter D logo on white background."


@dataclasses.dataclass
class Candidate:
    platform: str
    model: str
    sources: list[str] = dataclasses.field(default_factory=list)


class CandidateSet:
    def __init__(self) -> None:
        self.by_platform: dict[str, OrderedDict[str, Candidate]] = defaultdict(OrderedDict)

    def add(self, platform: str, model: str, source: str) -> None:
        model = normalize_model_id(model)
        if not model:
            return
        bucket = self.by_platform[platform]
        if model not in bucket:
            bucket[model] = Candidate(platform=platform, model=model)
        if source not in bucket[model].sources:
            bucket[model].sources.append(source)

    def extend(self, platform: str, models: list[str], source: str) -> None:
        for model in models:
            self.add(platform, model, source)

    def items(self, platform: str | None = None) -> list[Candidate]:
        platforms = [platform] if platform else sorted(self.by_platform)
        out: list[Candidate] = []
        for p in platforms:
            out.extend(self.by_platform.get(p, {}).values())
        return out


def mask_secret(secret: str) -> str:
    secret = secret.strip()
    if len(secret) <= 8:
        return "***"
    return f"{secret[:4]}...{secret[-4:]}"


def normalize_model_id(model: str) -> str:
    model = str(model or "").strip()
    if model.startswith("models/"):
        model = model[len("models/") :]
    model = model.strip()
    if not is_plausible_model_id(model):
        return ""
    return model


def is_plausible_model_id(model: str) -> bool:
    if not model or "*" in model:
        return False
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]*", model):
        return False
    lower = model.lower()
    if lower.endswith("models") or lower.endswith("mappings"):
        return False
    if "-" not in model and not re.search(r"\d", model) and not lower.startswith("nano"):
        return False
    return True


def classify_capability(platform: str, model: str) -> str:
    m = normalize_model_id(model).lower()
    if platform == "openai":
        if m.startswith("gpt-image-"):
            return "image"
        if "codex" in m or "coding" in m:
            return "codex"
        return "chat"
    if platform == "gemini":
        return "gemini-image" if is_image_model(m) else "gemini-text"
    if platform == "antigravity":
        if m.startswith("claude-"):
            return "claude-code"
        return "gemini-image" if is_image_model(m) else "gemini-text"
    return "chat"


def is_image_model(model: str) -> bool:
    m = model.lower()
    return "image" in m or "banana" in m


def display_name(model: str) -> str:
    words = re.split(r"[-_]+", normalize_model_id(model))
    return " ".join(w.upper() if w in {"gpt"} else w.capitalize() for w in words if w)


def http_json(
    method: str,
    url: str,
    api_key: str,
    payload: Any | None,
    timeout: float,
    extra_headers: dict[str, str] | None = None,
) -> tuple[int, bytes, float, str]:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    if payload is not None:
        headers["Content-Type"] = "application/json"
    if extra_headers:
        headers.update(extra_headers)
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            return resp.status, body, (time.perf_counter() - started) * 1000, ""
    except urllib.error.HTTPError as exc:
        body = exc.read()
        return exc.code, body, (time.perf_counter() - started) * 1000, summarize_error(body) or exc.reason
    except Exception as exc:  # noqa: BLE001 - CLI scanner should record network errors.
        return 0, b"", (time.perf_counter() - started) * 1000, str(exc)


def summarize_error(body: bytes, limit: int = 180) -> str:
    if not body:
        return ""
    text = body.decode("utf-8", errors="replace").strip()
    try:
        parsed = json.loads(text)
        err = parsed.get("error", parsed)
        if isinstance(err, dict):
            text = str(err.get("message") or err.get("type") or err)
    except Exception:
        pass
    text = re.sub(r"\s+", " ", text)
    return text[:limit]


def parse_json(body: bytes) -> Any:
    return json.loads(body.decode("utf-8", errors="replace"))


def extract_model_ids_from_models_response(body: bytes) -> list[str]:
    try:
        parsed = parse_json(body)
    except Exception:
        return []
    models = parsed.get("data") or parsed.get("models") or []
    out: list[str] = []
    if isinstance(models, list):
        for item in models:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                out.append(item.get("id") or item.get("name") or "")
    return [normalize_model_id(m) for m in out if normalize_model_id(m)]


def collect_local_candidates(candidates: CandidateSet) -> None:
    for platform, models in MANDATORY.items():
        candidates.extend(platform, models, "mandatory")

    collect_pricing_candidates(candidates)
    collect_regex_candidates(candidates, REPO_ROOT / "backend/internal/pkg/openai/constants.go", "openai", "openai-default")
    collect_regex_candidates(candidates, REPO_ROOT / "backend/internal/pkg/gemini/models.go", "gemini", "gemini-default")
    collect_regex_candidates(candidates, REPO_ROOT / "backend/internal/pkg/antigravity/claude_types.go", "antigravity", "antigravity-default")
    collect_regex_candidates(candidates, REPO_ROOT / "backend/internal/domain/constants.go", "antigravity", "antigravity-mapping")
    collect_regex_candidates(candidates, REPO_ROOT / "frontend/src/composables/useModelWhitelist.ts", "openai", "frontend-whitelist", r"(gpt[^'\"\s,]+|codex[^'\"\s,]+)")
    collect_regex_candidates(candidates, REPO_ROOT / "frontend/src/composables/useModelWhitelist.ts", "gemini", "frontend-whitelist", r"(gemini[^'\"\s,]+|nano[^'\"\s,]+)")
    collect_regex_candidates(candidates, REPO_ROOT / "frontend/src/composables/useModelWhitelist.ts", "antigravity", "frontend-whitelist", r"(claude[^'\"\s,]+|gemini[^'\"\s,]+|nano[^'\"\s,]+)")


def collect_pricing_candidates(candidates: CandidateSet) -> None:
    if not PRICING_JSON.exists():
        return
    try:
        pricing = json.loads(PRICING_JSON.read_text(encoding="utf-8"))
    except Exception:
        return
    for model, meta in pricing.items():
        if not isinstance(model, str):
            continue
        provider = str(meta.get("litellm_provider") or meta.get("provider") or "").lower() if isinstance(meta, dict) else ""
        m = model.lower()
        if m.startswith("gpt") or m.startswith("codex"):
            candidates.add("openai", model, "pricing")
        if m.startswith("gemini") or "gemini" in provider:
            candidates.add("gemini", model, "pricing")
            candidates.add("antigravity", model, "pricing")
        if m.startswith("claude"):
            candidates.add("antigravity", model, "pricing")


def collect_regex_candidates(
    candidates: CandidateSet,
    path: pathlib.Path,
    platform: str,
    source: str,
    pattern: str = r"(gpt[^'\"\s,]+|codex[^'\"\s,]+|gemini[^'\"\s,]+|claude[^'\"\s,]+|nano[^'\"\s,]+)",
) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    for model in re.findall(pattern, text):
        candidates.add(platform, model, source)


def collect_live_candidates(base_url: str, keys: dict[str, str], timeout: float, candidates: CandidateSet) -> None:
    endpoints = {
        "openai": "/v1/models",
        "gemini": "/v1beta/models",
        "antigravity": "/antigravity/v1beta/models",
    }
    for platform, endpoint in endpoints.items():
        key = keys.get(platform, "")
        if not key:
            continue
        url = urllib.parse.urljoin(base_url.rstrip("/") + "/", endpoint.lstrip("/"))
        print(f"[scan] fetch candidates {platform} {endpoint} key={mask_secret(key)}", file=sys.stderr)
        status, body, _, err = http_json("GET", url, key, None, timeout)
        if status == 200:
            candidates.extend(platform, extract_model_ids_from_models_response(body), f"live:{endpoint}")
        else:
            print(f"[scan] candidate fetch failed {platform} HTTP {status}: {err}", file=sys.stderr)


def scan_candidate(base_url: str, keys: dict[str, str], timeout: float, candidate: Candidate) -> dict[str, Any]:
    capability = classify_capability(candidate.platform, candidate.model)
    if candidate.platform == "openai":
        if capability == "image":
            return scan_openai_image(base_url, keys["openai"], timeout, candidate)
        return scan_openai_text(base_url, keys["openai"], timeout, candidate, capability)
    if candidate.platform == "gemini":
        return scan_gemini(base_url, "/v1beta", keys["gemini"], timeout, candidate, capability)
    if candidate.platform == "antigravity" and capability == "claude-code":
        return scan_antigravity_claude(base_url, keys["antigravity"], timeout, candidate)
    return scan_gemini(base_url, "/antigravity/v1beta", keys["antigravity"], timeout, candidate, capability)


def base_record(candidate: Candidate, endpoint: str, capability: str) -> dict[str, Any]:
    return {
        "platform": candidate.platform,
        "group": GROUP_LABEL[candidate.platform],
        "endpoint": endpoint,
        "model": candidate.model,
        "display_name": display_name(candidate.model),
        "capability": capability,
        "available": False,
        "http_status": 0,
        "response_kind": "error",
        "error_summary": "",
        "latency_ms": 0,
        "tested_at": dt.datetime.now(dt.UTC).isoformat(),
        "show_to_user": False,
        "notes": "; ".join(candidate.sources),
    }


def finish_record(record: dict[str, Any], status: int, body: bytes, latency: float, error: str, available: bool, kind: str) -> dict[str, Any]:
    record["http_status"] = status
    record["latency_ms"] = round(latency)
    record["available"] = bool(available)
    record["show_to_user"] = bool(available)
    record["response_kind"] = kind
    record["error_summary"] = "" if available else (error or summarize_error(body))
    return record


def scan_openai_text(base_url: str, key: str, timeout: float, candidate: Candidate, capability: str) -> dict[str, Any]:
    endpoint = "/v1/responses"
    record = base_record(candidate, endpoint, capability)
    payload = {"model": candidate.model, "input": TEXT_PROMPT_OPENAI, "max_output_tokens": 64}
    status, body, latency, err = http_json("POST", build_url(base_url, endpoint), key, payload, timeout)
    available = status == 200 and response_has_text(body)
    if not available:
        endpoint = "/v1/chat/completions"
        record["endpoint"] = endpoint
        payload = {
            "model": candidate.model,
            "messages": [{"role": "user", "content": TEXT_PROMPT_OPENAI}],
            "max_tokens": 64,
        }
        status, body, latency, err = http_json("POST", build_url(base_url, endpoint), key, payload, timeout)
        available = status == 200 and chat_has_text(body)
    return finish_record(record, status, body, latency, err, available, "text" if available else "error")


def scan_openai_image(base_url: str, key: str, timeout: float, candidate: Candidate) -> dict[str, Any]:
    endpoint = "/v1/images/generations"
    record = base_record(candidate, endpoint, "image")
    payload = {"model": candidate.model, "prompt": IMAGE_PROMPT, "size": "1024x1024", "n": 1}
    status, body, latency, err = http_json("POST", build_url(base_url, endpoint), key, payload, timeout)
    available = status == 200 and image_response_valid(body)
    return finish_record(record, status, body, latency, err, available, "image" if available else "error")


def scan_gemini(base_url: str, prefix: str, key: str, timeout: float, candidate: Candidate, capability: str) -> dict[str, Any]:
    model_path = urllib.parse.quote(normalize_model_id(candidate.model), safe="")
    endpoint = f"{prefix}/models/{model_path}:streamGenerateContent?alt=sse"
    record = base_record(candidate, endpoint, capability)
    prompt = IMAGE_PROMPT if capability.endswith("image") else TEXT_PROMPT_GEMINI
    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    status, body, latency, err = http_json("POST", build_url(base_url, endpoint), key, payload, timeout)
    has_content = sse_has_inline_data(body) if capability.endswith("image") else sse_has_text(body)
    kind = "image" if capability.endswith("image") and has_content else "sse" if has_content else "error"
    return finish_record(record, status, body, latency, err, status == 200 and has_content, kind)


def scan_antigravity_claude(base_url: str, key: str, timeout: float, candidate: Candidate) -> dict[str, Any]:
    endpoint = "/antigravity/v1/messages"
    record = base_record(candidate, endpoint, "claude-code")
    payload = {
        "model": candidate.model,
        "max_tokens": 64,
        "messages": [{"role": "user", "content": TEXT_PROMPT_ANTIGRAVITY}],
    }
    headers = {"anthropic-version": "2023-06-01"}
    status, body, latency, err = http_json("POST", build_url(base_url, endpoint), key, payload, timeout, headers)
    return finish_record(record, status, body, latency, err, status == 200 and claude_has_text(body), "text" if status == 200 else "error")


def build_url(base_url: str, endpoint: str) -> str:
    return urllib.parse.urljoin(base_url.rstrip("/") + "/", endpoint.lstrip("/"))


def response_has_text(body: bytes) -> bool:
    try:
        data = parse_json(body)
    except Exception:
        return False
    if isinstance(data.get("output_text"), str) and data["output_text"].strip():
        return True
    for item in data.get("output", []) or []:
        for content in item.get("content", []) or []:
            if str(content.get("text") or "").strip():
                return True
    return False


def chat_has_text(body: bytes) -> bool:
    try:
        data = parse_json(body)
    except Exception:
        return False
    for choice in data.get("choices", []) or []:
        msg = choice.get("message") or {}
        if str(msg.get("content") or "").strip():
            return True
    return False


def claude_has_text(body: bytes) -> bool:
    try:
        data = parse_json(body)
    except Exception:
        return False
    for part in data.get("content", []) or []:
        if str(part.get("text") or "").strip():
            return True
    return False


def image_response_valid(body: bytes) -> bool:
    try:
        data = parse_json(body)
    except Exception:
        return looks_like_image_bytes(body)
    for item in data.get("data", []) or []:
        if item.get("b64_json") and valid_b64_image(item["b64_json"]):
            return True
        if item.get("url"):
            return True
    return response_has_inline_image(data)


def response_has_inline_image(data: Any) -> bool:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in {"inlineData", "inline_data"} and isinstance(value, dict):
                raw = value.get("data")
                return isinstance(raw, str) and len(raw) > 32
            if key in {"b64_json", "result"} and isinstance(value, str) and valid_b64_image(value):
                return True
            if response_has_inline_image(value):
                return True
    if isinstance(data, list):
        return any(response_has_inline_image(item) for item in data)
    return False


def valid_b64_image(raw: str) -> bool:
    try:
        decoded = base64.b64decode(raw, validate=False)
    except Exception:
        return False
    return looks_like_image_bytes(decoded)


def looks_like_image_bytes(raw: bytes) -> bool:
    return raw.startswith(b"\x89PNG") or raw.startswith(b"\xff\xd8") or raw.startswith(b"RIFF")


def sse_events(body: bytes) -> list[Any]:
    text = body.decode("utf-8", errors="replace")
    out: list[Any] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("data:"):
            continue
        payload = line[5:].strip()
        if not payload or payload == "[DONE]":
            continue
        try:
            out.append(json.loads(payload))
        except Exception:
            continue
    return out


def sse_has_text(body: bytes) -> bool:
    for event in sse_events(body):
        if response_has_candidate_text(event):
            return True
    return False


def sse_has_inline_data(body: bytes) -> bool:
    for event in sse_events(body):
        if response_has_inline_image(event):
            return True
    return False


def response_has_candidate_text(data: Any) -> bool:
    if isinstance(data, dict):
        if isinstance(data.get("text"), str) and data["text"].strip():
            return True
        return any(response_has_candidate_text(v) for v in data.values())
    if isinstance(data, list):
        return any(response_has_candidate_text(v) for v in data)
    return False


def write_outputs(records: list[dict[str, Any]], json_path: pathlib.Path, md_path: pathlib.Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown_table(records), encoding="utf-8")


def markdown_table(records: list[dict[str, Any]]) -> str:
    lines = ["# DGWay Model Availability Scan", ""]
    for platform in ["openai", "gemini", "antigravity"]:
        rows = [r for r in records if r["platform"] == platform]
        if not rows:
            continue
        lines += [f"## {PLATFORM_LABEL[platform]}", "", "| Model | Capability | Available | HTTP | Kind | Latency | Error |", "|---|---:|---:|---:|---|---:|---|"]
        for r in sorted(rows, key=lambda x: (not x["available"], x["capability"], x["model"])):
            err = str(r["error_summary"] or "").replace("|", "\\|")
            lines.append(
                f"| `{r['model']}` | `{r['capability']}` | {'yes' if r['available'] else 'no'} | {r['http_status']} | `{r['response_kind']}` | {r['latency_ms']}ms | {err} |"
            )
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://8.148.191.211")
    parser.add_argument("--openai-key", default="")
    parser.add_argument("--gemini-key", default="")
    parser.add_argument("--antigravity-key", default="")
    parser.add_argument("--output-json", default="test-output/model-scan/available-models.json")
    parser.add_argument("--output-md", default="test-output/model-scan/available-models.md")
    parser.add_argument("--platform", choices=["openai", "gemini", "antigravity", "all"], default="all")
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--sleep", type=float, default=0.0)
    parser.add_argument("--timeout", type=float, default=45.0)
    parser.add_argument("--skip-live-candidates", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    keys = {
        "openai": args.openai_key,
        "gemini": args.gemini_key,
        "antigravity": args.antigravity_key,
    }
    platforms = ["openai", "gemini", "antigravity"] if args.platform == "all" else [args.platform]
    missing = [p for p in platforms if not keys.get(p)]
    if missing:
        print(f"missing API key(s): {', '.join(missing)}", file=sys.stderr)
        return 2

    candidates = CandidateSet()
    collect_local_candidates(candidates)
    if not args.skip_live_candidates:
        collect_live_candidates(args.base_url, keys, args.timeout, candidates)

    jobs = [c for c in candidates.items(None) if c.platform in platforms]
    print(f"[scan] testing {len(jobs)} candidates via {args.base_url}", file=sys.stderr)
    records: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as pool:
        future_map = {}
        for candidate in jobs:
            future = pool.submit(scan_candidate, args.base_url, keys, args.timeout, candidate)
            future_map[future] = candidate
            if args.sleep > 0:
                time.sleep(args.sleep)
        for future in concurrent.futures.as_completed(future_map):
            candidate = future_map[future]
            try:
                record = future.result()
            except Exception as exc:  # noqa: BLE001
                record = base_record(candidate, "", classify_capability(candidate.platform, candidate.model))
                record["error_summary"] = str(exc)
            records.append(record)
            print(
                f"[scan] {record['platform']} {record['model']} {record['capability']} "
                f"HTTP {record['http_status']} available={record['available']}",
                file=sys.stderr,
            )

    records.sort(key=lambda r: (r["platform"], r["capability"], r["model"]))
    write_outputs(records, pathlib.Path(args.output_json), pathlib.Path(args.output_md))
    print(f"[scan] wrote {args.output_json}", file=sys.stderr)
    print(f"[scan] wrote {args.output_md}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
