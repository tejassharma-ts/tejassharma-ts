"""Generate portfolio-themed SVG assets for the GitHub profile README."""
import base64, io, re, sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.varLib import instancer

PORT = Path.home() / "code/self/me"
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

# ---- palette (from tailwind.config.ts) ----
THEMES = {
    "light": dict(head="#363333", body="#4c4848", muted="#878484", chip="#706d6d",
                  chipText="#F7F7F7", dot="#4C4848", accent="#ff850f", line="#F0F0F0", ring="#ffffff"),
    "dark": dict(head="#F0F0F0", body="#c8c6c6", muted="#adabab", chip="#4c4848",
                 chipText="#F7F7F7", dot="#878484", accent="#ff850f", line="#363333", ring="#0d1117"),
}
CHARS = "".join(chr(c) for c in range(32, 127)) + "–—·’é…"

# ---- fonts: subset + embed ----
def prep(ttf: TTFont):
    s = subset.Subsetter(subset.Options(flavor="woff2", layout_features=["kern"]))
    s.populate(text=CHARS)
    s.subset(ttf)
    ttf.flavor = "woff2"
    b = io.BytesIO(); ttf.save(b)
    return base64.b64encode(b.getvalue()).decode()

abril = TTFont(PORT / "assets/AbrilFatface-Regular.ttf")
inter_var = TTFont(PORT / "assets/Inter-VariableFont_slnt,wght.ttf")
inter_b = instancer.instantiateVariableFont(TTFont(PORT / "assets/Inter-VariableFont_slnt,wght.ttf"), {"wght": 700, "slnt": 0})
inter_r = instancer.instantiateVariableFont(inter_var, {"wght": 400, "slnt": 0})

class F:
    def __init__(self, font, family):
        self.cmap = font.getBestCmap(); self.hmtx = font["hmtx"]; self.upm = font["head"].unitsPerEm
        self.family = family
    def w(self, text, size, ls=0):
        return sum(self.hmtx[self.cmap.get(ord(c), self.cmap[32])][0] for c in text) * size / self.upm + ls * len(text)

ABRIL, INTERB, INTERR = F(abril, "Abril"), F(inter_b, "InterB"), F(inter_r, "InterR")
FONT_DATA = {"Abril": prep(abril), "InterB": prep(inter_b), "InterR": prep(inter_r)}

def style(*fams):
    return "<style>" + "".join(
        f"@font-face{{font-family:'{f}';src:url(data:font/woff2;base64,{FONT_DATA[f]}) format('woff2')}}" for f in fams
    ) + "</style>"

def svg(w, h, body, fams, label):
    label = esc(label).replace('"', "&quot;")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}"><title>{label}</title><defs>{style(*fams)}</defs>{body}</svg>')

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def write(name, theme, content):
    (OUT / f"{name}-{theme}.svg").write_text(content)

W = 840

# ---- spark (copied from components/spark-svg.tsx) ----
spark_src = (PORT / "components/spark-svg.tsx").read_text()
SPARK_PATHS = re.findall(r"d='([^']+)'", spark_src)
def spark(x, y, size, color):
    s = size / 111
    paths = "".join(f'<path d="{d}" fill="{color}"/>' for d in SPARK_PATHS)
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'{paths}</g>')

def dots(x, y, cols, rows, gap, color, r=2.4):
    return "".join(f'<circle cx="{x+i*gap}" cy="{y+j*gap}" r="{r}" fill="{color}"/>'
                   for i in range(cols) for j in range(rows))

# ---- hero ----
me_b64 = base64.b64encode((PORT / "public/images/me.png").read_bytes()).decode()
think = (PORT / "public/images/me-think.svg").read_text()
think_b64 = base64.b64encode(think.encode()).decode()

