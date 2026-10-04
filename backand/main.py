from fastapi import FastAPI

app = FastAPI(
    title="KisanMitra AI",
    description="AI Rural Decision Assistant",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "project": "KisanMitra AI",
        "message": "AI Rural Decision Assistant is running",
        "status": "success"
    }