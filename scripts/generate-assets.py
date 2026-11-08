"""Generates the monochrome, animated SVG assets for the GitHub profile README.
Every asset is produced in a dark and a light variant."""
import os, sys
from xml.sax.saxutils import escape as esc

OUT = sys.argv[1]

THEMES = {
    "dark": dict(bg="#0a0a0a", border="#262626", text="#ededed", muted="#8f8f8f", faint="#1c1c1c", dot="#2e2e2e", chip="#141414"),
    "light": dict(bg="#fafafa", border="#e4e4e4", text="#111111", muted="#6b6b6b", faint="#efefef", dot="#d9d9d9", chip="#ffffff"),
}
SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
EASE = "cubic-bezier(0.23, 1, 0.32, 1)"  # strong ease-out

BASE_CSS = f"""
.sans {{ font-family: {SANS}; }}
.mono {{ font-family: {MONO}; }}
.in {{ opacity: 0; animation: in 900ms {EASE} both; transform-box: fill-box; }}
@keyframes in {{
  from {{ opacity: 0; transform: translateY(8px); filter: blur(6px); }}
  to   {{ opacity: 1; transform: translateY(0);   filter: blur(0); }}
}}
.pulse {{ transform-box: fill-box; transform-origin: center; animation: pulse 2.4s {EASE} infinite; }}
@keyframes pulse {{
  0%   {{ transform: scale(1);   opacity: .55; }}
  70%  {{ transform: scale(3.2); opacity: 0; }}
  100% {{ transform: scale(3.2); opacity: 0; }}
}}
@media (prefers-reduced-motion: reduce) {{
  * {{ animation: none !important; opacity: 1 !important; }}
}}
"""


def d(ms):
    return f'style="animation-delay:{ms}ms"'


def svg(w, h, body, css, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}">\n<title>{esc(title)}</title>\n'
            f'<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n')


def write(name, theme, content):
    with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w") as f:
        f.write(content)


def rail(t, x0, x1, y, dur, reverse=False, delay=0):
    """A thin track with sleepers and a small train gliding along it."""
    ticks = "".join(f'<rect x="{x}" y="{y-4}" width="1" height="8" fill="{t["border"]}"/>'
                    for x in range(x0, x1 + 1, 18))
    span = x1 - x0
    frm, to = (span + 60, -120) if reverse else (-120, span + 60)
    grad_dir = 'x1="1" x2="0"' if reverse else 'x1="0" x2="1"'
    css = f"""
.train{y} {{ animation: ride{y} {dur}s linear {delay}s infinite; }}
@keyframes ride{y} {{ from {{ transform: translateX({frm}px); }} to {{ transform: translateX({to}px); }} }}"""
    body = f"""
<defs>
  <linearGradient id="trail{y}" {grad_dir} y1="0" y2="0">
    <stop offset="0" stop-color="{t['text']}" stop-opacity="0"/>
    <stop offset="1" stop-color="{t['text']}" stop-opacity=".9"/>
  </linearGradient>
  <clipPath id="clip{y}"><rect x="{x0}" y="{y-10}" width="{span}" height="20"/></clipPath>
</defs>
{ticks}
<rect x="{x0}" y="{y-1}" width="{span}" height="1" fill="{t['border']}"/>
<g clip-path="url(#clip{y})"><g class="train{y}">
  <rect x="{x0}" y="{y-1.5}" width="90" height="3" fill="url(#trail{y})"/>
  <rect x="{x0 + (0 if reverse else 82)}" y="{y-3}" width="22" height="6" rx="3" fill="{t['text']}"/>
</g></g>"""
    return body, css


# ───────────────────────── HEADER ─────────────────────────
WORDS = ["real-time maps", "mobile apps", "data pipelines", "things that ship"]