def hero(t):
    c = THEMES[t]
    lines = ["Hello,", "I’m Tejas,", "front-end dev"]
    size = 60
    tx, ty = 64, 118
    text = "".join(
        f'<text x="{tx}" y="{ty + i*72}" font-family="Abril" font-size="{size}" fill="{c["head"]}" '
        f'style="animation:up .5s {0.1*i:.1f}s cubic-bezier(.22,1,.36,1) both">{esc(l)}</text>'
        for i, l in enumerate(lines))
    sub_y = ty + 2*72 + 46
    sub = (f'<text x="{tx}" y="{sub_y}" font-family="InterR" font-size="17" fill="{c["body"]}" '
           f'style="animation:up .5s .35s both">who keeps wandering down the stack:</text>'
           f'<text x="{tx}" y="{sub_y+26}" font-family="InterR" font-size="17" fill="{c["body"]}" '
           f'style="animation:up .5s .45s both">sockets, caches, protocols &amp; C.</text>')
    # photo
    px, py, ps = 548, 64, 244
    photo = (
        dots(px + ps - 70, py - 18, 7, 7, 14, c["dot"]) +
        dots(px - 18, py + ps - 70, 7, 7, 14, c["dot"]) +
        f'<clipPath id="r"><rect x="{px}" y="{py}" width="{ps}" height="{ps}" rx="8"/></clipPath>'
        f'<rect x="{px-6}" y="{py-6}" width="{ps+12}" height="{ps+12}" rx="12" fill="{c["ring"]}"/>'
        f'<image href="data:image/png;base64,{me_b64}" x="{px}" y="{py}" width="{ps}" height="{ps}" clip-path="url(#r)"/>'
        f'<rect x="{px}" y="{py}" width="{ps}" height="{ps}" rx="8" fill="none" stroke="#ffad5e" stroke-width="2.5"/>'
        f'<image href="data:image/svg+xml;base64,{think_b64}" x="{px+ps-82}" y="{py+34}" width="40" height="42"/>' +
        "".join(f'<circle cx="{px+ps-58+i*7}" cy="{py+26}" r="1.6" fill="#F7F7F7" '
                f'style="animation:pulse 1.6s {i*0.15:.2f}s infinite"/>' for i in range(5))
    )
    anim = ("<style>@keyframes up{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}"
            "@keyframes pop{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}"
            "@keyframes pulse{50%{opacity:.25}}</style>")
    body = anim + spark(4, 6, 92, c["head"] if t == "light" else c["head"]) + text + sub + photo
    write("hero", t, svg(W, 380, body, ["Abril", "InterR"], "Hello, I'm Tejas, front-end dev who keeps wandering down the stack"))

# ---- section heading: .about; ----
def heading(name, text, align, t):
    c = THEMES[t]; size = 50
    w = ABRIL.w("." + text, size) + ABRIL.w(";", 42) + 8
    x = 6 if align == "left" else W - w - 6
    body = (f'<text x="{x}" y="66" font-family="Abril" font-size="{size}" fill="{c["head"]}">'
            f'<tspan fill="{c["accent"]}">.</tspan><tspan dx="6">{esc(text)}</tspan>'
            f'<tspan font-size="42">;</tspan></text>')
    write(f"h-{name}", t, svg(W, 88, body, ["Abril"], f".{text};"))

# ---- chips (bg-secondary-400 rounded-[5px] font-bold text-sm) ----
def chip_row(items, x, y, c, size=13.5, max_w=W):
    out, cx, cy = [], x, y
    for it in items:
        w = INTERB.w(it, size) + 36
        if cx + w > max_w:
            cx, cy = x, cy + 38
        out.append(f'<rect x="{cx}" y="{cy}" width="{w:.1f}" height="28" rx="5" fill="{c["chip"]}"/>'
                   f'<text x="{cx + w/2:.1f}" y="{cy+19}" text-anchor="middle" font-family="InterB" '
                   f'font-size="{size}" fill="{c["chipText"]}">{esc(it)}</text>')
        cx += w + 12
    return "".join(out), cy + 28

def chips(name, items, t, label):
    c = THEMES[t]
    body, h = chip_row(items, 2, 2, c)
    write(f"chips-{name}", t, svg(W, int(h + 4), body, ["InterB"], label))

# ---- project title block: panorama label + Abril title + chips, timeline dot ----
def project(name, label, title, stack, t):
    c = THEMES[t]
    body = (f'<line x1="9" y1="0" x2="9" y2="400" stroke="{c["line"]}" stroke-width="2"/>'
            f'<circle cx="9" cy="16" r="7" fill="{c["ring"]}" stroke="{c["accent"]}" stroke-width="2.5"/>'
            f'<text x="40" y="22" font-family="Abril" font-size="15" letter-spacing="5" fill="{c["body"]}">{esc(label.upper())}</text>'
            f'<text x="40" y="74" font-family="Abril" font-size="40" fill="{c["head"]}">{esc(title)}</text>')
    rows, h = chip_row(stack, 40, 94, c)
    write(f"p-{name}", t, svg(W, int(h + 6), body.replace('y2="400"', f'y2="{int(h+6)}"') + rows,
                               ["Abril", "InterB"], f"{title}: {', '.join(stack)}"))

