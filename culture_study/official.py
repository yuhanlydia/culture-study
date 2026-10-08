"""Execute original acquired scorer definitions with explicit dependencies.
The bridge avoids provider SDK import side effects. Semantic parity is REQUIRED.
"""
import ast
import importlib.util
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from string import punctuation
from .io import read_json, git_blob, file_hash, digest

def checked_source(root, asset_dir, relative):
    lock = read_json(Path(root) / "research/sources.lock.json")
    item = next(x for x in lock["benchmarks"]["blend"]["files"] if x["path"] == relative)
    path = Path(asset_dir) / "BLEnD" / relative
    if git_blob(path) != item["git_blob_sha"]:
        raise ValueError("Changed official scorer source: " + relative)
    return path.read_text(encoding="utf-8"), str(path)

def definitions(root, asset_dir, relative, names, namespace):
    text, filename = checked_source(root, asset_dir, relative)
    tree = ast.parse(text, filename=filename)
    nodes = [x for x in tree.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name in names]
    if {x.name for x in nodes} != set(names):
        raise ValueError("Official function inventory changed")
    module = ast.Module(body=nodes, type_ignores=[])
    exec(compile(ast.fix_missing_locations(module), filename, "exec"), namespace)
    return digest({x.name: ast.dump(x, include_attributes=False) for x in nodes})

def parser(root, asset_dir):
    """Retain the exact AST statements from upstream's prediction extraction."""
    namespace = {"re": re, "json": json}
    definitions(root, asset_dir, "utils.py", ["get_json_str"], namespace)
    text, filename = checked_source(root, asset_dir, "evaluation/multiple_choice_evaluation.py")
    tree = ast.parse(text, filename)
    function = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == "get_model_mc_response")
    loop = next(x for x in function.body if isinstance(x, ast.For))
    start = next(i for i, x in enumerate(loop.body)
                 if isinstance(x, ast.Assign) and any(isinstance(y, ast.Name) and y.id == "json_res" for y in x.targets))
    end = next(i for i, x in enumerate(loop.body) if i > start and isinstance(x, ast.Expr)
               and isinstance(x.value, ast.Call) and isinstance(x.value.func, ast.Name) and x.value.func.id == "write_csv_row")
    body = loop.body[start:end]
    code = ast.FunctionDef(name="extract_mc", args=ast.arguments(posonlyargs=[],
        args=[ast.arg(arg="full_res"), ast.arg(arg="row"), ast.arg(arg="prompt")],
        kwonlyargs=[], kw_defaults=[], defaults=[]), body=body + [ast.Return(value=ast.Name(id="final_ans", ctx=ast.Load()))],
        decorator_list=[])
    exec(compile(ast.fix_missing_locations(ast.Module(body=[code], type_ignores=[])), filename, "exec"), namespace)
    return namespace["extract_mc"], digest(ast.dump(code, include_attributes=False))

