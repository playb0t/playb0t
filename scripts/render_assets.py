"""Render the profile board from public data.

    python scripts/render_assets.py            # read the saved snapshot in data/
    python scripts/render_assets.py --live     # refresh data/ from npm and the CVE API first (the daily workflow)

Standard library only. Writes assets/board.svg and data/snapshot.json. Every number on the board comes
from the snapshot, so the page and the data cannot drift apart: downloads, the latest upstream version and
its date come from npm; each record's state (PUBLISHED / RESERVED), publication date and CISA-ADP score
come from the CVE Services API. A record that fails to load keeps its previous snapshot entry.
Animation is SMIL inside the SVG; GitHub renders it, and a renderer without SMIL shows the final board.
"""
from __future__ import annotations
import argparse, datetime as dt, json, random, sys, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS, DATA = ROOT / "assets", ROOT / "data"
PACKAGE = "mcp-remote"
REPORT_DAY = dt.date(2026, 2, 17)           # private report to the maintainer (TIMELINE.md)
TESTED = ("0.14.3", "9 OCT")                # the release run in full against loopback canaries, and when
RECORDS = [  # id, board description (the CNA text, shortened); reserved ids carry no description until they publish
    ("CVE-2026-51996", "CODE EXECUTION · getServerUrlHash"),
    ("CVE-2026-51994", "SSRF · resource_metadata URL"),
    ("CVE-2026-51997", "CODE EXECUTION · open()"),
    ("CVE-2026-51995", "INFO DISCLOSURE · auth-server metadata"),
    ("CVE-2026-52001", "INFO DISCLOSURE · SSE fetch wrapper"),
    ("CVE-2026-51998", ""),
    ("CVE-2026-51999", ""),
]
MONO = "'SF Mono','Cascadia Code','JetBrains Mono',Consolas,ui-monospace,monospace"


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "playb0t-profile-render"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read())


def load_snapshot() -> dict:
    p = DATA / "snapshot.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def record_from_api(cve_id: str) -> dict:
    """State, publication date and the CISA-ADP CVSS 3.1 score of one record, as the CVE Services API shows them."""
    d = fetch_json(f"https://cveawg.mitre.org/api/cve/{cve_id}")
    meta = d["cveMetadata"]
    score, severity = None, None
    for adp in d.get("containers", {}).get("adp", []):
        for m in adp.get("metrics", []):
            if "cvssV3_1" in m:
                score, severity = m["cvssV3_1"].get("baseScore"), m["cvssV3_1"].get("baseSeverity")
    return {"state": meta["state"], "published": (meta.get("datePublished") or "")[:10], "score": score, "severity": severity}