def header(t):
    W, H = 1200, 400
    mono_cw = 0.6 * 22  # mono glyph width at 22px
    prefix = "$ now building "
    px = 56 + len(prefix) * mono_cw
    cycle = 2.6 * len(WORDS)
    words = ""
    for i, w in enumerate(WORDS):
        cx = px + len(w) * mono_cw + 4
        words += (f'<g class="word" style="animation-delay:{1.2 + i * 2.6:.1f}s">'
                  f'<text x="{px}" y="300" class="mono" font-size="22" fill="{t["text"]}">{esc(w)}</text>'
                  f'<rect class="caret" x="{cx}" y="282" width="11" height="22" fill="{t["text"]}"/></g>')
    css = f"""
.word {{ opacity: 0; transform-box: fill-box; animation: word {cycle}s {EASE} infinite both; }}
@keyframes word {{
  0%   {{ opacity: 0; transform: translateY(6px); filter: blur(4px); }}
  4%   {{ opacity: 1; transform: translateY(0);   filter: blur(0); }}
  22%  {{ opacity: 1; transform: translateY(0);   filter: blur(0); }}
  25%  {{ opacity: 0; transform: translateY(-6px); filter: blur(4px); }}
  100% {{ opacity: 0; }}
}}
.caret {{ animation: blink 1s steps(1) infinite; }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}"""
    rb, rcss = rail(t, 56, W - 56, 352, 14)
    body = f"""
<defs>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.1" fill="{t['dot']}"/>
  </pattern>
  <radialGradient id="fade" cx="0.82" cy="0.35" r="0.6">
    <stop offset="0" stop-color="#fff" stop-opacity="1"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <clipPath id="card"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="20"/></clipPath>
</defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="20" fill="{t['bg']}" stroke="{t['border']}"/>
<g clip-path="url(#card)"><rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#m)"/></g>

<text x="56" y="64" class="mono in" {d(0)} font-size="15" fill="{t['muted']}">~/otazua</text>
<g class="in" {d(80)}>
  <circle class="pulse" cx="{W-246}" cy="59" r="4" fill="{t['text']}"/>
  <circle cx="{W-246}" cy="59" r="4" fill="{t['text']}"/>
  <text x="{W-56}" y="64" text-anchor="end" class="mono" font-size="15" fill="{t['muted']}">open to internships</text>
</g>

<text x="50" y="196" class="sans in" {d(160)} font-size="112" font-weight="650" letter-spacing="-5" fill="{t['text']}">Otazua</text>
<text x="56" y="244" class="sans in" {d(260)} font-size="24" fill="{t['muted']}">Data Science &amp; Business Administration student · UPNA</text>
<text x="56" y="300" class="mono in" {d(360)} font-size="22" fill="{t['muted']}">{esc(prefix)}</text>
{words}
<g class="in" {d(460)}>{rb}</g>
"""
    return svg(W, H, body, css + rcss, "Otazua — Data Science & Business Administration student at UPNA")


# ───────────────────────── PROJECT CARDS ─────────────────────────
PROJECTS = [
    ("trainviewer", "01", "TrainViewer", "Live",
     ["Real-time map of Spain's rail network:", "live trains on real tracks, official Adif", "incidents and station boards."],
     ["JavaScript", "Leaflet", "Supabase", "Actions"]),
    ("euskago", "02", "EuskaGo", "In development",
     ["Learn Basque, Duolingo-style. Streaks,", "spaced repetition, audio lessons and", "offline sync on iOS & Android."],
     ["React Native", "Expo", "TypeScript", "Supabase"]),
    ("momentum", "03", "Momentum", "Shipped",
     ["A minimal, animated launch page with a", "waitlist, crafted with React, Tailwind", "and shadcn/ui."],
     ["React", "Vite", "Tailwind", "Supabase"]),
    ("homelab", "04", "Homelab", "Self-hosted",
     ["Network-wide ad blocking with Pi-hole", "and custom lists, plus self-hosting", "experiments on a Raspberry Pi."],
     ["Pi-hole", "Linux", "Raspberry Pi"]),
]


