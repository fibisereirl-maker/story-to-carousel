#!/usr/bin/env python3
"""story-to-carousel — genera carruseles de marca (1080x1080) desde un JSON.
Corre sobre forge-studio-lite (Node + Playwright). Aporte de FIBISER a Imperio Agentico. MIT.

Uso:
  export FORGE_ROOT=/ruta/a/forge-studio-lite
  python3 story-to-carousel.py story.json
  cd "$FORGE_ROOT" && npx tsx --env-file=.env src/pipelines/carousel.ts .
"""
import json, os, sys, html, re

ROOT = os.environ.get("FORGE_ROOT", ".")
SRC = os.path.join(ROOT, "slides", "source")

PALETTES = {
    "dark-orange": dict(bg="#0F1216", surface="#191E25", primary="#F2790F",
                        primary_deep="#C55A05", accent="#FFC061", steel="#39485A",
                        glow="rgba(242,121,15,0.18)"),
    "dark-blue":   dict(bg="#0A0F1C", surface="#141B2E", primary="#2E8BFF",
                        primary_deep="#1E63C9", accent="#67E8F9", steel="#33415C",
                        glow="rgba(46,139,255,0.20)"),
}

def fmt(t):
    t = html.escape(t or "")
    t = t.replace("[hl]", '<span class="hl">').replace("[/hl]", "</span>")
    t = t.replace("[b]", "<b>").replace("[/b]", "</b>")
    return t.replace("\n", "<br>")

def head(p):
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><style>
@font-face{{font-family:"Geist";src:url("https://cdn.jsdelivr.net/npm/geist@1.5.1/dist/fonts/geist-sans/Geist-Variable.woff2") format("woff2-variations");font-weight:100 900;font-display:swap;}}
@font-face{{font-family:"Geist Mono";src:url("https://cdn.jsdelivr.net/npm/geist@1.5.1/dist/fonts/geist-mono/Geist-Mono-Variable.woff2") format("woff2-variations");font-weight:100 900;font-display:swap;}}
:root{{--bg:{p['bg']};--surface:{p['surface']};--primary:{p['primary']};--primary-deep:{p['primary_deep']};--accent:{p['accent']};--text:#FFFFFF;--muted:#9BA6B2;--steel:{p['steel']};}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1080px;background:var(--bg);color:var(--text);overflow:hidden;font-family:"Geist",system-ui,sans-serif;-webkit-font-smoothing:antialiased;}}
.slide{{width:1080px;height:1080px;padding:100px;display:flex;flex-direction:column;justify-content:center;position:relative;background:radial-gradient(120% 90% at 88% 6%,{p['glow']} 0%,rgba(0,0,0,0) 46%),var(--bg);}}
.slide::after{{content:"";position:absolute;left:0;bottom:0;width:100%;height:12px;background:linear-gradient(90deg,var(--primary-deep),var(--primary) 45%,var(--accent));}}
.kicker{{font-family:"Geist Mono",monospace;font-size:26px;font-weight:600;letter-spacing:5px;text-transform:uppercase;color:var(--primary);margin-bottom:44px;}}
.headline{{font-size:92px;font-weight:800;line-height:1.03;letter-spacing:-2px;margin-bottom:40px;}}
.headline .hl{{color:var(--primary);}}
.support{{font-size:40px;line-height:1.35;color:var(--muted);max-width:860px;font-weight:400;}}
.support b{{color:var(--text);font-weight:600;}}
.list{{margin-top:14px;display:flex;flex-direction:column;gap:26px;}}
.li{{display:flex;align-items:center;gap:26px;font-size:44px;font-weight:600;}}
.dot{{width:20px;height:20px;border-radius:6px;background:var(--primary);flex:none;transform:rotate(45deg);}}
.chips{{display:flex;flex-wrap:wrap;gap:20px;margin:8px 0;}}
.chip{{background:var(--surface);border:1px solid var(--steel);border-radius:14px;padding:22px 34px;font-size:38px;font-weight:600;}}
.quote{{font-size:52px;font-weight:700;line-height:1.25;border-left:8px solid var(--primary);padding-left:40px;margin:10px 0;}}
.big{{font-family:"Geist Mono",monospace;font-size:150px;font-weight:800;color:var(--primary);line-height:1;margin-bottom:20px;}}
.wa{{display:inline-flex;align-items:center;gap:18px;background:var(--primary);color:var(--bg);font-weight:800;font-size:44px;padding:28px 48px;border-radius:18px;margin-top:24px;width:max-content;}}
.foot{{position:absolute;left:100px;bottom:64px;display:flex;align-items:center;gap:22px;font-family:"Geist Mono",monospace;font-size:30px;letter-spacing:2px;color:var(--muted);}}
.brandmark{{font-family:"Geist",sans-serif;font-weight:800;letter-spacing:1px;color:var(--text);font-size:34px;}}
.brandmark .b{{color:var(--primary);}}
.pageno{{position:absolute;top:80px;left:100px;font-family:"Geist Mono",monospace;font-size:28px;color:var(--steel);letter-spacing:3px;}}
</style></head><body><div class="slide">"""

def render(s, n, brand, tag):
    P = [f'<div class="pageno">{n:02d}</div>']
    if s.get("big"):     P.append(f'<div class="big">{fmt(s["big"])}</div>')
    if s.get("kicker"):  P.append(f'<div class="kicker">{fmt(s["kicker"])}</div>')
    if s.get("quote"):   P.append(f'<div class="quote">{fmt(s["quote"])}</div>')
    if s.get("headline"):P.append(f'<div class="headline">{fmt(s["headline"])}</div>')
    if s.get("list"):    P.append('<div class="list">' + "".join(f'<div class="li"><span class="dot"></span>{fmt(i)}</div>' for i in s["list"]) + '</div>')
    if s.get("chips"):   P.append('<div class="chips">' + "".join(f'<div class="chip">{fmt(c)}</div>' for c in s["chips"]) + '</div>')
    if s.get("support"): P.append(f'<div class="support">{fmt(s["support"])}</div>')
    if s.get("cta"):     P.append(f'<div class="wa">&#9654;&nbsp; {fmt(s["cta"])}</div>')
    P.append(f'<div class="foot"><span class="brandmark">{brand}</span><span>&middot; {html.escape(tag)}</span></div>')
    return "".join(P) + "</div></body></html>"

def main():
    story = json.load(open(sys.argv[1], encoding="utf-8"))
    p = PALETTES.get(story.get("palette", "dark-orange"), PALETTES["dark-orange"])
    if isinstance(story.get("palette"), dict): p = {**PALETTES["dark-orange"], **story["palette"]}
    brand = story.get("brand", 'TU <span class="b">MAR</span>CA')
    tag = story.get("tag", "TU MARCA")
    os.makedirs(SRC, exist_ok=True)
    for f in os.listdir(SRC):
        if re.match(r"slide-\d+\.html", f): os.remove(os.path.join(SRC, f))
    for i, s in enumerate(story["slides"], 1):
        open(os.path.join(SRC, f"slide-{i:02d}.html"), "w", encoding="utf-8").write(head(p) + render(s, i, brand, tag))
    print(f"OK {len(story['slides'])} slides -> {SRC}")
    print(f'Ahora: cd "{ROOT}" && npx tsx --env-file=.env src/pipelines/carousel.ts .')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: python3 story-to-carousel.py story.json  (define FORGE_ROOT primero)"); sys.exit(1)
    main()
