#!/usr/bin/env python3 -I
"""Build the files a Design System artifact page would generate, for a local snapshot.

Usage: python3 -I build_local_view.py <snapshot dir>   (e.g. artifact/dga)

Reads  <dir>/project/tokens.json, design-system.json, components/*/preview.html, README.md
Writes <dir>/project/tokens.css            compiled per artifact-type/reference/format.md
       <dir>/project/manifest.json         v3 catalogue
       <dir>/project/api/tokens.md         token card per theme (for agents)
       <dir>/project/components/<C>/preview.local.html   preview + tokens.css + bundle.css linked
       <dir>/project/index.local.html      offline gallery (open with file://)
       <dir>/SHA256SUMS                    checksums of the snapshot files (not the generated ones)

Snapshot files are untrusted data: this script only reads them as JSON/text and
never executes anything from them.
"""
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.abspath(sys.argv[1])
# two layouts: an artifact snapshot (<dir>/project/...) writes *.local.html beside the
# originals; a repo checkout (<dir>/tokens.json directly) writes index.html and patches
# preview.html in place (idempotent).
SNAPSHOT = os.path.exists(os.path.join(ROOT, "project", "tokens.json"))
P = os.path.join(ROOT, "project") if SNAPSHOT else ROOT
PREFIX = "project/" if SNAPSHOT else ""
PREVIEW_OUT = "preview.local.html" if SNAPSHOT else "preview.html"
INDEX_OUT = "index.local.html" if SNAPSHOT else "index.html"
GENERATED = {PREFIX + "tokens.css", PREFIX + "manifest.json", PREFIX + "api/tokens.md",
             PREFIX + INDEX_OUT, "SHA256SUMS", "SOURCE.md"}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", rel, f"({len(text.encode())} bytes)")


tokens = json.loads(read(os.path.join(P, "tokens.json")))
index = json.loads(read(os.path.join(P, "design-system.json")))

themes = [t["id"] for t in tokens["color"]["themes"]]
first = themes[0]
ALIAS = re.compile(r"^\{([A-Za-z0-9][A-Za-z0-9_.-]{0,63})\}$")


def css_name(name):
    return "--" + name.replace(".", "\\.")


def css_value(v):
    m = ALIAS.match(v) if isinstance(v, str) else None
    return f"var({css_name(m.group(1))})" if m else v


def theme_value(tok, theme):
    v = tok["value"]
    if isinstance(v, str):
        return v if theme == first else None
    return v.get(theme)


# ---------- tokens.css ----------
lines = [f"/* tokens.css compiled locally from tokens.json ({tokens.get('name')} v{tokens.get('version')}) */"]
per_theme = ("color", "shadow")

# first theme: every color/shadow token
lines.append(f':root, [data-theme="{first}"] {{')
for fam in per_theme:
    for t in tokens.get(fam, {}).get("tokens", []):
        v = theme_value(t, first)
        if v is None:  # borrow a later theme's value
            v = next((theme_value(t, th) for th in themes[1:] if theme_value(t, th)), None)
        if v is not None:
            lines.append(f"  {css_name(t['name'])}: {css_value(v)};")
lines.append("}")

# further themes: overrides (aliases re-declared)
for th in themes[1:]:
    lines.append(f'[data-theme="{th}"] {{')
    for fam in per_theme:
        for t in tokens.get(fam, {}).get("tokens", []):
            v = theme_value(t, th)
            if v is not None:
                lines.append(f"  {css_name(t['name'])}: {css_value(v)};")
    lines.append("}")

# theme-independent: spacing, radius, other families, font families
lines.append(":root {")
for fam, data in tokens.items():
    if fam in ("name", "version", "color", "shadow", "type") or not isinstance(data, dict):
        continue
    for t in data.get("tokens", []):
        v = t["value"]
        if isinstance(v, (int, float)):
            v = f"{v}px"
        lines.append(f"  {css_name(t['name'])}: {v};")
for key, stack in tokens.get("type", {}).get("families", {}).items():
    lines.append(f"  --font-{key}: {stack};")
lines.append("}")

# @font-face for local font files
for f in tokens.get("type", {}).get("fonts", []):
    file = f["file"] if "/" in f["file"] else f"fonts/{f['file']}"
    lines.append("@font-face {")
    lines.append(f"  font-family: \"{f['family']}\";")
    lines.append(f"  src: url(\"{file}\");")
    if f.get("weight"):
        lines.append(f"  font-weight: {f['weight']};")
    if f.get("style"):
        lines.append(f"  font-style: {f['style']};")
    lines.append("}")

