"""Traceable residual outcomes, not fabricated Natural Gate 0 episodes."""
from collections import defaultdict
from pathlib import Path
from .io import (read_json, jsonl, append_jsonl, atomic_json, file_hash,
                 load_complete_run, utc)

def collect(prepared_dir, direct_run, alternative_run, direct_score, alternative_score, destination):
    prepared_dir, direct_run, alternative_run, direct_score, alternative_score, destination = map(Path,
        (prepared_dir, direct_run, alternative_run, direct_score, alternative_score, destination))
    if destination.exists():
        raise FileExistsError("Preserve prior census snapshot")
    d = read_json(direct_score / "score.json")
    a = read_json(alternative_score / "score.json")
    task = d["task"]
    if a["task"] != task or d["model"] != a["model"]:
        raise ValueError("Census requires same native task/model identity")
    if d["predictions_sha256"] != file_hash(direct_run / "predictions.jsonl") or a["predictions_sha256"] != file_hash(alternative_run / "predictions.jsonl"):
        raise ValueError("Scored predictions changed")
    prepared = prepared_dir / (task + ".jsonl")
    # Bind outcome evidence to its actual run, prepared inputs and scored bytes.
    # Predictions alone do not authenticate a mutable outcomes.jsonl.
    for receipt, run_path, score_path in ((d, direct_run, direct_score),
                                           (a, alternative_run, alternative_score)):
        for field, path in (("manifest_sha256", run_path / "manifest.json"),
                            ("prepared_sha256", prepared),
                            ("outcomes_sha256", score_path / "outcomes.jsonl")):
            if receipt[field] != file_hash(path):
                raise ValueError("Census score binding changed: " + field)
        run_manifest = read_json(run_path / "manifest.json")
        if any(receipt[field] != run_manifest[field] for field in ("task", "model", "arm")):
            raise ValueError("Census score/run identity differs")
    _, direct, dm, _ = load_complete_run(direct_run, prepared)
    _, alternative, am, _ = load_complete_run(alternative_run, prepared)
    if dm["source_digest"] != am["source_digest"] or dm["config"] != am["config"]:
        raise ValueError("Census arms used different code/settings")
    # SAQ compares fixed native inst-4 versus pers-3 within the complete direct
    # run. This is a prompt diagnosis, not a method-effect comparison or a new
    # native aggregate endpoint. Both source outcomes and unit IDs are retained.
    def indexed(path, prompt_filter=None):
        out = {}
        for row in jsonl(path):
            if prompt_filter and row["prompt_id"] != prompt_filter:
                continue
            key = (str(row["cluster_id"]), row["country"], row["language"], None if prompt_filter else row["prompt_id"], row.get("native_id"))
            if key in out:
                raise ValueError("Duplicate native outcome key")
            out[key] = row
        return out
    ds = indexed(direct_score / "outcomes.jsonl", "inst-4" if task == "blend_saq" else None)
    als = indexed(alternative_score / "outcomes.jsonl", "pers-3" if task == "blend_saq" else None)
    if set(ds) != set(als):
        raise ValueError("Alternative/native outcome coverage differs")
    destination.mkdir(parents=True)
    failures = 0
    unresolved = 0
    for key, outcome in ds.items():
        if outcome["value"] != 0:
            continue
        failures += 1
        alt = als[key]
        unresolved += int(alt["value"] == 0)
        unit_ids = outcome["unit_ids"]
        append_jsonl(destination / "residuals.jsonl",
            {"task": task, "cluster_id": outcome["cluster_id"], "country": outcome["country"],
             "language": outcome["language"], "prompt_id": outcome["prompt_id"],
             "native_id": outcome.get("native_id"), "direct_value": outcome["value"],
             "alternative_value": alt["value"], "unit_ids": unit_ids,
             "direct_records": [direct[x] for x in unit_ids],
             "alternative_records": [alternative[x] for x in alt["unit_ids"]],
             "mechanism_classification": None, "affected": None, "downstream_loss_attribution": None,
             "not_a_gate0_case": True})
    summary = {"collected_at": utc(), "native_outcome_denominator": len(ds), "direct_failures": failures,
               "failures_unresolved_by_this_alternative": unresolved,
               "direct_score_sha256": file_hash(direct_score / "score.json"),
               "direct_outcomes_sha256": d["outcomes_sha256"],
               "alternative_outcomes_sha256": a["outcomes_sha256"],
               "prepared_sha256": file_hash(prepared),
               "alternative_score_sha256": file_hash(alternative_score / "score.json"),
               "native_scorer_qualification": "must inspect actual parity/CB qualification receipts",
               "gate0": "not_assessed; residual outcome alone is not mechanism/value evidence",
               "test_use": "diagnosis only; no fitting, tuning or confirmation claim"}
    atomic_json(destination / "census.json", summary)
    return summary
