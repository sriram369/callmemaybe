# Swaram - Multilingual Voice Chat Application

A real-time voice-to-voice conversational AI application powered by Sarvam AI, enabling natural hands-free conversations across 11+ Indian languages.

## Features

- **Continuous Conversation** - Click once to start, speak naturally back-and-forth like a phone call
- **Adaptive Silence Detection** - Auto-calibrates to your environment's background noise for reliable auto-stop
- **Smart Farewell Detection** - Say "bye" or "goodbye" to naturally end the conversation
- **Speech-to-Text** - Powered by Sarvam's Saarika v2.5 model
- **AI Chat** - Conversational responses via Sarvam-m language model
- **Text-to-Speech** - Natural voice responses using Sarvam's Bulbul v2
- **11+ Indian Languages** - Hindi, English, Bengali, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu, Gujarati
- **Customizable AI Personality** - Master prompt system via `system_prompt.py` for easy behavior customization
- **Clean White & Blue UI** - Minimalist design with Instrument Serif typography

## Tech Stack

- **Backend**: Python, FastAPI, httpx
- **Frontend**: Vanilla JavaScript, Web Audio API
- **AI/ML**: Sarvam AI APIs (STT, Chat Completions, TTS)
- **Voice Detection**: RMS-based adaptive silence detection with dynamic threshold calibration
- **Deployment**: Vercel

## How It Works

```
User speaks → STT (Speech-to-Text) → AI Chat (Sarvam-m) → TTS (Text-to-Speech) → User hears response
                                          ↑                                              |
                                          └──────── Continuous conversation loop ─────────┘
```

## Conversation Flow

1. Click the orb once to start
2. Stay quiet for 0.5s (background noise calibration)
3. Speak naturally in your preferred language
4. Stop speaking - auto-detects silence after 1.2 seconds
5. AI responds with voice
6. Automatically starts listening for your next turn (hands-free)
7. Say "bye" to end, or click the orb to stop manually

## Project Structure

```
Swaram-Trial/
├── main.py              # FastAPI backend - API endpoints (STT, Chat, TTS)
├── system_prompt.py     # Master prompt configuration - AI personality & behavior
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel deployment configuration
├── .env                 # API keys (not committed to git)
├── .env.example         # Environment variable template
├── .gitignore           # Git ignore rules
└── static/
    └── index.html       # Frontend - UI, orb, voice detection, conversation logic
```

## Local Development

### Prerequisites

- Python 3.8+
- Sarvam API Key ([Get one here](https://dashboard.sarvam.ai/admin))

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sriram369/callmemaybe.git
   cd callmemaybe
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```bash
   cp .env.example .env
   ```
   Then add your Sarvam API key to `.env`:
   ```
   SARVAM_API_KEY=your_actual_api_key_here
   ```

5. Run the server:
   ```bash
   export SARVAM_API_KEY=your_actual_api_key_here
   python3 -m uvicorn main:app --reload
   ```

6. Open your browser to `http://localhost:8000`

## Deployment to Vercel

1. Push your code to GitHub

2. Go to [Vercel](https://vercel.com) and sign in with GitHub

3. Click "Add New Project" and import your repository

4. Configure environment variables:
   - Add `SARVAM_API_KEY` with your API key value

5. Deploy!

## Customizing the AI Personality

Edit `system_prompt.py` to change Swaram's behavior:

- **Personality** - Modify tone, style, and approach
- **Response length** - Adjust `max_tokens` in `CHAT_CONFIG`
- **Creativity** - Tune `temperature` (0.0 = consistent, 1.0 = creative)
- **Specialization** - Add domain-specific instructions
- **Language behavior** - Control how it handles multilingual conversations

## Supported Languages

| Language | Code |
|----------|------|
| Hindi | hi-IN |
| English (India) | en-IN |
| Bengali | bn-IN |
| Kannada | kn-IN |
| Malayalam | ml-IN |
| Marathi | mr-IN |
| Odia | od-IN |
| Punjabi | pa-IN |
| Tamil | ta-IN |
| Telugu | te-IN |
| Gujarati | gu-IN |

## Voice Options

| Voice | Gender |
|-------|--------|
| Anushka | Female |
| Bhumi | Female |
| Meera | Female |
| Arvind | Male |

## Technical Highlights

- **Adaptive Silence Detection**: Calibrates background noise in first 500ms, sets dynamic threshold (backgroundNoise + 0.02) for reliable speech/silence detection in any environment
- **25-Second Safety Limit**: Prevents exceeding Sarvam's 30-second audio limit
- **State Machine Architecture**: IDLE → LISTENING → PROCESSING → SPEAKING with clean transitions
- **Continuous Conversation Loop**: Auto-starts listening after AI responds, with smart farewell detection to break the loop
- **Master Prompt System**: Separate configuration file for easy AI personality customization without touching core code

## License

MIT
