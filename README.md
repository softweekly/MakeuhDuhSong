# 🎭 Parody Song Creator - Creative Tool

A comprehensive creative tool for writing parody songs with AI assistance, built for comedy songwriters and content creators.

## � Important: ElevenLabs Policy Compliance

**Music generation is limited by ElevenLabs policies** - we cannot create backing tracks that sound like specific copyrighted songs or reference artists by name. However, **all lyric writing features work perfectly!**

- ✅ **Full AI lyric assistance** for writing parodies
- ✅ **Song structure analysis** and rhythm matching  
- ✅ **Original backing tracks** in appropriate styles
- ❌ **Cannot imitate specific songs** or artists by name

See [ELEVENLABS_POLICY_COMPLIANCE.md](ELEVENLABS_POLICY_COMPLIANCE.md) for complete details.

## �🚀 Quick Start
### 🆕 NEW USERS - Start Here!
**First time using this tool?** Check out our comprehensive [**BEGINNER_GUIDE.md**](BEGINNER_GUIDE.md) for:
- Complete setup walkthrough
- API key configuration help
- Step-by-step first parody creation
- Troubleshooting common issues
- Tips for great results

### Experienced Users - Quick Setup
### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Copy `.env` file and add your API keys:
- Get ElevenLabs API key from [elevenlabs.io](https://elevenlabs.io)
- Get OpenAI API key from [openai.com](https://openai.com)

**⚠️ Important:** Read [ELEVENLABS_POLICY_COMPLIANCE.md](ELEVENLABS_POLICY_COMPLIANCE.md) for music generation limitations.

### 3. Run the Tool
```bash
python parody_song_creator.py
```

## 🎯 Features

### Core Creative Tools
- **Original Song Analysis**: AI analyzes song structure, rhyme schemes, and patterns
- **Parody Idea Generation**: Get creative concepts based on your topic
- **Lyric Writing Assistant**: AI helps write lyrics while preserving rhythm and rhyme
- **Interactive Refinement**: Iteratively improve lyrics with AI feedback
- **Music Generation**: Create backing tracks using ElevenLabs
- **Vocal Guides**: Generate spoken versions of your lyrics

### Project Management
- **Save/Load Projects**: Organize your parody songs
- **Version Control**: Track changes and iterations
- **Audio Export**: Generate MP3 files for your creations

### Workflow Features
- **Structure Preservation**: Maintains original song's rhythm and flow
- **Rhyme Scheme Matching**: Keeps rhymes consistent with original
- **Syllable Counting**: Ensures lyrics fit the melody
- **Multiple Ideas**: Generate various concepts to choose from

## 🎵 How to Use

### Creating Your First Parody

1. **Start the Program**
   ```bash
   python parody_song_creator.py
   ```

2. **Choose "Create New Parody"**
   - Enter the original song title and artist
   - Describe what your parody is about
   - Paste the original lyrics

3. **AI Analysis**
   - The tool analyzes the song structure
   - Identifies rhyme patterns and rhythm
   - Suggests parody angles

4. **Select Your Concept**
   - Choose from AI-generated ideas
   - Or describe your own concept

5. **Generate Lyrics**
   - AI writes parody lyrics matching the original structure
   - Review and refine as needed
   - Make iterative improvements

6. **Create Audio**
   - Generate backing track
   - Create vocal guide (optional)
   - Export as MP3 files

### Project Organization
```
parody_projects/
├── my_funny_song/
│   ├── project.json          # Project data and metadata
│   ├── parody_lyrics.txt     # Final lyrics
│   ├── backing_track.mp3     # Generated music
│   └── vocal_guide.mp3       # Spoken lyrics guide
└── another_parody/
    ├── project.json
    └── ...
```

## 🛠️ Advanced Usage

### Custom Voice Settings
Edit `.env` to use different voices:
```
DEFAULT_VOICE_ID=your_preferred_voice_id
```

### Music Style Customization
Modify `SongStructure` in your projects to change:
- Genre and instrumentation
- Tempo and key
- Mood and style

### Batch Processing
For multiple parodies, you can extend the CLI or create scripts that use the `ParodyCreator` class directly.

## 🎭 Example Workflow

```python
from parody_song_creator import ParodyCreator

creator = ParodyCreator()

# Analyze original song
analysis = creator.analyze_original_song(
    lyrics="...", 
    title="Original Song", 
    artist="Original Artist"
)

# Generate parody
parody_lyrics = creator.create_parody_lyrics(
    original_lyrics="...",
    concept="Make it about coding",
    rhyme_scheme=analysis["rhyme_scheme"]
)

# Create music
song_structure = creator.create_song_structure(
    title="My Code Parody",
    original_artist="Original Artist", 
    original_title="Original Song",
    genre="comedy"
)

music_data = creator.generate_music_track(song_structure, parody_lyrics)
```

## 🔧 Configuration Options

### Environment Variables
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key
- `OPENAI_API_KEY`: Your OpenAI API key
- `DEFAULT_VOICE_ID`: Voice for speech generation
- `DEFAULT_MUSIC_LENGTH`: Length of generated tracks (ms)

### Customizable Parameters
- **Music Length**: Adjust preview length (default: 30 seconds)
- **Voice Models**: Choose different ElevenLabs voices
- **AI Models**: Switch between different OpenAI models
- **Project Storage**: Change where projects are saved

## 🚀 Future Expansion (AI Agent System)

This creative tool is designed to evolve into a full AI agent system:

### Planned Features
- **Auto-Publishing**: Direct upload to platforms
- **Content Scheduling**: Automated release timing
- **Trend Analysis**: AI-powered topic suggestions
- **Multi-Format Export**: Video, audio, lyrics, sheet music
- **Collaboration Tools**: Multi-user project sharing
- **Voice Cloning**: Custom voice training
- **Live Performance**: Real-time generation for shows

### Architecture Ready for Agents
The modular design allows easy integration of:
- Web dashboard for remote control
- API endpoints for external systems
- Database integration for large-scale projects
- Machine learning pipeline for improvement
- Integration with your steeltoepia.com site

## 📝 Tips for Great Parodies

### Content Strategy
1. **Know Your Audience**: Match humor to your target demographic
2. **Current Events**: Reference trending topics for relevance
3. **Universal Themes**: Work, relationships, technology work well
4. **Respect Boundaries**: Keep content appropriate and fun

### Technical Tips
1. **Syllable Matching**: Count syllables carefully for natural flow
2. **Rhyme Consistency**: Maintain the original's rhyme scheme
3. **Rhythm Preservation**: Test by singing along to the original
4. **Hook Placement**: Put your best lines in the chorus

### Creative Process
1. **Start with Concept**: Have a clear comedic angle
2. **List Key Terms**: Brainstorm topic-related vocabulary
3. **Match Phrases**: Find words that fit the original's rhythm
4. **Test and Refine**: Sing it back and adjust as needed

## 🔍 Troubleshooting

### Common Issues
- **API Errors**: Check your API keys in `.env`
- **Audio Generation Fails**: Verify ElevenLabs credits
- **Lyrics Don't Match Rhythm**: Try the refinement feature
- **Project Won't Save**: Check file permissions

### Getting Help
- Review your API key setup
- Check the console for error messages
- Verify internet connection for AI services
- Test with a simple, well-known song first

## 📈 Analytics & Improvement

Track your parody success:
- Save audience feedback in project notes
- Note which concepts work best
- Track rhyme schemes that flow naturally
- Build a personal style guide over time

---

**Ready to create hilarious parodies? Start with `python parody_song_creator.py` and let your creativity flow!** 🎵🎭