"""Native endpoints and faithful-bridge outputs. Qualification remains separate."""
import contextlib
import csv
import json
from collections import defaultdict
from pathlib import Path
from .io import (atomic_json, append_jsonl, read_json, file_hash, load_complete_run, source_digest, utc)
from .official import definitions, scorer_namespace, checked_source
from .prepare import COUNTRY_LANG

def score(root, asset_dir, prepared_dir, run_dir, destination, dependencies=None):
    import pandas as pd
    root, asset_dir, prepared_dir, run_dir, destination = map(Path, (root, asset_dir, prepared_dir, run_dir, destination))
    if destination.exists():
        raise FileExistsError("Retain previous scoring attempt; choose a new destination")
    manifest = read_json(run_dir / "manifest.json")
    task = manifest["task"]
    inputs, outputs, manifest, attempts = load_complete_run(run_dir, prepared_dir / (task + ".jsonl"))
    coverage = read_json(prepared_dir / "coverage.json")
    if manifest["source_digest"] != source_digest(root):
        raise ValueError("Source changed since inference; new child run/qualification required")
    acquired = read_json(asset_dir / "acquisition.json")
    if file_hash(asset_dir / "acquisition.json") != coverage["acquisition_sha256"]:
        raise ValueError("Acquisition receipt changed since preparation")
    for name, expected in acquired["files"].items():
        if file_hash(asset_dir / name) != expected:
            raise ValueError("Native source/annotation asset changed: " + name)
    if manifest["coverage_sha256"] != file_hash(prepared_dir / "coverage.json"):
        raise ValueError("Coverage changed")
    destination.mkdir(parents=True)
    groups = defaultdict(list)
    for unit in inputs:
        groups[unit["cluster_id"]].append(unit)
    aggregates = {}
    function_hashes = {}
    if task in ("cb_easy", "cb_hard"):
        culture_correct = defaultdict(list)
        for cluster, units in groups.items():
            values = [int(outputs[x["unit_id"]]["final_answer"] == x["gold"]) for x in units]
            if task == "cb_hard" and len(units) != 4:
                raise ValueError("Not a full native Hard group")
            value = int(all(values))
            country = units[0]["country"]
            culture_correct[country].append(value)
            append_jsonl(destination / "outcomes.jsonl",
                {"cluster_id": cluster, "country": country, "language": "English", "prompt_id": units[0]["prompt_id"],
                 "value": value, "metric": "group_accuracy" if task == "cb_hard" else "accuracy",
                 "incorrect_rows": len(values) - sum(values), "rows": len(values),
                 "unit_ids": [x["unit_id"] for x in units]})
        count = sum(map(len, culture_correct.values()))
        aggregates = {"unit": "fraction", "primary": sum(map(sum, culture_correct.values())) / count,
                      "denominator_questions": count,
                      "country": {k: {"accuracy": sum(v) / len(v), "denominator": len(v)}
                                  for k, v in culture_correct.items()},
                      "parser_qualification": "pending official parity; source-defined endpoint only"}
    elif task == "blend_mcq":
        namespace = {"pd": pd}
        from tqdm.auto import tqdm
        namespace["tqdm"] = tqdm
        function_hashes["mc"] = definitions(root, asset_dir, "evaluation/multiple_choice_evaluation.py",
                                             ["multiple_choice_score"], namespace)
        joined = []
        for unit in inputs:
            answer = outputs[unit["unit_id"]]["final_answer"]
            row = {"MCQID": unit["native_id"], "ID": unit["cluster_id"], "country": unit["country"],
                   "answer_idx": unit["gold"], "final_ans": answer}
            joined.append(row)
            append_jsonl(destination / "outcomes.jsonl",
                {"cluster_id": unit["cluster_id"], "native_id": unit["native_id"], "country": unit["country"],
                 "language": "English", "prompt_id": unit["prompt_id"], "value": int(str(answer) == str(unit["gold"])),
                 "metric": "accuracy", "unit_ids": [unit["unit_id"]]})
        pd.DataFrame(joined).to_csv(destination / "native_mcq.csv", index=False)
        country = {}
        with (destination / "native_stdout.log").open("w", encoding="utf-8") as log, contextlib.redirect_stdout(log):
            for code in COUNTRY_LANG:
                result = namespace["multiple_choice_score"]("model", str(destination), "native_mcq.csv",
                                                            None, None, None, code)
                country[code] = {"accuracy": float(result),
                                 "denominator": sum(x["country"] == code for x in joined)}
        aggregates = {"unit": "fraction", "country": country,
                      "micro": sum(int(str(x["answer_idx"]) == str(x["final_ans"])) for x in joined) / len(joined),
                      "macro": sum(x["accuracy"] for x in country.values()) / len(country),
                      "denominator_rows": len(joined)}
    elif task == "blend_saq":
        if dependencies is None:
            raise ValueError("Complete scorer dependency binding required")
        cells = defaultdict(list)
        for unit in inputs:
            cells[(unit["country"], unit["language"], unit["prompt_id"])].append(unit)
        scores = {}
        with (destination / "native_stdout.log").open("w", encoding="utf-8") as log, contextlib.redirect_stdout(log):
            for (country, language, prompt_id), units in cells.items():
                namespace, hashes = scorer_namespace(root, asset_dir, language, dependencies)
                function_hashes[country + "/" + language + "/" + prompt_id] = hashes
                annotations = read_json(asset_dir / "BLEnD" / units[0]["annotation_file"])
                response_df = pd.DataFrame([{"ID": x["native_id"], "prompt": x["prompt"],
                                             "response": outputs[x["unit_id"]]["raw_response"]} for x in units])
                binary, weight, per_id = namespace["soft_exact_match"](country, language, annotations,
                                                                       response_df, "ID", "response")
                denominator = int(per_id["binary_score"].notna().sum())
                if denominator != coverage["tasks"]["blend_saq"]["eligible_questions_per_country"][country]:
                    raise ValueError("Official SAQ eligibility denominator differs")
                per_id.to_csv(destination / (country + "-" + language + "-" + prompt_id + ".csv"), index=False)
                scores[country + "/" + language + "/" + prompt_id] = {
                    "SEM_B": float(binary), "SEM_W": float(weight), "denominator": denominator}
                by_id = {x["native_id"]: x for x in units}
                for _, row in per_id.iterrows():
                    qid = row["ID"]
                    if pd.isna(row["binary_score"]):
                        continue  # Official exclusion, recorded in coverage.
                    append_jsonl(destination / "outcomes.jsonl",
                        {"cluster_id": qid, "country": country, "language": language, "prompt_id": prompt_id,
                         "value": float(row["binary_score"]), "weight_value": float(row["weight_score"]),
                         "metric": "SEM_B", "unit_ids": [by_id[qid]["unit_id"]]})
        cell_average = {}
        for country, local in COUNTRY_LANG.items():
            for language in (["English"] if local == "English" else ["English", local]):
                pair = [scores[country + "/" + language + "/" + pid] for pid in ("inst-4", "pers-3")]
                cell_average[country + "/" + language] = {
                    "SEM_B": sum(x["SEM_B"] for x in pair) / 2,
                    "SEM_W": sum(x["SEM_W"] for x in pair) / 2,
                    "denominator_per_prompt": pair[0]["denominator"]}
        language_macro = {}
        for setting in ("English", "Local"):
            selected = [cell_average[c + "/" + ("English" if setting == "English" else local)]
                        for c, local in COUNTRY_LANG.items()]
            language_macro[setting] = {metric: sum(x[metric] for x in selected) / len(selected)
                                      for metric in ("SEM_B", "SEM_W")}
        aggregates = {"unit": "percent", "prompt_cells": scores, "prompt_averaged_cells": cell_average,
                      "macro_setting": language_macro, "qualifier": "native function outputs; parity receipt still required"}
    else:
        raise ValueError("Unknown native task")
    result = {"scored_at": utc(), "task": task, "arm": manifest["arm"], "model": manifest["model"],
              "predictions_sha256": file_hash(run_dir / "predictions.jsonl"),
              "manifest_sha256": file_hash(run_dir / "manifest.json"),
              "prepared_sha256": file_hash(prepared_dir / (task + ".jsonl")),
              "outcomes_sha256": file_hash(destination / "outcomes.jsonl"),
              "score_artifacts": {p.name: file_hash(p) for p in sorted(destination.glob("*.csv"))},
              "dependencies_sha256": file_hash(dependencies) if dependencies else None,
              "function_hashes": function_hashes, "aggregates": aggregates,
              "native_units": len(inputs), "attempts": len(attempts),
              "validity": "source_bridge_output_not_yet_qualified"}
    atomic_json(destination / "score.json", result)
    return result

