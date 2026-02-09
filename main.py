import os
import base64
import logging
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import httpx
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Swaram")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sarvam API Configuration
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
if not SARVAM_API_KEY:
    logger.warning("SARVAM_API_KEY environment variable not set!")

SARVAM_BASE_URL = "https://api.sarvam.ai"

# Pydantic models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    language_code: str = "hi-IN"

class TTSRequest(BaseModel):
    text: str
    language_code: str = "hi-IN"
    speaker: str = "Anushka"

@app.post("/api/stt")
async def speech_to_text(file: UploadFile = File(...), language_code: str = Form("unknown")):
    """
    Convert speech to text using Sarvam API
    """
    print(f"--> STT Request Received: {file.filename}, language: {language_code}")
    if not SARVAM_API_KEY:
        raise HTTPException(status_code=500, detail="Server misconfiguration: API Key missing")

    url = f"{SARVAM_BASE_URL}/speech-to-text"
    headers = {"api-subscription-key": SARVAM_API_KEY}
    
    # Read file content
    file_content = await file.read()
    print(f"    File size: {len(file_content)} bytes")
    
    # Prepare multipart data
    files = {
        "file": (file.filename, file_content, file.content_type)
    }
    data = {
        "model": "saarika:v2.5",
        "language_code": language_code
    }

    async with httpx.AsyncClient() as client:
        try:
            print("    Sending request to Sarvam STT...")
            response = await client.post(url, headers=headers, files=files, data=data, timeout=30.0)
            print(f"    Sarvam STT Response Status: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            print(f"    STT Result: {result}")
            return result
        except httpx.HTTPStatusError as e:
            logger.error(f"Sarvam STT API error: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Sarvam API error: {e.response.text}")
        except Exception as e:
            logger.error(f"STT error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_completion(request: ChatRequest):
    """
    Get chat completion from Sarvam API
    """
    print(f"--> Chat Request Received: {len(request.messages)} messages")
    if not SARVAM_API_KEY:
        raise HTTPException(status_code=500, detail="Server misconfiguration: API Key missing")

    url = f"{SARVAM_BASE_URL}/v1/chat/completions"
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Construct system prompt if not present or ensure it guides the model correctly
    system_prompt = {
        "role": "system",
        "content": "You are a helpful conversational assistant. Respond in the same language the user speaks. Keep responses concise (1-3 sentences) since they will be spoken aloud."
    }
    
    original_messages = [msg.dict() for msg in request.messages]
    
    # Ensure system prompt is first
    if not original_messages or original_messages[0]["role"] != "system":
        messages = [system_prompt] + original_messages
    else:
        messages = original_messages

    payload = {
        "model": "sarvam-m",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 300
    }

    async with httpx.AsyncClient() as client:
        try:
            print("    Sending request to Sarvam Chat...")
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            print(f"    Sarvam Chat Response Status: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            # Extract content for easier frontend consumption
            content = result["choices"][0]["message"]["content"]
            print(f"    Chat Reply: {content}")
            return {"reply": content, "raw": result}
        except httpx.HTTPStatusError as e:
            logger.error(f"Sarvam Chat API error: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Sarvam API error: {e.response.text}")
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech using Sarvam API
    """
    print(f"--> TTS Request Received: {request.text[:50]}...")
    if not SARVAM_API_KEY:
        raise HTTPException(status_code=500, detail="Server misconfiguration: API Key missing")

    url = f"{SARVAM_BASE_URL}/text-to-speech"
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": request.text[:1499], # Use slicing to strictly enforce limit
        "target_language_code": request.language_code,
        "speaker": request.speaker.lower(), # Ensure speaker is lowercase for Sarvam API (e.g. "Anushka" -> "anushka")
        "model": "bulbul:v2",
        "enable_preprocessing": True
    }

    async with httpx.AsyncClient() as client:
        try:
            print(" Sending request to Sarvam TTS...")
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            print(f"    Sarvam TTS Response Status: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            if "audios" in result and len(result["audios"]) > 0:
                print("    TTS Audio received")
                return {"audio_base64": result["audios"][0]}
            else:
                raise HTTPException(status_code=500, detail="No audio returned from Sarvam API")
        except httpx.HTTPStatusError as e:
            logger.error(f"Sarvam TTS API error: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Sarvam API error: {e.response.text}")
        except Exception as e:
            logger.error(f"TTS error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")
