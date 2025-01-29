from fastapi import FastAPI, Request
import requests

app = FastAPI()

OLLAMA_URL = "http://127.0.0.1:11434"

@app.post("/api/generate")
async def generate(request: Request):
    # Read incoming JSON request
    data = await request.json()

    # Forward request to Ollama
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=data)
    response_data = response.json()

    # Extract only the "response" field (ignoring everything else)
    think_response = response_data.get("response", "No response received.")

    return {"response": think_response}
