import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

# ---- COMPOSITION PLAN ----
composition_plan = """
Title: Midnight Signals
Genre: Synth-pop, electronic
Mood: Nostalgic, late-night, emotional
Tempo: 100 BPM
Key: A minor

Structure:
Intro, Verse, Pre-Chorus, Chorus, Verse, Chorus, Bridge, Chorus, Outro

Instrumentation:
Analog synth bass, soft electronic drums, atmospheric pads, pluck lead

Vocal Style:
Breathy, intimate, emotional, layered harmonies in chorus

Lyrics:

[Verse 1]
City lights are flickering in broken lines
Static whispers through the satellites
Driving slow with nowhere left to go
Just your voice on the radio

[Pre-Chorus]
And I know you're miles away
But it feels like yesterday
Every signal that I chase
Leads me back into your space

[Chorus]
We were midnight signals in the dark
Burning bright but falling all apart
Every word we never got to say
Echoes through the static anyway
We were just a frequency
Lost in endless memory
Calling out across the night
Fading into neon light

[Verse 2]
Rearview mirror shows a ghost of you
Every street feels like déjà vu
Turn the dial but all I ever find
Is your echo running through my mind

[Bridge]
If I could rewrite the sound
Turn the silence inside out
Would you hear me calling still
Through the noise, beyond the thrill?

[Outro]
(midnight signals fading...)
"""

# ---- GENERATION CALL ----
# NOTE: This uses a generic "generate" pattern.
# The exact method name may differ depending on your SDK version.

audio = client.text_to_speech.convert(
    voice_id="EXAVITQu4vr4xnSDxMaL",  # replace with a voice you like
    model_id="eleven_multilingual_v2",
    text=composition_plan,
)

# ---- SAVE OUTPUT ----
save(audio, "midnight_signals.mp3")

print("Audio saved as midnight_signals.mp3")