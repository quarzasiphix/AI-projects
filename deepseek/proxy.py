from fastapi import FastAPI, Request
import requests
import json
from fastapi.responses import StreamingResponse

app = FastAPI()

OLLAMA_URL = "http://127.0.0.1:11434"

def stream_ollama_response(data):
    """ Stream only the 'response' field from Ollama, keeping <think> intact. """
    buffer = ""  # Store streamed text before sending

    with requests.post(f"{OLLAMA_URL}/api/generate", json=data, stream=True) as response:
        for chunk in response.iter_lines(decode_unicode=True):  # ✅ Ensure proper UTF-8 decoding
            if chunk:
                try:
                    # Parse JSON chunk
                    json_data = json.loads(chunk)
                    response_text = json_data.get("response", "").strip()

                    # Store response
                    buffer += response_text

                    # Only send non-empty responses
                    if buffer:
                        yield buffer + "\n"
                        buffer = ""  # Reset buffer after sending

                except json.JSONDecodeError:
                    continue  # Ignore broken JSON parts

@app.post("/api/generate")
async def generate(request: Request):
    data = await request.json()
    return StreamingResponse(stream_ollama_response(data), media_type="text/plain")
