"""CLI inner commands for Local trusted native execution plans."""
import argparse
from pathlib import Path
from .io import canonical

def main():
    parser = argparse.ArgumentParser(prog="python -m culture_study")
    parser.add_argument("--root", default=".", help="Actual project checkout path")
    sub = parser.add_subparsers(dest="command", required=True)
    b = sub.add_parser("bind")
    b.add_argument("--out", required=True)
    a = sub.add_parser("acquire")
    a.add_argument("--assets", required=True)
    a.add_argument("--bindings", required=True)
    a.add_argument("--models", action="store_true")
    v = sub.add_parser("validate-assets")
    v.add_argument("--assets", required=True)
    v.add_argument("--bindings", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--assets", required=True)
    p.add_argument("--bindings", required=True)
    p.add_argument("--out", required=True)
    r = sub.add_parser("run")
    r.add_argument("--assets", required=True)
    r.add_argument("--bindings", required=True)
    r.add_argument("--prepared", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--model", required=True, choices=["llama_1b", "qwen_7b"])
    r.add_argument("--task", required=True, choices=["cb_easy", "cb_hard", "blend_mcq", "blend_saq"])
    r.add_argument("--arm", required=True, choices=["direct", "label_likelihood"])
    r.add_argument("--device", required=True)
    s = sub.add_parser("score")
    s.add_argument("--assets", required=True)
    s.add_argument("--prepared", required=True)
    s.add_argument("--run", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--dependencies")
    q = sub.add_parser("parity-saq")
    q.add_argument("--assets", required=True)
    q.add_argument("--prepared", required=True)
    q.add_argument("--run", required=True)
    q.add_argument("--bridge-scores", required=True)
    q.add_argument("--dependencies", required=True)
    q.add_argument("--out", required=True)
    c = sub.add_parser("census")
    c.add_argument("--prepared", required=True)
    c.add_argument("--direct-run", required=True)
    c.add_argument("--alternative-run", required=True)
    c.add_argument("--direct-score", required=True)
    c.add_argument("--alternative-score", required=True)
    c.add_argument("--out", required=True)
    l = sub.add_parser("audit-likelihood")
    l.add_argument("--prepared", required=True)
    l.add_argument("--left-run", required=True)
    l.add_argument("--right-run", required=True)
    l.add_argument("--out", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.command == "bind":
        from .assets import bind
        result = bind(root, Path(args.out).resolve())
    elif args.command == "acquire":
        from .assets import acquire
        result = acquire(root, Path(args.assets).resolve(), Path(args.bindings).resolve(), args.models)
    elif args.command == "validate-assets":
        from .assets import validate_assets
        result = validate_assets(root, Path(args.assets).resolve(), Path(args.bindings).resolve())
    elif args.command == "prepare":
        from .prepare import prepare
        result = prepare(root, Path(args.assets).resolve(), Path(args.bindings).resolve(), Path(args.out).resolve())
    elif args.command == "run":
        from .inference import run
        result = run(root, Path(args.assets).resolve(), Path(args.bindings).resolve(), Path(args.prepared).resolve(),
                     Path(args.out).resolve(), args.model, args.task, args.arm, args.device)
    elif args.command == "score":
        from .scoring import score
        result = score(root, Path(args.assets).resolve(), Path(args.prepared).resolve(), Path(args.run).resolve(),
                       Path(args.out).resolve(), Path(args.dependencies).resolve() if args.dependencies else None)
    elif args.command == "parity-saq":
        from .scoring import parity_saq
        result = parity_saq(root, Path(args.assets).resolve(), Path(args.prepared).resolve(), Path(args.run).resolve(),
                            Path(args.bridge_scores).resolve(), Path(args.out).resolve(), Path(args.dependencies).resolve())
    elif args.command == "census":
        from .census import collect
        result = collect(Path(args.prepared).resolve(), Path(args.direct_run).resolve(), Path(args.alternative_run).resolve(),
                         Path(args.direct_score).resolve(), Path(args.alternative_score).resolve(), Path(args.out).resolve())
    elif args.command == "audit-likelihood":
        from .likelihood_audit import compare
        result = compare(Path(args.prepared).resolve(), Path(args.left_run).resolve(),
                         Path(args.right_run).resolve(), Path(args.out).resolve())
    else:
        raise ValueError("Unknown command")
    print(canonical(result))

if __name__ == "__main__":
    main()

