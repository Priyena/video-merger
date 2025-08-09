from .video_analyzer import VideoAnalyzer
from .prompt_generator import PromptGenerator
from .video_generator import VideoGenerator
from .video_processor import VideoProcessor
import os

class EnhancedAdPipeline:
    def __init__(self):
        self.analyzer = VideoAnalyzer()
        self.prompt_gen = PromptGenerator()
        self.video_gen = VideoGenerator()
        self.processor = VideoProcessor()
    
    def set_gemini_key(self, key):
        self.prompt_gen.set_api_key(key)
    
    def process_videos(self, video1_path, video2_path, target_duration, use_ai, progress=None):
        if progress:
            progress(0.1, desc="Analyzing first video...")
        
        analysis1 = self.analyzer.analyze_video(video1_path)
        if not analysis1:
            return {'success': False, 'error': 'Failed to analyze first video'}
        
        if progress:
            progress(0.3, desc="Merging videos...")
        
        merged_video = self.processor.merge_videos(video1_path, video2_path, target_duration)
        if not merged_video:
            return {'success': False, 'error': 'Failed to merge videos'}
        
        current_duration = analysis1['duration']
        if video2_path and os.path.exists(video2_path):
            analysis2 = self.analyzer.analyze_video(video2_path)
            if analysis2:
                current_duration += analysis2['duration']
        
        final_video = merged_video
        ai_generated = False
        
        if use_ai and current_duration < target_duration and analysis1.get('last_frame') is not None:
            if progress:
                progress(0.5, desc="Generating AI prompt...")
            
            prompt = self.prompt_gen.generate_video_prompt(analysis1, target_duration)
            
            if progress:
                progress(0.6, desc="Generating AI video...")
            
            ai_frames = self.video_gen.generate_video(
                analysis1['last_frame'], 
                prompt, 
                duration=min(3, target_duration - current_duration)
            )
            
            if ai_frames:
                if progress:
                    progress(0.8, desc="Adding AI extension...")
                
                extended_video = self.processor.add_ai_extension(merged_video, ai_frames, target_duration)
                if extended_video:
                    final_video = extended_video
                    ai_generated = True
        
        if progress:
            progress(0.95, desc="Finalizing...")
        
        return {
            'success': True,
            'output_video': final_video,
            'original_duration': analysis1['duration'],
            'second_video': video2_path is not None,
            'ai_generated': ai_generated
        }
