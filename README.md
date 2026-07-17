```text
playb0t · independent AI security research
───────────────────────────────────────────
 focus    trust boundaries in agent tooling —
          hooks, rewrite pipelines, the local
          files an LLM agent auto-trusts
 method   threat-model the auto-trust,
          then ship the mitigation
 ethics   coordinated disclosure
```

I look at where LLM coding agents hand execution to local infrastructure
with no human in the loop — and I harden it.

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

```python
interests = ["cognitive exploits", "cryptographic architecture", "coordinated disclosure"]
```
