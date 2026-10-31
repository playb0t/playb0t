"""Render the profile's neon panels: link buttons and merged-pull-request cards.

    python scripts/render_cards.py

Standard library only. Writes assets/btn-*.svg and assets/card-*.svg. Colours follow the playb0t banner:
deep teal glass, a cyan outline and the red/cyan glitch offset on the headline.
"""
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
BG, GLASS, EDGE, CYAN, RED, ICE, MUTED = "#010607", "#04191c", "#0a3a40", "#01fafa", "#fd0000", "#e6fbfd", "#7fb5bd"
SANS = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
HEAVY = "'Arial Black', 'Segoe UI Black', Arial, sans-serif"
WRAP = 62  # characters per description line on a card


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def panel(w: int, h: int, cut: int) -> str:
    # The angular panel of the old channel: a chamfered top-right corner and a notch at the bottom left.
    return f"M8 4 H{w - cut} L{w - 4} {cut} V{h - 8} H{w // 4} L{w // 4 - 14} {h - 4} H8 Z"


def glow_defs(uid: str) -> str:
    return (f'<defs><filter id="g{uid}" x="-20%" y="-40%" width="140%" height="180%">'
            f'<feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<linearGradient id="s{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#062a2f"/><stop offset="1" stop-color="{GLASS}"/></linearGradient></defs>')


def glitch_text(x: float, y: float, text: str, size: int, family: str, weight: str = "900", italic: bool = True) -> str:
    style = ' font-style="italic"' if italic else ""
    t = esc(text)
    common = f'font-family="{family}" font-size="{size}" font-weight="{weight}"{style}'
    return (f'<text x="{x - 2}" y="{y}" {common} fill="{RED}" opacity="0.85">{t}</text>'
            f'<text x="{x + 2}" y="{y}" {common} fill="{CYAN}" opacity="0.85">{t}</text>'
            f'<text x="{x}" y="{y}" {common} fill="{ICE}">{t}</text>')


def button(label: str, hint: str, uid: str) -> str:
    w, h = 340, 104
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}: {esc(hint)}">',
        glow_defs(uid),
        f'<path d="{panel(w, h, 26)}" fill="url(#s{uid})" stroke="{CYAN}" stroke-width="2.5" filter="url(#g{uid})"/>',
        glitch_text(30, 62, label, 34, HEAVY),
        f'<text x="31" y="86" font-family="{SANS}" font-size="13" fill="{MUTED}" letter-spacing="2">{esc(hint.upper())}</text>',
        f'<circle cx="{w - 34}" cy="{h - 24}" r="5" fill="{CYAN}" filter="url(#g{uid})"/>',
        "</svg>"])


def card(title: str, pr: str, line: str, stats: str, when: str, uid: str) -> str:
    w, h = 640, 236
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)} {esc(pr)}, merged {esc(when)}: {esc(line)}. {esc(stats)}">',
           glow_defs(uid),
           f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>',
           f'<path d="{panel(w, h, 34)}" fill="url(#s{uid})" stroke="{CYAN}" stroke-width="2" filter="url(#g{uid})"/>',
           f'<text x="34" y="46" font-family="{SANS}" font-size="15" font-weight="700" fill="{CYAN}" letter-spacing="3">MERGED · {esc(when.upper())}</text>',
           glitch_text(32, 98, title, 36, HEAVY),
           f'<text x="34" y="134" font-family="{SANS}" font-size="20" font-weight="600" fill="{ICE}">{esc(pr)}</text>']
    words, rows, cur = line.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > WRAP:
            rows.append(cur); cur = wd
        else:
            cur = (cur + " " + wd).strip()
    rows.append(cur)
    for i, r in enumerate(rows[:2]):
        out.append(f'<text x="34" y="{164 + 24 * i}" font-family="{SANS}" font-size="17" fill="{MUTED}">{esc(r)}</text>')
    out.append(f'<text x="{w - 40}" y="{h - 26}" font-family="{SANS}" font-size="14" fill="{CYAN}" text-anchor="end" letter-spacing="1">{esc(stats)}</text>')
    out.append("</svg>")
    return "\n".join(out)


BUTTONS = [("RESEARCH", "five CVE records", "research"), ("MATRIX", "host measurements", "matrix"),
           ("IMPACT", "playb0t.com ledger", "impact"), ("WRITING", "articles", "writing")]
CARDS = [
    ("NVIDIA NeMo", "Agent Toolkit #2497", "Validate the token resource when no audience is configured; agreed first in issue #2484.", "+250 −10 · 9 files", "30 Oct 2026", "nvidia"),
    ("VS Code docs", "microsoft/vscode-docs #10542", "Documented how to set an OAuth client secret: it stays out of mcp.json, in VS Code's secret storage.", "+3 · 1 file", "29 Oct 2026", "vscode"),
    ("Supabase", "supabase/supabase #51646", "Moved the Devin MCP preset from an unpinned mcp-remote bridge to native HTTP configuration.", "+46 −38 · 4 files", "14 Oct 2026", "supabase"),
    ("Quarkus", "quarkusio/quarkus #57563", "The Dev UI's MCP panel generates a native Zed URL instead of an unpinned bridge.", "+1 −5 · 1 file", "21 Oct 2026", "quarkus"),
]


def main() -> None:
    for label, hint, uid in BUTTONS:
        (ASSETS / f"btn-{uid}.svg").write_text(button(label, hint, uid) + "\n", encoding="utf-8", newline="\n")
    for title, pr, line, stats, when, uid in CARDS:
        (ASSETS / f"card-{uid}.svg").write_text(card(title, pr, line, stats, when, uid) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(BUTTONS)} buttons, {len(CARDS)} cards")


if __name__ == "__main__":
    main()
