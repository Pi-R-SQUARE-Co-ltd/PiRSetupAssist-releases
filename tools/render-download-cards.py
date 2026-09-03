#!/usr/bin/env python3
"""วาดการ์ดยอดดาวน์โหลดเป็น SVG ทั้งแบบต่อรุ่นและแบบรวมทุกรุ่น

ทำไมเป็นไฟล์ในรีโป ไม่ใช่ป้ายจากบริการภายนอก
  ป้ายสำเร็จรูปหน้าตาเหมือนกันหมดทุกโปรเจกต์ และป้ายรายไฟล์ของ shields
  บังคับต่อท้ายชื่อไฟล์ในค่าของป้าย ตัดไม่ได้ · การ์ดนี้จึงวาดเอง คุมได้ทั้งใบ

วาดสองชุดเสมอ สว่างกับมืด แล้วให้หน้าที่ใช้เลือกด้วย <picture>
เพราะ GitHub มีทั้งสองธีม และการ์ดพื้นขาวใบเดียวจะแสบตาในธีมมืด

รันโดย .github/workflows/download-counts.yml ตามเวลา · รันมือก็ได้
    GH_TOKEN=$(gh auth token) python3 tools/render-download-cards.py
"""
import json
import os
import pathlib
import urllib.request

REPO = "Pi-R-SQUARE-Co-ltd/PiRSetupAssist-releases"
OUT = pathlib.Path(__file__).resolve().parent.parent / "badges"

# ชื่อไฟล์แจก → ชื่อที่แสดงบนการ์ด · เรียงตามลำดับที่อยากให้ขึ้น
DIST_FILES = {
    "PiRSetupAssist-macOS.zip":   "macOS",
    "PiRSetupAssist-Windows.exe": "Windows",
    "PiRSetupAssist-Windows.zip": "Windows zip",
    "PiRSetupAssist-1.0.zip":     "รุ่นแรก",      # v1.0 ยังไม่ได้แยกไฟล์ตามระบบ
}

FONT = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',"
        "Arial,'Noto Sans Thai',sans-serif")
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

THEMES = {
    #        พื้น       ขอบ        เส้นคั่น   หัวข้อ    ป้ายแถว   ตัวเลข    เน้น
    "light": ("#ffffff", "#e6e1db", "#f0ece7", "#8b8680", "#57534e", "#2b2926", "#c8552f"),
    "dark":  ("#161514", "#2e2b28", "#252220", "#8b8680", "#a8a29e", "#ece9e5", "#e8825d"),
}


def api(path):
    req = urllib.request.Request(
        f"https://api.github.com/{path}",
        headers={"Accept": "application/vnd.github+json",
                 "User-Agent": "pir-download-cards"})
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def rows_of(assets):
    """[(ชื่อที่แสดง, ยอด)] เรียงตาม DIST_FILES · ไฟล์ที่ไม่รู้จักไม่นับ"""
    got = {a["name"]: a["download_count"] for a in assets}
    return [(label, got[name]) for name, label in DIST_FILES.items() if name in got]


def card(title, right, rows, theme):
    """การ์ดหนึ่งใบ · หัวข้อ + รายการ + ยอดรวมล่างสุด"""
    bg, border, rule, head, label, value, accent = THEMES[theme]
    W = 300
    top, line_h, foot = 46, 26, 44
    H = top + line_h * len(rows) + foot
    y = top + 22
    body = []
    for name, n in rows:
        body.append(
            f'<text x="20" y="{y}" font-size="12.5" fill="{label}" font-family="{FONT}">{name}</text>'
            f'<text x="{W-20}" y="{y}" font-size="12.5" font-weight="600" fill="{value}"'
            f' text-anchor="end" font-family="{MONO}">{n:,}</text>')
        y += line_h
    total = sum(n for _, n in rows)
    sep = y - line_h + 10
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title} {total}">
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="13.5" fill="{bg}" stroke="{border}"/>
<text x="20" y="29" font-size="11.5" fill="{head}" font-family="{FONT}" letter-spacing=".4">{title}</text>
<text x="{W-20}" y="29" font-size="11.5" fill="{head}" text-anchor="end" font-family="{MONO}">{right}</text>
<line x1="0" y1="45" x2="{W}" y2="45" stroke="{rule}"/>
{"".join(body)}
<line x1="0" y1="{sep}" x2="{W}" y2="{sep}" stroke="{rule}"/>
<text x="20" y="{sep+24}" font-size="12.5" font-weight="600" fill="{value}" font-family="{FONT}">รวม</text>
<text x="{W-20}" y="{sep+26}" font-size="17" font-weight="700" fill="{accent}" text-anchor="end" font-family="{MONO}">{total:,}</text>
</svg>
'''


def write(stem, title, right, rows):
    if not rows:
        return
    for theme in THEMES:
        (OUT / f"{stem}-{theme}.svg").write_text(card(title, right, rows, theme), encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    releases = api(f"repos/{REPO}/releases?per_page=100")
    grand = {}
    for rel in releases:
        rows = rows_of(rel["assets"])
        write(rel["tag_name"], "ยอดดาวน์โหลด", rel["tag_name"], rows)
        for name, n in rows:
            grand[name] = grand.get(name, 0) + n
    order = [l for l in DIST_FILES.values() if l in grand]
    write("all", "ยอดดาวน์โหลดทั้งหมด", f"{len(releases)} รุ่น",
          [(l, grand[l]) for l in order])
    print(f"วาดแล้ว {len(releases)} รุ่น + ใบรวม · รวมทุกไฟล์ {sum(grand.values()):,} ครั้ง")


if __name__ == "__main__":
    main()
