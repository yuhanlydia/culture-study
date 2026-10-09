"""Compare two complete native label-likelihood runs after a source repair.

This inspects software equivalence and resource evidence. It does not score a
benchmark, certify a scientific gate, or select a numerical tolerance from data.
"""
import math
from pathlib import Path
from .io import (load_complete_run, append_jsonl, atomic_json, file_hash, utc)


def compare(prepared_dir, left_run, right_run, destination):
    prepared_dir, left_run, right_run, destination = map(
        Path, (prepared_dir, left_run, right_run, destination))
    if destination.exists():
        raise FileExistsError("Keep the previous audit; choose a new destination")
    # Read identity only to locate the common prepared task. Completeness and
    # output integrity are independently checked by load_complete_run below.
    from .io import read_json
    task = read_json(left_run / "manifest.json")["task"]
    if task not in ("cb_easy", "cb_hard", "blend_mcq"):
        raise ValueError("This audit requires a native categorical task")
    prepared = prepared_dir / (task + ".jsonl")
    inputs, left, lm, _ = load_complete_run(left_run, prepared)
    other_inputs, right, rm, _ = load_complete_run(right_run, prepared)
    if inputs != other_inputs:
        raise ValueError("Different prepared native inputs")
    for field in ("task", "arm", "model", "model_files", "bindings_sha256",
                  "prepared_sha256", "coverage_sha256", "config", "hardware"):
        if lm[field] != rm[field]:
            raise ValueError("Non-source change in likelihood audit: " + field)
    if lm["arm"] != "label_likelihood":
        raise ValueError("Both runs must use the whole-label likelihood arm")
    destination.mkdir(parents=True)
    maximum_delta = 0.0
    changed_raw = changed_final = changed_strict = 0
    label_count = 0
    for unit in inputs:
        lrec, rrec = left[unit["unit_id"]], right[unit["unit_id"]]
        labels = unit["labels"]
        if not labels or any(rec["input_digest"] != unit["input_digest"]
                             for rec in (lrec, rrec)):
            raise ValueError("Prepared/prediction input identity differs")
        for rec in (lrec, rrec):
            if set(rec["label_logprob"]) != set(labels):
                raise ValueError("Missing or extra canonical label score")
            if set(rec["label_token_ids"]) != set(labels):
                raise ValueError("Missing canonical label tokenization")
        if lrec["label_token_ids"] != rrec["label_token_ids"]:
            raise ValueError("Tokenization differs between source revisions")
        deltas = {}
        for label in labels:
            lv, rv = lrec["label_logprob"][label], rrec["label_logprob"][label]
            if not math.isfinite(lv) or not math.isfinite(rv):
                raise ValueError("Non-finite retained label likelihood")
            deltas[label] = abs(rv - lv)
        maximum_delta = max(maximum_delta, max(deltas.values()))
        label_count += len(labels)
        raw_changed = lrec["raw_response"] != rrec["raw_response"]
        final_changed = lrec["final_answer"] != rrec["final_answer"]
        strict_changed = lrec["strict_label"] != rrec["strict_label"]
        changed_raw += int(raw_changed)
        changed_final += int(final_changed)
        changed_strict += int(strict_changed)
        append_jsonl(destination / "comparisons.jsonl", {
            "unit_id": unit["unit_id"], "native_id": unit["native_id"],
            "cluster_id": unit["cluster_id"], "country": unit["country"],
            "label_logprob_abs_delta": deltas,
            "raw_changed": raw_changed, "final_changed": final_changed,
            "strict_changed": strict_changed,
            "left_peak_allocated_bytes": lrec["peak_allocated_bytes"],
            "right_peak_allocated_bytes": rrec["peak_allocated_bytes"],
            "left_processed_tokens": lrec["processed_tokens"],
            "right_processed_tokens": rrec["processed_tokens"],
            "left_forward_calls": lrec["forward_calls"],
            "right_forward_calls": rrec["forward_calls"],
            "left_elapsed_seconds": lrec["elapsed_seconds"],
            "right_elapsed_seconds": rrec["elapsed_seconds"],
        })
    result = {
        "status": "software_comparison_observed_not_qualified",
        "observed_at": utc(), "task": task, "native_units": len(inputs),
        "canonical_labels_compared": label_count,
        "max_label_logprob_abs_delta": maximum_delta,
        "raw_changes": changed_raw, "final_changes": changed_final,
        "strict_changes": changed_strict,
        "left_source_digest": lm["source_digest"],
        "right_source_digest": rm["source_digest"],
        "left_manifest_sha256": file_hash(left_run / "manifest.json"),
        "right_manifest_sha256": file_hash(right_run / "manifest.json"),
        "left_complete_sha256": file_hash(left_run / "complete.json"),
        "right_complete_sha256": file_hash(right_run / "complete.json"),
        "left_predictions_sha256": file_hash(left_run / "predictions.jsonl"),
        "right_predictions_sha256": file_hash(right_run / "predictions.jsonl"),
        "prepared_sha256": file_hash(prepared),
        "comparisons_sha256": file_hash(destination / "comparisons.jsonl"),
        "qualification": "Requires the predeclared numerical criterion, source"
                         " review and official native scorer qualification.",
        "scientific_effect": "not_assessed",
    }
    atomic_json(destination / "audit.json", result)
    return result
