"""Local-only acquisition. Nothing is downloaded at module import."""
import re
import urllib.request
from pathlib import Path
from .io import atomic_json, read_json, file_hash, git_blob, utc

SHA = re.compile(r"^[0-9a-f]{40}$")

def bind(root, destination):
    from huggingface_hub import HfApi
    root = Path(root)
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError("Existing binding retained; use a new explicit destination for changed inputs")
    lock = read_json(root / "research/sources.lock.json")
    api = HfApi()
    cb = lock["benchmarks"]["culturalbench"]
    cb_info = api.dataset_info(cb["repo_id"], revision=cb["revision_prefix"])
    if not SHA.fullmatch(cb_info.sha) or not cb_info.sha.startswith(cb["revision_prefix"]):
        raise ValueError("CulturalBench source prefix could not be resolved faithfully")
    models = {}
    for key, config in lock["models"].items():
        requested = config["revision"]
        info = api.model_info(config["repo_id"], revision=requested or "main")
        if not SHA.fullmatch(info.sha) or (requested and info.sha != requested):
            raise ValueError(f"Unresolved model identity: {key}")
        models[key] = {"repo_id": config["repo_id"], "revision": info.sha,
                       "files": sorted(x.rfilename for x in info.siblings)}
    atomic_json(destination, {"bound_at": utc(), "source_lock_sha256": file_hash(root / "research/sources.lock.json"),
                              "culturalbench_revision": cb_info.sha, "models": models})
    return str(destination)

def download(url, path):
    """Two bounded attempts; no silent replacement of existing content."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    temp = path.with_name(path.name + ".partial")
    for attempt in range(2):
        try:
            with urllib.request.urlopen(url, timeout=120) as response, temp.open("wb") as handle:
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    handle.write(block)
            temp.replace(path)
            return
        except Exception:
            if attempt == 1:
                raise

def acquire(root, asset_dir, bindings, include_models=False):
    from huggingface_hub import snapshot_download
    root, asset_dir = Path(root), Path(asset_dir)
    lock = read_json(root / "research/sources.lock.json")
    binding = read_json(bindings)
    if binding["source_lock_sha256"] != file_hash(root / "research/sources.lock.json"):
        raise ValueError("Binding belongs to another source lock")
    asset_dir.mkdir(parents=True, exist_ok=True)
    blend = lock["benchmarks"]["blend"]
    receipt = {"acquired_at": utc(), "bindings_sha256": file_hash(bindings), "files": {}, "models": {}}
    for item in blend["files"]:
        path = asset_dir / "BLEnD" / item["path"]
        url = f"https://raw.githubusercontent.com/{blend['repository']}/{blend['commit']}/{item['path']}"
        download(url, path)
        if git_blob(path) != item["git_blob_sha"] or path.stat().st_size != item["bytes"]:
            raise ValueError(f"Pinned Git blob mismatch: {path}; retain suspect asset for diagnosis")
        receipt["files"]["BLEnD/" + item["path"]] = file_hash(path)
    cb = lock["benchmarks"]["culturalbench"]
    revision = binding["culturalbench_revision"]
    if not SHA.fullmatch(revision) or not revision.startswith(cb["revision_prefix"]):
        raise ValueError("Unpinned CulturalBench revision")
    snapshot_download(cb["repo_id"], repo_type="dataset", revision=revision,
                      allow_patterns=cb["files"], local_dir=str(asset_dir / "CulturalBench"))
    for name in cb["files"]:
        path = asset_dir / "CulturalBench" / name
        receipt["files"]["CulturalBench/" + name] = file_hash(path)
    if include_models:
        for key, config in binding["models"].items():
            if not SHA.fullmatch(config["revision"]):
                raise ValueError("Unpinned model")
            model_dir = asset_dir / "models" / key
            snapshot_download(config["repo_id"], revision=config["revision"], local_dir=str(model_dir),
                              allow_patterns=["*.json", "*.safetensors", "tokenizer.model", "*.txt", "LICENSE*", "README.md"])
            shards = sorted(model_dir.glob("*.safetensors"))
            if not shards:
                raise ValueError(f"No model weights acquired for {key}")
            receipt["models"][key] = {
                "repo_id": config["repo_id"], "revision": config["revision"],
                "files": {p.name: file_hash(p) for p in sorted(model_dir.iterdir()) if p.is_file()}}
    atomic_json(asset_dir / "acquisition.json", receipt)
    return receipt

def validate_assets(root, asset_dir, bindings):
    root, asset_dir = Path(root), Path(asset_dir)
    receipt = read_json(asset_dir / "acquisition.json")
    if receipt["bindings_sha256"] != file_hash(bindings):
        raise ValueError("Binding changed")
    binding = read_json(bindings)
    if binding["source_lock_sha256"] != file_hash(root / "research/sources.lock.json"):
        raise ValueError("Source lock changed")
    for name, expected in receipt["files"].items():
        if file_hash(asset_dir / name) != expected:
            raise ValueError(f"Acquired asset changed: {name}")
    lock = read_json(root / "research/sources.lock.json")
    expected_names = {"BLEnD/" + x["path"] for x in lock["benchmarks"]["blend"]["files"]}
    expected_names |= {"CulturalBench/" + x for x in lock["benchmarks"]["culturalbench"]["files"]}
    if set(receipt["files"]) != expected_names:
        raise ValueError("Incomplete acquisition inventory")
    for key, item in receipt["models"].items():
        for name, expected in item["files"].items():
            if file_hash(asset_dir / "models" / key / name) != expected:
                raise ValueError(f"Model artifact changed: {key}/{name}")
    return receipt
