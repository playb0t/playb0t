<p align="center">
  <img src="assets/board.svg" width="100%" alt="Split-flap airport board. Departures, the research half: CVE-2026-51996 code execution, CISA 9.8; CVE-2026-51994 SSRF, 9.1; CVE-2026-51997 code execution, 8.8; CVE-2026-51995 information disclosure, 7.5; CVE-2026-52001 information disclosure, 7.5, all published 24 September 2026; CVE-2026-51998 and CVE-2026-51999 reserved for this request, not yet published; mcp-remote 0.15.1 still follows the reported path on 15 October, no fix; the fix expected since 17 February is delayed, days counted daily. Arrivals, the engineering half: Supabase PR 51646, Devin preset moved to native HTTP, arrived 14 October; dashboard-icons PR 2954, MCP setup dialog moved to native HTTP, arrived 19 October; dashboard-icons PR 2991, OAuth challenge for legacy batches, arrived 20 October; Alibaba Cloud iac-code PR 390, docs example without the bridge, arrived 20 October; Quarkus agent-mcp PR 295, skill writes kept inside the skills directory, arrived 21 October; Quarkus PR 57563, Dev UI Zed panel to native HTTP, arrived 21 October; coord-hub, boarding. Ticker: npm downloads since the private report, read daily; 62 of 62 stable releases carry the path; selected code under 12 other npm names and 8 other Git repositories; this page makes no requests to third-party servers.">
</p>

**AI systems engineer & security researcher.** I build and investigate the infrastructure that connects AI agents to tools and services: MCP integrations, OAuth interoperability and runtime trust boundaries. I trace a problem from the configuration and the authorization flow to the process that makes the request, then fix it upstream with regression tests. Both halves ask one question: **who decided that this request was allowed?**

## Upstream engineering

