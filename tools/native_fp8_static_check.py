import ast
import json
import pathlib
import subprocess
import zipfile
import yaml

NATIVE_SHA = "8a55b8eacf9020a0b421a3c50a927c4a40e61604"
subprocess.run(
    ["git", "fetch", "--depth=1", "origin", NATIVE_SHA], check=True
)
files = ["vllm/models/kimi_k3/nvidia/dspark_mla.py", "vllm/v1/attention/ops/rocm_aiter_mla_prefill.py", "vllm/v1/attention/ops/rocm_aiter_mla_fp8_quant.py", "vllm/v1/attention/ops/rocm_aiter_mla_fp8_prefill.py", "vllm/v1/attention/backends/mla/rocm_aiter_mla.py", "vllm/v1/attention/backends/mla/prefill/aiter_flash_attn.py", "vllm/envs.py", "tests/kernels/attention/test_rocm_aiter_mla_prefill_fusions.py", ".buildkite/test_areas/kernels.yaml", "docs/configuration/env_vars.md"]
python_files = [f for f in files if f.endswith(".py")]
results = {}
matches = subprocess.check_output(
    ["git", "grep", "-l", "-F", "fused_qkv_per_tensor_quant", "--", "vllm", "tests"],
    text=True,
).splitlines()
calls = []
for path in matches:
    for node in ast.walk(ast.parse(pathlib.Path(path).read_text())):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "fused_qkv_per_tensor_quant"
        ):
            assert len(node.args) == 3 and not node.keywords, (path, node.lineno)
            calls.append({"file": path, "line": node.lineno})
assert calls
results["quantizer_calls"] = {"exit_code": 0, "calls": calls}
print("Quantizer callers use only the retained three inputs:", calls, flush=True)
for label, command in [
    ("ruff_check", [".venv/bin/ruff", "check", *python_files]),
    ("ruff_format_check", [".venv/bin/ruff", "format", "--check", *python_files]),
    ("pre_commit", [".venv/bin/pre-commit", "run", "--files", *files]),
    ("exact_native_files", ["git", "diff", "--exit-code", NATIVE_SHA, "--", *files]),
]:
    proc = subprocess.run(command, text=True, capture_output=True)
    print(label, proc.returncode, proc.stdout, proc.stderr, flush=True)
    results[label] = {"exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
for path in python_files:
    ast.parse(pathlib.Path(path).read_text())
yaml.safe_load(pathlib.Path(".buildkite/test_areas/kernels.yaml").read_text())
payload = {"native_sha": NATIVE_SHA, "files": {p: pathlib.Path(p).read_text() for p in files}, "results": results}
pathlib.Path("native-static-results.json").write_text(json.dumps(payload))
with zipfile.ZipFile("native-static-files.zip", "w", zipfile.ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path)
if any(result["exit_code"] for result in results.values()):
    raise SystemExit(1)
