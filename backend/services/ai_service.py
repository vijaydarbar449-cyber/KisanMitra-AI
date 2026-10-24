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


def ask_gemini(prompt: str, tries: int = 3) -> str:
    """Gemini ને પ્રશ્ન પૂછે છે. 503/429 (ભીડ) આવે તો ફરી પ્રયત્ન કરે છે."""
    for i in range(tries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            return response.text
        except Exception as e:
            if ("503" in str(e) or "429" in str(e)) and i < tries - 1:
                time.sleep(2 * (i + 1))
                continue
            raise


def generate_ai_response(message: str, language: str = "gu") -> str:
    """ai.py આ ફંક્શન બોલાવે છે. ભાષા મુજબ જવાબ આપે છે."""
    lang = LANGUAGE_NAMES.get(language, "ગુજરાતી")
    prompt = f"{message}\n\n(જવાબ {lang} ભાષામાં આપો.)"
    return ask_gemini(prompt)