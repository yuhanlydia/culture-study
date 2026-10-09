"""Prepare every native unit; labels are never used to construct prompts."""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from .assets import validate_assets
from .io import atomic_json, append_jsonl, read_json, file_hash, digest, utc

COUNTRY_LANG = {
    "UK": "English", "US": "English", "South_Korea": "Korean", "Algeria": "Arabic",
    "China": "Chinese", "Indonesia": "Indonesian", "Spain": "Spanish", "Iran": "Persian",
    "Mexico": "Spanish", "Assam": "Assamese", "Greece": "Greek", "Ethiopia": "Amharic",
    "Northern_Nigeria": "Hausa", "Azerbaijan": "Azerbaijani",
    "North_Korea": "Korean", "West_Java": "Sundanese"
}

def rows(path, required):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not set(required) <= set(reader.fieldnames or []):
            raise ValueError(f"Native schema mismatch in {path}: {reader.fieldnames}")
        for row in reader:
            if None in row:
                raise ValueError(f"Malformed native CSV row in {path}")
            yield row

def unique(items, key, name):
    ids = [x[key] for x in items]
    if len(ids) != len(set(ids)):
        raise ValueError(f"Duplicate native {key}: {name}")

def bool_label(value):
    value = value.strip().lower()
    if value not in ("true", "false"):
        raise ValueError(f"Not a native True/False label: {value}")
    return "True" if value == "true" else "False"