| Project | Status | Contribution |
| --- | --- | --- |
| [Supabase](https://github.com/supabase/supabase/pull/51646) | **Merged**, 14 October 2026 | Moved the Devin MCP preset from an unpinned `mcp-remote` bridge to native HTTP configuration, removed the dead bridge type, added shared setup instructions and brought Devin into the common client URL round-trip test. 4 files, +46/−38, 273 package tests. |
| [homarr-labs / dashboard-icons](https://github.com/homarr-labs/dashboard-icons/pull/2954) | **Merged**, 19 October 2026 | Moved the MCP setup dialog's VS Code, Claude Code, Claude Desktop, Windsurf and Zed tabs from an unpinned `mcp-remote` bridge to native HTTP connections; the custom-client tab keeps the bridge, pinned to 0.15.1. 5 files, +119/−30, 12 Chromium dialog tests. The maintainer checked every tab and merged with a fix of his own on top. |
| [homarr-labs / dashboard-icons](https://github.com/homarr-labs/dashboard-icons/pull/2991) | **Merged**, 20 October 2026 | Found while preparing the change above: the MCP route skipped the OAuth sign-in challenge and the per-call rate limit for legacy JSON-RPC batches. The fix reads every `tools/call` in a batch, challenges before dispatch and sizes the body limit by request class. 3 files, +482/−9, 1,572 tests. |
| [Alibaba Cloud / iac-code](https://github.com/aliyun/iac-code/pull/390) | **Merged**, 20 October 2026 | Replaced the `npx mcp-remote` wrapper example in the MCP passthrough documentation with a local stdio server, in English and six locales, with a note that a remote HTTP server needs no wrapper. 15 files, +76/−72, 139 pytest checks and the docs site built for seven locales. |
| [Quarkus / quarkus-agent-mcp](https://github.com/quarkusio/quarkus-agent-mcp/pull/295) | **Merged**, 21 October 2026 | Skill writes stay inside the skills directory: dot segments are rejected before any directory is created, the project and global roots are resolved and checked before writing, and `SKILL.md` is opened without following links. Reported privately to the Quarkus security team first, who assessed it as hardening and asked for the fix as a public pull request. 2 files, +185/−7, 482 tests including 11 boundary cases. |
| [Quarkus](https://github.com/quarkusio/quarkus/pull/57563) | **Merged**, 21 October 2026 | The Dev UI's MCP panel generates a native `context_servers` URL for Zed instead of an unpinned `mcp-remote` bridge and drops the Node.js prerequisite from that panel. 1 file, +1/−5, milestone 4.0. The maintainer asked for a live Zed run before merging and got it in the thread. |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk/pull/119) | **Merged** | SHA-256 integrity verification for installed agent hooks. Operational commands refuse to run when the hook differs from its recorded baseline. [Writeup and limitations](https://github.com/playb0t/rtk-hook-integrity). |

Verification behind the table. Supabase: Devin CLI 3000.11.3 and portable Devin Desktop 3.10.48 against a local OAuth fixture, then the hosted OAuth flow completed by the upstream reviewer. dashboard-icons: the generated configurations and the dialog's Chromium tests locally, then every client tab checked by the maintainer at two viewports before the merge; the batch fix against a loopback PocketBase fixture, with the gap first reproduced on the unmodified head. Alibaba Cloud: the documentation site built for seven locales and every snippet checked on the built pages. Quarkus: the skill-write fix against a real stdio MCP server, with the two escaping paths first reproduced on the unmodified build; Zed Stable 1.24.4 on Windows against a Quarkus 4.0.0.Beta1 dev-mode application with the configuration copied from the panel, no `Authorization` header, initialization and 25 tools, posted in the thread before the merge.

Earlier steps on the same line: [UltraRAG #538](https://github.com/OpenBMB/UltraRAG/pull/538) fixed the remote-MCP launch I reported within 27 hours and credited the report; [Appwrite #14465](https://github.com/appwrite/appwrite/issues/14465) is open; a local patch with regression tests is ready and waits for the maintainers' go-ahead.

## How I work

- **Client interoperability:** setup, authentication, tool discovery and reconnect behaviour tested on versioned client binaries.
- **Runtime verification:** HTTP requests correlated with process IDs and process trees, so the record says which component made the request.
- **Reproducible fixes:** source versions, traces, negative controls and regression tests preserved. Local-fixture results are kept apart from live-service validation.

## Security research

Five published CVE records reference my research into `mcp-remote`. All five carry CISA-ADP assessments, with scores up to **9.8 Critical**: [CVE-2026-51994](https://www.cve.org/CVERecord?id=CVE-2026-51994) · [CVE-2026-51995](https://www.cve.org/CVERecord?id=CVE-2026-51995) · [CVE-2026-51996](https://www.cve.org/CVERecord?id=CVE-2026-51996) · [CVE-2026-51997](https://www.cve.org/CVERecord?id=CVE-2026-51997) · [CVE-2026-52001](https://www.cve.org/CVERecord?id=CVE-2026-52001).

The research examines how remote metadata influences request destinations, browser launches and credential handling. The advisories separate local reproductions, source review and hardening findings, with version-specific scope and limitations.

**Still open.** On 14 October 2026 the maintainer published four releases, 0.14.4 to 0.15.1, the first since 21 September; none of them names a record. Release 0.15.1 was run in full against loopback canaries on 15 October 2026, with the same procedure as the 0.14.3 run of 9 October. It still follows the server-selected request path of CVE-2026-51994 and makes the authorization-server request of CVE-2026-51995, HTTP 302 redirect included; the helper functions behind all five records are byte-identical to 0.14.3. The current release, 0.15.2 of 20 October, names no record either; it differs from 0.15.1 by one statement and leaves those helpers and the bundled client unchanged, and it has not been run in full. No fix has been stated since the private report of 17 February 2026. The official MCP SDKs closed this class in September 2026 ([TypeScript](https://github.com/modelcontextprotocol/typescript-sdk/security/advisories/GHSA-6qxp-vccf-f47h), [Python](https://github.com/modelcontextprotocol/python-sdk/security/advisories/GHSA-qx49-fqc8-xw99)); mcp-remote 0.15.1 and 0.15.2 still bundle `@modelcontextprotocol/client` 2.0.0, inside the affected range.

[Research and advisories](https://github.com/playb0t/mcp-remote-oauth-security) · [Reproduction dossier](https://github.com/playb0t/mcp-remote-oauth-security/blob/main/docs/research-2026-10-09/RESEARCH_DOSSIER.md) · [0.15.1 follow-up](https://github.com/playb0t/mcp-remote-oauth-security/blob/main/docs/research-2026-10-15/README.md) · [Scope and corrections](https://github.com/playb0t/mcp-remote-oauth-security/blob/main/CORRECTIONS.md) · [Disclosure timeline](https://github.com/playb0t/mcp-remote-oauth-security/blob/main/TIMELINE.md) · [Impact ledger](https://playb0t.com)

## Host and bridge measurements

[MCP Host Matrix](https://github.com/playb0t/mcp-host-matrix) compares what MCP hosts document with what they do on a bench: five native hosts and the `mcp-remote` bridge, six directions, pinned versions and synthetic fixtures, with controls and limits beside every result. Selected disconnect actions did not revoke in 12 of 12 base windows: no revocation request reached the provider, and the prior refresh token still worked in a separate replay with the client's own credentials. Prior authority survived a build replacement in 8 of 8 cells. Evidence snapshot: 25 October 2026.

## Building: coord-hub

A local coordination layer for existing AI agents operated by different people: explicit task state, scoped delegation, human approval and verifiable execution records. It carries the same question into multi-agent systems: who can authorize an agent's next action? Active engineering work.

## Writing

- [Five mcp-remote CVE records, five CISA scores, no stated fix](https://www.linkedin.com/pulse/five-mcp-remote-cve-records-cisa-scores-stated-fix-alex-gercog-gbrfc/) · 8 October 2026, second edition
- [The Signature Was Valid. The Moment Was Gone.](https://www.linkedin.com/pulse/signature-valid-moment-gone-alex-gercog-fhncc/) · 23 September 2026
- [Who Authorized the Swarm?](https://www.linkedin.com/pulse/who-authorized-swarm-alex-gercog-gkmzc/) · 13 September 2026

<p align="center">
  <sub>The board is re-rendered every day from the npm downloads API by <a href=".github/workflows/refresh-assets.yml">a workflow in this repository</a>. The source is <a href="scripts/render_assets.py">one script</a>, the data <a href="data/snapshot.json">one file</a>. No image on this page comes from a third party.</sub><br>
  <a href="https://playb0t.com">playb0t.com</a> · <a href="https://x.com/playb_0t">@playb_0t</a> · <a href="https://github.com/playb0t/mcp-remote-oauth-security">research repository</a> · <a href="https://github.com/playb0t/mcp-host-matrix">host matrix</a> · <a href="https://github.com/playb0t/mcp-remote-oauth-security/blob/v1.0.2/CITATION.cff">citation</a>
</p>
