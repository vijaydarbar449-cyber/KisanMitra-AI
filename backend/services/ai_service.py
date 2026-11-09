import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

# .env પ્રોજેક્ટના બહારના ફોલ્ડરમાં છે (KisanMitra-AI\.env)
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH, override=True)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-3.8-flash"

MAX_HISTORY_TURNS = 10      # પાછલા કેટલા સંદેશા યાદ રાખવા
MAX_TURN_CHARS = 2000       # દરેક સંદેશાની મહત્તમ લંબાઈ

SYSTEM_PROMPT = (
    "તમે KisanMitra AI છો, ગુજરાતના ખેડૂતો માટેના મદદગાર. "
    "હંમેશા સરળ ગુજરાતીમાં, ટૂંકા અને વ્યવહારુ જવાબ આપો. "
    "પાક, રોગ, જીવાત, ખાતર, પાણી અને હવામાન વિશે મદદ કરો. "
    "રાસાયણિક દવાનું ચોક્કસ પ્રમાણ (મિલી/ગ્રામ) ન આપો; દવાનું નામ જણાવો અને "
    "પ્રમાણ માટે દવાના લેબલ કે કૃષિ અધિકારીની સલાહ લેવા કહો. "
    "દવા વાપરતી વખતે સલામતી જણાવો અને ગંભીર કેસમાં "
    "સ્થાનિક કૃષિ અધિકારી કે કૃષિ વિજ્ઞાન કેન્દ્રનો સંપર્ક કરવાની સલાહ આપો. "
    "ખેતી સિવાયના વિષયો પર નમ્રતાથી ના પાડો."
)

LANGUAGE_NAMES = {
    "gu": "ગુજરાતી",
    "hi": "હિન્દી",
    "en": "English",
}

IMAGE_PROMPT = (
    "આ પાક/છોડના પાનનો ફોટો છે. સરળ ગુજરાતીમાં જણાવો: "
    "1) છોડમાં કયો રોગ, જીવાત કે ઉણપ હોઈ શકે, "
    "2) તેના લક્ષણો ફોટામાં શું દેખાય છે, "
    "3) ઘરેલું/જૈવિક ઉપાય, "
    "4) રાસાયણિક દવાનું નામ (પ્રમાણ ન આપો, લેબલ વાંચવા કહો). "
    "ફોટો સ્પષ્ટ ન હોય કે છોડનો ન હોય તો તે જણાવો અને ખાતરીપૂર્વક નિદાન ન કરો. "
    "અંતે કૃષિ અધિકારી કે KVK ની સલાહ લેવા કહો."
)


def _call_gemini(contents, tries: int = 3) -> str:
    """Gemini ને બોલાવે છે. 503/429 (ભીડ) આવે તો ફરી પ્રયત્ન કરે છે."""
    for i in range(tries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            return response.text
        except Exception as e:
            if ("503" in str(e) or "429" in str(e)) and i < tries - 1:
                time.sleep(2 * (i + 1))
                continue
            raise


def ask_gemini(prompt: str, tries: int = 3) -> str:
    """સાદો ટેક્સ્ટ પ્રશ્ન."""
    return _call_gemini(prompt, tries)


def generate_ai_response(message: str, language: str = "gu", history=None) -> str:
    """ai.py આ ફંક્શન બોલાવે છે. history = [{"role": "user"/"model", "text": "..."}]"""
    lang = LANGUAGE_NAMES.get(language, "ગુજરાતી")

    contents = []
    for turn in (history or [])[-MAX_HISTORY_TURNS:]:
        role = "model" if turn.get("role") == "model" else "user"
        text = (turn.get("text") or "").strip()[:MAX_TURN_CHARS]
        if text:
            contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=text)])
            )

    # વાતચીત હંમેશા user ના સંદેશાથી શરૂ થવી જોઈએ
    while contents and contents[0].role == "model":
        contents.pop(0)

    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=f"{message}\n\n(જવાબ {lang} ભાષામાં આપો.)")],
        )
    )
    return _call_gemini(contents)


def analyze_crop_image(image_bytes: bytes, mime_type: str = "image/jpeg", question: str = "") -> str:
    """પાકના ફોટા પરથી રોગની ઓળખ."""
    prompt = IMAGE_PROMPT
    if question:
        prompt += f"\nખેડૂતનો પ્રશ્ન: {question}"

    contents = [
        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
        prompt,
    ]
    return _call_gemini(contents)