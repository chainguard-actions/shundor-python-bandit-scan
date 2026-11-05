"""Print the sorted set of ruleIds and the result count from a SARIF file.

Usage: python3 sarif_rules.py results.sarif [rules|count]
"""
import json
import sys

path = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else "rules"
with open(path) as f:
    data = json.load(f)
results = [r for run in data.get("runs", []) for r in (run.get("results") or [])]
if mode == "count":
    print(len(results))
else:
    print(" ".join(sorted({r.get("ruleId", "") for r in results})))
