import ast
import json
import pathlib
import subprocess
import zipfile

import yaml

files = ['vllm/v1/attention/ops/rocm_aiter_mla_fp8_quant.py', 'vllm/v1/attention/ops/rocm_aiter_mla_fp8_prefill.py', 'vllm/v1/attention/backends/mla/rocm_aiter_mla.py', 'vllm/v1/attention/backends/mla/prefill/aiter_flash_attn.py', 'vllm/envs.py', 'tests/kernels/attention/test_rocm_aiter_mla_prefill_fusions.py', '.buildkite/test_areas/kernels.yaml', 'docs/configuration/env_vars.md']
python_files = [f for f in files if f.endswith(".py")]
results = {}
for label, command in [
    ("ruff_fix", [".venv/bin/ruff", "check", "--fix", *python_files]),
    ("ruff_format", [".venv/bin/ruff", "format", *python_files]),
    ("ruff_check", [".venv/bin/ruff", "check", *python_files]),
    ("ruff_format_check", [".venv/bin/ruff", "format", "--check", *python_files]),
]:
    proc = subprocess.run(command, text=True, capture_output=True)
    print(label, proc.returncode, proc.stdout, proc.stderr, flush=True)
    results[label] = {"exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
for path in python_files:
    ast.parse(pathlib.Path(path).read_text())
results["python_ast"] = "passed"
yaml.safe_load(pathlib.Path(".buildkite/test_areas/kernels.yaml").read_text())
results["buildkite_yaml"] = "passed"
proc = subprocess.run([".venv/bin/pre-commit", "run", "--files", *files], text=True, capture_output=True)
print("pre_commit", proc.returncode, proc.stdout, proc.stderr, flush=True)
results["pre_commit"] = {"exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
payload = {"files": {p: pathlib.Path(p).read_text() for p in files}, "results": results}
pathlib.Path("native-static-results.json").write_text(json.dumps(payload))
with zipfile.ZipFile("native-static-files.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for path in files:
        z.write(path)
if results["ruff_check"]["exit_code"] or results["ruff_format_check"]["exit_code"]:
    raise SystemExit(1)
