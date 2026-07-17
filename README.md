<p align="center">
  <img src="assets/banner.svg" width="760" alt="playb0t — independent AI security research">
</p>

I look at where LLM coding agents hand execution to local infrastructure with no
human in the loop — and I harden it.

### Selected work

**[rtk-ai/rtk](https://github.com/rtk-ai/rtk)** · 71k★ · Rust command-proxy for coding agents

> **SHA-256 hook-integrity verification** — [PR #119](https://github.com/rtk-ai/rtk/pull/119), merged after security review.
>
> RTK's `PreToolUse` hook auto-approves every rewritten command, so any process
> running as the user — a malicious `postinstall`, a compromised dependency — can
> overwrite the hook and slip commands past the agent's permission prompt. I shipped
> the fail-closed integrity gate: a 525-line Rust module with a five-state
> verification machine, an `rtk verify` subcommand, read-only baseline hashes, and
> 14 unit tests. Tampered hook → RTK refuses to run.
>
> Writeup → [`rtk-hook-integrity`](https://github.com/playb0t/rtk-hook-integrity)

```python
interests = ["cognitive exploits", "cryptographic architecture", "coordinated disclosure"]
```
