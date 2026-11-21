import json
import logging
import re
import threading
from pathlib import Path

from google.genai import types

from services.ai_service import MODEL, client

logger = logging.getLogger("uvicorn.error")

# ગુજરાતી અને English ના શબ્દો અહીં છે (હાથે લખેલા)
FRONTEND_I18N = Path(__file__).resolve().parents[2] / "frontend" / "i18n"
# બાકીની ભાષાઓનું ભાષાંતર એકવાર થઈને અહીં સચવાય છે
CACHE_DIR = Path(__file__).resolve().parents[1] / "i18n_cache"

# નવી ભાષા ઉમેરવા માટે અહીં એક લાઇન ઉમેરો
LANGUAGES = [
    {"code": "gu", "native": "ગુજરાતી", "english": "Gujarati", "speech": "gu-IN"},
    {"code": "hi", "native": "हिन्दी", "english": "Hindi", "speech": "hi-IN"},
    {"code": "en", "native": "English", "english": "English", "speech": "en-IN"},
    {"code": "mr", "native": "मराठी", "english": "Marathi", "speech": "mr-IN"},
    {"code": "pa", "native": "ਪੰਜਾਬੀ", "english": "Punjabi", "speech": "pa-IN"},
    {"code": "bn", "native": "বাংলা", "english": "Bengali", "speech": "bn-IN"},
    {"code": "ta", "native": "தமிழ்", "english": "Tamil", "speech": "ta-IN"},
    {"code": "te", "native": "తెలుగు", "english": "Telugu", "speech": "te-IN"},
    {"code": "kn", "native": "ಕನ್ನಡ", "english": "Kannada", "speech": "kn-IN"},
    {"code": "ml", "native": "മലയാളം", "english": "Malayalam", "speech": "ml-IN"},
    {"code": "or", "native": "ଓଡ଼ିଆ", "english": "Odia", "speech": "or-IN"},
]
CODES = {lang["code"] for lang in LANGUAGES}

_PLACEHOLDER = re.compile(r"\{\w+\}")
_lock = threading.Lock()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _translate(code: str) -> dict:
    base = _read_json(FRONTEND_I18N / "en.json")
    info = next(lang for lang in LANGUAGES if lang["code"] == code)

    prompt = (
        "You are a professional translator for a mobile app used by farmers in India.\n"
        f"Translate the VALUES of the following JSON object from English into "
        f"{info['english']} ({info['native']}).\n"
        "Rules:\n"
        "- Keep every key exactly unchanged.\n"
        "- Use simple, everyday words that a village farmer understands.\n"
        "- Keep emojis, placeholders like {n}, {name}, {lat}, {lon}, {temp}, {hum}, {wind} "
        "exactly unchanged.\n"
        "- Keep these names in Latin letters: KisanMitra AI, PM-KISAN, iKhedut, KCC, KVK, "
        "OTP, PIN, GPS, MB, JPG, PNG, WEBP, Chrome, Edge, Windows, Android, Google.\n"
        "- Return ONLY the translated JSON object.\n\n"
        + json.dumps(base, ensure_ascii=False)
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    text = (response.text or "").strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("translation is not an object")

    out, missing = {}, 0
    for key, english in base.items():
        value = data.get(key)
        ok = (
            isinstance(value, str)
            and value.strip()
            and set(_PLACEHOLDER.findall(english)) == set(_PLACEHOLDER.findall(value))
        )
        if ok:
            out[key] = value
        else:
            out[key] = english
            missing += 1

    # ઘણું બધું ખૂટે તો ખરાબ ભાષાંતર સાચવવું નહીં
    if missing > len(base) * 0.25:
        raise RuntimeError(f"translation incomplete ({missing}/{len(base)} missing)")
    return out


def get_translations(code: str) -> dict:
    if code not in CODES:
        raise KeyError(code)

    if code in ("en", "gu"):
        return _read_json(FRONTEND_I18N / f"{code}.json")

    cache_file = CACHE_DIR / f"{code}.json"
    if cache_file.exists():
        return _read_json(cache_file)

    with _lock:
        if cache_file.exists():  # બીજા કોઈએ હમણાં જ બનાવી દીધી
            return _read_json(cache_file)
        data = _translate(code)
        CACHE_DIR.mkdir(exist_ok=True)
        cache_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        logger.info("Translated UI strings saved for language: %s", code)
        return data