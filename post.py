# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import requests

from content import (QURAN_REFS, SURAH_BN, HADITHS, SKIP_VERSES,
                     MAX_ARABIC_CHARS, MAX_BANGLA_CHARS)
from poster import bn, build_html, render_png

FB_PAGE_ID = os.environ.get("FB_PAGE_ID", "")
FB_PAGE_TOKEN = os.environ.get("FB_PAGE_TOKEN", "")
POSTER_FOOTER = os.environ.get("POSTER_FOOTER", "")
GRAPH = "https://graph.facebook.com/v21.0"
STATE_FILE = "posted.json"
TOTAL_AYAH = 6236


# ---------- state: ja post hoyeche tar hishab (repeat thamate) ----------
def load_state() -> dict:
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            st = json.load(f)
    except FileNotFoundError:
        st = {}
    st.setdefault("used", [])
    st.setdefault("next_global", 1)  # curated list sesh hole puro Quran er kromanushare
    return st


def save_state(st: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=1)


# ---------- Quran API ----------
_bn_ids = None


def bn_edition_ids():
    global _bn_ids
    if _bn_ids is None:
        _bn_ids = ["bn.bengali"]
        try:
            r = requests.get("https://api.alquran.cloud/v1/edition/language/bn", timeout=30)
            for e in r.json().get("data", []):
                if e.get("type") == "translation" and e["identifier"] not in _bn_ids:
                    _bn_ids.append(e["identifier"])
        except Exception as e:
            print("Bangla edition list paoa jay nai:", str(e)[:150])
    return _bn_ids


def fetch_quran(ref):
    """ref = 'surah:ayat' ba global ayat number. (arabic, bangla, surah, ayat, surah_arabic_naam)"""
    for edition in bn_edition_ids()[:3]:
        url = f"https://api.alquran.cloud/v1/ayah/{ref}/editions/quran-uthmani,{edition}"
        for attempt in range(2):
            try:
                r = requests.get(url, timeout=30)
                r.raise_for_status()
                d = r.json()["data"]
                arabic, bangla = d[0]["text"].strip(), d[1]["text"].strip()
                if arabic and bangla:
                    return (arabic, bangla, d[0]["surah"]["number"],
                            d[0]["numberInSurah"], d[0]["surah"].get("name", ""))
            except Exception as e:
                print(f"Quran API ({edition}) try {attempt + 1} hoy nai:", str(e)[:150])
                time.sleep(2)
    return None


def quran_ref_text(surah, ayah, arabic_name):
    if surah in SURAH_BN:
        return f"সূরা {SURAH_BN[surah]} {bn(surah)}:{bn(ayah)}"
    return f"{arabic_name} {bn(surah)}:{bn(ayah)}".strip()


def quran_ok(arabic, bangla, surah, ayah) -> bool:
    return (
        (surah, ayah) not in SKIP_VERSES
        and not (ayah == 1 and surah not in (1, 9))  # bismillah mishe thake
        and len(arabic) >= 12                          # "আলিফ-লাম-মীম" dhoroner ayat bad
        and len(arabic) <= MAX_ARABIC_CHARS
        and len(bangla) <= MAX_BANGLA_CHARS
    )


def quran_result(arabic, bangla, surah, ayah, name):
    ref = quran_ref_text(surah, ayah, name)
    caption = f"{arabic}\n\n{bangla}\n\n📖 {ref}\n\n#কুরআন #কুরআনের_বাণী #ইসলাম"
    return "quran", arabic, bangla, ref, caption, f"q:{surah}:{ayah}"


# ---------- kon ta post hobe ----------
def next_hadith(st):
    for i, (bangla, ref) in enumerate(HADITHS):
        if f"h:{i}" not in st["used"]:
            caption = f"{bangla}\n\n📖 {ref}\n\n#হাদীস #হাদীসের_বাণী #ইসলাম"
            return "hadith", "", bangla, ref, caption, f"h:{i}"
    return None


def next_quran(st):
    used = set(st["used"])
    # 1) age curated (bachai kora) ayat gulo
    for s, a in QURAN_REFS:
        if f"q:{s}:{a}" in used:
            continue
        got = fetch_quran(f"{s}:{a}")
        if got and quran_ok(got[0], got[1], got[2], got[3]):
            return quran_result(*got)
    # 2) tarpor puro Quran kromanushare, ja post hoyeche ta bad diye
    tries = 0
    while st["next_global"] <= TOTAL_AYAH and tries < 25:
        g = st["next_global"]
        st["next_global"] = g + 1
        tries += 1
        got = fetch_quran(g)
        if not got:
            st["next_global"] = g  # API somossha, ei number e abar chesta hobe
            break
        if f"q:{got[2]}:{got[3]}" in used:
            continue
        if quran_ok(got[0], got[1], got[2], got[3]):
            return quran_result(*got)
    return None


def choose(st):
    n = len(st["used"])
    want_hadith_first = n % 3 == 2  # proti 3 ta post e 1ta hadis
    order = (next_hadith, next_quran) if want_hadith_first else (next_quran, next_hadith)
    for fn in order:
        res = fn(st)
        if res:
            return res
    return None


def post_photo(image: bytes, caption: str) -> dict:
    r = requests.post(
        f"{GRAPH}/{FB_PAGE_ID}/photos",
        data={"caption": caption, "access_token": FB_PAGE_TOKEN},
        files={"source": ("poster.png", image, "image/png")},
        timeout=120,
    )
    if not r.ok:
        raise RuntimeError(f"Facebook error {r.status_code}: {r.text}")
    return r.json()


def main():
    dry = "--dry-run" in sys.argv
    st = load_state()
    res = choose(st)
    if not res:
        raise SystemExit("Notun kono content baki nai (ba Quran API paoa jay nai). Repeat korbo na, tai post kori nai.")
    kind, arabic, bangla, ref, caption, item_id = res
    print("Item:", item_id, ref)

    html_text = build_html(kind, arabic, bangla, ref, POSTER_FOOTER, seed=len(st["used"]))
    png = render_png(html_text, "poster.png")

    if dry:
        print("Dry run: poster.png toiri, post/state save kori nai.\n\n" + caption)
        return

    print("Posted:", post_photo(png, caption))
    st["used"].append(item_id)
    save_state(st)  # post hoyar por-i save, jate bhul kore repeat na hoy


if __name__ == "__main__":
    main()
