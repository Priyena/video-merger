import cv2
import os

def get_video_info(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 24
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0
        cap.release()
        return {'fps': fps, 'duration': duration, 'resolution': (width, height), 'frame_count': frame_count}
    except:
        return None

def validate_video_file(video_path):
    if not video_path or not os.path.exists(video_path):
        return False
    info = get_video_info(video_path)
    return info is not None and info['duration'] > 0
