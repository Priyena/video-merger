import google.generativeai as genai
from config.settings import PROCESSING_CONFIG

class PromptGenerator:
    def __init__(self):
        self.model = None
        self.gemini_key = None
    
    def set_api_key(self, key):
        if key and key.strip():
            try:
                genai.configure(api_key=key.strip())
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.gemini_key = key.strip()
            except:
                self.model = None
    
    def generate_video_prompt(self, analysis, target_duration):
        if not self.model or not analysis:
            return self._fallback_prompt(analysis)
        
        try:
            context = f"""
Video Analysis:
- Duration: {analysis.get('duration', 0):.1f}s
- Transcript: {analysis.get('transcript', 'No audio')}
- Scene type: {analysis.get('scene_type', 'unknown')}
- Colors: {', '.join(analysis.get('dominant_colors', [])[:3])}

Target: {target_duration}s commercial

Generate a creative prompt for Stable Video Diffusion to extend this commercial.
Keep it under 100 words, focus on visual elements, camera movement, and commercial appeal.
"""
            
            response = self.model.generate_content(context)
            prompt = response.text.strip()
            
            if len(prompt) > 20:
                return prompt
            else:
                return self._fallback_prompt(analysis)
                
        except Exception as e:
            return self._fallback_prompt(analysis)
    
    def _fallback_prompt(self, analysis):
        if not analysis:
            return "professional commercial product showcase, smooth camera movement, high quality, cinematic lighting"
        
        scene_type = analysis.get('scene_type', 'product')
        transcript = analysis.get('transcript', '').lower()
        
        prompts = {
            'lifestyle': "vibrant lifestyle commercial, people enjoying, dynamic movement, warm lighting",
            'tech': "sleek tech commercial, modern interface, clean design, professional lighting", 
            'product': "premium product showcase, elegant presentation, studio lighting"
        }
        
        base_prompt = prompts.get(scene_type, prompts['product'])
        
        if 'outdoor' in transcript:
            base_prompt += ", outdoor setting"
        elif 'indoor' in transcript:
            base_prompt += ", indoor environment"
            
        return base_prompt + ", commercial quality, smooth transitions"
