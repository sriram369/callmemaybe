# CallMeMaybe - Voice Chat Application

A multilingual voice chat application powered by Sarvam AI APIs, supporting Hindi, English, Bengali, and more Indian languages.

## Features

- 🎤 **Speech-to-Text**: Convert speech to text using Sarvam's Saarika v2.5 model
- 💬 **AI Chat**: Natural conversations with Sarvam's language model
- 🔊 **Text-to-Speech**: Natural-sounding voice responses with multiple speaker options
- 🌐 **Multilingual**: Support for 10+ Indian languages
- ⚡ **Real-time**: Fast, responsive voice interactions

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla JavaScript with Web Audio API
- **AI**: Sarvam AI APIs (STT, Chat, TTS)
- **Deployment**: Vercel

## Local Development

### Prerequisites

- Python 3.8+
- Sarvam API Key ([Get one here](https://www.sarvam.ai/))

### Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd Swaram-Trial
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```bash
   cp .env.example .env
   ```
   Then add your Sarvam API key to `.env`:
   ```
   SARVAM_API_KEY=your_actual_api_key_here
   ```

4. Run the server:
   ```bash
   python3 -m uvicorn main:app --reload
   ```

5. Open your browser to `http://localhost:8000`

## Deployment to Vercel

1. Push your code to GitHub (see instructions below)

2. Go to [Vercel](https://vercel.com) and sign in with GitHub

3. Click "Add New Project" and import your repository

4. Configure environment variables:
   - Add `SARVAM_API_KEY` with your API key value

5. Deploy! Vercel will automatically detect the Python app and deploy it

## Pushing to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Voice chat application"

# Create a new repository on GitHub, then:
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

## Usage

1. Click the orb to start speaking
2. Speak your message in your chosen language
3. Click again to manually stop recording (or wait for auto-silence detection)
4. The AI will respond with voice

## Supported Languages

- Hindi (hi-IN)
- English India (en-IN)
- Bengali (bn-IN)
- Kannada (kn-IN)
- Malayalam (ml-IN)
- Marathi (mr-IN)
- Odia (od-IN)
- Punjabi (pa-IN)
- Tamil (ta-IN)
- Telugu (te-IN)
- Gujarati (gu-IN)

## Voice Options

- Anushka (Female)
- Bhumi (Female)
- Meera (Female)
- Arvind (Male)

## Known Issues

- Auto-silence detection may not work reliably in noisy environments - use manual click to stop recording

## License

MIT
