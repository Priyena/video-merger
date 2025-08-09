import cv2
import numpy as np
import whisper
from sklearn.cluster import KMeans

class VideoAnalyzer:
    def __init__(self):
        self.whisper_model = None
        try:
            self.whisper_model = whisper.load_model("tiny")
        except:
            pass
    
    def analyze_video(self, video_path):
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 24
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps
            
            frames = []
            for idx in [0, frame_count//4, frame_count//2, 3*frame_count//4, frame_count-1]:
                cap.set(cv2.CAP_PROP_POS_FRAMES, min(idx, frame_count-1))
                ret, frame = cap.read()
                if ret:
                    frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            cap.release()
            
            transcript = ""
            if self.whisper_model:
                try:
                    result = self.whisper_model.transcribe(video_path)
                    transcript = result["text"].strip()
                except:
                    pass
            
            colors = ['#808080']
            if frames:
                try:
                    all_pixels = []
                    for frame in frames[:3]:
                        resized = cv2.resize(frame, (50, 50))
                        pixels = resized.reshape(-1, 3)
                        all_pixels.extend(pixels[::5])
                    
                    if all_pixels:
                        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
                        kmeans.fit(all_pixels)
                        colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in kmeans.cluster_centers_.astype(int)]
                except:
                    pass
            
            scene_type = "product"
            if transcript:
                transcript_lower = transcript.lower()
                if any(word in transcript_lower for word in ['happy', 'fun', 'joy', 'celebration']):
                    scene_type = "lifestyle"
                elif any(word in transcript_lower for word in ['tech', 'innovation', 'digital']):
                    scene_type = "tech"
            
            return {
                'duration': duration,
                'fps': fps,
                'resolution': (width, height),
                'frames': frames,
                'last_frame': frames[-1] if frames else None,
                'transcript': transcript,
                'dominant_colors': colors,
                'scene_type': scene_type
            }
        except Exception as e:
            return None
