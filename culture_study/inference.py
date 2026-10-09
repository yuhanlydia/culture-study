"""Frozen direct and whole-label likelihood baselines; local single-device runner."""
import os
import re
import time
import math
from pathlib import Path
from .io import (atomic_json, append_jsonl, read_json, jsonl, file_hash, digest,
                 source_digest, utc)
from .official import parser

def strict_label(text, labels):
    text = text.strip()
    found = re.fullmatch("(" + "|".join(re.escape(x) for x in labels) + r")[.)]?\s*", text)
    return found.group(1) if found else None

def run(root, asset_dir, bindings, prepared_dir, run_dir, model_key, task, arm, device):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    root, asset_dir, prepared_dir, run_dir = map(Path, (root, asset_dir, prepared_dir, run_dir))
    if arm not in ("direct", "label_likelihood"):
        raise ValueError("Unknown baseline")
    config = read_json(root / "configs/prelude.json")
    if model_key not in config["model_keys"] or task not in config["tasks"]:
        raise ValueError("Model/task outside frozen prelude")
    if arm == "label_likelihood" and task not in config["label_likelihood_tasks"]:
        raise ValueError("No reference-free categorical likelihood arm for open SAQ")
    if not device.startswith("cuda"):
        raise ValueError("Actual GPU device required; bind through Local native resource plan")
    coverage = read_json(prepared_dir / "coverage.json")
    prepared = prepared_dir / (task + ".jsonl")
    if file_hash(prepared) != coverage["prepared_sha256"][task]:
        raise ValueError("Prepared inputs changed")
    binding = read_json(bindings)
    acquired = read_json(asset_dir / "acquisition.json")
    if file_hash(bindings) != acquired["bindings_sha256"] or file_hash(bindings) != coverage["bindings_sha256"]:
        raise ValueError("Input binding differs")
    model_info = binding["models"][model_key]
    model_files = acquired["models"][model_key]["files"]
    model_dir = asset_dir / "models" / model_key
    for name, expected in model_files.items():
        if file_hash(model_dir / name) != expected:
            raise ValueError("Model artifact changed")
    units = list(jsonl(prepared))
    if len(units) != coverage["tasks"][task]["rows"]:
        raise ValueError("Full native unit count differs")
    run_dir.mkdir(parents=True, exist_ok=True)
    hardware = {"device": device, "gpu_name": torch.cuda.get_device_name(device),
                "total_memory_bytes": torch.cuda.get_device_properties(device).total_memory,
                "visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
                "torch": torch.__version__, "cuda": torch.version.cuda}
    manifest = {"status": "runtime_manifest", "model": model_info, "model_files": model_files,
                "task": task, "arm": arm, "prepared_sha256": file_hash(prepared),
                "coverage_sha256": file_hash(prepared_dir / "coverage.json"),
                "source_digest": source_digest(root), "config": config,
                "hardware": hardware, "bindings_sha256": file_hash(bindings)}
    manifest_path = run_dir / "manifest.json"
    if manifest_path.exists() and read_json(manifest_path) != manifest:
        raise ValueError("Run manifest changed; preserve old run and choose a new directory")
    atomic_json(manifest_path, manifest)
    manifest_digest = digest(manifest)
    done = {}
    predictions = run_dir / "predictions.jsonl"
    if predictions.exists():
        for item in jsonl(predictions):
            if item["manifest_digest"] != manifest_digest:
                raise ValueError("Mixed prediction manifests")
            done[item["unit_id"]] = item
    wanted = {x["unit_id"] for x in units}
    if not set(done) <= wanted:
        raise ValueError("Foreign native units in existing log")
    attempts = sum(1 for _ in jsonl(predictions)) if predictions.exists() else 0
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(model_dir, local_files_only=True,
             trust_remote_code=False, torch_dtype=torch.bfloat16, attn_implementation="eager").to(device).eval()
    extract_mc, mc_parser_digest = parser(root, asset_dir) if task == "blend_mcq" else (None, None)
    torch.manual_seed(0)
    torch.cuda.manual_seed_all(0)
    torch.backends.cuda.matmul.allow_tf32 = False

    call_stats = {"forward_calls": 0, "processed_tokens": 0}
    def count_forward(module, args, kwargs):
        ids = kwargs.get("input_ids", args[0] if args else None)
        if ids is not None:
            call_stats["forward_calls"] += 1
            call_stats["processed_tokens"] += int(ids.numel())
    model.register_forward_pre_hook(count_forward, with_kwargs=True)

    for unit in units:
        call_stats["forward_calls"] = 0
        call_stats["processed_tokens"] = 0
        previous = done.get(unit["unit_id"])
        if previous and previous["status"] == "ok":
            if previous["input_digest"] != unit["input_digest"]:
                raise ValueError("Changed input on resume")
            continue
        attempt = 1 + (previous["attempt"] if previous else 0)
        if attempt > 2:
            raise RuntimeError("Bounded two attempts exhausted; park affected run")
        start = time.perf_counter()
        torch.cuda.reset_peak_memory_stats(device)
        record = {"unit_id": unit["unit_id"], "native_id": unit["native_id"], "input_digest": unit["input_digest"],
                  "manifest_digest": manifest_digest, "attempt": attempt, "started_at": utc()}
        try:
            rendered = tokenizer.apply_chat_template([{"role": "user", "content": unit["prompt"]}],
                        tokenize=False, add_generation_prompt=True)
            prefix = tokenizer(rendered, add_special_tokens=False, return_tensors="pt").input_ids.to(device)
            if arm == "direct" and prefix.shape[1] + config["generation"][task] > model.config.max_position_embeddings:
                raise ValueError("Native prompt exceeds model context; never silently truncate")
            label_scores = {}
            label_token_ids = {}
            label_probabilities = {}
            output_tokens = 0
            with torch.inference_mode():
                if arm == "direct":
                    generated = model.generate(prefix, max_new_tokens=config["generation"][task],
                                do_sample=False, pad_token_id=tokenizer.eos_token_id)
                    suffix = generated[0, prefix.shape[1]:]
                    raw = tokenizer.decode(suffix, skip_special_tokens=True)
                    output_tokens = len(suffix)
                else:
                    for label in unit["labels"]:
                        whole = tokenizer(rendered + label, add_special_tokens=False, return_tensors="pt").input_ids.to(device)
                        if whole.shape[1] <= prefix.shape[1] or not torch.equal(whole[:, :prefix.shape[1]], prefix):
                            raise ValueError("Tokenizer boundary changes; cannot substitute first-token score")
                        if whole.shape[1] > model.config.max_position_embeddings:
                            raise ValueError("Native prompt plus whole label exceeds model context")
                        continuation = whole[0, prefix.shape[1]:]
                        # Only continuation positions enter this prefix-event
                        # likelihood. Do not materialize float32 log probabilities
                        # for every prompt token or retain an unused KV cache.
                        output = model(whole, use_cache=False)
                        continuation_logits = output.logits[0, prefix.shape[1] - 1:whole.shape[1] - 1].float()
                        del output
                        log_probs = continuation_logits.log_softmax(dim=-1)
                        value = log_probs.gather(1, continuation[:, None]).sum().item()
                        del continuation_logits, log_probs
                        if not math.isfinite(value):
                            raise ValueError("Non-finite whole-label log probability")
                        label_scores[label] = value
                        label_token_ids[label] = continuation.tolist()
                    raw = max(unit["labels"], key=lambda label: label_scores[label])
                    offset = max(label_scores.values())
                    mass = sum(math.exp(value - offset) for value in label_scores.values())
                    label_probabilities = {label: math.exp(value - offset) / mass
                                           for label, value in label_scores.items()}
            torch.cuda.synchronize(device)
            strict = strict_label(raw, unit["labels"]) if unit["labels"] else None
            if task == "blend_mcq":
                official = extract_mc(raw, {"choices": __import__("json").dumps(unit["choices"])}, unit["prompt"])
            else:
                official = strict
            record.update(status="ok", raw_response=raw, strict_label=strict, final_answer=official,
                          label_logprob=label_scores, label_token_ids=label_token_ids,
                          label_probabilities=label_probabilities,
                          probability_semantics=("model_prefix_probability_conditional_on_legal_labels"
                                                 if arm == "label_likelihood" else None),
                          parser_digest=mc_parser_digest, prompt_tokens=int(prefix.shape[1]),
                          forward_calls=call_stats["forward_calls"], processed_tokens=call_stats["processed_tokens"],
                          generated_tokens=output_tokens, elapsed_seconds=time.perf_counter() - start,
                          peak_allocated_bytes=torch.cuda.max_memory_allocated(device))
        except Exception as exc:
            record.update(status="error", error_type=type(exc).__name__, error=str(exc),
                          elapsed_seconds=time.perf_counter() - start)
            append_jsonl(predictions, record)
            raise
        append_jsonl(predictions, record)
        done[unit["unit_id"]] = record
        attempts += 1
    atomic_json(run_dir / "complete.json",
                {"completed_at": utc(), "manifest_digest": manifest_digest,
                 "predictions_sha256": file_hash(predictions), "native_units": len(units),
                 "attempts": attempts, "scientific_validity": "not_established",
                 "software_and_scorer_qualification": "pending"})
    return str(run_dir)

