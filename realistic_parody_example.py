#!/usr/bin/env python3
"""
Realistic Parody Creator - Voice-Only Version
What we can actually do with ElevenLabs today
"""

import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Example parody lyrics (based on "Twinkle, Twinkle, Little Star")
parody_lyrics = """
Meowing, meowing, at three AM,
How you love to wake up them.
Standing on my chest so high,
Like a furry dictator in the sky.
Meowing, meowing, won't you please,
Let me sleep just five more ZZZs!
"""

print("🎤 Creating voice performance of parody lyrics...")

# Generate spoken/sung version of the parody
audio = client.text_to_speech.convert(
    voice_id="EXAVITQu4vr4xnSDxMaL",  # You can try different voice IDs
    model_id="eleven_multilingual_v2",
    text=parody_lyrics,
)

# Save the vocal guide
save(audio, "cat_parody_vocal_guide.mp3")

print("✅ Vocal guide saved as: cat_parody_vocal_guide.mp3")
print("🎯 This is what ElevenLabs can actually do - high quality voice!")
print("💡 You can sing along to this to learn your parody!")