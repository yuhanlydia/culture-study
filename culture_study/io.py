"""Provenance, atomic writes and complete-run checks."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

def utc():
    return datetime.now(timezone.utc).isoformat()

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)

def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()

def file_hash(path, algorithm="sha256"):
    h = hashlib.new(algorithm)
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def git_blob(path):
    path = Path(path)
    h = hashlib.sha1()
    h.update(("blob " + str(path.stat().st_size) + "\0").encode())
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def read_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)

def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp-" + str(os.getpid()))
    with temp.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)

def jsonl(path):
    with Path(path).open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_no}: truncated/invalid JSON; preserve and repair run") from exc

def append_jsonl(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(canonical(value) + "\n")
        handle.flush()
        os.fsync(handle.fileno())

def source_digest(root):
    root = Path(root)
    paths = sorted((root / "culture_study").glob("*.py"))
    paths += [root / "pyproject.toml", root / "configs/prelude.json"]
    return digest({str(p.relative_to(root)): file_hash(p) for p in paths})

def load_complete_run(run_dir, prepared):
    run_dir = Path(run_dir)
    manifest = read_json(run_dir / "manifest.json")
    if manifest["prepared_sha256"] != file_hash(prepared):
        raise ValueError("Prepared inputs changed since inference")
    last = {}
    attempts = []
    for item in jsonl(run_dir / "predictions.jsonl"):
        if item["manifest_digest"] != digest(manifest):
            raise ValueError("Mixed inference manifests")
        last[item["unit_id"]] = item
        attempts.append(item)
    inputs = list(jsonl(prepared))
    wanted = {x["unit_id"] for x in inputs}
    if len(wanted) != len(inputs):
        raise ValueError("Duplicate prepared unit IDs")
    if set(last) != wanted or any(x["status"] != "ok" for x in last.values()):
        raise ValueError("Incomplete/failed native run; no completed score receipt")
    receipt = read_json(run_dir / "complete.json")
    if receipt["predictions_sha256"] != file_hash(run_dir / "predictions.jsonl"):
        raise ValueError("Predictions changed after completion")
    if receipt["manifest_digest"] != digest(manifest):
        raise ValueError("Completion manifest differs")
    return inputs, last, manifest, attempts

