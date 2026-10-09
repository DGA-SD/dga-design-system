#!/usr/bin/env python3 -I
"""Export tokens.json (Anthropic Design System artifact format) to W3C DTCG files.

Usage: python3 -I export_dtcg.py <tokens.json> <out dir>

Writes <out>/base.tokens.json    spacing, radius, font families, typography composites
       <out>/light.tokens.json   color + shadow for the first theme
       <out>/<theme>.tokens.json one file per further theme (overrides only)

DTCG has no theme concept of its own; one file per theme is the usual layering
(Style Dictionary / Tokens Studio "sets"). Values are kept as plain strings
("16px", "#ffffff") rather than the newer object forms, for the widest tool support.
"""
import json
import os
import re
import sys

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
t = json.load(open(src, encoding="utf-8"))
themes = [x["id"] for x in t["color"]["themes"]]
first = themes[0]
ALIAS = re.compile(r"^\{([A-Za-z0-9][A-Za-z0-9_.-]{0,63})\}$")
SHADOW = re.compile(r"^(inset\s+)?(-?[\d.]+(?:px)?)\s+(-?[\d.]+(?:px)?)\s+(-?[\d.]+(?:px)?)(?:\s+(-?[\d.]+(?:px)?))?\s+(.+)$")


def px(v):
    return "0px" if v == "0" else (v if v.endswith("px") else f"{v}px")


def ref(name, group):
    m = ALIAS.match(name) if isinstance(name, str) else None
    return f"{{{group}.{m.group(1)}}}" if m else name


def val(tok, theme):
    v = tok["value"]
    return v if isinstance(v, str) else v.get(theme)


def tok_entry(typ, value, usage=None):
    e = {"$type": typ, "$value": value}
    if usage:
        e["$description"] = usage
    return e


def shadow_value(s):
    m = SHADOW.match(s.strip())
    if not m:
        return s
    inset, x, y, blur, spread, color = m.groups()
    d = {"color": color.strip(), "offsetX": px(x), "offsetY": px(y), "blur": px(blur), "spread": px(spread or "0")}
    if inset:
        d["inset"] = True
    return d


def dump(name, data):
    path = os.path.join(out, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("wrote", path)


# ---- per theme: color + shadow ----
for i, th in enumerate(themes):
    doc = {"$schema": "https://tr.designtokens.org/format/", "color": {}, "shadow": {}}
    for tok in t["color"]["tokens"]:
        v = val(tok, th)
        if v is None and i == 0:
            v = next((val(tok, o) for o in themes[1:] if val(tok, o)), None)
        if v is None:
            continue  # later theme inherits the first: no override entry
        doc["color"][tok["name"]] = tok_entry("color", ref(v, "color"), tok.get("usage") if i == 0 else None)
    for tok in t.get("shadow", {}).get("tokens", []):
        v = val(tok, th)
        if v is None:
            continue
        doc["shadow"][tok["name"]] = tok_entry("shadow", shadow_value(v), tok.get("usage") if i == 0 else None)
    dump(f"{th}.tokens.json", doc)

# ---- base: spacing, radius, other families, fonts, typography ----
base = {"$schema": "https://tr.designtokens.org/format/"}
for fam, data in t.items():
    if fam in ("name", "version", "color", "shadow", "type") or not isinstance(data, dict):
        continue
    base[fam] = {}
    for tok in data.get("tokens", []):
        v = tok["value"]
        v = f"{v}px" if isinstance(v, (int, float)) else v
        typ = "dimension" if re.match(r"^-?[\d.]+(px|rem|em|%)?$", str(v)) else None
        e = tok_entry(typ, v, tok.get("usage")) if typ else {"$value": v, "$description": tok.get("usage", "")}
        base[fam][tok["name"]] = e
ty = t.get("type", {})
base["fontFamily"] = {k: tok_entry("fontFamily", [s.strip().strip('"') for s in v.split(",")]) for k, v in ty.get("families", {}).items()}
base["typography"] = {}
for g in ty.get("groups", []):
    for s in g.get("styles", []):
        fam = s.get("family", g["family"])
        comp = {"fontFamily": f"{{fontFamily.{fam}}}"}
        if "fontSize" in s:
            comp["fontSize"] = f"{s['fontSize']}px" if isinstance(s["fontSize"], (int, float)) else s["fontSize"]
        if "fontWeight" in s:
            comp["fontWeight"] = s["fontWeight"]
        if "lineHeight" in s:
            comp["lineHeight"] = s["lineHeight"]
        if "letterSpacing" in s:
            comp["letterSpacing"] = s["letterSpacing"]
        e = tok_entry("typography", comp, s.get("usage"))
        e["$extensions"] = {"dga.group": g["name"]}
        base["typography"][s["name"]] = e
dump("base.tokens.json", base)
