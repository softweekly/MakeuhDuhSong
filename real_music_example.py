#!/usr/bin/env python3
"""
Real Music Generation Example
This demonstrates actual music generation (not just voice narration)
"""

import os
from dotenv import load_dotenv
from parody_song_creator import ParodyCreator, SongStructure

load_dotenv()

# Create the parody creator instance
creator = ParodyCreator()

# Define a song structure for music generation
song_structure = SongStructure(
    title="Comedy Backing Track",
    original_artist="Generic",
    original_title="Test Song",
    genre="comedy",
    tempo=120,
    key="C major",
    mood=["upbeat", "playful", "comedic"],
    structure=["intro", "verse", "chorus", "verse", "chorus", "outro"],
    instrumentation={
        "primary": "acoustic guitar",
        "rhythm": "light drums", 
        "bass": "upbeat bass",
        "extra": "piano accents"
    },
    vocal_style={
        "style": "spoken comedy",
        "tempo": "moderate"
    }
)

# Set up music generation options
music_options = {
    'length_ms': 30000,  # 30 seconds
    'use_composition_plan': True,
    'include_vocals': False,  # Instrumental only
    'style': 'comedic'
}

print("🎼 Generating REAL MUSIC (not just voice)...")
print("=" * 50)
print(f"Title: {song_structure.title}")
print(f"Genre: {song_structure.genre}")
print(f"Tempo: {song_structure.tempo} BPM")
print(f"Length: 30 seconds")
print("=" * 50)

try:
    # Generate actual music track
    music_data = creator.generate_music_track(
        song_structure=song_structure, 
        advanced_options=music_options
    )
    
    if music_data:
        # Save the actual music file
        with open("real_music_example.mp3", "wb") as f:
            f.write(music_data)
        print("✅ SUCCESS: Real music generated and saved as 'real_music_example.mp3'")
        print("🎵 This contains actual instruments and music composition!")
    else:
        print("❌ Music generation failed - no data returned")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nThis might be because:")
    print("1. ElevenLabs Music API requires a paid subscription")
    print("2. The API key doesn't have music generation permissions")
    print("3. ElevenLabs Music API may not be available in your region")
    print("\nThe text-to-speech feature (what worked before) is different from music generation")