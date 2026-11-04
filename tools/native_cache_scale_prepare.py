import ast
import json
from pathlib import Path
import subprocess
import zipfile

FILES = ["vllm/v1/attention/ops/rocm_aiter_mla_fp8_quant.py","vllm/v1/attention/ops/rocm_aiter_mla_fp8_prefill.py","vllm/v1/attention/backends/mla/rocm_aiter_mla.py","vllm/v1/attention/backends/mla/prefill/aiter_flash_attn.py","tests/kernels/attention/test_rocm_aiter_mla_prefill_fusions.py","docs/configuration/env_vars.md"]
results = {}
commands = [
    ("ruff_fix", [".venv/bin/ruff", "check", "--fix", *[p for p in FILES if p.endswith(".py")]]),
    ("ruff_format", [".venv/bin/ruff", "format", *[p for p in FILES if p.endswith(".py")]]),
    ("ruff_check", [".venv/bin/ruff", "check", *[p for p in FILES if p.endswith(".py")]]),
    ("pre_commit", [".venv/bin/pre-commit", "run", "--files", *FILES]),
]
try:
    for name, command in commands:
        p = subprocess.run(command, text=True, capture_output=True)
        results[name] = {"exit_code": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
        print(name, p.returncode, p.stdout, p.stderr, flush=True)
    for path in FILES:
        if path.endswith(".py"):
            ast.parse(Path(path).read_text())
finally:
    payload = {
        "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "files": {p: Path(p).read_text() for p in FILES},
        "results": results,
        "scope": "Formatting preparation and static checks; no GPU or model validation",
    }
    Path("native-cache-scale-preparation.json").write_text(json.dumps(payload))
    with zipfile.ZipFile("native-cache-scale-files.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for path in FILES:
            archive.write(path)
if len(results) != len(commands) or any(v["exit_code"] for v in results.values()):
    raise SystemExit(1)
