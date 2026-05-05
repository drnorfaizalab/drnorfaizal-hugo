#!/usr/bin/env python3
"""
social_ledger.py — Professional network tracker in Notion

Commands:
  setup         Create Notion databases (first run only)
  add-contact   Add a new contact
  add-favour    Log a favour (given or received)
  view          List all contacts with balance and liquidity
  balance       Show who owes whom
  top           Top 10 most liquid contacts
  sync          Recompute all balances and liquidity scores
"""

import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

TOOLS_DIR = Path(__file__).parent
ROOT_DIR = TOOLS_DIR.parent
CONFIG_FILE = TOOLS_DIR / ".social_ledger_config.json"

FAVOUR_TYPES = ["Referral", "Advice", "Endorsement", "Cover", "Teaching", "Introduction", "Other"]

WEIGHT_MAP = {
    "1": "1 — Minor",
    "2": "2 — Small",
    "3": "3 — Moderate",
    "4": "4 — Significant",
    "5": "5 — Major",
}

# ─── ENV ─────────────────────────────────────────────────────────────────────

def load_env():
    env_path = ROOT_DIR / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

# ─── NOTION CLIENT ───────────────────────────────────────────────────────────

def get_notion():
    try:
        from notion_client import Client
    except ImportError:
        sys.exit("Missing: pip install notion-client")
    key = os.getenv("NOTION_API_KEY")
    if not key:
        sys.exit("❌ NOTION_API_KEY not set in .env")
    return Client(auth=key)

# ─── CONFIG ──────────────────────────────────────────────────────────────────

def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return {}

def save_config(cfg):
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

def require_config():
    cfg = load_config()
    if "contacts_db_id" not in cfg or "favours_db_id" not in cfg:
        sys.exit("❌ Run setup first: python social_ledger.py setup")
    return cfg

# ─── PROPERTY READERS ────────────────────────────────────────────────────────

def prop_text(prop):
    parts = prop.get("title") or prop.get("rich_text") or []
    return "".join(p["plain_text"] for p in parts)

def prop_select(prop):
    s = prop.get("select")
    return s["name"] if s else ""

def prop_number(prop):
    return prop.get("number") or 0

def prop_date(prop):
    d = prop.get("date")
    if d and d.get("start"):
        return date.fromisoformat(d["start"][:10])
    return None

def weight_int(weight_name):
    try:
        return int(weight_name.split(" ")[0])
    except (ValueError, AttributeError, IndexError):
        return 1

# ─── LIQUIDITY ───────────────────────────────────────────────────────────────

def compute_liquidity(last_date, count_90d, balance):
    """
    Decay: drops 3 pts/day since last contact (hits 0 at ~33 days).
    Activity bonus: +10 per interaction in last 90 days, capped at 30.
    Balance bonus: small boost if they owe you (positive balance).
    """
    if last_date is None:
        return 0
    days_ago = (date.today() - last_date).days
    decay = max(0, 100 - days_ago * 3)
    activity = min(30, count_90d * 10)
    balance_boost = min(10, max(0, balance * 2))
    return min(100, round(decay + activity + balance_boost))

def liquidity_bar(score):
    filled = score // 10
    return "█" * filled + "░" * (10 - filled)

def liquidity_label(score):
    if score >= 70:
        return "High"
    if score >= 40:
        return "Med"
    return "Low "

# ─── SETUP ───────────────────────────────────────────────────────────────────

