import numpy as np
import cv2

class ColorGrading:
    def apply_commercial_grade(self, clip):
        def color_grade(get_frame, t):
            frame = get_frame(t)
            enhanced = np.clip(frame * 1.05 + 3, 0, 255)
            enhanced = self._temperature_adjust(enhanced)
            return enhanced.astype(np.uint8)
        return clip.fl(color_grade)
    
    def _temperature_adjust(self, frame):
        frame[:, :, 0] = np.clip(frame[:, :, 0] * 1.02, 0, 255)
        frame[:, :, 2] = np.clip(frame[:, :, 2] * 0.98, 0, 255)
        return frame

class TransitionEffects:
    def crossfade(self, clip, duration):
        return clip.crossfadein(duration)
    
    def slow_zoom(self, clip, zoom_factor=0.05):
        def zoom_effect(get_frame, t):
            frame = get_frame(t)
            progress = t / clip.duration
            current_zoom = 1 + progress * zoom_factor
            h, w = frame.shape[:2]
            new_h, new_w = int(h / current_zoom), int(w / current_zoom)
            start_y = (h - new_h) // 2
            start_x = (w - new_w) // 2
            cropped = frame[start_y:start_y + new_h, start_x:start_x + new_w]
            return cv2.resize(cropped, (w, h))
        return clip.fl(zoom_effect)
