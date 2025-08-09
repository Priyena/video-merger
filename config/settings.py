import os

DEVICE = "cuda" if os.environ.get('CUDA_AVAILABLE') == 'true' else "cpu"

MODEL_CONFIG = {
    'whisper_model': 'tiny',
    'svd_model': 'stabilityai/stable-video-diffusion-img2vid-xt',
    'torch_dtype': 'float16' if DEVICE == 'cuda' else 'float32',
}

PROCESSING_CONFIG = {
    'max_frames': 25,
    'generation_steps': 8,
    'guidance_scale': 3.0,
    'fps': 24,
    'default_resolution': (1024, 576),
    'fallback_resolution': (512, 320),
}

UI_CONFIG = {
    'title': "Enhanced AI Ad Tool",
    'theme': "soft",
    'css': """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    """
}

PATHS = {
    'temp_dir': '/tmp/ad_processing',
    'cache_dir': '/tmp/ad_cache',
}

os.makedirs(PATHS['temp_dir'], exist_ok=True)
os.makedirs(PATHS['cache_dir'], exist_ok=True)