def cmd_setup(notion):
    cfg = load_config()
    page_id = os.getenv("NOTION_LEDGER_PAGE_ID", "").strip()
    if not page_id:
        page_id = input("Notion parent page ID (from URL after notion.so/): ").strip()
    if not page_id:
        sys.exit("❌ Page ID required")

    if "contacts_db_id" not in cfg:
        db = notion.databases.create(
            parent={"type": "page_id", "page_id": page_id},
            title=[{"type": "text", "text": {"content": "Social Ledger — Contacts"}}],
            properties={
                "Name":             {"title": {}},
                "Contact":          {"rich_text": {}},
                "Subspecialty":     {"select": {"options": []}},
                "Hospital":         {"select": {"options": []}},
                "Balance":          {"number": {"format": "number"}},
                "Liquidity":        {"number": {"format": "number"}},
                "Last Interaction": {"date": {}},
                "Notes":            {"rich_text": {}},
            },
        )
        cfg["contacts_db_id"] = db["id"]
        print(f"✓ Contacts DB: {db['url']}")
    else:
        print("✓ Contacts DB already exists")

    if "favours_db_id" not in cfg:
        db = notion.databases.create(
            parent={"type": "page_id", "page_id": page_id},
            title=[{"type": "text", "text": {"content": "Social Ledger — Favours"}}],
            properties={
                "Description": {"title": {}},
                "Contact": {
                    "relation": {
                        "database_id": cfg["contacts_db_id"],
                        "single_property": {},
                    }
                },
                "Date":      {"date": {}},
                "Direction": {"select": {"options": [
                    {"name": "Gave",     "color": "green"},
                    {"name": "Received", "color": "blue"},
                ]}},
                "Type": {"select": {"options": [
                    {"name": "Referral",      "color": "purple"},
                    {"name": "Advice",        "color": "yellow"},
                    {"name": "Endorsement",   "color": "orange"},
                    {"name": "Cover",         "color": "red"},
                    {"name": "Teaching",      "color": "pink"},
                    {"name": "Introduction",  "color": "gray"},
                    {"name": "Other",         "color": "default"},
                ]}},
                "Weight": {"select": {"options": [
                    {"name": "1 — Minor",       "color": "gray"},
                    {"name": "2 — Small",       "color": "yellow"},
                    {"name": "3 — Moderate",    "color": "orange"},
                    {"name": "4 — Significant", "color": "red"},
                    {"name": "5 — Major",       "color": "purple"},
                ]}},
            },
        )
        cfg["favours_db_id"] = db["id"]
        print(f"✓ Favours DB: {db['url']}")
    else:
        print("✓ Favours DB already exists")

    save_config(cfg)
    print("\n✓ Setup complete.")
    print("  Add NOTION_LEDGER_PAGE_ID to .env to skip the prompt next time.")

# ─── ADD CONTACT ─────────────────────────────────────────────────────────────

def cmd_add_contact(notion):
    cfg = require_config()

    print("\n— Add Contact ─────────────────────────")
    name = input("Name: ").strip()
    if not name:
        sys.exit("❌ Name required")

    contact     = input("Contact (phone/email): ").strip()
    subspecialty = input("Subspecialty: ").strip()
    hospital    = input("Hospital: ").strip()
    notes       = input("Notes (optional): ").strip()

    props = {
        "Name":     {"title":     [{"text": {"content": name}}]},
        "Contact":  {"rich_text": [{"text": {"content": contact}}]},
        "Balance":  {"number": 0},
        "Liquidity": {"number": 0},
    }
    if subspecialty:
        props["Subspecialty"] = {"select": {"name": subspecialty}}
    if hospital:
        props["Hospital"] = {"select": {"name": hospital}}
    if notes:
        props["Notes"] = {"rich_text": [{"text": {"content": notes}}]}

    page = notion.pages.create(
        parent={"database_id": cfg["contacts_db_id"]},
        properties=props,
    )
    print(f"\n✓ Added: {name}")
    print(f"  {page['url']}")

# ─── SEARCH CONTACT ──────────────────────────────────────────────────────────

def search_contact(notion, cfg, query):
    res = notion.databases.query(
        database_id=cfg["contacts_db_id"],
        filter={"property": "Name", "title": {"contains": query}},
    )
    pages = res.get("results", [])
    if not pages:
        sys.exit(f"❌ No contact matching '{query}'")
    if len(pages) == 1:
        return pages[0]

    print(f"\nMultiple matches for '{query}':")
    for i, p in enumerate(pages, 1):
        name = prop_text(p["properties"]["Name"])
        sub  = prop_select(p["properties"].get("Subspecialty", {"select": None}))
        hosp = prop_select(p["properties"].get("Hospital", {"select": None}))
        print(f"  {i}. {name} — {sub}, {hosp}")
    idx = int(input("Select [1]: ").strip() or "1") - 1
    return pages[idx]

# ─── ADD FAVOUR ──────────────────────────────────────────────────────────────