def card(t, p):
    _, idx, title, status, desc, chips = p
    W, H = 600, 340
    cw = 0.6 * 14
    st_w = len(status) * cw
    lines = "".join(f'<text x="44" y="{168 + i*28}" class="sans" font-size="18" fill="{t["muted"]}">{esc(l)}</text>'
                    for i, l in enumerate(desc))
    x, chips_svg = 44, ""
    for i, c in enumerate(chips):
        w = len(c) * 0.6 * 13 + 28
        chips_svg += (f'<g class="in" {d(320 + i*60)}><rect x="{x}" y="270" width="{w:.0f}" height="30" rx="15" '
                      f'fill="{t["chip"]}" stroke="{t["border"]}"/><text x="{x + w/2:.1f}" y="290" text-anchor="middle" '
                      f'class="mono" font-size="13" fill="{t["muted"]}">{esc(c)}</text></g>')
        x += w + 8
    body = f"""
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="{t['bg']}" stroke="{t['border']}"/>
<text x="44" y="62" class="mono in" {d(0)} font-size="14" fill="{t['muted']}">{idx}</text>
<g class="in" {d(60)}>
  <circle class="pulse" cx="{W-44-st_w-14}" cy="57" r="3.5" fill="{t['text']}"/>
  <circle cx="{W-44-st_w-14}" cy="57" r="3.5" fill="{t['text']}"/>
  <text x="{W-44}" y="62" text-anchor="end" class="mono" font-size="14" fill="{t['muted']}">{esc(status)}</text>
</g>
<text x="42" y="126" class="sans in" {d(120)} font-size="36" font-weight="600" letter-spacing="-1.2" fill="{t['text']}">{esc(title)}</text>
<g class="in" {d(200)}>{lines}</g>
{chips_svg}
<text x="{W-44}" y="292" text-anchor="end" class="sans in" {d(560)} font-size="22" fill="{t['muted']}">↗</text>
"""
    return svg(W, H, body, "", f"{title} — {' '.join(desc)}")


# ───────────────────────── SECTION DIVIDERS ─────────────────────────
SECTIONS = [("about", "01"), ("stack", "02"), ("projects", "03"), ("activity", "04"), ("contact", "05")]


def section(t, name, idx):
    W, H = 1200, 64
    label = f"{idx} / {name}"
    lx = 8 + len(label) * 0.6 * 18 + 20
    css = f"""
.draw {{ stroke-dasharray: {W}; stroke-dashoffset: {W}; animation: draw 1.6s {EASE} 200ms forwards; }}
@keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}"""
    body = f"""
<text x="8" y="40" class="mono in" font-size="18" fill="{t['muted']}">{idx} <tspan fill="{t['border']}">/</tspan> <tspan fill="{t['text']}">{name}</tspan></text>
<line class="draw" x1="{lx:.0f}" y1="34" x2="{W-8}" y2="34" stroke="{t['border']}" stroke-width="1"/>
"""
    return svg(W, H, body, css, name.capitalize())


# ───────────────────────── PILLS ─────────────────────────
PILLS = [("linkedin", "LinkedIn"), ("instagram", "Instagram")]


def pill(t, label, delay):
    W, H = 200, 52
    body = f"""
<g class="in" {d(delay)}>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{(H-2)/2}" fill="{t['bg']}" stroke="{t['border']}"/>
<text x="{W/2 - 8}" y="32" text-anchor="middle" class="sans" font-size="17" font-weight="500" fill="{t['text']}">{esc(label)}</text>
<text x="{W/2 + len(label)*4.6 + 4}" y="32" text-anchor="start" class="sans" font-size="16" fill="{t['muted']}">↗</text>
</g>"""
    return svg(W, H, body, "", label)


# ───────────────────────── FOOTER ─────────────────────────
def footer(t):
    W, H = 1200, 150
    rb, rcss = rail(t, 0, W, 120, 18, reverse=True, delay=1)
    body = f"""
<text x="{W/2}" y="52" text-anchor="middle" class="sans in" font-size="22" fill="{t['text']}">Thanks for stopping by.</text>
<text x="{W/2}" y="84" text-anchor="middle" class="mono in" {d(120)} font-size="15" fill="{t['muted']}">made with care in Navarre</text>
<g class="in" {d(240)}>{rb}</g>
"""
    return svg(W, H, body, rcss, "Thanks for stopping by")


for th, t in THEMES.items():
    write("header", th, header(t))
    for p in PROJECTS:
        write(f"card-{p[0]}", th, card(t, p))
    for n, i in SECTIONS:
        write(f"section-{n}", th, section(t, n, i))
    for i, (k, label) in enumerate(PILLS):
        write(f"pill-{k}", th, pill(t, label, i * 80))
    write("footer", th, footer(t))
print("ok", len(os.listdir(OUT)))
