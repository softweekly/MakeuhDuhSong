#!/usr/bin/env python3
"""
Parody Song Creator - Creative Tool for Songwriting
A comprehensive tool for creating parody songs with AI assistance
"""

import os
import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import openai
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from dotenv import load_dotenv

load_dotenv()

@dataclass
class SongStructure:
    """Data class for song structure"""
    title: str
    original_artist: str
    original_title: str
    genre: str
    tempo: int
    key: str
    mood: List[str]
    structure: List[str]
    instrumentation: Dict[str, str]
    vocal_style: Dict[str, any]
    
@dataclass
class LyricSection:
    """Data class for lyric sections"""
    section_type: str
    original_lyrics: List[str]
    parody_lyrics: List[str]
    rhyme_scheme: str
    syllable_count: List[int]

class ParodyCreator:
    """Main class for creating parody songs"""
    
    def __init__(self):
        self.elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.projects_dir = Path("parody_projects")
        self.projects_dir.mkdir(exist_ok=True)
        
    def analyze_original_song(self, lyrics: str, title: str, artist: str) -> Dict:
        """Analyze original song structure and patterns"""
        print(f"🔍 Analyzing '{title}' by {artist}...")
        
        # Use AI to analyze song structure
        analysis_prompt = f"""
        Analyze this song for parody creation. Provide:
        1. Song structure (verse, chorus, bridge, etc.)
        2. Rhyme scheme for each section
        3. Syllable patterns
        4. Key themes and concepts
        5. Memorable phrases or hooks
        6. Suggested parody angles

        Song: "{title}" by {artist}
        Lyrics:
        {lyrics}
        
        Return as structured JSON.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.3
        )
        
        try:
            analysis = json.loads(response.choices[0].message.content)
        except:
            # Fallback to basic analysis
            analysis = self._basic_song_analysis(lyrics)
            
        return analysis
    
    def _basic_song_analysis(self, lyrics: str) -> Dict:
        """Basic song analysis fallback"""
        sections = re.split(r'\n\s*\n', lyrics.strip())
        return {
            "structure": ["verse", "chorus"] * (len(sections) // 2),
            "sections": sections,
            "suggested_themes": ["humor", "satire", "current events"]
        }
    
    def generate_parody_ideas(self, original_analysis: Dict, topic: str, style: str = "humorous") -> List[str]:
        """Generate parody concept ideas"""
        print(f"💡 Generating parody ideas for topic: {topic}")
        
        idea_prompt = f"""
        Create 5 creative parody ideas for this song based on the topic "{topic}".
        
        Original song analysis: {json.dumps(original_analysis, indent=2)}
        
        Style: {style}
        
        For each idea, provide:
        1. Main concept/angle
        2. Key themes to replace
        3. Sample hook line
        4. Difficulty level (1-10)
        
        Make them creative but respectful.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": idea_prompt}],
            temperature=0.7
        )
        
        return response.choices[0].message.content.split('\n\n')
    
    def create_parody_lyrics(self, original_lyrics: str, concept: str, 
                           rhyme_scheme: Dict, preserve_structure: bool = True) -> str:
        """Generate parody lyrics with structure preservation"""
        print(f"✍️ Writing parody lyrics with concept: {concept}")
        
        lyrics_prompt = f"""
        Create parody lyrics based on this concept: "{concept}"
        
        Original lyrics:
        {original_lyrics}
        
        Requirements:
        1. {'Preserve exact syllable count and rhythm' if preserve_structure else 'Maintain general flow'}
        2. Keep the rhyme scheme: {rhyme_scheme}
        3. Make it funny but appropriate
        4. Ensure singability
        5. Replace key words/phrases while keeping the structure
        
        Return only the parody lyrics, formatted like the original.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": lyrics_prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content.strip()
    
    def refine_lyrics_section(self, section: str, feedback: str) -> str:
        """Refine specific lyrics section based on feedback"""
        refinement_prompt = f"""
        Improve this lyric section based on the feedback:
        
        Current lyrics:
        {section}
        
        Feedback: {feedback}
        
        Provide an improved version that addresses the feedback while maintaining rhythm and rhyme.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": refinement_prompt}],
            temperature=0.6
        )
        
        return response.choices[0].message.content.strip()
    
    def create_song_structure(self, title: str, original_artist: str, 
                            original_title: str, genre: str) -> SongStructure:
        """Create song structure object"""
        return SongStructure(
            title=title,
            original_artist=original_artist,
            original_title=original_title,
            genre=genre,
            tempo=120,  # Default, can be customized
            key="C major",  # Default, can be customized
            mood=["humorous", "energetic"],
            structure=["intro", "verse", "chorus", "verse", "chorus", "bridge", "chorus", "outro"],
            instrumentation={
                "drums": "acoustic",
                "bass": "electric",
                "guitar": "acoustic rhythm",
                "lead": "vocal"
            },
            vocal_style={
                "style": "expressive",
                "effects": ["reverb"],
                "harmonies": False
            }
        )
    
    def generate_music_track(self, song_structure: SongStructure, lyrics: str = "", advanced_options: Dict = None) -> bytes:
        """Generate music track using ElevenLabs Music API (Policy Compliant)"""
        print(f"🎵 Generating music for '{song_structure.title}'...")
        
        # Get advanced options or use defaults
        options = advanced_options or {}
        music_length = options.get('length_ms', 60000)  # Default 60 seconds
        use_composition_plan = options.get('use_composition_plan', True)
        include_vocals = options.get('include_vocals', False)
        
        try:
            if use_composition_plan:
                return self._generate_with_composition_plan(song_structure, lyrics, options)
            else:
                return self._generate_with_simple_prompt(song_structure, options)
                
        except Exception as e:
            print(f"⚠️ Music generation failed: {e}")
            # Check if it's a policy violation
            if hasattr(e, 'body') and e.body and 'detail' in e.body:
                if e.body['detail'].get('status') == 'bad_prompt':
                    print("🚨 Policy violation detected - using generic fallback")
                    return self._generate_generic_music_track(song_structure, options)
            return b""
    
    def _generate_with_composition_plan(self, song_structure: SongStructure, lyrics: str, options: Dict) -> bytes:
        """Generate music using detailed composition plan"""
        print("🎼 Creating detailed composition plan...")
        
        # Create composition plan based on song structure
        composition_plan_prompt = self._create_composition_plan_prompt(song_structure, lyrics, options)
        
        try:
            # Generate composition plan first
            composition_plan = self.elevenlabs.music.composition_plan.create(
                prompt=composition_plan_prompt,
                music_length_ms=options.get('length_ms', 60000)
            )
            
            print("🎶 Generating music from composition plan...")
            
            # Generate music from the plan
            track = self.elevenlabs.music.compose(
                composition_plan=composition_plan
            )
            
            audio_data = b""
            for chunk in track:
                audio_data += chunk
                
            return audio_data
            
        except Exception as e:
            print(f"⚠️ Composition plan failed, trying simple prompt: {e}")
            return self._generate_with_simple_prompt(song_structure, options)
    
    def _generate_with_simple_prompt(self, song_structure: SongStructure, options: Dict) -> bytes:
        """Generate music using simple prompt"""
        print("🎵 Using simple prompt generation...")
        
        # Create policy-compliant music prompt
        music_prompt = self._create_simple_music_prompt(song_structure, options)
        
        track = self.elevenlabs.music.compose(
            prompt=music_prompt,
            music_length_ms=options.get('length_ms', 60000)
        )
        
        audio_data = b""
        for chunk in track:
            audio_data += chunk
            
        return audio_data
    
    def _create_composition_plan_prompt(self, song_structure: SongStructure, lyrics: str, options: Dict) -> str:
        """Create detailed composition plan prompt"""
        
        # Analyze lyrics for timing if provided
        sections = []
        if lyrics:
            lyric_sections = self._parse_lyric_sections(lyrics)
            for i, section in enumerate(lyric_sections):
                section_name = song_structure.structure[i] if i < len(song_structure.structure) else f"Section {i+1}"
                sections.append({
                    'name': section_name,
                    'lyrics': section,
                    'duration': self._estimate_section_duration(section, song_structure.tempo)
                })
        
        # Create comprehensive composition plan prompt
        prompt = f"""
        Create a {song_structure.genre} instrumental track for a comedy parody performance.
        
        Overall Style:
        - Genre: {song_structure.genre}
        - Tempo: {song_structure.tempo} BPM
        - Key: {song_structure.key}
        - Mood: {', '.join(song_structure.mood)}
        - Energy: Upbeat and engaging for comedic performance
        
        Instrumentation:
        """
        
        for instrument, style in song_structure.instrumentation.items():
            prompt += f"- {instrument}: {style}\n        "
        
        prompt += f"""
        
        Song Structure ({len(song_structure.structure)} sections):
        """
        
        for i, section_name in enumerate(song_structure.structure):
            section_duration = 8000 if i == 0 else 12000  # Intro shorter, others longer
            if 'outro' in section_name.lower():
                section_duration = 6000
                
            prompt += f"""
        {i+1}. {section_name.title()}:
           - Duration: {section_duration}ms
           - Style: {"Instrumental intro" if 'intro' in section_name.lower() else 
                    "Vocal-ready arrangement" if 'verse' in section_name.lower() or 'chorus' in section_name.lower() else
                    "Instrumental bridge" if 'bridge' in section_name.lower() else
                    "Fade out conclusion" if 'outro' in section_name.lower() else
                    "Dynamic section"}
           """
        
        # Add performance requirements
        prompt += f"""
        
        Performance Requirements:
        - Clear rhythm for vocal synchronization
        - Space for comedic timing
        - Dynamic enough to support humor
        - Professional quality for audience engagement
        - Avoid overpowering vocals
        
        Style Specifications:
        - Keep it original and non-copyrighted
        - Make it catchy and memorable  
        - Suitable for comedy performance
        - Length: {options.get('length_ms', 60000)}ms total
        """
        
        return prompt.strip()
    
    def _create_simple_music_prompt(self, song_structure: SongStructure, options: Dict) -> str:
        """Create simple music prompt (policy compliant)"""
        
        mood_desc = "upbeat and comedic" if "humorous" in song_structure.mood else ', '.join(song_structure.mood)
        
        prompt = f"""
        Create an original {song_structure.genre} instrumental track perfect for comedy performances.
        
        Musical Style:
        - Tempo: {song_structure.tempo} BPM
        - Key: {song_structure.key}
        - Mood: {mood_desc}
        - Energy: High and engaging
        
        Instrumentation: {', '.join(f'{k} ({v})' for k, v in song_structure.instrumentation.items())}
        
        Requirements:
        - Clear, steady rhythm for vocal synchronization
        - Space for comedic timing and emphasis
        - Catchy and memorable melody
        - Professional quality for live or recorded performance
        - Avoid overwhelming the vocals
        
        Make it original, energetic, and perfect for parody song performance.
        Length: {options.get('length_ms', 60000)}ms
        """
        
        return prompt.strip()
    
    def _parse_lyric_sections(self, lyrics: str) -> List[str]:
        """Parse lyrics into sections"""
        # Split on common section markers or double newlines
        sections = []
        current_section = ""
        
        lines = lyrics.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):  # Section marker
                if current_section:
                    sections.append(current_section.strip())
                    current_section = ""
            else:
                current_section += line + '\n'
        
        if current_section.strip():
            sections.append(current_section.strip())
            
        return sections
    
    def _estimate_section_duration(self, section_text: str, tempo: int) -> int:
        """Estimate section duration based on text length and tempo"""
        # Simple estimation: ~4 lines = ~8 seconds at 120 BPM
        lines = [line for line in section_text.split('\n') if line.strip()]
        base_duration = len(lines) * 2000  # 2 seconds per line
        
        # Adjust for tempo
        tempo_factor = 120 / tempo if tempo > 0 else 1
        adjusted_duration = int(base_duration * tempo_factor)
        
        # Reasonable bounds
        return max(4000, min(20000, adjusted_duration))  # 4-20 seconds
    
    def _generate_generic_music_track(self, song_structure: SongStructure, options: Dict = None) -> bytes:
        """Generate generic music track without any copyrighted references"""
        print("🎵 Generating generic backing track...")
        
        options = options or {}
        
        # Ultra-safe prompt with no references to copyrighted material
        generic_prompt = f"""
        Create an original {song_structure.genre} instrumental track.
        Tempo: {song_structure.tempo} BPM
        Key: {song_structure.key}
        Mood: upbeat and energetic
        Perfect for comedy performances and vocal accompaniment.
        Include clear rhythm patterns and catchy melodies.
        Length: {options.get('length_ms', 60000)}ms
        """
        
        try:
            track = self.elevenlabs.music.compose(
                prompt=generic_prompt,
                music_length_ms=options.get('length_ms', 60000),
            )
            
            audio_data = b""
            for chunk in track:
                audio_data += chunk
                
            return audio_data
        except Exception as e:
            print(f"⚠️ Even generic music generation failed: {e}")
            return b""
    
    def generate_vocal_track(self, lyrics: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL") -> bytes:
        """Generate vocal track for lyrics"""
        print(f"🎤 Generating vocal track...")
        
        try:
            audio = self.elevenlabs.text_to_speech.convert(
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                text=lyrics,
            )
            return audio
        except Exception as e:
            print(f"⚠️ Vocal generation failed: {e}")
            return b""
    
    def save_project(self, project_name: str, song_structure: SongStructure, 
                    original_lyrics: str, parody_lyrics: str, analysis: Dict) -> str:
        """Save project to file"""
        project_dir = self.projects_dir / project_name.replace(" ", "_").lower()
        project_dir.mkdir(exist_ok=True)
        
        # Save project data
        project_data = {
            "song_structure": asdict(song_structure),
            "original_lyrics": original_lyrics,
            "parody_lyrics": parody_lyrics,
            "analysis": analysis,
            "created_date": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        project_file = project_dir / "project.json"
        with open(project_file, 'w') as f:
            json.dump(project_data, f, indent=2)
        
        # Save lyrics separately
        lyrics_file = project_dir / "parody_lyrics.txt"
        with open(lyrics_file, 'w') as f:
            f.write(parody_lyrics)
            
        print(f"📁 Project saved to: {project_dir}")
        return str(project_dir)
    
    def load_project(self, project_name: str) -> Dict:
        """Load existing project"""
        project_dir = self.projects_dir / project_name.replace(" ", "_").lower()
        project_file = project_dir / "project.json"
        
        if project_file.exists():
            with open(project_file, 'r') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"Project '{project_name}' not found")
    
    def list_projects(self) -> List[str]:
        """List all available projects"""
        projects = []
        for project_dir in self.projects_dir.iterdir():
            if project_dir.is_dir() and (project_dir / "project.json").exists():
                projects.append(project_dir.name.replace("_", " ").title())
        return projects

# Interactive CLI for creative workflow
class ParodyCreatorCLI:
    """Command-line interface for the parody creator"""
    
    def __init__(self):
        self.creator = ParodyCreator()
        
    def run(self):
        """Main CLI loop"""
        print("🎵 Welcome to the Parody Song Creator! 🎭")
        print("=" * 50)
        
        while True:
            self.show_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.create_new_parody()
            elif choice == '2':
                self.continue_existing_project()
            elif choice == '3':
                self.list_projects()
            elif choice == '4':
                self.generate_music_only()
            elif choice == '5':
                print("👋 Thanks for using Parody Song Creator!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def show_menu(self):
        """Display main menu"""
        print("\n🎯 What would you like to do?")
        print("1. Create new parody")
        print("2. Continue existing project")
        print("3. List all projects")
        print("4. Generate music track only")
        print("5. Exit")
    
    def create_new_parody(self):
        """Create new parody workflow"""
        print("\n🎨 Creating a new parody...")
        
        # Get basic info
        original_title = input("Original song title: ")
        original_artist = input("Original artist: ")
        parody_topic = input("What's your parody about? ")
        
        print("\n📝 Please paste the original lyrics (press Enter twice when done):")
        original_lyrics = self.get_multiline_input()
        
        # Analyze original song
        analysis = self.creator.analyze_original_song(original_lyrics, original_title, original_artist)
        
        # Generate parody ideas
        ideas = self.creator.generate_parody_ideas(analysis, parody_topic)
        
        print("\n💡 Here are some parody ideas:")
        for i, idea in enumerate(ideas[:5], 1):
            print(f"{i}. {idea[:100]}...")
        
        # Get concept choice
        concept_choice = input("\nChoose an idea (1-5) or describe your own concept: ")
        if concept_choice.isdigit() and 1 <= int(concept_choice) <= 5:
            concept = ideas[int(concept_choice) - 1]
        else:
            concept = concept_choice
        
        # Generate parody lyrics
        parody_lyrics = self.creator.create_parody_lyrics(
            original_lyrics, concept, analysis.get("rhyme_scheme", {})
        )
        
        print("\n✨ Generated parody lyrics:")
        print("-" * 40)
        print(parody_lyrics)
        print("-" * 40)
        
        # Allow refinement
        while True:
            feedback = input("\nAny changes needed? (Enter feedback or 'done'): ")
            if feedback.lower() == 'done':
                break
            parody_lyrics = self.creator.refine_lyrics_section(parody_lyrics, feedback)
            print("\n📝 Revised lyrics:")
            print("-" * 40)
            print(parody_lyrics)
            print("-" * 40)
        
        # Save project
        project_name = input("\nProject name: ")
        song_structure = self.creator.create_song_structure(
            project_name, original_artist, original_title, "comedy"
        )
        
        project_path = self.creator.save_project(
            project_name, song_structure, original_lyrics, parody_lyrics, analysis
        )
        
        # Optional: Generate music
        generate_music = input("\nGenerate music track? (y/n): ").lower() == 'y'
        if generate_music:
            self.generate_audio_tracks(song_structure, parody_lyrics, project_path)
    
    def generate_audio_tracks(self, song_structure: SongStructure, lyrics: str, project_path: str):
        """Generate audio tracks for the project"""
        print("\n🎵 Generating audio tracks...")
        
        # Generate music track
        music_data = self.creator.generate_music_track(song_structure, lyrics)
        if music_data:
            music_file = Path(project_path) / "backing_track.mp3"
            with open(music_file, 'wb') as f:
                f.write(music_data)
            print(f"🎶 Music track saved: {music_file}")
        
        # Generate vocal track
        generate_vocal = input("Generate vocal guide? (y/n): ").lower() == 'y'
        if generate_vocal:
            vocal_data = self.creator.generate_vocal_track(lyrics)
            if vocal_data:
                vocal_file = Path(project_path) / "vocal_guide.mp3"
                save(vocal_data, str(vocal_file))
                print(f"🎤 Vocal guide saved: {vocal_file}")
    
    def get_multiline_input(self) -> str:
        """Get multiline input from user"""
        lines = []
        while True:
            line = input()
            if line == "":
                if lines and lines[-1] == "":
                    break
            lines.append(line)
        return "\n".join(lines[:-1]) if lines and lines[-1] == "" else "\n".join(lines)
    
    def continue_existing_project(self):
        """Continue working on existing project"""
        projects = self.creator.list_projects()
        if not projects:
            print("📁 No existing projects found.")
            return
        
        print("\n📂 Existing projects:")
        for i, project in enumerate(projects, 1):
            print(f"{i}. {project}")
        
        choice = input("\nSelect project number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(projects):
            project_name = projects[int(choice) - 1]
            project_data = self.creator.load_project(project_name)
            
            print(f"\n📖 Loaded project: {project_name}")
            print(f"Original: {project_data['song_structure']['original_title']}")
            print("\nCurrent lyrics:")
            print("-" * 40)
            print(project_data['parody_lyrics'])
            print("-" * 40)
            
            # Allow editing
            action = input("\nWhat would you like to do? (edit/music/done): ").lower()
            if action == 'edit':
                feedback = input("What needs to be changed? ")
                new_lyrics = self.creator.refine_lyrics_section(
                    project_data['parody_lyrics'], feedback
                )
                project_data['parody_lyrics'] = new_lyrics
                
                # Save updated project
                song_structure = SongStructure(**project_data['song_structure'])
                self.creator.save_project(
                    project_name, song_structure, 
                    project_data['original_lyrics'], new_lyrics, 
                    project_data['analysis']
                )
                print("✅ Project updated!")
                
            elif action == 'music':
                song_structure = SongStructure(**project_data['song_structure'])
                project_path = str(self.creator.projects_dir / project_name.replace(" ", "_").lower())
                self.generate_audio_tracks(song_structure, project_data['parody_lyrics'], project_path)
    
    def list_projects(self):
        """List all projects"""
        projects = self.creator.list_projects()
        if projects:
            print("\n📂 Your parody projects:")
            for i, project in enumerate(projects, 1):
                try:
                    project_data = self.creator.load_project(project)
                    original = project_data['song_structure']['original_title']
                    created = project_data['created_date'][:10]
                    print(f"{i}. {project} (based on '{original}') - {created}")
                except:
                    print(f"{i}. {project} (data error)")
        else:
            print("📁 No projects found.")
    
    def generate_music_only(self):
        """Generate music track without lyrics"""
        print("\n🎵 Music-only generation")
        
        genre = input("Genre: ")
        tempo = input("Tempo (BPM): ")
        mood = input("Mood/style: ")
        
        # Create basic structure
        song_structure = SongStructure(
            title="Instrumental Track",
            original_artist="",
            original_title="",
            genre=genre,
            tempo=int(tempo) if tempo.isdigit() else 120,
            key="C major",
            mood=[mood],
            structure=["intro", "verse", "chorus"],
            instrumentation={"all": "electronic"},
            vocal_style={}
        )
        
        music_data = self.creator.generate_music_track(song_structure, "")
        if music_data:
            filename = f"instrumental_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            with open(filename, 'wb') as f:
                f.write(music_data)
            print(f"🎶 Music saved as: {filename}")

if __name__ == "__main__":
    try:
        cli = ParodyCreatorCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your API keys and internet connection.")