def cmd_add_favour(notion):
    cfg = require_config()

    print("\n— Log Favour ──────────────────────────")
    query = input("Contact name: ").strip()
    contact = search_contact(notion, cfg, query)
    contact_id   = contact["id"]
    contact_name = prop_text(contact["properties"]["Name"])

    print(f"Contact: {contact_name}")
    d_raw = input("Direction — (G)ave / (R)eceived: ").strip().upper()
    direction = "Gave" if d_raw.startswith("G") else "Received"

    print(f"Type — {', '.join(FAVOUR_TYPES)}")
    t_raw = input("Type: ").strip().title()
    favour_type = t_raw if t_raw in FAVOUR_TYPES else "Other"

    w_raw = input("Weight [1–5, default 3]: ").strip()
    weight = WEIGHT_MAP.get(w_raw, "3 — Moderate")

    description = input("Description: ").strip()
    date_raw    = input(f"Date [{date.today()}]: ").strip()
    favour_date = date_raw if date_raw else str(date.today())

    notion.pages.create(
        parent={"database_id": cfg["favours_db_id"]},
        properties={
            "Description": {"title": [{"text": {"content": description or f"{direction}: {favour_type}"}}]},
            "Contact":     {"relation": [{"id": contact_id}]},
            "Date":        {"date": {"start": favour_date}},
            "Direction":   {"select": {"name": direction}},
            "Type":        {"select": {"name": favour_type}},
            "Weight":      {"select": {"name": weight}},
        },
    )

    _update_metrics(notion, cfg, contact_id)
    print(f"\n✓ Logged [{direction}] {favour_type} — {contact_name}")

# ─── METRICS ─────────────────────────────────────────────────────────────────

def _update_metrics(notion, cfg, contact_id):
    res = notion.databases.query(
        database_id=cfg["favours_db_id"],
        filter={"property": "Contact", "relation": {"contains": contact_id}},
    )
    favours = res.get("results", [])

    balance   = 0
    last_date = None
    count_90d = 0
    cutoff    = date.today() - timedelta(days=90)

    for f in favours:
        fp        = f["properties"]
        direction = prop_select(fp.get("Direction", {"select": None}))
        w         = weight_int(prop_select(fp.get("Weight", {"select": None})))
        fdate     = prop_date(fp.get("Date", {"date": None}))

        balance += w if direction == "Gave" else -w

        if fdate:
            if last_date is None or fdate > last_date:
                last_date = fdate
            if fdate >= cutoff:
                count_90d += 1

    liquidity = compute_liquidity(last_date, count_90d, balance)

    update = {
        "Balance":  {"number": balance},
        "Liquidity": {"number": liquidity},
    }
    if last_date:
        update["Last Interaction"] = {"date": {"start": str(last_date)}}

    notion.pages.update(page_id=contact_id, properties=update)

# ─── VIEW ────────────────────────────────────────────────────────────────────

def cmd_view(notion, sort_by="liquidity"):
    cfg = require_config()
    pages = _all_contacts(notion, cfg)

    rows = []
    for p in pages:
        pp = p["properties"]
        rows.append({
            "name":        prop_text(pp.get("Name", {"title": []})),
            "subspecialty": prop_select(pp.get("Subspecialty", {"select": None})),
            "hospital":    prop_select(pp.get("Hospital", {"select": None})),
            "contact":     prop_text(pp.get("Contact", {"rich_text": []})),
            "balance":     prop_number(pp.get("Balance", {"number": 0})),
            "liquidity":   prop_number(pp.get("Liquidity", {"number": 0})),
        })

    key_fn = {
        "liquidity": lambda r: -r["liquidity"],
        "balance":   lambda r: -r["balance"],
        "name":      lambda r: r["name"].lower(),
    }
    rows.sort(key=key_fn.get(sort_by, key_fn["liquidity"]))

    W = 80
    print(f"\n{'─' * W}")
    print(f"{'SOCIAL LEDGER':^{W}}")
    print(f"{'─' * W}")
    print(f"{'Name':<24} {'Subspecialty':<18} {'Hospital':<14} {'Bal':>4} {'Liq':>4}  {'':10} Status")
    print(f"{'─' * W}")
    for r in rows:
        bal_str = f"+{r['balance']}" if r['balance'] > 0 else str(r['balance'])
        bar = liquidity_bar(r['liquidity'])
        print(
            f"{r['name']:<24} {r['subspecialty']:<18} {r['hospital']:<14}"
            f" {bal_str:>4} {r['liquidity']:>4}  {bar} {liquidity_label(r['liquidity'])}"
        )
    print(f"{'─' * W}")
    print(f"{len(rows)} contacts\n")

