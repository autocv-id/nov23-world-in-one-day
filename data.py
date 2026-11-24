"""NI23 v6 content: every string on the page comes from here.

Facts trace to ~/workspace/makefun/ni23/facts-2026-11-23.md (sections 1, 7, 8)
and build-report-v2.md (the v2 refreshes: measles, German schools, Zambia,
Iran blockade, Bitcoin).
"""

MINUS = "−"
REGIONS = ["ASIA", "EUROPE", "AMERICAS", "MIDDLE EAST", "AFRICA", "OCEANIA", "GLOBAL"]
EXPECTED_TALLY = {"ASIA": 6, "EUROPE": 5, "AMERICAS": 5, "MIDDLE EAST": 2,
                  "AFRICA": 1, "OCEANIA": 1, "GLOBAL": 1}

# n, tier, region, headline, deck/detail, tag, source, scene number, unit
# Larges and mediums carry a scene number + unit; briefs carry a detail line.
LARGES = [
    dict(n=1, region="EUROPE", head="Belgium shuts skies",
         deck="Skeyes strike halts ATC: 429 flights, 59,500 passengers hit.",
         tag="OFFICIAL", src="Skeyes · AFP", num="429", unit="FLIGHTS"),
    dict(n=2, region="AMERICAS", head="Huang back as CEO",
         deck="Reinstated as CEO; Trump welcomes it. Shares +31.48%, +$952B.",
         tag="CONFIRMED", src="Reuters · CNN", num="+31%", unit="SHARES"),
    dict(n=3, region="AMERICAS", head="Wall St jumps 4.7%",
         deck="S&P 500 +4.73%, Nasdaq +6.51%: best day since April 2025.",
         tag="CONFIRMED", src="Reuters · CNN · AP", num="+4.73%", unit="S&P 500"),
]

MEDIUMS = [
    dict(n=4, region="ASIA", head="Asia's AI rout deepens",
         deck=f"KOSPI {MINUS}3.3% at 4,708.54; Taiwan {MINUS}17% in a week.",
         tag="REPORTED", src="Reuters", num=f"{MINUS}3.3%", unit="KOSPI CLOSE"),
    dict(n=5, region="AFRICA", head="UN demands Benghazi probe",
         deck="UNSMIL: Libya “must not become a battleground.”",
         tag="OFFICIAL", src="UNSMIL · Arab News", num="UN", unit="PROBE"),
    dict(n=6, region="OCEANIA", head="Bowen under fire over COP31",
         deck="Monday fallout: opposition wants the minister out.",
         tag="REPORTED", src="Reuters", num="1.5°C", unit="LIMIT"),
    dict(n=7, region="ASIA", head="India–Nepal train rolls",
         deck="Modi and Nepal's Shah flag off Saryu-Kamala Express, 604 km.",
         tag="OFFICIAL", src="IANS", num="604", unit="KM"),
    dict(n=8, region="MIDDLE EAST", head="Gaza strikes kill 3",
         deck="3 killed, 4 injured overnight in Deir al-Balah, Khan Younis.",
         tag="REPORTED", src="Anadolu", num="3", unit="KILLED"),
    dict(n=9, region="ASIA", head="Wellington Test drawn",
         deck="NZ 239/5 hold out vs India's 720/9 dec; Mitchell 49*.",
         tag="CONFIRMED", src="ESPNcricinfo", num="239/5", unit="DRAWN"),
    dict(n=10, region="EUROPE", head="Ukraine hits 3 oil sites",
         deck="Drones hit sites in Rostov, Perm and Tatarstan.",
         tag="REPORTED", src="Ukraine Monitor", num="3", unit="OIL SITES"),
    dict(n=11, region="ASIA", head="Fire toll hits 24",
         deck="24 dead, ~30 missing at Cikande candy factory.",
         tag="REPORTED", src="Reuters", num="24", unit="DEAD"),
    dict(n=12, region="ASIA", head="Seoul reshuffles security team",
         deck="Kang Kum-sil named first female spy chief; two more picks.",
         tag="REPORTED", src="Reuters", num="3", unit="NOMINEES"),
    dict(n=13, region="EUROPE", head="Europe stocks rebound",
         deck="STOXX 600 +1.87%, DAX +2.3%; five-day losing run ends.",
         tag="REPORTED", src="MT Newswires", num="+1.87%", unit="STOXX 600"),
]