# a class per type style
for g in tokens.get("type", {}).get("groups", []):
    for s in g.get("styles", []):
        fam = s.get("family", g.get("family"))
        decl = [f"font-family: var(--font-{fam})"]
        for k, prop in (("fontSize", "font-size"), ("lineHeight", "line-height"),
                        ("fontWeight", "font-weight"), ("letterSpacing", "letter-spacing"),
                        ("fontStyle", "font-style")):
            if k in s:
                v = s[k]
                if isinstance(v, (int, float)) and k in ("fontSize", "letterSpacing"):
                    v = f"{v}px"
                decl.append(f"{prop}: {v}")
        lines.append(f".{s['name']} {{ " + "; ".join(decl) + "; }")

write(PREFIX + "tokens.css", "\n".join(lines) + "\n")

# ---------- components ----------
MARK = re.compile(r"^<!--\s*@dsCard([^>]*)-->")
comps = []
cdir = os.path.join(P, "components")
for name in sorted(os.listdir(cdir)):
    folder = os.path.join(cdir, name)
    if not os.path.isdir(folder):
        continue
    preview = os.path.join(folder, "preview.html")
    readme = os.path.join(folder, "README.md")
    if not (os.path.exists(preview) or os.path.exists(readme)):
        continue
    entry = {"name": name}
    attrs = {}
    if os.path.exists(preview):
        html = read(preview)
        m = MARK.match(html)
        if m:
            for k, v in re.findall(r'(\w+)=("[^"]*"|\S+)', m.group(1)):
                attrs[k] = v.strip('"')
        if "group" in attrs:
            entry["group"] = attrs["group"]
        # patch: tokens.css + bundle.css, blob -> local asset, theme from ?theme=
        blobs = {}
        for g in index.get("assetGroups", {}).values():
            for fname, rec in g.get("files", {}).items():
                blobs[rec["blob"]] = f"../../assets/{g['name']}/{rec['name']}"
        local = html
        for bid, rel in blobs.items():
            local = local.replace(f"/_blob/{bid}", rel)
        inject = ('<link rel="stylesheet" href="../../tokens.css">'
                  '<link rel="stylesheet" href="../bundle.css">'
                  '<script>document.documentElement.dataset.theme='
                  f'new URLSearchParams(location.search).get("theme")||"{first}";</script>')
        if 'href="../../tokens.css"' in local:
            pass  # already patched (repo layout, re-run)
        elif "<head>" in local:
            local = local.replace("<head>", "<head>" + inject, 1)
        else:
            local = re.sub(r"(<html[^>]*>)", r"\1<head>" + inject + "</head>", local, count=1)
        with open(os.path.join(folder, PREVIEW_OUT), "w", encoding="utf-8") as f:
            f.write(local)
    if os.path.exists(readme):
        text = re.sub(r"^#\s.*\n+", "", read(readme).strip())
        entry["summary"] = re.split(r"(?<=[.!?])\s", text, 1)[0][:280]
    entry["_height"] = int(attrs.get("height", 120))
    entry["_width"] = int(attrs["width"]) if "width" in attrs else None
    comps.append(entry)