# ─── BALANCE ─────────────────────────────────────────────────────────────────

def cmd_balance(notion):
    cfg = require_config()
    pages = _all_contacts(notion, cfg)

    owe_you, you_owe, even = [], [], []
    for p in pages:
        pp      = p["properties"]
        name    = prop_text(pp.get("Name", {"title": []}))
        balance = prop_number(pp.get("Balance", {"number": 0}))
        if balance > 0:
            owe_you.append((name, balance))
        elif balance < 0:
            you_owe.append((name, balance))
        else:
            even.append(name)

    owe_you.sort(key=lambda x: -x[1])
    you_owe.sort(key=lambda x: x[1])

    print("\n── They owe you ───────────────────────")
    for name, b in owe_you:
        print(f"  {name:<30} +{b}")
    if not owe_you:
        print("  (none)")

    print("\n── You owe them ───────────────────────")
    for name, b in you_owe:
        print(f"  {name:<30}  {b}")
    if not you_owe:
        print("  (none)")

    print(f"\n── Even ({len(even)}) {'─' * 30}")
    if even:
        print("  " + ", ".join(even))
    print()

# ─── TOP ─────────────────────────────────────────────────────────────────────

def cmd_top(notion, n=10):
    cfg = require_config()
    pages = _all_contacts(notion, cfg)

    rows = []
    for p in pages:
        pp = p["properties"]
        rows.append({
            "name":      prop_text(pp.get("Name", {"title": []})),
            "sub":       prop_select(pp.get("Subspecialty", {"select": None})),
            "liquidity": prop_number(pp.get("Liquidity", {"number": 0})),
        })

    rows.sort(key=lambda r: -r["liquidity"])

    print(f"\nTop {n} — Most Liquid Contacts")
    print("─" * 55)
    for i, r in enumerate(rows[:n], 1):
        bar = liquidity_bar(r["liquidity"])
        print(f"  {i:>2}. {r['name']:<28} {bar} {r['liquidity']:>3}")
    print()

# ─── SYNC ────────────────────────────────────────────────────────────────────

def cmd_sync(notion):
    cfg = require_config()
    pages = _all_contacts(notion, cfg)
    print(f"Syncing {len(pages)} contacts...")
    for p in pages:
        name = prop_text(p["properties"].get("Name", {"title": []}))
        _update_metrics(notion, cfg, p["id"])
        print(f"  ✓ {name}")
    print("Done.\n")

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def _all_contacts(notion, cfg):
    results, cursor = [], None
    while True:
        kwargs = {"database_id": cfg["contacts_db_id"]}
        if cursor:
            kwargs["start_cursor"] = cursor
        res = notion.databases.query(**kwargs)
        results.extend(res.get("results", []))
        if not res.get("has_more"):
            break
        cursor = res.get("next_cursor")
    return results

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    load_env()

    parser = argparse.ArgumentParser(description="Social Ledger — Professional network tracker")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("setup",       help="Create Notion databases (first run)")
    sub.add_parser("add-contact", help="Add a new contact")
    sub.add_parser("add-favour",  help="Log a favour")
    sub.add_parser("balance",     help="Show who owes whom")
    sub.add_parser("top",         help="Top 10 most liquid contacts")
    sub.add_parser("sync",        help="Recompute all balances and liquidity scores")

    view_p = sub.add_parser("view", help="List all contacts")
    view_p.add_argument("--sort", choices=["liquidity", "balance", "name"], default="liquidity")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return

    notion = get_notion()

    if   args.cmd == "setup":       cmd_setup(notion)
    elif args.cmd == "add-contact": cmd_add_contact(notion)
    elif args.cmd == "add-favour":  cmd_add_favour(notion)
    elif args.cmd == "view":        cmd_view(notion, sort_by=args.sort)
    elif args.cmd == "balance":     cmd_balance(notion)
    elif args.cmd == "top":         cmd_top(notion)
    elif args.cmd == "sync":        cmd_sync(notion)


if __name__ == "__main__":
    main()