def prepare(root, asset_dir, bindings, destination):
    root, asset_dir, destination = Path(root), Path(asset_dir), Path(destination)
    if destination.exists():
        raise FileExistsError("Prepared inputs are immutable; choose a new destination")
    acquired = validate_assets(root, asset_dir, bindings)
    lock = read_json(root / "research/sources.lock.json")
    cfg = read_json(root / "configs/prelude.json")
    saq_contract = lock["benchmarks"]["blend"]["saq_input_contract"]
    if saq_contract["upstream_commit"] != lock["benchmarks"]["blend"]["commit"]:
        raise ValueError("SAQ column contract belongs to another BLEnD revision")
    question_columns = saq_contract["question_columns"]
    if set(question_columns) != set(COUNTRY_LANG):
        raise ValueError("Incomplete native SAQ language-column mapping")
    for country, local in COUNTRY_LANG.items():
        wanted_languages = {"English", local}
        mapping = question_columns[country]
        if set(mapping) != wanted_languages or not set(mapping.values()) <= {"Question", "Translation"}:
            raise ValueError("Invalid SAQ language-column mapping: " + country)
    destination.mkdir(parents=True)
    inventories = {}
    unit_ids = set()

    def save(task, unit):
        if unit["unit_id"] in unit_ids:
            raise ValueError("Duplicate prepared unit")
        unit_ids.add(unit["unit_id"])
        unit["task"] = task
        unit["split"] = "test"
        unit["input_digest"] = digest({k: unit[k] for k in
                                      ("task", "unit_id", "prompt", "labels", "source")})
        append_jsonl(destination / (task + ".jsonl"), unit)

    base = asset_dir / "CulturalBench"
    easy = list(rows(base / "CulturalBench-Easy.csv",
                     ["data_idx", "question_idx", "prompt_question", "answer", "country",
                      "prompt_option_a", "prompt_option_b", "prompt_option_c", "prompt_option_d"]))
    hard = list(rows(base / "CulturalBench-Hard.csv",
                     ["data_idx", "question_idx", "prompt_question", "prompt_option", "answer", "country"]))
    for items, name in ((easy, "Easy"), (hard, "Hard")):
        unique(items, "data_idx", name)
    unique(easy, "question_idx", "Easy")
    expected = lock["benchmarks"]["culturalbench"]
    if len(easy) != expected["expected_easy_questions"] or len(hard) != expected["expected_hard_rows"]:
        raise ValueError("CulturalBench release cardinality differs; do not silently mix paper/data versions")
    grouped = defaultdict(list)
    for row in hard:
        grouped[row["question_idx"]].append(row)
    if set(grouped) != {x["question_idx"] for x in easy} or any(len(v) != 4 for v in grouped.values()):
        raise ValueError("Easy/Hard question coverage or four-row grouping differs")
    for group in grouped.values():
        if len({(x["country"], x["prompt_question"]) for x in group}) != 1:
            raise ValueError("Inconsistent native Hard group")
    for row in easy:
        if row["answer"].strip() not in "ABCD" or len(row["answer"].strip()) != 1:
            raise ValueError("Unexpected Easy reference label")
        options = "\n".join(f"{lab}. {row['prompt_option_' + lab.lower()]}" for lab in "ABCD")
        prompt = "Choose one option. Reply only with A, B, C, or D.\n\nQuestion: " + row["prompt_question"] + "\n" + options + "\nAnswer:"
        save("cb_easy", {"unit_id": "cb_easy/" + row["data_idx"], "native_id": row["data_idx"],
             "cluster_id": row["question_idx"], "country": row["country"], "language": "English",
             "prompt_id": "fixed_easy_v1", "prompt": prompt, "labels": list("ABCD"), "gold": row["answer"].strip(),
             "source": {"file": "CulturalBench-Easy.csv", "sha256": acquired["files"]["CulturalBench/CulturalBench-Easy.csv"]}})
    for row in hard:
        prompt = ("Question: " + row["prompt_question"] + "\nAnswer: " + row["prompt_option"] +
                  "\nIs this answer true or false for this question? You must choose either True or False.")
        save("cb_hard", {"unit_id": "cb_hard/" + row["data_idx"], "native_id": row["data_idx"],
             "cluster_id": row["question_idx"], "country": row["country"], "language": "English",
             "prompt_id": "paper_hard_v1", "prompt": prompt, "labels": ["True", "False"], "gold": bool_label(row["answer"]),
             "source": {"file": "CulturalBench-Hard.csv", "sha256": acquired["files"]["CulturalBench/CulturalBench-Hard.csv"]}})
    inventories["cb_easy"] = {"rows": len(easy), "questions": len(easy), "countries": dict(Counter(x["country"] for x in easy))}
    inventories["cb_hard"] = {"rows": len(hard), "questions": len(grouped)}

    blend = asset_dir / "BLEnD"
    saq_count = 0
    saq_cells = {}
    shared_ids = None
    eligibility = {}
    for country, local in COUNTRY_LANG.items():
        question_path = blend / "data/questions" / (country + "_questions.csv")
        questions = list(rows(question_path, ["ID", "Question", "Translation"]))
        unique(questions, "ID", country)
        ids = {x["ID"] for x in questions}
        if len(ids) != lock["benchmarks"]["blend"]["expected_saq_templates_per_country"]:
            raise ValueError(f"Original 500-template coverage differs in {country}")
        if shared_ids is None:
            shared_ids = ids
        elif ids != shared_ids:
            raise ValueError("BLEnD global template ID correspondence differs")
        prompt_rows = list(rows(blend / "data/prompts" / (country + "_prompts.csv"),
                                ["id", "English", "Translation"]))
        unique(prompt_rows, "id", country + " prompts")
        prompts = {x["id"]: x for x in prompt_rows}
        annotations = read_json(blend / "data/annotations" / (country + "_data.json"))
        if set(annotations) != ids:
            raise ValueError("BLEnD annotation/question ID coverage differs")
        eligible = []
        for qid, annotation in annotations.items():
            idks = annotation["idks"]
            agg = annotation["aggregated_answers"]
            if idks["no-answer"] + idks["not-applicable"] < 3 and idks["idk"] < 5 and len(agg):
                if agg[0]["count"] <= 0:
                    raise ValueError("Invalid official SEM-W normalization")
                eligible.append(qid)
        eligibility[country] = len(eligible)
        languages = ["English"] if local == "English" else ["English", local]
        for language in languages:
            cell = country + "/" + language
            saq_cells[cell] = len(questions) * len(cfg["saq_prompts"])
            question_column = question_columns[country][language]
            prompt_column = "English" if language == "English" else "Translation"
            for prompt_id in cfg["saq_prompts"]:
                template = prompts[prompt_id][prompt_column]
                if "{q}" not in template:
                    raise ValueError("Native prompt placeholder missing")
                for row in questions:
                    # Bind the actual pinned release, whose question CSVs use
                    # Question for local text and Translation for English in
                    # the 14 non-English cultures. Prompt CSV columns have
                    # different semantics. Do not infer language from headers.
                    question = row[question_column]
                    # Exact operation in pinned upstream replace_country_name().
                    if language == "English" and local != "English":
                        question = question.replace("your country", country.replace("_", " "))
                    if not question:
                        raise ValueError("Empty native question/translation")
                    prompt = template.replace("{q}", question)
                    save("blend_saq", {"unit_id": f"blend_saq/{country}/{language}/{prompt_id}/{row['ID']}",
                         "native_id": row["ID"], "cluster_id": row["ID"], "country": country, "language": language,
                         "prompt_id": prompt_id, "prompt": prompt, "labels": [], "gold": None,
                         "annotation_file": "data/annotations/" + country + "_data.json",
                         "source": {"file": str(question_path.relative_to(blend)),
                                    "input_contract_id": saq_contract["contract_id"],
                                    "question_column": question_column,
                                    "prompt_column": prompt_column,
                                    "question_sha256": acquired["files"]["BLEnD/" + str(question_path.relative_to(blend))],
                                    "prompt_sha256": acquired["files"]["BLEnD/data/prompts/" + country + "_prompts.csv"]}})
                    saq_count += 1
    inventories["blend_saq"] = {"rows": saq_count, "cells": saq_cells,
                               "input_contract_id": saq_contract["contract_id"],
                               "question_columns": question_columns,
                               "eligible_questions_per_country": eligibility, "templates": len(shared_ids)}

    mc_ids = set()
    mc_counts = Counter()
    for shard in ("mc_questions_file-1.csv", "mc_questions_file-2.csv"):
        path = blend / "evaluation/mc_data/v1.1" / shard
        shard_sha256 = file_hash(path)
        for row in rows(path, ["MCQID", "ID", "country", "prompt", "choices", "choice_countries", "answer_idx"]):
            if row["MCQID"] in mc_ids:
                raise ValueError("Duplicate MCQID across native shards")
            if row["country"] not in COUNTRY_LANG or row["ID"] not in shared_ids:
                raise ValueError("MCQ culture/template identity outside original scope")
            choices = json.loads(row["choices"])
            if not isinstance(choices, dict) or set(choices) != set("ABCD") or row["answer_idx"] not in choices:
                raise ValueError("Native MCQ option contract changed")
            mc_ids.add(row["MCQID"])
            mc_counts[row["country"]] += 1
            save("blend_mcq", {"unit_id": "blend_mcq/" + row["MCQID"], "native_id": row["MCQID"],
                 "cluster_id": row["ID"], "country": row["country"], "language": "English",
                 "prompt_id": "upstream_mcq", "prompt": row["prompt"], "labels": list("ABCD"),
                 "choices": choices, "gold": row["answer_idx"],
                 "source": {"file": str(path.relative_to(blend)), "sha256": shard_sha256}})
    if set(mc_counts) != set(COUNTRY_LANG):
        raise ValueError("Incomplete MCQ culture coverage")
    inventories["blend_mcq"] = {"rows": len(mc_ids), "countries": dict(mc_counts), "shards": 2,
                                 "paper_2024_count_not_assumed": True}
    hashes = {task: file_hash(destination / (task + ".jsonl")) for task in cfg["tasks"]}
    result = {"prepared_at": utc(), "source_lock_sha256": file_hash(root / "research/sources.lock.json"),
              "bindings_sha256": file_hash(bindings), "acquisition_sha256": file_hash(asset_dir / "acquisition.json"),
              "config_sha256": file_hash(root / "configs/prelude.json"),
              "tasks": inventories, "prepared_sha256": hashes}
    atomic_json(destination / "coverage.json", result)
    return result
