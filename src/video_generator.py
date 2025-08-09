import torch
from diffusers import StableVideoDiffusionPipeline
from PIL import Image
import numpy as np
from config.settings import DEVICE, MODEL_CONFIG, PROCESSING_CONFIG

class VideoGenerator:
    def __init__(self):
        self.pipeline = None
        self._load_models()
    
    def _load_models(self):
        if DEVICE == "cuda":
            try:
                self.pipeline = StableVideoDiffusionPipeline.from_pretrained(
                    MODEL_CONFIG['svd_model'],
                    torch_dtype=torch.float16,
                    variant="fp16"
                )
                self.pipeline.to("cuda")
                self.pipeline.enable_model_cpu_offload()
            except Exception as e:
                print(f"Failed to load SVD: {e}")
    
    def generate_video(self, image, prompt, duration=2):
        if not self.pipeline:
            return None
        
        try:
            if isinstance(image, np.ndarray):
                if image.dtype == np.float32:
                    image = (image * 255).astype(np.uint8)
                image = Image.fromarray(image)
            
            image = image.resize(PROCESSING_CONFIG['default_resolution'])
            
            num_frames = min(PROCESSING_CONFIG['max_frames'], int(duration * PROCESSING_CONFIG['fps']))
            
            frames = self.pipeline(
                image,
                height=PROCESSING_CONFIG['default_resolution'][1],
                width=PROCESSING_CONFIG['default_resolution'][0],
                num_frames=num_frames,
                decode_chunk_size=8,
                motion_bucket_id=127,
                fps=7,
                noise_aug_strength=0.02,
                num_inference_steps=PROCESSING_CONFIG['generation_steps']
            ).frames[0]
            
            return [np.array(frame) for frame in frames]
            
        except Exception as e:
            print(f"Video generation failed: {e}")
            return None
