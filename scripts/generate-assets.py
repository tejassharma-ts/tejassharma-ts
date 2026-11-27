"""Render the profile README's terminal card (Gruvbox Material + Comic Mono, like my kitty).

Usage: python generate-assets.py <out-dir>    (needs: pip install fonttools brotli)
"""
import base64, io, sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "assets")
OUT.mkdir(parents=True, exist_ok=True)
FONT = "/usr/share/fonts/TTF/ComicMono.ttf"

# kitty/current-theme.conf
BG, FG, MUTED, BORDER = "#191b1c", "#d4be98", "#928374", "#d8a657"
RED, GREEN, YELLOW, BLUE, PURPLE, AQUA, ORANGE = "#ea6962", "#a9b665", "#d8a657", "#7daea3", "#d3869b", "#89b482", "#e78a4e"
PALETTE = ["#45403d", RED, GREEN, ORANGE, BLUE, PURPLE, AQUA, FG]

font = TTFont(FONT)
s = subset.Subsetter(subset.Options(flavor="woff2"))
s.populate(text="".join(chr(c) for c in range(32, 127)))
s.subset(font)
font.flavor = "woff2"
buf = io.BytesIO(); font.save(buf)
FONT_B64 = base64.b64encode(buf.getvalue()).decode()

SIZE, LH = 15, 25
CW = 1116 / 2048 * SIZE          # Comic Mono advance width
PAD_X, PAD_Y = 30, 40
W = 840

def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# each line = list of (text, color) segments
def prompt(cmd):
    return [("tejas", GREEN), ("@", FG), ("arch", BLUE), (" ~ ", FG), ("$ ", YELLOW), (cmd, FG)]

LOGO = [
    r"       /\       ",
    r"      /  \      ",
    r"     /\   \     ",
    r"    /      \    ",
    r"   /   ,,   \   ",
    r"  /   |  |  -\  ",
    r" /_-''    ''-_\ ",
]
INFO = [
    [("tejas", GREEN), ("@", FG), ("arch", BLUE)],
    [("----------", MUTED)],
    [("role    ", YELLOW), ("programmer, low-level nerd", FG)],
    [("os      ", YELLOW), ("arch linux + sway", FG)],
    [("editor  ", YELLOW), ("vim (btw)", FG)],
    [("shell   ", YELLOW), ("zsh + tmux + kitty", FG)],
    [("reading ", YELLOW), ("code: the hidden language of computer hardware and software", FG)],
]

lines = [prompt("fastfetch"), []]
for logo, info in zip(LOGO, INFO):
    lines.append([("  " + logo, BLUE), ("   ", FG)] + info)
lines.append(["PALETTE"])
ABOUT = [
    [("hey, i'm tejas ", FG), (":)", YELLOW), (" i write software, then take it apart to see how it works.", FG)],
    [("computer science nerd at heart: ", FG), ("books, algorithms, data structures, linux,", AQUA)],
    [("operating systems", AQUA), (", anything that shows what the machine is *actually* doing.", FG)],
    [("usually found in a terminal, reading man pages for fun.", FG)],
    [],
    [("follower of humanity: ", PURPLE), ("be kind, share what you know, help where you can.", FG)],
]
lines += [[], prompt("cat about.txt")] + ABOUT
SKILLS = [
    ("languages",    "c, c++, typescript, javascript, bash, lua"),
    ("web",          "react, next.js, node.js, express, tanstack query, zustand"),
    ("architecture", "rest apis, websockets, modular monoliths, crdts, caching"),
    ("infra",        "postgresql, mongodb, redis, docker, prisma, drizzle"),
    ("tools",        "git, vim, tmux, lazygit, figma, linux"),
]
lines += [[], prompt("cat skills.toml")]
lines += [[("[", MUTED), (k, YELLOW), ("]", MUTED), (" " * (15 - len(k)), FG), (v, FG)] for k, v in SKILLS]
lines += [[], prompt("ls ~/github"),
          [("rcat/  obscene/  xv6-riscv/  Xchedule/", BLUE)],
          [], prompt("cat now.txt"),
          [("writing a redis in c++, one syscall at a time.", FG)],
          [], prompt("") + [("CURSOR", None)]]

H = PAD_Y * 2 + LH * len(lines) - 6
out = []
for i, segs in enumerate(lines):
    y = PAD_Y + 12 + i * LH
    if segs == ["PALETTE"]:
        x0 = PAD_X + CW * (2 + len(LOGO[0]) + 3)
        out += [f'<rect x="{x0 + k*CW*3:.1f}" y="{y-13}" width="{CW*3:.1f}" height="17" fill="{c}"/>' for k, c in enumerate(PALETTE)]
        continue
    col = 0
    tspans = []
    for text, color in segs:
        if text == "CURSOR":
            out.append(f'<rect x="{PAD_X + col*CW:.1f}" y="{y-14}" width="{CW:.1f}" height="19" fill="{RED}"/>')
            continue
        tspans.append(f'<tspan fill="{color}">{esc(text)}</tspan>')
        col += len(text)
    if tspans:
        out.append(f'<text x="{PAD_X}" y="{y}" xml:space="preserve">{"".join(tspans)}</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="tejas@arch: programmer, low-level nerd. Arch + Sway, Vim. Writes C, C++, TypeScript and Lua. Interested in operating systems, networking, distributed systems, databases, compilers and how computers work. Currently writing a Redis in C++.">
<title>tejas@arch</title>
<defs><style>@font-face{{font-family:'CM';src:url(data:font/woff2;base64,{FONT_B64}) format('woff2')}}
text{{font-family:'CM','Comic Mono',monospace;font-size:{SIZE}px}}</style></defs>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="{BG}" stroke="{BORDER}"/>
{"".join(out)}
</svg>'''
(OUT / "terminal.svg").write_text(svg)

# small link "buttons" in the same style
def link(name, label, color):
    w = round(CW * (len(label) + 7))
    body = (f'<rect x="0.5" y="0.5" width="{w-1}" height="31" fill="{BG}" stroke="{color}"/>'
            f'<text x="{w/2}" y="21" text-anchor="middle" fill="{color}">[ {esc(label)} ]</text>')
    (OUT / f"{name}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="32" viewBox="0 0 {w} 32" role="img" aria-label="{esc(label)}">'
        f'<defs><style>@font-face{{font-family:\'CM\';src:url(data:font/woff2;base64,{FONT_B64}) format(\'woff2\')}}'
        f'text{{font-family:\'CM\',monospace;font-size:{SIZE}px}}</style></defs>{body}</svg>')

link("link-portfolio", "tejassharma.in", YELLOW)
link("link-mail", "mail", GREEN)
print("ok")
