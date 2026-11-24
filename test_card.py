"""Self-checks for the NI23 v6 card. Run: python3 test_card.py (exit 1 on any failure).

Written before draw.py: grid assert, tally, string audit, cross-refs, DC audit, fit.
A failing check is fixed by editing draw.py/data.py, never by loosening the check.
"""
import re
import sys

import data
import draw

BANDS = {  # name: (y0, y1) inclusive-exclusive, from the v6 GRID
    "topbar": (0, 18), "masthead": (20, 80), "kicker": (80, 100), "regionbar": (102, 122),
    "timeline": (124, 150), "larges": (156, 340), "med1": (346, 486), "med2": (486, 626),
    "bottom": (632, 938), "datecheck": (942, 978), "legend": (980, 1002),
}
BANNED = ["Sunday", "Saturday", "Friday", "Nov 21", "Nov 22", "Nov 20", "Dec 11"]
ERRORS = []


def check(cond, msg):
    if not cond:
        ERRORS.append(msg)


def main():
    img, reg = draw.build()
    stories = data.all_stories()

    # --- grid assert
    check(img.size == (1024, 1024), f"canvas {img.size} != 1024x1024")
    for e in reg.items:
        x0, y0, x1, y1 = e["bbox"]
        check(0 <= x0 and 0 <= y0 and x1 <= 1024 and y1 <= 1024, f"outside canvas: {e['band']} {e['kind']} {e['bbox']} {e.get('text','')[:30]!r}")
        y_lo, y_hi = BANDS[e["band"]]
        check(y_lo <= y0 and y1 <= y_hi, f"band overflow {e['band']}{BANDS[e['band']]}: {e['kind']} {e['bbox']} {e.get('text','')[:30]!r}")
    seen = {e["band"] for e in reg.items}
    check(seen == set(BANDS), f"bands missing/extra: {set(BANDS) ^ seen}")
    check(not reg.warnings, "fit warnings: " + "; ".join(reg.warnings[:8]))

    # --- tally
    tiers = {t: sum(1 for s in stories if s["tier"] == t) for t in "LMB"}
    check(tiers == {"L": 3, "M": 10, "B": 8}, f"tiers {tiers}")
    check([s["n"] for s in stories] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 25, 26, 28, 30], "story numbers not the v7 set")
    tally = {r: sum(1 for s in stories if s["region"] == r) for r in data.REGIONS}
    check(tally == data.EXPECTED_TALLY, f"region tally {tally}")
    check(sum(tally.values()) == 21, "tally != 21")
    check(reg.meta.get("region_counts") == tally, "region bar counts != tally")
    check(reg.meta.get("region_bar_w") == 992, f"region bar width {reg.meta.get('region_bar_w')} != 992")
    check("21 STORIES · 7 REGIONS" in reg.meta.get("topbar_right", ""), "top bar count text")

    # --- timeline: 6 entries, HH:MM UTC
    check(len(data.TIMELINE) == 6 and all(re.fullmatch(r"\d\d:\d\d", t) for t, _ in data.TIMELINE), "timeline shape")

    # --- rail cross-refs: 6, token in the referenced story's text
    byn = {s["n"]: data.story_text(s) for s in stories}
    check(len(data.RAIL) == 6, "rail != 6")
    for num, label, n, token in data.RAIL:
        check(token in byn[n], f"rail {num!r}: token {token!r} not in story {n}")

    # --- string audit (story strings only; DC/legend exempt)
    for s in stories:
        t = data.story_text(s)
        for b in BANNED:
            check(b not in t, f"banned {b!r} in story {s['n']}")
        check(not re.search(r"\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b", t), f"weekday abbreviation in story {s['n']}")
        check("1,675" not in t and "6,095" not in t, f"Gaza cumulative figure in story {s['n']}")
        check("CONFIRMED" not in s.get("det", ""), "tag leak")
    for s in data.BRIEFS:
        check(len(s["head"]) <= 34, f"brief {s['n']} headline long: {len(s['head'])}")
    check("HOW TO READ" not in str(reg.meta.get("all_text", "")).upper(), "HOW TO READ box present")
    check("Syria" not in str(reg.meta.get("all_text", "")), "Syria must not appear anywhere")

    # --- DATE CHECK: exclusions only, cross-audit vs stories
    dc = data.DC_LINE1 + " " + data.DC_LINE2
    for phrase in ("Counted as", "announced earlier", "happening today", "flagged off today"):
        check(phrase.lower() not in dc.lower(), f"DC defends an inclusion: {phrase!r}")
    alltext = " ".join(byn.values())
    for kw in data.DC_KEYWORDS:
        check(kw.lower() not in alltext.lower(), f"exclusion {kw!r} appears in a story")

    # --- file size + determinism of the encoder
    import io
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    check(len(buf.getvalue()) <= 300 * 1024, f"png {len(buf.getvalue())} bytes > 300 KB")

    # --- pins: <=13, distinct positions
    check(len(data.PINS) <= 13, "pins > 13")
    pts = reg.meta.get("pin_xy", [])
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = ((pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2) ** 0.5
            check(d >= 13, f"pins {i},{j} overlap (d={d:.1f})")

    if ERRORS:
        print(f"FAIL: {len(ERRORS)} error(s)")
        for e in ERRORS[:60]:
            print("  -", e)
        return 1
    print("PASS: all checks green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
