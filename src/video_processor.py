import moviepy.editor as mp
import numpy as np
import os
from config.settings import PATHS, PROCESSING_CONFIG

class VideoProcessor:
    def __init__(self):
        pass
    
    def merge_videos(self, video1_path, video2_path=None, target_duration=20):
        try:
            clips = []
            total_duration = 0
            
            clip1 = mp.VideoFileClip(video1_path)
            clips.append(clip1)
            total_duration += clip1.duration
            
            if video2_path and os.path.exists(video2_path):
                clip2 = mp.VideoFileClip(video2_path)
                clips.append(clip2.crossfadein(0.5))
                total_duration += clip2.duration
            
            if len(clips) > 1:
                merged = mp.concatenate_videoclips(clips, method="compose")
            else:
                merged = clips[0]
            
            if total_duration < target_duration:
                extend_time = target_duration - total_duration
                if extend_time > 0:
                    loop_times = int(extend_time / merged.duration) + 1
                    extended = mp.concatenate_videoclips([merged] * (loop_times + 1))
                    merged = extended.subclip(0, target_duration)
            elif total_duration > target_duration:
                merged = merged.subclip(0, target_duration)
            
            merged = self._apply_effects(merged)
            
            output_path = os.path.join(PATHS['temp_dir'], f"merged_{hash(video1_path)}.mp4")
            merged.write_videofile(
                output_path, 
                fps=PROCESSING_CONFIG['fps'],
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=os.path.join(PATHS['temp_dir'], 'temp_audio.m4a'),
                remove_temp=True,
                logger=None,
                verbose=False
            )
            
            for clip in clips:
                clip.close()
            merged.close()
            
            return output_path
            
        except Exception as e:
            print(f"Video merge failed: {e}")
            return None
    
    def add_ai_extension(self, video_path, ai_frames, target_duration):
        if not ai_frames or not video_path:
            return video_path
        
        try:
            main_clip = mp.VideoFileClip(video_path)
            
            frame_array = np.array(ai_frames)
            ai_clip = mp.ImageSequenceClip([frame for frame in frame_array], fps=PROCESSING_CONFIG['fps'])
            
            ai_clip = ai_clip.resize(main_clip.size)
            
            combined = mp.concatenate_videoclips([main_clip, ai_clip.crossfadein(0.3)])
            
            if combined.duration > target_duration:
                combined = combined.subclip(0, target_duration)
            
            output_path = os.path.join(PATHS['temp_dir'], f"extended_{hash(video_path)}.mp4")
            combined.write_videofile(
                output_path,
                fps=PROCESSING_CONFIG['fps'], 
                codec='libx264',
                temp_audiofile=os.path.join(PATHS['temp_dir'], 'temp_audio2.m4a'),
                remove_temp=True,
                logger=None,
                verbose=False
            )
            
            main_clip.close()
            ai_clip.close()
            combined.close()
            
            return output_path
            
        except Exception as e:
            print(f"AI extension failed: {e}")
            return video_path
    
    def _apply_effects(self, clip):
        try:
            def color_correct(get_frame, t):
                frame = get_frame(t)
                enhanced = np.clip(frame * 1.05 + 2, 0, 255)
                enhanced[:, :, 0] = np.clip(enhanced[:, :, 0] * 1.02, 0, 255)
                return enhanced.astype(np.uint8)
            
            return clip.fl(color_correct)
        except:
            return clip
