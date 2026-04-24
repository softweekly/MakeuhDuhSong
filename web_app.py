#!/usr/bin/env python3
"""
Web Interface for Parody Song Creator
Simple Flask web app for browser-based song creation
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
import json
from pathlib import Path
from parody_song_creator import ParodyCreator, SongStructure
import tempfile
import io
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Initialize the parody creator
creator = ParodyCreator()

@app.route('/')
def index():
    """Main dashboard"""
    projects = creator.list_projects()
    return render_template('index.html', projects=projects)

@app.route('/create')
def create_page():
    """Create new parody page"""
    return render_template('create.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_song():
    """API endpoint to analyze original song"""
    data = request.get_json()
    
    try:
        analysis = creator.analyze_original_song(
            lyrics=data['lyrics'],
            title=data['title'], 
            artist=data['artist']
        )
        return jsonify({'success': True, 'analysis': analysis})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/generate_ideas', methods=['POST'])
def generate_ideas():
    """Generate parody ideas"""
    data = request.get_json()
    
    try:
        ideas = creator.generate_parody_ideas(
            original_analysis=data['analysis'],
            topic=data['topic'],
            style=data.get('style', 'humorous')
        )
        return jsonify({'success': True, 'ideas': ideas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/generate_lyrics', methods=['POST'])
def generate_lyrics():
    """Generate parody lyrics"""
    data = request.get_json()
    
    try:
        parody_lyrics = creator.create_parody_lyrics(
            original_lyrics=data['original_lyrics'],
            concept=data['concept'],
            rhyme_scheme=data.get('rhyme_scheme', {}),
            preserve_structure=data.get('preserve_structure', True)
        )
        return jsonify({'success': True, 'lyrics': parody_lyrics})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/refine_lyrics', methods=['POST'])
def refine_lyrics():
    """Refine lyrics based on feedback"""
    data = request.get_json()
    
    try:
        refined_lyrics = creator.refine_lyrics_section(
            section=data['lyrics'],
            feedback=data['feedback']
        )
        return jsonify({'success': True, 'lyrics': refined_lyrics})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/save_project', methods=['POST'])
def save_project():
    """Save project"""
    data = request.get_json()
    
    try:
        song_structure = creator.create_song_structure(
            title=data['project_name'],
            original_artist=data['original_artist'],
            original_title=data['original_title'],
            genre=data.get('genre', 'comedy')
        )
        
        project_path = creator.save_project(
            project_name=data['project_name'],
            song_structure=song_structure,
            original_lyrics=data['original_lyrics'],
            parody_lyrics=data['parody_lyrics'],
            analysis=data['analysis']
        )
        
        return jsonify({'success': True, 'project_path': project_path})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/generate_music', methods=['POST'])
def generate_music():
    """Generate music track with advanced options"""
    data = request.get_json()
    
    try:
        song_structure = SongStructure(**data['song_structure'])
        
        # Get advanced music options from request
        advanced_options = {
            'length_ms': int(data.get('music_length', 60)) * 1000,  # Convert seconds to milliseconds
            'use_composition_plan': data.get('use_composition_plan', True),
            'include_vocals': data.get('include_vocals', False),
            'music_style': data.get('music_style', 'instrumental')
        }
        
        lyrics = data.get('lyrics', '')
        music_data = creator.generate_music_track(song_structure, lyrics, advanced_options)
        
        if music_data:
            # Save temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.write(music_data)
            temp_file.close()
            
            return jsonify({
                'success': True, 
                'file_path': temp_file.name,
                'download_url': f'/download_temp/{os.path.basename(temp_file.name)}',
                'file_size': len(music_data),
                'duration': advanced_options['length_ms'] / 1000
            })
        else:
            return jsonify({'success': False, 'error': 'Music generation failed'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/generate_vocal', methods=['POST'])
def generate_vocal():
    """Generate vocal track"""
    data = request.get_json()
    
    try:
        vocal_data = creator.generate_vocal_track(
            lyrics=data['lyrics'],
            voice_id=data.get('voice_id', 'EXAVITQu4vr4xnSDxMaL')
        )
        
        if vocal_data:
            # Save temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            with open(temp_file.name, 'wb') as f:
                for chunk in vocal_data:
                    f.write(chunk)
            temp_file.close()
            
            return jsonify({
                'success': True,
                'download_url': f'/download_temp/{os.path.basename(temp_file.name)}'
            })
        else:
            return jsonify({'success': False, 'error': 'Vocal generation failed'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/project/<project_name>')
def view_project(project_name):
    """View existing project"""
    try:
        project_data = creator.load_project(project_name)
        return render_template('project.html', 
                             project_name=project_name, 
                             project_data=project_data)
    except FileNotFoundError:
        return "Project not found", 404

@app.route('/download_temp/<filename>')
def download_temp(filename):
    """Download temporary audio file"""
    temp_path = os.path.join(tempfile.gettempdir(), filename)
    if os.path.exists(temp_path):
        return send_file(temp_path, as_attachment=True)
    else:
        return "File not found", 404

@app.route('/api/projects')
def list_projects():
    """API to list all projects"""
    projects = []
    for project_name in creator.list_projects():
        try:
            project_data = creator.load_project(project_name)
            projects.append({
                'name': project_name,
                'title': project_data['song_structure']['title'],
                'original': f"{project_data['song_structure']['original_title']} by {project_data['song_structure']['original_artist']}",
                'created': project_data['created_date'][:10],
                'url': f'/project/{project_name.replace(" ", "_").lower()}'
            })
        except:
            continue
    
    return jsonify(projects)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)