def dependency_namespace(language, dependency_file):
    """Actual assets/pins are a Local binding; absent assets stop affected SAQ."""
    import numpy as np
    import pandas as pd
    import spacy
    from tqdm.auto import tqdm
    dep = read_json(dependency_file)
    if dep.get("status") != "locally_bound":
        raise ValueError("Scorer dependency template is not an actual binding")
    if not dep.get("resource_files") or not dep.get("resolved_packages"):
        raise ValueError("Complete resource hashes/package versions required")
    required_assets = {"en_core_web_sm", "spark_lemma_es", "spark_lemma_am", "cltk_grc"}
    assets = dep.get("pretrained_assets", {})
    if set(assets) != required_assets:
        raise ValueError("Missing pretrained scorer asset inventory")
    for name, asset in assets.items():
        if not isinstance(asset, dict) or not asset.get("version") or not asset.get("files"):
            raise ValueError("Pretrained scorer asset not pinned: " + name)
        if any(path not in dep["resource_files"] for path in asset["files"]):
            raise ValueError("Pretrained asset lacks file hashes: " + name)
    import subprocess
    for key in ("az_stemmer_dir", "sustem_dir", "indic_library_dir", "indic_resources_dir"):
        directory = dep.get(key)
        expected = dep.get("resolved_git_revisions", {}).get(key)
        if not directory or not expected or not re.fullmatch(r"[0-9a-f]{40}", expected):
            raise ValueError("Unbound scorer source: " + key)
        actual = subprocess.check_output(["git", "-C", directory, "rev-parse", "HEAD"], text=True).strip()
        if actual != expected:
            raise ValueError("Changed scorer source revision: " + key)
    import importlib.metadata
    for package, expected in dep["resolved_packages"].items():
        if importlib.metadata.version(package) != expected:
            raise ValueError("Changed scorer package: " + package)
    for path, expected in dep.get("resource_files", {}).items():
        if file_hash(path) != expected:
            raise ValueError("Changed scoring resource: " + path)
    ns = {"os": os, "sys": sys, "re": re, "json": json, "np": np, "pd": pd,
          "tqdm": tqdm, "spacy": spacy, "ud": unicodedata, "punctuation": punctuation}
    if language == "Korean":
        from konlpy.tag import Okt
        ns["Okt"] = Okt
    elif language == "Hausa":
        import hausastemmer
        ns["hausastemmer"] = hausastemmer
    elif language == "Azerbaijani":
        repo = Path(dep["az_stemmer_dir"]).resolve()
        sys.path.insert(0, str(repo.parent))
        from stemmer.stemmer import Stemmer
        ns["AZStemmer"] = Stemmer
    elif language == "Indonesian":
        from nlp_id.lemmatizer import Lemmatizer
        ns["IDLemmatizer"] = Lemmatizer
    elif language == "Persian":
        from hazm import Lemmatizer
        ns["PRLemmatizer"] = Lemmatizer
    elif language == "Arabic":
        from qalsadi.lemmatizer import Lemmatizer
        ns["ARLeammatizer"] = Lemmatizer
    elif language == "Greek":
        from cltk import NLP
        ns["NLP"] = NLP
    elif language in ("Spanish", "Amharic"):
        import sparknlp
        from sparknlp.base import DocumentAssembler, LightPipeline
        from sparknlp.annotator import Tokenizer, LemmatizerModel
        from pyspark.ml import Pipeline
        ns.update(sparknlp=sparknlp, DocumentAssembler=DocumentAssembler, LightPipeline=LightPipeline,
                  Tokenizer=Tokenizer, LemmatizerModel=LemmatizerModel, Pipeline=Pipeline)
    elif language == "Sundanese":
        path = Path(dep["sustem_dir"]).resolve() / "SUSTEM_S.py"
        spec = importlib.util.spec_from_file_location("culture_sustem", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        ns["EcsStemmer"] = module.EcsStemmer
    elif language == "Chinese":
        import jieba
        ns["jieba"] = jieba
    elif language == "Assamese":
        lib = str(Path(dep["indic_library_dir"]).resolve())
        sys.path.insert(0, lib)
        from indicnlp import common, loader
        from indicnlp.tokenize import indic_tokenize
        ns.update(common=common, loader=loader, indic_tokenize=indic_tokenize,
                  INDIC_NLP_RESOURCES=str(Path(dep["indic_resources_dir"]).resolve()))
    elif language != "English":
        raise ValueError("Unknown original language: " + language)
    return ns

def scorer_namespace(root, asset_dir, language, dependency_file):
    namespace = dependency_namespace(language, dependency_file)
    hashes = {}
    hashes["utils"] = definitions(root, asset_dir, "evaluation/evaluation_utils.py",
               ["delete_prompt_from_answer", "get_llm_response_by_id"], namespace)
    hashes["exact"] = definitions(root, asset_dir, "evaluation/exact_match.py",
               ["lemma_check", "soft_exact_match"], namespace)
    hashes["mc"] = definitions(root, asset_dir, "evaluation/multiple_choice_evaluation.py",
               ["multiple_choice_score"], namespace)
    return namespace, hashes