BRIEFS = [
    # Cut for v7 (weakest by news weight, 17 -> 8): 16 PMI (duplicated in the UTC timeline), 19,
    # 20, 21, 22, 23, 24 (routine holiday), 27, 29. Kept: 14, 15, 17, 18, 25, 26, 28, 30.
    dict(n=14, region="AMERICAS", head="DOJ seeks $1B+ in crypto", det="Binance hack by N. Korea · Reuters"),
    dict(n=15, region="AMERICAS", head="CrowdStrike buys Zscaler", det="$44B cyber deal · Reuters"),
    dict(n=17, region="AMERICAS", head="Trump halts Iowa blast", det="Army paused by court · Reuters"),
    dict(n=18, region="EUROPE", head="Puigdemont free to return", det="Spain court shelves case · Reuters"),
    dict(n=25, region="ASIA", head="Measles: zero deaths", det="Toll stays 1,352 · DGHS"),
    dict(n=26, region="EUROPE", head="450 schools get threats", det="Bomb threats by email · Bild"),
    dict(n=28, region="MIDDLE EAST", head="Iran vows blockade fight", det="“All available tools” · Reuters"),
    dict(n=30, region="GLOBAL", head="Bitcoin at $61,846", det="Up 12% off low · Cointelegraph"),
]

KICKER = "Belgium shuts its skies · Nvidia reinstates Huang, shares +31% · Wall St jumps 4.7%"

# Timeline: (UTC time, label) — every entry from a named source.
TIMELINE = [
    ("00:00", f"KOSPI opens {MINUS}2.8%"),
    ("01:02", "UNSMIL probe call"),
    ("06:00", "Belgium ATC halted"),
    ("06:30", f"KOSPI closes {MINUS}3.3%"),
    ("14:45", "US flash PMI 54.6"),
    ("21:00", "Wall St closes +4.7%"),
]

# Rail: (number text, label, story n, token that must appear in that story's text)
RAIL = [
    ("429", "flights grounded · 1", 1, "429"),
    ("+31%", "Nvidia shares · 2", 2, "+31"),
    ("+4.73%", "S&P 500 gain · 3", 3, "+4.73%"),
    (f"{MINUS}3.3%", "KOSPI close · 4", 4, f"{MINUS}3.3%"),
    ("24", "dead in fire · 11", 11, "24"),
    ("+1.87%", "STOXX 600 · 13", 13, "+1.87%"),
]

DC_LINE1 = ("LEFT OUT — earlier day: Merkury sunk · 186-drone wave + Dymer · COP31 collapse itself · "
            "Trump meme-coin gala · MBS–Radev (all Sun)")
DC_LINE2 = ("Also left out: Trump's Iran remarks (Sun) · Lebanon explosives · Rajasthan crash · Lisbon march (all Sat) · "
            "NOT YET: FIDE Game 1 · Miss Universe (both Tue)")
DC_KEYWORDS = ["Merkury", "Dymer", "meme-coin", "Radev", "Lebanon", "Rajasthan", "Lisbon",
               "FIDE", "Miss Universe", "186-drone", "Iran remarks"]

LEGEND = ("CONFIRMED = 2+ outlets · OFFICIAL = on the record · REPORTED = one wire · CLAIM = one side's account · "
          "Scenes are drawn illustrations, not photographs.")

# Map pins: (label, lon, lat, city name for the key). Story 12 shares Seoul with 4.
# n, lon, lat, key name, (pin dx, dy offset in px; leader line drawn when non-zero)
PINS = [
    ("1", 4.35, 50.85, "Brussels", (-11, -9)),
    ("2", -121.96, 37.37, "Santa Clara", (0, 0)),
    ("3", -74.0, 40.7, "New York", (0, 0)),
    ("4", 127.0, 37.5, "Seoul", (-9, -5)),
    ("5", 20.07, 32.12, "Benghazi", (-6, 7)),
    ("6", 149.13, -35.28, "Canberra", (0, 0)),
    ("7", 82.2, 26.8, "Ayodhya", (0, 0)),
    ("8", 34.4, 31.5, "Gaza", (8, 7)),
    ("9", 174.78, -41.29, "Wellington", (-9, -2)),
    ("10", 56.2, 58.0, "Perm", (0, 0)),
    ("11", 106.3, -6.2, "Cikande", (0, 0)),
    ("12", 127.0, 37.5, "Seoul", (8, 6)),
    ("13", 8.7, 50.1, "Frankfurt", (6, 9)),
]


def all_stories():
    out = []
    for t, lst in (("L", LARGES), ("M", MEDIUMS), ("B", BRIEFS)):
        for s in lst:
            out.append(dict(s, tier=t))
    return sorted(out, key=lambda s: s["n"])


def story_text(s):
    parts = [s["head"], s.get("deck", ""), s.get("det", ""), s.get("num", ""), s.get("unit", ""), s.get("src", "")]
    return " ".join(p for p in parts if p)
