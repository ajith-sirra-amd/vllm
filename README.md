# Retired FP8 static-validation branches

Created 2026-11-11. This is a history archive, not a runnable source checkout. Each retired branch tip is a direct parent of this commit. The tree contains only this recovery inventory; use the recorded commit to inspect or restore source.

These seven temporary validation branches were created by the assistant during PR #64288 work. Their checks are complete; the PR, integration and runtime-count implementation branches are retained separately. Creation was checked against the session tool-call record; author identity or a name prefix alone was not used.

| Retired branch | Recoverable tip |
| --- | --- |
| checks/fp8-native-tests-2f946cb | [5a22cffd0f52b41589d69a52f8b3cb08bcccfdc0](https://github.com/ajith-sirra-amd/vllm/tree/5a22cffd0f52b41589d69a52f8b3cb08bcccfdc0) |
| checks/fp8-native-tests-332d6c9 | [e1a71392429dce6b68996f473bd891aa670df3e8](https://github.com/ajith-sirra-amd/vllm/tree/e1a71392429dce6b68996f473bd891aa670df3e8) |
| checks/pr64288-asm-static-20261104 | [2fd5369890b7267e2c5c99e791e0365aa13e4f42](https://github.com/ajith-sirra-amd/vllm/tree/2fd5369890b7267e2c5c99e791e0365aa13e4f42) |
| checks/pr64288-integrate-static-20261105 | [ea6bc5839134953ab9dc43e69aff725868f53175](https://github.com/ajith-sirra-amd/vllm/tree/ea6bc5839134953ab9dc43e69aff725868f53175) |
| checks/pr64288-rendered-docs-20261102 | [fd45f3bf23b53f28d71624cb2be188b321705bd9](https://github.com/ajith-sirra-amd/vllm/tree/fd45f3bf23b53f28d71624cb2be188b321705bd9) |
| checks/pr64288-review-static-20261104 | [0b6706c590cd1fc14eaed54ecc3bb42ecfca3139](https://github.com/ajith-sirra-amd/vllm/tree/0b6706c590cd1fc14eaed54ecc3bb42ecfca3139) |
| checks/pr64288-runtime-counts-20261105 | [2dc5bcea4b9df8c20e535ff22121af5c0971b967](https://github.com/ajith-sirra-amd/vllm/tree/2dc5bcea4b9df8c20e535ff22121af5c0971b967) |

Restore only when authorized: fetching this archive makes every recorded tip reachable. Recreating a checks branch may trigger its old workflow. Runs are currently stopped. PR #64288 and its implementation were not changed by cleanup.
