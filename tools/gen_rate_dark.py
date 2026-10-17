"""Generate assets/rate-dark.css: a dark theme for the Rate Calculation case study.

The original document (source/Rate Calculation Logic Builder Design.html) is light-only.
This reads its stylesheet and inline styles and writes dark equivalents, scoped to
html[data-theme="dark"]. The embedded product prototype (#proto-embed) is left light on
purpose: it shows the real product UI.

Run from the project root:  python3 tools/gen_rate_dark.py
"""
import re

SRC = "source/Rate Calculation Logic Builder Design.html"
OUT = "assets/rate-dark.css"
D = 'html[data-theme="dark"]'
NOT_PROTO = ":not(#proto-embed, #proto-embed *)"

BG = "#151412"      # page background in dark
TEXT = "#EEEBE5"    # primary text in dark
LINE = "#2C2A26"    # borders in dark
BAND = "#0D0C0B"    # dark bands that used --ink as a background

lines = open(SRC).read().split("\n")
# The prototype sits between <style id="proto-styles"> and the end of its script.
start = next(i for i, l in enumerate(lines) if '<style id="proto-styles">' in l)
end = next(i for i in range(len(lines) - 1, 0, -1) if lines[i].strip() == "</script>" and "flow guide ends here" in lines[i + 1])
doc = "\n".join(lines[:start] + lines[end + 1:])
css = re.findall(r"<style[^>]*>(.*?)</style>", doc, re.S)[0]
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def rgb(c):
    c = c.strip().lower()
    if c.startswith("#"):
        h = c[1:]
        if len(h) == 3:
            h = "".join(x * 2 for x in h)
        if len(h) != 6:
            return None
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)), 1.0
    m = re.match(r"rgba?\(([^)]*)\)", c)
    if m:
        p = [x.strip() for x in m.group(1).split(",")]
        a = float(p[3]) if len(p) > 3 else 1.0
        return tuple(int(float(x)) for x in p[:3]), a
    if c in ("#fff", "white"):
        return (255, 255, 255), 1.0
    return None


def lum(t):
    return (0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2]) / 255


def map_color(prop, val):
    """Return a dark-theme replacement for one declaration value, or None to leave it."""
    if "var(--ink)" in val and prop.startswith("background"):
        return val.replace("var(--ink)", BAND)
    cols = re.findall(r"#[0-9a-fA-F]{3,6}\b|rgba?\([^)]*\)|\bwhite\b", val)
    if not cols:
        return None
    out, changed = val, False
    for c in cols:
        parsed = rgb(c)
        if not parsed:
            continue
        t, a = parsed
        L = lum(t)
        new = None
        if prop.startswith("background") or prop in ("fill",):
            if L > 0.7:
                new = f"color-mix(in srgb,{c} 7%,{BG})" if a == 1 else f"rgba(255,255,255,{min(a, .06)})"
            elif L < 0.12 and a < 1:  # soft dark overlays / shadows-as-background
                new = f"rgba(255,255,255,{a})"
        elif prop == "color" or prop in ("stroke",):
            if L < 0.35:
                new = f"color-mix(in srgb,{c} 12%,{TEXT})"
            elif L < 0.62:
                new = f"color-mix(in srgb,{c} 45%,{TEXT})"
        elif prop.startswith("border") or prop.startswith("outline"):
            if L > 0.7:
                new = f"color-mix(in srgb,{c} 14%,{LINE})"
            elif L < 0.12 and a < 1:
                new = f"rgba(255,255,255,{max(a, .08)})"
        elif prop == "box-shadow":
            if L < 0.12:
                new = f"rgba(0,0,0,{min(1, a * 3):.2f})"
        if new:
            out = out.replace(c, new, 1)
            changed = True
    return out if changed else None


PROPS = ("background", "background-color", "color", "border", "border-color", "border-top", "border-bottom",
         "border-left", "border-right", "border-top-color", "border-bottom-color", "outline", "fill", "stroke", "box-shadow")


def scope(sel):
    sel = sel.strip()
    if sel.startswith(("html", ":root")):
        return None
    if sel.startswith("body"):
        return f"{D} {sel}"
    return f"{D} {sel}{NOT_PROTO}"


def walk(text):
    """Yield (media_or_None, selector, body) for every rule, one level of @media deep."""
    i = 0
    while i < len(text):
        j = text.find("{", i)
        if j < 0:
            break
        head = text[i:j].strip()
        depth, k = 1, j + 1
        while depth and k < len(text):
            depth += {"{": 1, "}": -1}.get(text[k], 0)
            k += 1
        body = text[j + 1:k - 1]
        if head.startswith("@media"):
            for _, s, b in walk(body):
                yield head, s, b
        elif not head.startswith("@"):
            yield None, head, body
        i = k