manifest = {
    "manifestVersion": 3,
    "name": index.get("title", tokens.get("name")),
    "namespace": index.get("namespace", ""),
    "libraries": index.get("libraries", []),
    "components": [{k: v for k, v in c.items() if not k.startswith("_")} for c in comps],
    "lastChange": index.get("lastChange"),
    "assetGroups": [
        {"name": g["name"], "tile": g.get("tile"), "order": g.get("order", []),
         "files": [{"path": f"assets/{g['name']}/{r['name']}", "id": r["blob"]} for r in g.get("files", {}).values()]}
        for g in index.get("assetGroups", {}).values()],
    "_generatedBy": "build_local_view.py (local snapshot, not the page)",
}
write(PREFIX + "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

# ---------- api/tokens.md ----------
md = [f"# Tokens: {tokens.get('name')}", "", f"Themes: {', '.join(themes)} (first = {first})", ""]
for fam in ("color", "shadow"):
    toks = tokens.get(fam, {}).get("tokens", [])
    if not toks:
        continue
    md += [f"## {fam}", "", "| token | " + " | ".join(themes) + " | usage |", "|---|" + "---|" * len(themes) + "---|"]
    for t in toks:
        vals = [theme_value(t, th) or "(inherits)" for th in themes]
        md.append(f"| `{t['name']}` | " + " | ".join(f"`{v}`" for v in vals) + f" | {t.get('usage', '')} |")
    md.append("")
for fam, data in tokens.items():
    if fam in ("name", "version", "color", "shadow", "type") or not isinstance(data, dict):
        continue
    md += [f"## {fam}", "", "| token | value | usage |", "|---|---|---|"]
    for t in data.get("tokens", []):
        md.append(f"| `{t['name']}` | `{t['value']}` | {t.get('usage', '')} |")
    md.append("")
ty = tokens.get("type", {})
md += ["## type", ""]
for k, v in ty.get("families", {}).items():
    md.append(f"- `--font-{k}`: `{v}`")
md.append("")
for g in ty.get("groups", []):
    md += [f"### {g['name']} (family `{g['family']}`)", "", "| style | size | line | weight | usage |", "|---|---|---|---|---|"]
    for s in g.get("styles", []):
        md.append(f"| `.{s['name']}` | {s.get('fontSize', '')} | {s.get('lineHeight', '')} | {s.get('fontWeight', '')} | {s.get('usage', '')} |")
    md.append("")
write(PREFIX + "api/tokens.md", "\n".join(md))

# ---------- gallery ----------
readme_text = read(os.path.join(P, "README.md")) if os.path.exists(os.path.join(P, "README.md")) else ""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def swatches():
    out = []
    for t in tokens["color"]["tokens"]:
        v = theme_value(t, first)
        cells = "".join(f'<div class="sw" style="background:{css_value(theme_value(t, th) or v)}" title="{th}"></div>' for th in themes)
        out.append(f'<div class="tok"><div class="sws">{cells}</div><div><code>{esc(t["name"])}</code>'
                   f'<small>{" / ".join(esc(str(theme_value(t, th) or "")) for th in themes)}</small>'
                   f'<p>{esc(t.get("usage", ""))}</p></div></div>')
    return "\n".join(out)


def simple(fam):
    return "\n".join(
        f'<div class="tok"><div class="demo demo-{fam}" style="--v:{t["value"] if isinstance(t["value"], str) else theme_value(t, first)}"></div>'
        f'<div><code>{esc(t["name"])}</code><small>{esc(str(t["value"]))}</small><p>{esc(t.get("usage", ""))}</p></div></div>'
        for t in tokens.get(fam, {}).get("tokens", []))


def typo():
    out = []
    for g in ty.get("groups", []):
        out.append(f"<h3>{esc(g['name'])} <small>family {esc(g['family'])}</small></h3>")
        for s in g.get("styles", []):
            sample = s.get("sample") or "สำนักงานพัฒนารัฐบาลดิจิทัล Digital Government"
            out.append(f'<div class="ty"><div class="{s["name"]}">{esc(sample)}</div>'
                       f'<small><code>.{esc(s["name"])}</code> {s.get("fontSize", "")}/{s.get("lineHeight", "")} {s.get("fontWeight", "")} {esc(s.get("usage", ""))}</small></div>')
    return "\n".join(out)


def cards():
    out = []
    groups = {}
    for c in comps:
        groups.setdefault(c.get("group", "Cover" if c["name"] == "Cover" else "Other"), []).append(c)
    for gname, items in groups.items():
        out.append(f"<h3>{esc(gname)}</h3>")
        for c in items:
            w = f' style="width:{c["_width"]}px;max-width:100%"' if c["_width"] else ""
            out.append(f'<div class="card"><div class="card-h"><b>{esc(c["name"])}</b> <span>{esc(c.get("summary", ""))}</span></div>'
                       f'<iframe data-src="components/{c["name"]}/{PREVIEW_OUT}" height="{c["_height"]}"{w} loading="lazy"></iframe></div>')
    return "\n".join(out)


gallery = f"""<!doctype html>
<html lang="th" data-theme="{first}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(index.get('title', 'Design System'))} Design System{" (local snapshot)" if SNAPSHOT else ""}</title>
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components/bundle.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>
<style>
body{{margin:0;font-family:var(--font-sans,system-ui);background:var(--surface);color:var(--ink);line-height:1.5}}
header{{position:sticky;top:0;z-index:2;display:flex;gap:16px;align-items:center;padding:12px 24px;background:var(--navy);color:var(--on-navy)}}
header a{{color:var(--on-navy);text-decoration:none;opacity:.85}} header a:hover{{opacity:1}}
header button{{margin-left:auto;padding:6px 12px;border-radius:var(--radius-sm,6px);border:1px solid var(--on-navy);background:transparent;color:var(--on-navy);cursor:pointer}}
main{{max-width:1200px;margin:0 auto;padding:24px}} section{{margin-bottom:48px}} h2{{border-bottom:1px solid var(--line);padding-bottom:8px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.tok{{display:flex;gap:12px;align-items:flex-start;padding:12px;border:1px solid var(--line);border-radius:var(--radius-md,12px);background:var(--surface-subtle)}}
.tok code{{font-weight:600}} .tok small{{display:block;color:var(--ink-muted)}} .tok p{{margin:4px 0 0;font-size:13px;color:var(--ink-secondary)}}
.sws{{display:flex;flex-shrink:0;border-radius:8px;overflow:hidden;border:1px solid var(--line)}} .sw{{width:28px;height:56px}}
.demo{{flex-shrink:0;width:56px;height:56px;background:var(--surface);border:1px solid var(--line)}}
.demo-spacing{{background:var(--orange-soft);width:var(--v);min-width:4px;max-width:96px;height:24px}}
.demo-radius{{border-radius:var(--v);background:var(--navy)}} .demo-shadow{{box-shadow:var(--v);border:0}}
.ty{{padding:12px 0;border-bottom:1px dashed var(--line)}} .ty small{{display:block;color:var(--ink-muted);font:12px/18px var(--font-sans)}}
.card{{margin:12px 0;border:1px solid var(--line);border-radius:var(--radius-md,12px);overflow:hidden;background:var(--surface)}}
.card-h{{padding:8px 12px;background:var(--surface-subtle);font-size:14px}} .card-h span{{color:var(--ink-muted)}}
.card iframe{{display:block;width:100%;border:0;background:var(--surface)}}
.prose{{max-width:760px}} .prose img{{max-width:100%}} pre{{white-space:pre-wrap}}
</style>
</head>
<body>
<header><b>{esc(index.get('title', 'Design System'))}</b>
<a href="#overview">Overview</a><a href="#colors">Colors</a><a href="#type">Typography</a><a href="#spacing">Spacing</a><a href="#components">Components</a><a href="#assets">Assets</a>
<button id="theme">theme: {first}</button></header>
<main>
<p><small>หน้านี้ tokens.css และ manifest.json สร้างจาก tokens.json ด้วย tools/build_local_view.py (ไม่ใช่หน้า claude.ai artifact) ดู SOURCE.md</small></p>
<section id="overview"><h2>Overview</h2>
<div class="card"><div class="card-h"><b>Cover</b></div><iframe data-src="components/Cover/{PREVIEW_OUT}" height="288"></iframe></div>
<div class="prose" id="readme"><pre>{esc(readme_text)}</pre></div></section>
<section id="colors"><h2>Colors <small>themes: {", ".join(themes)}</small></h2><div class="grid">{swatches()}</div></section>
<section id="type"><h2>Typography</h2>{typo()}</section>
<section id="spacing"><h2>Spacing</h2><div class="grid">{simple("spacing")}</div>
<h2>Radius</h2><div class="grid">{simple("radius")}</div><h2>Shadows</h2><div class="grid">{simple("shadow")}</div></section>
<section id="components"><h2>Components</h2>{cards()}</section>
<section id="assets"><h2>Assets</h2>{"".join(f'<p><b>{esc(g["name"])}</b></p>' + "".join(f'<div class="tok"><img src="assets/{esc(g["name"])}/{esc(r["name"])}" style="max-height:96px;background:#fff;padding:8px"><div><code>{esc(r["name"])}</code><small>{r["type"]} {r["size"]} bytes</small></div></div>' for r in g.get("files", {}).values()) for g in index.get("assetGroups", {}).values())}</section>
</main>
<script>
(function(){{
  var root=document.documentElement, btn=document.getElementById('theme'), themes={json.dumps(themes)};
  function load(){{document.querySelectorAll('iframe[data-src]').forEach(function(f){{f.src=f.dataset.src+'?theme='+root.dataset.theme;}});}}
  btn.onclick=function(){{var i=themes.indexOf(root.dataset.theme);root.dataset.theme=themes[(i+1)%themes.length];btn.textContent='theme: '+root.dataset.theme;load();}};
  load();
  var el=document.getElementById('readme');
  if(window.marked){{el.innerHTML=marked.parse(el.firstChild.textContent);}}
}})();
</script>
</body>
</html>
"""
write(PREFIX + INDEX_OUT, gallery)

# ---------- SHA256SUMS of snapshot files (what the artifact served) ----------
if not SNAPSHOT:
    print("done (repo layout)", datetime.now(timezone.utc).isoformat())
    sys.exit(0)
sums = []
for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d != "api"]
    for fn in sorted(files):
        rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
        if rel in GENERATED or fn.endswith(".local.html") or fn == ".DS_Store":
            continue
        h = hashlib.sha256(open(os.path.join(dirpath, fn), "rb").read()).hexdigest()
        sums.append(f"{h}  {rel}")
write("SHA256SUMS", "\n".join(sorted(sums, key=lambda s: s.split("  ", 1)[1])) + "\n")
print("done", datetime.now(timezone.utc).isoformat())
