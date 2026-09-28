<p align="center">
  <img src="https://raw.githubusercontent.com/playb0t/playb0t/6e8f687/assets/banner.svg" width="760" alt="playb0t — MCP and agent trust-boundary security research">
</p>

I look at where MCP clients and LLM coding agents hand trust to remote metadata
or local infrastructure with no human in the loop — and I harden it.

### Selected work

**[mcp-remote OAuth trust-boundary research](https://github.com/playb0t/mcp-remote-oauth-security)** · 7 advisory records · 5 published CVE references

> **Reviewed surfaces** — resource metadata, authorization-server discovery,
> redirect handling, browser navigation, local credentials, and SSE transport.
>
> Public research release for `geelen/mcp-remote`, reviewed through `0.1.38`.
> Relevant ranges differ by advisory: two localhost-canary PoCs, three bounded
> source-review findings, and two defense-in-depth/correction records. No
> weaponized exploit code published.
>
> Research repository → [`mcp-remote-oauth-security`](https://github.com/playb0t/mcp-remote-oauth-security)

**CVE publication milestone.** Five MITRE records published on **2026-09-24**
link directly to the versioned research advisories (verified 2026-09-28):

| Public CVE record | Research record | Evidence class in v1.0.1 |
|---|---|---|
| [CVE-2026-51994](https://www.cve.org/CVERecord?id=CVE-2026-51994) | [F-01: resource-metadata SSRF](https://github.com/playb0t/mcp-remote-oauth-security/blob/v1.0.1/advisories/F-01-resource-metadata-ssrf.md) | Localhost canary, reverified |
| [CVE-2026-51995](https://www.cve.org/CVERecord?id=CVE-2026-51995) | [F-02: authorization-server blind SSRF](https://github.com/playb0t/mcp-remote-oauth-security/blob/v1.0.1/advisories/F-02-authorization-server-ssrf.md) | Localhost canary, reverified |
| [CVE-2026-51996](https://www.cve.org/CVERecord?id=CVE-2026-51996) | [F-04: MD5 namespace hardening](https://github.com/playb0t/mcp-remote-oauth-security/blob/v1.0.1/advisories/F-04-md5-token-isolation.md) | Corrected / defense-in-depth |
| [CVE-2026-51997](https://www.cve.org/CVERecord?id=CVE-2026-51997) | [F-08: browser destination validation](https://github.com/playb0t/mcp-remote-oauth-security/blob/v1.0.1/advisories/F-08-browser-url-validation.md) | Source review |
| [CVE-2026-52001](https://www.cve.org/CVERecord?id=CVE-2026-52001) | [F-11: token-origin binding](https://github.com/playb0t/mcp-remote-oauth-security/blob/v1.0.1/advisories/F-11-sse-token-origin-scope.md) | Corrected / defense-in-depth |

Some CVE descriptions are broader than the corrected research evidence.
My technical claims follow the [v1.0.1 correction log](https://github.com/playb0t/mcp-remote-oauth-security/blob/v1.0.1/CORRECTIONS.md)
and the evidence class stated in each advisory.

**[rtk-ai/rtk](https://github.com/rtk-ai/rtk)** · 74k★ · Rust command-proxy for coding agents

> **SHA-256 hook-integrity verification** - [PR #119](https://github.com/rtk-ai/rtk/pull/119), merged after security review.
>
> RTK's `PreToolUse` hook auto-approves every rewritten command, so any process
> running as the user - a malicious `postinstall`, a compromised dependency — can
> overwrite the hook and slip commands past the agent's permission prompt. I shipped
> the fail-closed integrity gate: a 525-line Rust module with a five-state
> verification machine, an `rtk verify` subcommand, read-only baseline hashes, and
> 14 unit tests. Tampered hook → RTK refuses to run.
>
> Writeup → [`rtk-hook-integrity`](https://github.com/playb0t/rtk-hook-integrity)

```python
interests = ["MCP/OAuth trust boundaries", "cryptographic architecture", "coordinated disclosure"]
```