def parity_saq(root, asset_dir, prepared_dir, run_dir, bridge_scores, destination, dependencies):
    """Live official module versus bridge on the SAME native predictions.
    No fabricated oracle/reference scores and no stored verdict reuse.
    """
    import importlib
    import os
    import sys
    import pandas as pd
    # Upstream scoring requires a different cwd. Resolve all caller paths first.
    root, asset_dir, prepared_dir, run_dir, bridge_scores, destination = (
        Path(p).resolve() for p in
        (root, asset_dir, prepared_dir, run_dir, bridge_scores, destination))
    dependencies = Path(dependencies).resolve()
    if destination.exists():
        raise FileExistsError("Preserve prior parity attempt")
    destination.mkdir(parents=True)
    manifest = read_json(run_dir / "manifest.json")
    if manifest["task"] != "blend_saq":
        raise ValueError("SAQ parity requires a complete SAQ run")
    inputs, outputs, _, _ = load_complete_run(run_dir, prepared_dir / "blend_saq.jsonl")
    bridge_receipt = read_json(bridge_scores / "score.json")
    if bridge_receipt["predictions_sha256"] != file_hash(run_dir / "predictions.jsonl"):
        raise ValueError("Parity predictions differ")
    if bridge_receipt["dependencies_sha256"] != file_hash(dependencies):
        raise ValueError("Parity scorer resources differ")
    for field, path in (("manifest_sha256", run_dir / "manifest.json"),
                        ("prepared_sha256", prepared_dir / "blend_saq.jsonl"),
                        ("outcomes_sha256", bridge_scores / "outcomes.jsonl")):
        if bridge_receipt[field] != file_hash(path):
            raise ValueError("Parity score binding changed: " + field)
    if any(bridge_receipt[field] != manifest[field] for field in ("task", "model", "arm")):
        raise ValueError("Parity score/run identity differs")
    if manifest["source_digest"] != source_digest(root):
        raise ValueError("Parity requires the scored source revision")
    if not bridge_receipt.get("score_artifacts"):
        raise ValueError("Parity requires hashed native per-ID CSV artifacts; retain old scores")
    expected_csvs = {x["country"] + "-" + x["language"] + "-" + x["prompt_id"] + ".csv"
                     for x in inputs}
    if set(bridge_receipt["score_artifacts"]) != expected_csvs:
        raise ValueError("Parity native CSV artifact coverage differs")
    for name, expected_hash in bridge_receipt["score_artifacts"].items():
        if Path(name).name != name or file_hash(bridge_scores / name) != expected_hash:
            raise ValueError("Parity native score artifact changed: " + name)
    checked_source(root, asset_dir, "evaluation/exact_match.py")
    checked_source(root, asset_dir, "evaluation/evaluation_utils.py")
    checked_source(root, asset_dir, "utils.py")
    dep = read_json(dependencies)
    if dep.get("status") != "locally_bound" or not dep.get("resource_files"):
        raise ValueError("Parity requires bound scorer resources")
    for resource_path, expected_hash in dep["resource_files"].items():
        if file_hash(resource_path) != expected_hash:
            raise ValueError("Parity scoring resource changed: " + resource_path)
    previous_cwd = Path.cwd()
    previous_sys_path = sys.path[:]
    try:
        # Standard upstream imports require its provider SDKs and complete scorer resources.
        for path in (str(asset_dir / "BLEnD"), str(asset_dir / "BLEnD/evaluation"),
                     str(Path(dep["az_stemmer_dir"]).resolve().parent),
                     str(Path(dep["sustem_dir"]).resolve().parent)):
            sys.path.insert(0, path)
        os.chdir(Path(dep["original_scorer_cwd"]).resolve())
        official = importlib.import_module("exact_match")
        if Path(official.__file__).resolve() != asset_dir / "BLEnD/evaluation/exact_match.py":
            raise ValueError("Parity imported a different exact_match module")
        for module_name, relative in (("evaluation_utils", "evaluation/evaluation_utils.py"),
                                      ("utils", "utils.py")):
            module = sys.modules.get(module_name)
            if module is None or Path(module.__file__).resolve() != asset_dir / "BLEnD" / relative:
                raise ValueError("Parity imported a different upstream module: " + module_name)
        groups = defaultdict(list)
        for x in inputs:
            groups[(x["country"], x["language"], x["prompt_id"])].append(x)
        checks = []
        for (country, language, pid), units in groups.items():
            annotations = read_json(asset_dir / "BLEnD" / units[0]["annotation_file"])
            frame = pd.DataFrame([{"ID": x["native_id"], "prompt": x["prompt"],
                                   "response": outputs[x["unit_id"]]["raw_response"]} for x in units])
            with (destination / (country + "-" + language + "-" + pid + ".log")).open("w", encoding="utf-8") as log, contextlib.redirect_stdout(log):
                b, w, observed = official.soft_exact_match(country, language, annotations, frame, "ID", "response")
            expected = pd.read_csv(bridge_scores / (country + "-" + language + "-" + pid + ".csv"),
                                   dtype={"ID": str})
            actual = observed.set_index("ID")[["binary_score", "weight_score"]].sort_index().astype(float)
            expected = expected.set_index("ID")[["binary_score", "weight_score"]].sort_index().astype(float)
            pd.testing.assert_frame_equal(actual, expected, check_exact=True)
            cell = bridge_receipt["aggregates"]["prompt_cells"][country + "/" + language + "/" + pid]
            if abs(float(b) - cell["SEM_B"]) > 1e-12 or abs(float(w) - cell["SEM_W"]) > 1e-12:
                raise ValueError("Official SAQ aggregate parity failed")
            observed.to_csv(destination / (country + "-" + language + "-" + pid + ".csv"), index=False)
            checks.append({"country": country, "language": language, "prompt_id": pid, "identical": True})
        receipt = {"checked_at": utc(), "checks": checks, "predictions_sha256": file_hash(run_dir / "predictions.jsonl"),
                   "bridge_receipt_sha256": file_hash(bridge_scores / "score.json"),
                   "dependencies_sha256": file_hash(dependencies),
                   "scope": "SAQ functions/values on these predictions and exact assets only",
                   "does_not_establish": ["CB extraction parity", "baseline fairness", "causal mechanism", "candidate effect"]}
        atomic_json(destination / "parity.json", receipt)
        return receipt
    finally:
        os.chdir(previous_cwd)
        sys.path[:] = previous_sys_path

