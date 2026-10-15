import os
import random
import sys
import requests
from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
FB_PAGE_ID = os.environ["FB_PAGE_ID"]
FB_PAGE_TOKEN = os.environ["FB_PAGE_TOKEN"]

TEXT_MODEL = "gemini-2.5-flash"
IMAGE_MODEL = "gemini-2.5-flash-image"
GRAPH = "https://graph.facebook.com/v21.0"

# Nijer topic gulo ekhane bodlan
TOPICS = [
    "pariboarik mashik bajet kivabe korben",
    "joruri tohobil (emergency fund) keno dorkar",
    "dainik khoroc likhe rakhar obhyash",
    "bachchar poRashona er jonno shonchoy",
    "ay-byoy er hishab sohoj vabe rakhar tip",
    "ঋণ ba dhar kombate smart upay",
]

client = genai.Client(api_key=GEMINI_API_KEY)


def make_caption(topic: str) -> str:
    prompt = (
        "Tumi 'Yasa Smart Finance' naamer ekta bangali family finance app er "
        "Facebook page er content writer. Nicher topic niye shuddho Bangla te "
        "ekta chhoto (3-4 line), shohoj, kajer tip soho caption lekho. "
        "Shesh e 2-3 ta hashtag dao. Sudhu caption ta dao, onno kichu na.\n\n"
        f"Topic: {topic}"
    )
    resp = client.models.generate_content(model=TEXT_MODEL, contents=prompt)
    return resp.text.strip()


def make_image(topic: str) -> bytes:
    prompt = (
        "Clean, modern, friendly illustration for a family finance app social "
        "media post. No text in the image. Warm colors. Topic: " + topic
    )
    resp = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
    )
    for part in resp.candidates[0].content.parts:
        if part.inline_data and part.inline_data.data:
            return part.inline_data.data
    raise RuntimeError("Gemini theke image ashe nai")


def post_to_facebook(image: bytes, caption: str) -> dict:
    r = requests.post(
        f"{GRAPH}/{FB_PAGE_ID}/photos",
        data={"caption": caption, "access_token": FB_PAGE_TOKEN},
        files={"source": ("post.png", image, "image/png")},
        timeout=120,
    )
    if not r.ok:
        raise RuntimeError(f"Facebook error {r.status_code}: {r.text}")
    return r.json()


def main():
    topic = random.choice(TOPICS)
    print("Topic:", topic)
    try:
        caption = make_caption(topic)
        image = make_image(topic)
    except Exception as e:
        # Quota sesh hole ba error hole ei bar skip, workflow fail korbe na
        print("Generate korte parlam na, skip kortesi:", e)
        sys.exit(0)

    print("Posted:", post_to_facebook(image, caption))


if __name__ == "__main__":
    main()