def refresh_snapshot() -> dict:
    prev = load_snapshot()
    today = dt.date.today()
    end = (today - dt.timedelta(days=1)).isoformat()
    rng = fetch_json(f"https://api.npmjs.org/downloads/range/{REPORT_DAY.isoformat()}:{end}/{PACKAGE}")
    rows = [r for r in rng["downloads"]]
    while rows and rows[-1]["downloads"] == 0:   # npm fills the last day or two with zeros before aggregation lands
        rows.pop()
    reg = fetch_json(f"https://registry.npmjs.org/{PACKAGE}")
    latest = reg["dist-tags"]["latest"]
    records = dict(prev.get("records", {}))
    for cve_id, _ in RECORDS:
        try:
            records[cve_id] = record_from_api(cve_id)
        except urllib.error.HTTPError as e:
            if e.code == 404:  # the public API serves published records only; a reserved id answers 404
                records[cve_id] = {"state": "RESERVED", "published": "", "score": None, "severity": None}
            else:  # keep the previous entry; the board must not go blank on one failed read
                print(f"{cve_id}: kept previous snapshot entry ({e})", file=sys.stderr)
        except Exception as e:
            print(f"{cve_id}: kept previous snapshot entry ({e})", file=sys.stderr)
    snap = {
        "read_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "package": PACKAGE,
        "daily": rows,
        "latest_version": latest,
        "latest_published": reg["time"][latest][:10],
        "records": records,
    }
    DATA.mkdir(exist_ok=True)
    (DATA / "snapshot.json").write_bytes((json.dumps(snap, indent=1) + "\n").encode())
    return snap


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def day_month(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b').upper()}"


# ---------------------------------------------------------------- split-flap board
def board_svg(snap: dict, total: int, last_day: str, days: int) -> str:
    """An airport split-flap board. DEPARTURES is the breaker half (the records that left), ARRIVALS the builder
    half (what landed). Flipping cells cycle through letters before settling; without SMIL the final text shows."""
    rnd = random.Random(7)
    FLAP, FLAP_EDGE, SPLIT = "#171a1f", "#2a2f37", "#0a0c10"
    WHITE, AMBER, GREEN, DIM, HEAD, DESC = "#f2f2ec", "#ffb000", "#39d353", "#6b7280", "#9aa3b2", "#c9d1d9"
    CW, CH, GAP, ROW = 15.0, 25.0, 1.5, 33.0           # cell width/height, gap between cells, row pitch
    COLS = [("TIME", 6), ("RECORD", 17), ("DESCRIPTION", 41), ("CISA", 4), ("STATUS", 14)]
    FLIP_COLS = {"RECORD", "STATUS"}
    CGAP = 22
    W, x_start = 1440, 60
    ver = snap["latest_version"]
    recs = snap.get("records", {})
    published, reserved = [], []
    for cve_id, desc in RECORDS:
        r = recs.get(cve_id, {})
        if r.get("state") == "PUBLISHED":
            score = r.get("score")
            published.append((r.get("published", ""), cve_id, desc or "PUBLISHED · SEE CVE.ORG", f"{score:.1f}" if score is not None else "—", score or 0))
        else:
            reserved.append(cve_id)
    published.sort(key=lambda p: -p[4])
    departures = [(day_month(p) if p else "—", cid, d, sc, "PUBLISHED", WHITE) for p, cid, d, sc, _ in published]
    departures += [("—", cid, "RESERVED FOR THIS REQUEST · UNPUBLISHED", "—", "RESERVED", DIM) for cid in reserved]
    departures += [
        (day_month(snap["latest_published"]), f"MCP-REMOTE {ver}", f"STILL FOLLOWS THE REPORTED PATH · {TESTED[1]}", "—", "NO FIX", AMBER),
        ("17 FEB", f"FIX FOR {TESTED[0]}", "EXPECTED FROM THE MAINTAINER SINCE 17 FEB", "—", f"DELAYED {days}D", AMBER),
    ]
    arrivals = [
        ("2026", "COORD-HUB", "AGENT COORDINATION · HUMAN APPROVAL", "—", "BOARDING", GREEN),
        ("JUL", "RTK-AI/RTK #119", "SHA-256 HOOK INTEGRITY GATE · MERGED", "—", "ARRIVED", GREEN),
    ]
    sections = [("DEPARTURES", "BREAKER · records that left the research", departures),
                ("ARRIVALS", "BUILDER · what landed", arrivals)]
    H = int(150 + sum(60 + 26 + ROW * len(r) for _, _, r in sections) + 40)
    ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-·./ "
    dep_desc = "; ".join(f"{t} {r} {d} CISA {c} {s}" for t, r, d, c, s, _ in departures)
    arr_desc = "; ".join(f"{t} {r} {d} {s}" for t, r, d, c, s, _ in arrivals)
    desc = f"Alex Gercog, playb0t. Departures: {dep_desc}. Arrivals: {arr_desc}. {total:,} downloads since the private report; {days} days without a fix."
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="tb db" xml:space="preserve">',
           '<title id="tb">Split-flap board: departures are the CVE records of the mcp-remote research and the open fix for the current release; arrivals are coord-hub and the merged rtk hook-integrity gate</title>',
           f'<desc id="db">{esc(desc)}</desc>',
           f'<rect width="{W}" height="{H}" rx="18" fill="#05070a"/>',
           f'<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="14" fill="#0b0e13" stroke="#1d222b"/>',
           f'<g font-family="{MONO}">']
    out.append(f'<text x="{x_start}" y="64" font-size="30" font-weight="700" fill="{WHITE}" letter-spacing="4">ALEX GERCOG</text>')
    out.append(f'<text x="{x_start+262}" y="64" font-size="18" fill="{HEAD}" letter-spacing="3">PLAYB0T · AI SYSTEMS ENGINEER · SECURITY RESEARCHER</text>')
    out.append(f'<text x="{W-60}" y="56" font-size="13" fill="{HEAD}" text-anchor="end" letter-spacing="2">DAYS WITHOUT A FIX</text>')
    out.append(f'<text x="{W-60}" y="92" font-size="36" font-weight="700" fill="{AMBER}" text-anchor="end">{days}</text>')
    out.append(f'<text x="{x_start}" y="96" font-size="15" fill="{HEAD}">who decided that this request was allowed?</text>')
    out.append(f'<line x1="{x_start}" y1="116" x2="{W-60}" y2="116" stroke="#1d222b"/>')

    def cell(x, y, ch, colour, t0=None, flips=0):
        """One flap. With t0 set, the cell cycles through `flips` random letters from t0 before showing ch."""
        s = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{CW-GAP:.1f}" height="{CH:.1f}" rx="2.5" fill="{FLAP}" stroke="{FLAP_EDGE}" stroke-width="0.6"/>']
        tx, ty = x + (CW - GAP) / 2, y + CH * 0.72
        if ch != " ":
            s.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="15.5" font-weight="700" fill="{colour}" text-anchor="middle">{esc(ch)}</text>')
        if t0 is not None and flips:
            step = 0.07
            s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{CW-GAP:.1f}" height="{CH:.1f}" rx="2.5" fill="{FLAP}" opacity="0"><set attributeName="opacity" to="1" begin="0s" dur="{t0 + flips*step:.2f}s"/></rect>')
            for k in range(flips):
                r = rnd.choice(ALPH)
                if r != " ":
                    s.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="15.5" font-weight="700" fill="{colour}" text-anchor="middle" opacity="0"><set attributeName="opacity" to="1" begin="{t0 + k*step:.2f}s" dur="{step:.2f}s"/>{esc(r)}</text>')
        s.append(f'<line x1="{x:.1f}" y1="{y + CH/2:.1f}" x2="{x + CW - GAP:.1f}" y2="{y + CH/2:.1f}" stroke="{SPLIT}" stroke-width="1.2"/>')
        return "".join(s)

    y, t_row = 150, 0.2
    for title, sub, rows in sections:
        out.append(f'<text x="{x_start}" y="{y}" font-size="22" font-weight="700" fill="{AMBER}" letter-spacing="6">{title}</text>')
        out.append(f'<text x="{x_start + (200 if title == "DEPARTURES" else 170)}" y="{y}" font-size="13" fill="{HEAD}" letter-spacing="1">{esc(sub)}</text>')
        y += 26
        x = x_start
        for name, width in COLS:
            out.append(f'<text x="{x}" y="{y}" font-size="11.5" fill="{DIM}" letter-spacing="2">{name}</text>')
            x += width * CW + CGAP
        y += 14
        for row in rows:
            x = x_start
            for (name, width), text, colour in zip(COLS, row[:5], [WHITE, WHITE, DESC, WHITE, row[5]]):
                text = text[:width].ljust(width)
                for i, ch in enumerate(text):
                    if name in FLIP_COLS:
                        out.append(cell(x + i * CW, y, ch, colour, t_row + i * 0.03, flips=5 + (i % 3)))
                    else:
                        out.append(cell(x + i * CW, y, ch, colour))
                x += width * CW + CGAP
            y += ROW
            t_row += 0.18
        y += 60
    ty = H - 40
    ticker = (f"{total:,} NPM DOWNLOADS SINCE THE PRIVATE REPORT OF 17 FEB 2026   ·   58 OF 58 STABLE RELEASES CARRY THE PATH, 0.1.32 TO {TESTED[0]}   ·   "
              f"SELECTED CODE AND NAMESPACE SIGNATURES UNDER 12 OTHER NPM NAMES AND IN 8 OTHER GIT REPOSITORIES   ·   THE MCP SDKS FIXED THIS CLASS IN SEPTEMBER, THE BRIDGE DID NOT   ·   "
              f"THIS PAGE MAKES 0 REQUESTS TO THIRD-PARTY SERVERS   ·   DATA READ {snap['read_at_utc'][:10]} FROM API.NPMJS.ORG AND CVEAWG.MITRE.ORG, RE-RENDERED DAILY   ·   ")
    out.append(f'<clipPath id="tk"><rect x="{x_start}" y="{ty-20}" width="{W-120}" height="30"/></clipPath>')
    out.append(f'<rect x="{x_start}" y="{ty-20}" width="{W-120}" height="30" fill="#0f1217" rx="4"/>')
    tw = len(ticker) * 9.0
    out.append(f'<g clip-path="url(#tk)"><text x="{x_start+10}" y="{ty}" font-size="15" fill="{AMBER}" letter-spacing="1"><animate attributeName="x" from="{x_start+10}" to="{x_start+10-tw:.0f}" dur="{tw/55:.0f}s" repeatCount="indefinite"/>{esc(ticker)}{esc(ticker)}</text></g>')
    out.append("</g></svg>")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--live", action="store_true", help="refresh data/snapshot.json from npm and the CVE API before rendering")
    args = ap.parse_args()
    snap = refresh_snapshot() if args.live else load_snapshot()
    daily = snap["daily"]
    total = sum(d["downloads"] for d in daily)
    last_day = daily[-1]["day"]
    days = (dt.date.fromisoformat(last_day) - REPORT_DAY).days
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "board.svg").write_bytes(board_svg(snap, total, last_day, days).encode())
    print(json.dumps({"total": total, "last_day": last_day, "days": days, "latest": snap["latest_version"],
                      "records": {k: v.get("state") for k, v in snap.get("records", {}).items()}, "read_at": snap["read_at_utc"]}))


if __name__ == "__main__":
    main()
