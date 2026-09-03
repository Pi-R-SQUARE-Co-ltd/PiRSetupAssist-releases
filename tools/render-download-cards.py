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
    "PiRSetupAssist-1.0.zip":     "first release",  # v1.0 ยังไม่ได้แยกไฟล์ตามระบบ
}

FONT = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',"
        "Arial,'Noto Sans Thai',sans-serif")
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

THEMES = {
    #        พื้นชิป    ตัวอักษร  ตัวเลข     ชิปเน้น    ตัวอักษรบนชิปเน้น
    "light": ("#f1eeea", "#6b665f", "#2b2926", "#c8552f", "#ffffff"),
    "dark":  ("#232120", "#a09a93", "#ece9e5", "#c8552f", "#ffffff"),
}

# ประมาณความกว้างตัวอักษร · ไม่ต้องเป๊ะ แค่ต้องไม่ให้ข้อความล้นชิป
# เผื่อไว้ทางกว้างเสมอ เพราะฟอนต์บนเครื่องคนดูไม่เหมือนกัน
W_LABEL = 6.9     # ป้ายชื่อ 11px (ไทยกับอังกฤษปนกัน)
W_DIGIT = 7.4     # ตัวเลข mono 12px


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


def load_exclude():
    """ยอดที่ทีมงานโหลดเองและไม่อยากให้นับ · ไม่มีไฟล์ = ไม่หักอะไรเลย"""
    f = OUT / "exclude.json"
    if not f.exists():
        return {}
    raw = json.loads(f.read_text(encoding="utf-8"))
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def rows_of(assets, skip):
    """[(ชื่อที่แสดง, ยอด)] เรียงตาม DIST_FILES · หักยอดของทีมงานออกแล้ว

    หักไม่ให้ต่ำกว่าศูนย์ เผื่อกรอกเกินจริงไว้ · ไฟล์ที่ไม่รู้จักไม่นับ
    """
    got = {a["name"]: a["download_count"] for a in assets}
    out = []
    for name, label in DIST_FILES.items():
        if name in got:
            out.append((label, max(0, got[name] - skip.get(name, 0))))
    return out


def card(title, right, rows, theme):
    """แถบบาง · ชิปติดกัน ยอดรวมนำหน้าเป็นชิปสีเน้น แล้วต่อด้วยแต่ละแพลตฟอร์ม

    เลือกทรงนี้เพราะเตี้ยที่สุด วางใต้เนื้อหาในหน้า release แล้วไม่แย่งความสนใจ
    แต่ยังบอกครบทุกแพลตฟอร์มในแถวเดียว ซึ่งป้ายสำเร็จรูปทำไม่ได้
    """
    chip_bg, label_c, value_c, lead_bg, lead_fg = THEMES[theme]
    H, PAD, GAP = 30, 13, 8
    total = sum(n for _, n in rows)
    segs = [("total", total, True)] + [(l, n, False) for l, n in rows]

    x, out = 0.0, []
    for label, n, lead in segs:
        txt = f"{n:,}"
        w = PAD * 2 + len(label) * W_LABEL + GAP + len(txt) * W_DIGIT
        bg = lead_bg if lead else chip_bg
        lf = lead_fg if lead else label_c
        vf = lead_fg if lead else value_c
        weight = "600" if lead else "500"
        out.append(
            f'<rect x="{x:.1f}" y="0" width="{w:.1f}" height="{H}" fill="{bg}"/>'
            f'<text x="{x+PAD:.1f}" y="19.5" font-size="11" fill="{lf}"'
            f' font-family="{FONT}">{label}</text>'
            f'<text x="{x+w-PAD:.1f}" y="19.5" font-size="12" font-weight="{weight}"'
            f' fill="{vf}" text-anchor="end" font-family="{MONO}">{txt}</text>')
        x += w

    W = round(x)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title} {total:,}">
<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="7"/></clipPath></defs>
<g clip-path="url(#c)">{"".join(out)}</g>
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
    exclude = load_exclude()
    grand = {}
    for rel in releases:
        rows = rows_of(rel["assets"], exclude.get(rel["tag_name"], {}))
        write(rel["tag_name"], "downloads", rel["tag_name"], rows)
        for name, n in rows:
            grand[name] = grand.get(name, 0) + n
    order = [l for l in DIST_FILES.values() if l in grand]
    write("all", "downloads", f"{len(releases)} releases",
          [(l, grand[l]) for l in order])
    print(f"วาดแล้ว {len(releases)} รุ่น + ใบรวม · รวมทุกไฟล์ {sum(grand.values()):,} ครั้ง")


if __name__ == "__main__":
    main()
