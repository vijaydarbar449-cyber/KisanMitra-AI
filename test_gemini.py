import os
from dotenv import load_dotenv
from google import genai

print("env file found:", load_dotenv(".env", override=True))
print("key loaded:", bool(os.environ.get("GEMINI_API_KEY")))

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="ટામેટાંના છોડમાં પાંદડા પીળા પડે તો શું કરવું? ટૂંકમાં ગુજરાતીમાં કહો.",
)
print(response.text)
