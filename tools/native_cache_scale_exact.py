import hashlib,json,subprocess
from pathlib import Path
NATIVE_SHA='cbf7d1dc1c83bdf6e19dafe849c5fee42943f2ce'
HASHES={'vllm/v1/attention/ops/rocm_aiter_mla_fp8_quant.py': '33dd0ca1425a1488e0cc802de358a48563616cc59aca098e51641eabc8efded1', 'vllm/v1/attention/ops/rocm_aiter_mla_fp8_prefill.py': 'e06410ce43a55e903f25ce0dc46d1613abcc72b411d587ea687e3d197035fb84', 'vllm/v1/attention/backends/mla/rocm_aiter_mla.py': '0d4d5d550d4934d179fbdaef2dd7425d7760e732676e9cd33e2cf8826a7cc10a', 'vllm/v1/attention/backends/mla/prefill/aiter_flash_attn.py': '5f92c5e3c45e7b5a2a7012716dd4d773fa6c6c0c9e40daf0093d8995aaca9bc7', 'tests/kernels/attention/test_rocm_aiter_mla_prefill_fusions.py': 'e4d2e9ebe9911a5687b00497135f62c5efc347ee39a57b8f4e71e4c21ad47c3b', 'docs/configuration/env_vars.md': 'b614a3324165c22f37a12eed125e5cebba5d35895c324f81836c0510207f3ba9'}
for path,expected in HASHES.items():
    actual=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    assert actual==expected,path
subprocess.run(["git","diff","--exit-code",NATIVE_SHA,"--",*HASHES],check=True)
Path("native-cache-scale-exact.json").write_text(json.dumps({
    "native_sha":NATIVE_SHA,
    "static_run":41830057231,
    "static_artifact":13323221697,
    "hashes":HASHES,
    "exact_source_match":True,
}))
