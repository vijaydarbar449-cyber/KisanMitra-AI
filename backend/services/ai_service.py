import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai


# Find project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Load .env from KisanMitra-AI folder
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)


# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        f"GEMINI_API_KEY not found. Check your .env file: {ENV_FILE}"
    )


# Create Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_ai_response(
    message: str,
    language: str = "gu"
) -> str:

    if language == "gu":
        instruction = """
        તમે KisanMitra AI છો.

        તમે ખેડૂતો માટે ગુજરાતી ભાષામાં સરળ,
        ઉપયોગી અને વ્યવહારુ ખેતી સલાહ આપતા AI assistant છો.

        તમે પાક, રોગ, જીવાત, પાણી, સિંચાઈ,
        ખેતી પદ્ધતિઓ અને સરકારી યોજનાઓ અંગે
        સામાન્ય માર્ગદર્શન આપી શકો છો.

        જવાબ સરળ ગુજરાતી ભાષામાં આપો.
        ખેડૂતને સરળતાથી સમજાય તેવી રીતે જવાબ આપો.
        """

    else:
        instruction = """
        You are KisanMitra AI.

        You provide simple, useful and practical
        agricultural guidance for farmers.

        You can help with crops, diseases, pests,
        irrigation, farming methods and general
        government scheme guidance.

        Give clear and practical answers.
        """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
{instruction}

User question:
{message}
"""
    )

    return response.text