# ---- panorama label alone ----
def panorama(name, text, t):
    c = THEMES[t]
    body = f'<text x="2" y="20" font-family="Abril" font-size="16" letter-spacing="5" fill="{c["body"]}">{esc(text.upper())}</text>'
    write(f"l-{name}", t, svg(W, 30, body, ["Abril"], text))

# ---- pill buttons ----
def button(name, text, variant, t):
    c = THEMES[t]; size = 16
    w = INTERR.w(text, size) + 52
    bg = c["accent"] if variant == "primary" else "#4c4848"
    body = (f'<rect x="1" y="1" width="{w:.1f}" height="38" rx="19" fill="{bg}"/>'
            f'<text x="{1 + w/2:.1f}" y="25.5" text-anchor="middle" font-family="InterR" font-size="{size}" fill="#ffffff">{esc(text)}</text>')
    write(f"b-{name}", t, svg(int(w + 2), 40, body, ["InterR"], text))

# ---- divider + footer ----
def divider(t):
    c = THEMES[t]
    write("divider", t, svg(W, 24, f'<rect x="{W/2-256}" y="11.6" width="512" height="1" rx="1" fill="{c["line"]}"/>', [], "divider"))

logo = (PORT / "public/images/logo.svg").read_text()
def footer(t):
    c = THEMES[t]
    lg = logo if t == "light" else logo.replace("#363333", "#F0F0F0").replace("#4C4848", "#c8c6c6").replace("#4c4848", "#c8c6c6")
    lb = base64.b64encode(lg.encode()).decode()
    body = (f'<image href="data:image/svg+xml;base64,{lb}" x="{W/2-88}" y="4" width="176" height="46"/>'
            f'<text x="{W/2}" y="84" text-anchor="middle" font-family="InterR" font-size="14" fill="{c["muted"]}">Code and Design – Me</text>')
    write("footer", t, svg(W, 96, body, ["InterR"], "Tejas — Code and Design: Me"))

for t in THEMES:
    hero(t)
    for i, (n, txt) in enumerate([("about", "about"), ("lowlevel", "under the hood"), ("building", "building"),
                                   ("toolbox", "toolbox"), ("shelf", "bookshelf"), ("beliefs", "beliefs"),
                                   ("setup", "setup"), ("hello", "say hello")]):
        heading(n, txt, "left" if i % 2 == 0 else "right", t)
    project("redis", "C++ · networking", "Redis, from scratch", ["C++", "TCP", "POSIX sockets", "pthreads", "Binary protocol"], t)
    project("lru", "C · data structures", "LRU cache", ["C", "Doubly linked list", "Manual memory"], t)
    project("socket", "C · networking", "Talking TCP by hand", ["C", "sockaddr_in", "Node.js", "Express"], t)
    project("brackets", "C · parsing", "Bracket checker", ["C", "Stack", "File I/O"], t)
    project("togetherlab", "in the works", "togetherlab", ["TypeScript", "Yjs / CRDTs", "WebSockets", "PostgreSQL", "Redis", "Docker"], t)
    chips("low", ["C", "C++", "POSIX sockets", "pthreads", "Linux", "Bash", "Vim"], t, "Low level: C, C++, POSIX sockets, pthreads, Linux, Bash, Vim")
    chips("web", ["TypeScript", "JavaScript", "React", "Next.js", "Node.js", "Express", "TanStack Query", "Zustand", "Tailwind CSS"], t,
          "Web: TypeScript, JavaScript, React, Next.js, Node.js, Express, TanStack Query, Zustand, Tailwind CSS")
    chips("data", ["PostgreSQL", "Redis", "MongoDB", "Prisma", "Drizzle", "WebSockets"], t, "Data: PostgreSQL, Redis, MongoDB, Prisma, Drizzle, WebSockets")
    for n, txt in [("low", "closer to the metal"), ("web", "the day job stack"), ("data", "data & realtime")]:
        panorama(n, txt, t)
    button("portfolio", "Visit my portfolio", "primary", t)
    button("email", "Say hello", "secondary", t)
    divider(t)
    footer(t)

print("ok", len(list(OUT.glob("*.svg"))))
