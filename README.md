# KisanMitra AI 🌾

AI-powered assistant for farmers. Farmers can ask crop questions in Gujarati and
upload a photo of a plant leaf to get a likely disease/pest diagnosis, powered by
Google Gemini.

## Features

- **AI chat** in Gujarati (also Hindi / English) with simple, practical farming advice
- **Conversation memory**: the app sends recent messages so follow-up questions make sense
- **Crop disease diagnosis** from a leaf photo (JPG, PNG, WEBP, up to 5 MB)
- **Login required**: AI endpoints need a valid token, so only registered users can use them
- **Safety rules**: the AI does not give exact pesticide doses; it tells farmers to read the
  product label and contact a local agriculture officer or KVK

## Tech stack

FastAPI, SQLAlchemy (SQLite), JWT auth (python-jose, passlib + bcrypt), Google Gemini (`google-genai`)

## Project structure

```
KisanMitra-AI/
├── .env                 # your secret keys (NOT in Git)
└── backend/
    ├── main.py          # app entry point
    ├── requirements.txt
    ├── api/             # routes: auth.py, ai.py, deps.py, profile.py
    ├── services/        # ai_service.py (Gemini), security.py (passwords, tokens)
    ├── database/        # database setup
    └── models/          # database models
```

## Setup

**1. Clone and create a virtual environment**

```
git clone https://github.com/vijaydarbar449-cyber/KisanMitra-AI.git
cd KisanMitra-AI
python -m venv venv
venv\Scripts\activate
```

**2. Install dependencies**

```
python -m pip install -r backend\requirements.txt
```

> `bcrypt` is pinned to `4.0.1` on purpose. Newer versions break `passlib`.

**3. Add your Gemini API key**

Get a key at https://aistudio.google.com/api-keys, then create a file named `.env`
in the project root (next to the `backend` folder):

```
GEMINI_API_KEY=your_key_here
```

Never commit `.env` and never share your key.

**4. Run the server** (from inside the `backend` folder)

```
cd backend
python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive API docs.

## API usage

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/auth/register` | No | Create an account (JSON body) |
| POST | `/api/v1/auth/login` | No | Get an access token (form: `username` = email, `password`) |
| POST | `/api/v1/ai/chat` | Bearer token | Ask a farming question |
| POST | `/api/v1/ai/diagnose` | Bearer token | Upload a leaf photo for diagnosis |

**Register**

```json
{"name": "Test User", "email": "test@example.com", "password": "Test@12345"}
```

**Chat** (send `Authorization: Bearer <token>`)

```json
{
  "message": "તેનો ઉપાય શું?",
  "language": "gu",
  "history": [
    {"role": "user", "text": "મારા ટામેટાંમાં સફેદ માખી આવી છે"},
    {"role": "model", "text": "સફેદ માખી ટામેટાંનો રસ ચૂસે છે."}
  ]
}
```

`history` is optional (up to 20 earlier messages; roles are `user` or `model`).

**Diagnose**: `multipart/form-data` with `image` (file) and optional `question` (text).

**Using the token in `/docs`**: call `/auth/login`, copy `access_token`, click **Authorize**,
and paste it in the **HTTPBearer** field (without the word `Bearer`).

## Security notes

- Keep `.env` out of Git (it is in `.gitignore`)
- Do not send passwords in URLs; `register` takes a JSON body
- AI answers are guidance only. For serious crop problems, farmers should contact the
  nearest Krishi Vigyan Kendra (KVK) or local agriculture officer

## Roadmap

- Frontend / mobile app
- Save chat history per user
- More languages