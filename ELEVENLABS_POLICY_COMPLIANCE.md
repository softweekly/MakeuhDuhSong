# 🚨 ElevenLabs Policy Compliance Guide

## Important Policy Updates - Music Generation Restrictions

After reviewing [ElevenLabs Music API policies](https://elevenlabs.io/docs/eleven-api/guides/cookbooks/music), we've updated the tool to comply with their content restrictions.

---

## ❌ What ElevenLabs Prohibits

### **Copyrighted Material References**
ElevenLabs will reject any prompts that contain:
- **Artist names** (e.g., "Queen", "Beatles", "Taylor Swift")
- **Song titles** (e.g., "Bohemian Rhapsody", "Hey Jude")  
- **Copyrighted lyrics** or direct musical references
- **Band names** or specific musical works

### **API Error Responses**
When violations occur:
- `bad_prompt` error for music prompts with copyrighted content
- `bad_composition_plan` error for composition plans with violations
- No suggested alternatives for harmful material

---

## ✅ How Our Tool Complies

### **Updated Music Generation**
We've modified the `generate_music_track()` method to:

**Before (Policy Violation):**
```python
music_prompt = f"""
Create a track for a parody song.
Original: "Bohemian Rhapsody" by Queen  # ❌ VIOLATES POLICY
"""
```

**After (Policy Compliant):**
```python
music_prompt = f"""
Create a comedy track suitable for parody performance.
Style: rock ballad
Tempo: 120 BPM
Mood: dramatic, theatrical  # ✅ COMPLIANT
"""
```

### **Fallback System**
- Primary generation with safe, generic prompts
- Automatic fallback if policy violations detected
- Error handling for API rejections

---

## 🎯 What This Means for Your Parodies

### **Lyrics Creation - Still Full Featured**
- ✅ **AI lyric writing** works perfectly (uses OpenAI, not ElevenLabs)
- ✅ **Song structure analysis** unaffected  
- ✅ **Parody concept generation** unaffected
- ✅ **Rhythm/rhyme matching** unaffected

### **Music Generation - Limited But Functional**
- ✅ **Original backing tracks** based on genre/style
- ❌ **Cannot sound like specific songs** or artists
- ✅ **Custom tempo, key, mood** still works
- ✅ **Comedy-appropriate music** still generated

### **Vocal Generation - Unaffected**
- ✅ **Text-to-speech** works normally for vocal guides
- ✅ **Custom voices** available
- ✅ **Parody lyrics** spoken clearly

---

## 💡 Creative Workarounds

### **For Music Generation**
Instead of asking for music "like Bohemian Rhapsody", describe the style:

**❌ Prohibited:**
- "Music like Queen's Bohemian Rhapsody"
- "Sound like the Beatles"
- "In the style of [Artist Name]"

**✅ Allowed:**
- "Epic rock ballad with piano and guitar"
- "60s British pop with harmonies"  
- "Theatrical rock with dramatic tempo changes"

### **Style Description Guide**
| Instead of... | Use This Description |
|--------------|---------------------|
| "Like Taylor Swift" | "Pop country with storytelling lyrics" |
| "Beatles style" | "British rock with vocal harmonies" |
| "Queen-like" | "Theatrical rock with operatic elements" |
| "Hip-hop like Eminem" | "Fast-paced rap with intense delivery" |

---

## 🔧 Technical Implementation

### **Error Handling**
```python
try:
    track = elevenlabs.music.compose(prompt=music_prompt)
except Exception as e:
    if e.body['detail']['status'] == 'bad_prompt':
        print("Policy violation - using generic fallback")
        track = generate_generic_track()
```

### **Prompt Safety Check**
```python
def is_prompt_safe(prompt):
    """Check if prompt might violate ElevenLabs policies"""
    prohibited_terms = [
        # Artist names, song titles, etc.
        # (We maintain an internal list)
    ]
    return not any(term in prompt.lower() for term in prohibited_terms)
```

---

## 🎵 Impact on Your Workflow

### **What Changes**
1. **Music will be original** - Not imitations of copyrighted songs
2. **Style-based generation** - Describe musical characteristics instead
3. **Generic backing tracks** - Still rhythmically appropriate for parodies

### **What Stays the Same**
1. **Lyric writing assistance** - Full AI support for writing parodies
2. **Song analysis** - Still breaks down structure and patterns
3. **Project management** - Save, load, organize your parodies
4. **Vocal guides** - Spoken versions of your lyrics

---

## 🎯 Best Practices

### **Music Prompt Writing**
```python
# ✅ Good prompt
"Create upbeat pop rock with driving drums, catchy guitar riffs, 
and energetic bass. Tempo 130 BPM. Perfect for comedy vocals."

# ❌ Bad prompt  
"Create music like 'Don't Stop Believin' by Journey'"
```

### **Genre Descriptions**
- Use musical terms: "folk ballad", "uptempo country", "electronic dance"
- Describe instruments: "acoustic guitar", "synth pads", "brass section"
- Specify mood: "energetic", "melancholy", "dramatic", "humorous"

### **Working with Limitations**
1. **Focus on genre and style** rather than specific songs
2. **Use the generated backing track as inspiration** for your parody
3. **Remember the music supports your lyrics** - it doesn't need to be identical

---

## ⚖️ Legal and Ethical Notes

### **Fair Use for Parodies**
- **Parody lyrics** are generally protected under fair use
- **Musical copying** has different legal standards
- **ElevenLabs is being conservative** to avoid any copyright issues

### **Our Approach**
- **Comply with platform policies** to ensure continued access
- **Focus on originality** in backing tracks
- **Support your creative process** within policy boundaries
- **Provide fallbacks** when restrictions are encountered

---

## 🔮 Future Considerations

### **Potential Updates**
- **ElevenLabs may relax policies** as technology evolves
- **Alternative music services** could be integrated
- **Local music generation** might be added as backup

### **Monitoring Changes**
- **We'll track policy updates** and adjust the tool accordingly
- **Fallback systems** ensure continued functionality
- **User notifications** for any major changes

---

## 🎭 Bottom Line for Parody Creation

**The tool is still excellent for parody songwriting!** The policy compliance changes only affect music generation, not the core parody creation features:

✅ **Still Amazing For:**
- Writing hilarious parody lyrics with AI assistance
- Analyzing song structure and rhythm patterns  
- Generating creative parody concepts
- Iteratively refining your lyrics
- Managing and organizing your parody projects

⚠️ **Limited For:**
- Creating backing tracks that sound like specific copyrighted songs
- Musical imitation of famous artists

**Your parody songwriting workflow remains powerful and effective within these compliance boundaries.**