out = {}
for media, sel, body in walk(css):
    decls = []
    for d in body.split(";"):
        if ":" not in d:
            continue
        p, v = d.split(":", 1)
        p = p.strip().lower()
        if p in PROPS:
            nv = map_color(p, v.strip())
            if nv:
                decls.append(f"{p}:{nv}")
    if not decls:
        continue
    sels = [s for s in (scope(x) for x in sel.split(",")) if s]
    if sels:
        out.setdefault(media, []).append(",".join(sels) + "{" + ";".join(decls) + "}")

# Inline style="" colours (outside the prototype): attribute selectors, !important to beat inline.
inline = set()
for st in re.findall(r'style="([^"]*)"', doc):
    for d in st.split(";"):
        if ":" not in d:
            continue
        p, v = d.split(":", 1)
        p, v = p.strip().lower(), v.strip()
        if p in PROPS and map_color(p, v):
            inline.add((p, v))
inline_rules = [f'{D} [style*="{p}:{v}"]{NOT_PROTO}{{{p}:{map_color(p, v)}!important}}' for p, v in sorted(inline)]

VARS = f"""{D} body{{
  --ink:{TEXT};--ink-2:#C2BFB8;--ink-3:#9C998F;--ink-4:#76736C;--ink-5:#3D3A35;--rule:{LINE};--surf:#1B1A17;--white:#1F1D1A;
  --red-lt:rgba(238,82,57,.13);--rlt:rgba(238,82,57,.13);--rmd:rgba(238,82,57,.38);--rdk:#ff8a75;
  --ok:#34c26f;--ok-lt:rgba(0,162,61,.15);--okb:rgba(0,162,61,.15);--okd:rgba(0,162,61,.38);
  --blue:#7b9cf2;--info:#7b9cf2;--blue-lt:rgba(59,106,224,.17);--infob:rgba(59,106,224,.17);--infod:rgba(59,106,224,.42);
  --purple:#a988f5;--pu:#a988f5;--purple-lt:rgba(124,58,237,.18);--pub:rgba(124,58,237,.18);--pud:rgba(139,85,238,.42);
  --warn:#f0a43a;--warn-lt:rgba(217,119,6,.15);--warnd:rgba(217,119,6,.42);
  color-scheme:dark;
}}
/* the prototype keeps the original light product UI */
{D} #proto-embed{{
  --ink:#111317;--ink-2:#3D4451;--ink-3:#6B7280;--ink-4:#9CA3AF;--ink-5:#D1D5DB;--rule:#E2E4E6;--surf:#F9FAFB;--white:#ffffff;
  --red-lt:#FFF2EF;--rlt:#FFF2EF;--rmd:#FFCDC4;--rdk:#C73825;--ok:#00A23D;--ok-lt:#E9F9EE;--okb:#E9F9EE;--okd:#BDE5AE;
  --blue:#1D4ED8;--info:#1D4ED8;--blue-lt:#EFF6FF;--infob:#EFF6FF;--infod:#C7D8F9;--purple:#7C3AED;--pu:#7C3AED;
  --purple-lt:#F5F0FF;--pub:#F5F0FF;--pud:#DDCAFB;--warn:#D97706;--warn-lt:#FFFBEB;--warnd:#FDE68A;color-scheme:light;
}}
{D} body{{background:{BG}}}
{D} .page{{background:{BG};color:var(--ink)}}
/* note: the prototype markup closes .page early, so later sections sit directly in <body> */
{D} .flow-guide{{background:#1B1A17!important}}
{D} .flow-guide [style*="background:#fff"]{{background:#1F1D1A!important;color:var(--ink)!important}}
"""

with open(OUT, "w") as f:
    f.write("/* Generated by tools/gen_rate_dark.py from the Rate source document. Do not edit by hand. */\n")
    f.write(VARS)
    for r in out.get(None, []):
        f.write(r + "\n")
    for media, rules in out.items():
        if media:
            f.write(media + "{\n" + "\n".join(rules) + "\n}\n")
    f.write("/* inline styles */\n" + "\n".join(inline_rules) + "\n")
    f.write(f"/* one page background everywhere (the generated body rule above is lighter) */\n{D} body{{background:{BG}!important}}\n")
print(OUT, sum(len(v) for v in out.values()), "rules,", len(inline_rules), "inline")
