<p align="center">
  <img src="assets/board.svg" width="100%" alt="Split-flap airport board. Departures, the breaker half: CVE-2026-51996 code execution, CISA 9.8; CVE-2026-51994 SSRF, 9.1; CVE-2026-51997 code execution, 8.8; CVE-2026-51995 information disclosure, 7.5; CVE-2026-52001 information disclosure, 7.5, all published 24 September 2026; CVE-2026-51998 and CVE-2026-51999 reserved for this request, not yet published; mcp-remote 0.14.3 still follows the reported path on 9 October, no fix; the fix expected since 17 February is delayed, days counted daily. Arrivals, the builder half: coord-hub, boarding; rtk-ai/rtk PR 119 SHA-256 hook integrity gate, arrived. Ticker: npm downloads since the private report, read daily; 58 of 58 stable releases carry the path; selected code under 12 other npm names and 8 other Git repositories; this page makes no requests to third-party servers.">
</p>

**AI systems engineer & security researcher.** I build coordination systems for AI agents and document trust-boundary failures in the infrastructure they run on. Both halves ask one question: **who decided that this request was allowed?**

## Breaker

[Research repository](https://github.com/playb0t/mcp-remote-oauth-security) · [Dossier, 9 October 2026](https://github.com/playb0t/mcp-remote-oauth-security/blob/main/docs/research-2026-10-09/RESEARCH_DOSSIER.md) · [Impact ledger](https://playb0t.com) · [Disclosure timeline](https://github.com/playb0t/mcp-remote-oauth-security/blob/main/TIMELINE.md)

- **Records:** [CVE-2026-51996](https://www.cve.org/CVERecord?id=CVE-2026-51996) · [CVE-2026-51994](https://www.cve.org/CVERecord?id=CVE-2026-51994) · [CVE-2026-51997](https://www.cve.org/CVERecord?id=CVE-2026-51997) · [CVE-2026-51995](https://www.cve.org/CVERecord?id=CVE-2026-51995) · [CVE-2026-52001](https://www.cve.org/CVERecord?id=CVE-2026-52001). The board shows the published MITRE CNA descriptions and the CISA-ADP CVSS 3.1 scores. The research's own evidence classes and limits are in the [scope and correction record](https://github.com/playb0t/mcp-remote-oauth-security/blob/v1.0.1/CORRECTIONS.md).
- **Still open.** The current release, 0.14.3, was run in full against loopback canaries on 9 October 2026. It still follows the server-selected request path of CVE-2026-51994 and makes the authorization-server request of CVE-2026-51995, HTTP 302 redirect included. The discovery helpers execute in all 58 stable releases from 0.1.32 to 0.14.3. The official MCP SDKs fixed this class in September 2026 ([TypeScript](https://github.com/modelcontextprotocol/typescript-sdk/security/advisories/GHSA-6qxp-vccf-f47h), [Python](https://github.com/modelcontextprotocol/python-sdk/security/advisories/GHSA-qx49-fqc8-xw99)). mcp-remote 0.14.3 still bundles `@modelcontextprotocol/client` 2.0.0, inside the affected range.
- **Method:** localhost-only canaries, integrity-checked archives, recorded procedures, no weaponized code. Severity is left to the CNA and CISA and reported as published. [agent-audit-kit v0.6.18](https://github.com/sattyamjjain/agent-audit-kit/releases/tag/v0.6.18) picked the records up within eight hours of the issue.

## Builder

- **coord-hub**, a local coordination layer for AI agents operated by different people: explicit task state, scoped delegation, human approval, verifiable records of execution. Active engineering work.
- **[rtk-ai/rtk, SHA-256 hook integrity](https://github.com/rtk-ai/rtk/pull/119)**: an installed coding-agent hook is checked against its recorded hash. Operational commands are refused on a mismatch. Merged. [Technical writeup](https://github.com/playb0t/rtk-hook-integrity).

## Writing

- [Five mcp-remote CVE records, five CISA scores, no stated fix](https://www.linkedin.com/pulse/five-mcp-remote-cve-records-cisa-scores-stated-fix-alex-gercog-gbrfc/) · 8 October 2026, second edition
- [The Signature Was Valid. The Moment Was Gone.](https://www.linkedin.com/pulse/signature-valid-moment-gone-alex-gercog-fhncc/) · 23 September 2026
- [Who Authorized the Swarm?](https://www.linkedin.com/pulse/who-authorized-swarm-alex-gercog-gkmzc/) · 13 September 2026

<p align="center">
  <sub>The board is re-rendered every day from the npm downloads API by <a href=".github/workflows/refresh-assets.yml">a workflow in this repository</a>. The source is <a href="scripts/render_assets.py">one script</a>, the data <a href="data/snapshot.json">one file</a>. No image on this page comes from a third party.</sub><br>
  <a href="https://playb0t.com">playb0t.com</a> · <a href="https://x.com/playb_0t">@playb_0t</a> · <a href="https://github.com/playb0t/mcp-remote-oauth-security">research repository</a> · <a href="https://github.com/playb0t/mcp-remote-oauth-security/blob/v1.0.2/CITATION.cff">citation</a>
</p>
