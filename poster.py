# -*- coding: utf-8 -*-
"""HTML/CSS theke colorful, shajano poster (PNG) toiri kore. Text kokhono AI banay na."""
import html
import random

PALETTES = [
    # (naam, dark, mid, light)
    ("emerald", "#053b2c", "#0b7a5a", "#2fd1a0"),
    ("royal",   "#10205c", "#2447b8", "#5aa2ff"),
    ("violet",  "#2d0f63", "#6d2bd1", "#d06bff"),
    ("sunset",  "#5c0f2a", "#c2264b", "#ff9a3c"),
    ("teal",    "#08403f", "#0f8f86", "#4fe3d0"),
    ("night",   "#14123f", "#3b2f9e", "#ff7ab6"),
]

BN_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")


def bn(n) -> str:
    return str(n).translate(BN_DIGITS)


def _size(length: int, steps) -> int:
    for limit, px in steps:
        if length <= limit:
            return px
    return steps[-1][1]


def build_html(kind: str, arabic: str, bangla: str, reference: str,
               footer: str = "", seed=None) -> str:
    rnd = random.Random(seed)
    _, dark, mid, light = rnd.choice(PALETTES)
    gold, gold2 = "#fcd34d", "#f59e0b"

    esc = html.escape
    badge = "পবিত্র কুরআন" if kind == "quran" else "হাদীস শরীফ"

    ar_px = _size(len(arabic), [(60, 64), (110, 54), (170, 46), (260, 40), (9999, 34)])
    bn_len = len(bangla)
    if arabic:
        bn_px = _size(bn_len, [(90, 50), (150, 44), (230, 38), (330, 33), (9999, 29)])
    else:
        bn_px = _size(bn_len, [(70, 68), (120, 60), (180, 52), (260, 45), (9999, 38)])

    arabic_block = (
        f'<div class="ar">{esc(arabic)}</div><div class="orn">'
        f'<span></span><i>❖</i><span></span></div>' if arabic else
        '<div class="quote">“</div>'
    )

    star_tile = (
        "data:image/svg+xml;utf8,"
        "<svg xmlns='http://www.w3.org/2000/svg' width='90' height='90' viewBox='0 0 90 90'>"
        "<g fill='none' stroke='white' stroke-opacity='0.13' stroke-width='1.6'>"
        "<rect x='25' y='25' width='40' height='40'/>"
        "<rect x='25' y='25' width='40' height='40' transform='rotate(45 45 45)'/>"
        "<circle cx='45' cy='45' r='9'/></g></svg>"
    )

    corner = (
        "<svg class='corner' viewBox='0 0 160 160' xmlns='http://www.w3.org/2000/svg'>"
        f"<g fill='none' stroke='{gold}' stroke-width='4'>"
        "<path d='M6 154 V50 Q6 6 50 6 H154'/>"
        "<path d='M26 154 V62 Q26 26 62 26 H154' stroke-width='2' stroke-opacity='.7'/></g>"
        f"<g fill='{gold}'><path d='M50 50 l14 14 l-14 14 l-14 -14 z'/>"
        "<circle cx='96' cy='16' r='5'/><circle cx='16' cy='96' r='5'/></g></svg>"
    )

    lantern = (
        "<svg class='lantern' viewBox='0 0 100 260' xmlns='http://www.w3.org/2000/svg'>"
        "<defs><radialGradient id='g' cx='50%' cy='55%' r='55%'>"
        "<stop offset='0' stop-color='#fff7c2'/><stop offset='.55' stop-color='#ffc83d'/>"
        "<stop offset='1' stop-color='#e8890c'/></radialGradient></defs>"
        f"<line x1='50' y1='0' x2='50' y2='70' stroke='{gold}' stroke-width='3'/>"
        f"<path d='M32 92 Q50 62 68 92 Z' fill='{gold}'/>"
        f"<rect x='28' y='92' width='44' height='8' rx='3' fill='{gold2}'/>"
        "<path d='M28 100 H72 L82 160 Q50 200 18 160 Z' fill='url(#g)' stroke='"
        f"{gold}' stroke-width='3'/>"
        f"<path d='M50 100 V184 M34 102 L30 168 M66 102 L70 168' stroke='{gold2}' stroke-width='2' opacity='.7'/>"
        f"<path d='M30 186 H70 L62 206 H38 Z' fill='{gold2}'/>"
        f"<circle cx='50' cy='218' r='7' fill='{gold}'/>"
        f"<path d='M50 225 L44 252 M50 225 L56 252 M50 225 V256' stroke='{gold}' stroke-width='3'/></svg>"
    )

    crescent = (
        "<svg class='moon' viewBox='0 0 140 120' xmlns='http://www.w3.org/2000/svg'>"
        "<defs><mask id='m'><rect width='140' height='120' fill='white'/>"
        "<circle cx='74' cy='54' r='38' fill='black'/></mask>"
        "<linearGradient id='mg' x1='0' y1='0' x2='1' y2='1'>"
        f"<stop offset='0' stop-color='{gold}'/><stop offset='1' stop-color='{gold2}'/></linearGradient></defs>"
        "<circle cx='58' cy='62' r='46' fill='url(#mg)' mask='url(#m)'/>"
        "<polygon fill='url(#mg)' points='108,34 112.6,47 126,47.4 115.4,55.6 119.2,68.6 108,61 96.8,68.6 100.6,55.6 90,47.4 103.4,47'/>"
        "</svg>"
    )

    footer_html = f'<div class="foot">{esc(footer)}</div>' if footer else ""

    return f"""<!doctype html>
<html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Amiri+Quran&family=Noto+Naskh+Arabic:wght@500;700&family=Noto+Sans+Bengali:wght@500;700&display=block" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{position:relative;font-family:'Noto Sans Bengali','Hind Siliguri','Noto Sans',sans-serif;color:#fff;
 background:
  radial-gradient(circle at 50% 18%, {light}cc 0%, transparent 46%),
  radial-gradient(circle at 12% 92%, {light}88 0%, transparent 40%),
  radial-gradient(circle at 92% 82%, {gold}44 0%, transparent 36%),
  linear-gradient(165deg,{mid} 0%,{dark} 100%);}}
.pattern{{position:absolute;inset:0;background-image:url("{star_tile}");background-size:90px 90px;opacity:.9}}
.vignette{{position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,transparent 55%,rgba(0,0,0,.38) 100%)}}
.frame{{position:absolute;inset:26px;border:6px solid {gold};border-radius:34px;box-shadow:0 0 28px {gold}66, inset 0 0 28px {gold}33}}
.frame2{{position:absolute;inset:46px;border:2px dashed {gold}aa;border-radius:24px}}
.corner{{position:absolute;width:150px;height:150px}}
.c1{{left:30px;top:30px}} .c2{{right:30px;top:30px;transform:scaleX(-1)}}
.c3{{left:30px;bottom:30px;transform:scaleY(-1)}} .c4{{right:30px;bottom:30px;transform:scale(-1,-1)}}
.lantern{{position:absolute;top:30px;width:96px;height:250px;filter:drop-shadow(0 0 22px #ffc83daa)}}
.l1{{left:120px}} .l2{{right:120px}}
.moon{{position:absolute;left:50%;top:78px;width:190px;transform:translateX(-50%);filter:drop-shadow(0 0 20px {gold}aa)}}
.wrap{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;padding-top:244px}}
.badge{{padding:12px 54px;border-radius:60px;font-weight:700;font-size:38px;color:#3b2a00;
 background:linear-gradient(90deg,{gold2},{gold},{gold2});box-shadow:0 6px 18px rgba(0,0,0,.35), 0 0 0 5px rgba(255,255,255,.18)}}
.card{{margin-top:30px;width:850px;height:770px;border-radius:425px 425px 44px 44px;
 background:linear-gradient(180deg,rgba(0,0,0,.34),rgba(0,0,0,.22));
 border:5px solid {gold};box-shadow:0 0 0 12px {gold}30, 0 20px 50px rgba(0,0,0,.4), inset 0 0 60px rgba(255,255,255,.07);
 display:flex;flex-direction:column;align-items:center;justify-content:center;padding:150px 70px 52px;text-align:center}}
.ar{{font-family:'Amiri Quran','Noto Naskh Arabic','Amiri',serif;direction:rtl;font-size:{ar_px}px;line-height:1.75;color:{gold};text-shadow:0 3px 14px rgba(0,0,0,.45)}}
.orn{{display:flex;align-items:center;gap:16px;margin:22px 0 22px;width:78%}}
.orn span{{flex:1;height:3px;background:linear-gradient(90deg,transparent,{gold},transparent)}}
.orn i{{font-style:normal;color:{gold};font-size:34px}}
.quote{{font-family:serif;font-size:140px;line-height:.6;color:{gold};height:70px}}
.bn{{font-size:{bn_px}px;line-height:1.6;font-weight:500;text-shadow:0 2px 10px rgba(0,0,0,.5)}}
.ref{{margin-top:26px;padding:14px 46px;border-radius:18px;font-size:32px;font-weight:700;color:#fff;
 background:linear-gradient(90deg,transparent,rgba(255,255,255,.2),transparent);border-top:2px solid {gold};border-bottom:2px solid {gold}}}
.foot{{position:absolute;left:0;right:0;text-align:center;bottom:58px;font-size:26px;color:{gold};letter-spacing:1px;font-weight:700}}
</style></head>
<body>
<div class="pattern"></div><div class="vignette"></div>
<div class="frame"></div><div class="frame2"></div>
<div class="corner c1">{corner}</div><div class="corner c2">{corner}</div>
<div class="corner c3">{corner}</div><div class="corner c4">{corner}</div>
<div class="l1 lantern-wrap">{lantern.replace("class='lantern'", "class='lantern l1'")}</div>
<div class="l2 lantern-wrap">{lantern.replace("class='lantern'", "class='lantern l2'")}</div>
{crescent}
<div class="wrap">
  <div class="badge">{badge}</div>
  <div class="card">{arabic_block}<div class="bn">{esc(bangla)}</div></div>
  <div class="ref">{esc(reference)}</div>
</div>
{footer_html}
</body></html>"""


def render_png(html_text: str, out_path: str) -> bytes:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        page.set_content(html_text)
        try:
            page.wait_for_load_state("networkidle", timeout=20000)
            page.evaluate("document.fonts.ready")
        except Exception as e:  # font load na hole system font diye cholbe
            print("Font load somossha (system font use hobe):", str(e)[:150])
        page.wait_for_timeout(500)
        png = page.screenshot(type="png")
        browser.close()
    with open(out_path, "wb") as f:
        f.write(png)
    return png
