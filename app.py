import gradio as gr
import os
import warnings
warnings.filterwarnings('ignore')

from src.pipeline import EnhancedAdPipeline
from config.settings import UI_CONFIG

def create_interface():
    pipeline = EnhancedAdPipeline()
    
    def process_videos_ui(video1, video2, target_duration, use_ai, gemini_key, progress=gr.Progress()):
        if video1 is None:
            return None, "❌ Please upload at least the first video"
        
        try:
            if gemini_key and gemini_key.strip():
                pipeline.set_gemini_key(gemini_key.strip())
            
            progress(0.1, desc="🔍 Analyzing videos...")
            
            result = pipeline.process_videos(video1, video2, target_duration, use_ai, progress)
            
            if result['success']:
                progress(1.0, desc="🎉 Complete!")
                
                status = f"✅ Video processing successful!\n"
                status += f"📊 Original duration: {result.get('original_duration', 0):.1f}s\n"
                if result.get('second_video'):
                    status += f"📊 Second video included\n"
                if result.get('ai_generated'):
                    status += "🤖 AI-generated extension added\n"
                status += f"🎯 Final duration: ~{target_duration}s"
                
                return result['output_video'], status
            else:
                return None, f"❌ Error: {result.get('error', 'Unknown error')}"
                
        except Exception as e:
            return None, f"❌ Error: {str(e)}"
    
    with gr.Blocks(**UI_CONFIG) as app:
        
        gr.Markdown("""
        
        🎬 Enhanced AI Ad Completion Tool
        
        
        **Transform your videos into professional commercials using AI!**
        
        ✨ **Features:** Dual video upload • AI video generation • Gemini-powered prompts • Professional processing
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📹 Video Inputs")
                
                video1_input = gr.Video(
                    label="🎬 Primary Video (Required)",
                    format="mp4"
                )
                
                video2_input = gr.Video(
                    label="🎬 Secondary Video (Optional)",
                    format="mp4"
                )
                
                gr.Markdown("### ⚙️ Settings")
                
                duration_slider = gr.Slider(
                    minimum=10,
                    maximum=45,
                    value=20,
                    step=1,
                    label="🎯 Target Duration (seconds)"
                )
                
                ai_toggle = gr.Checkbox(
                    value=True,
                    label="🤖 Use AI Video Generation",
                    info="Generate new content using AI (requires GPU)"
                )
                
                gemini_key_input = gr.Textbox(
                    label="🔑 Gemini API Key (Optional)",
                    placeholder="Enter your Gemini API key for better prompts",
                    type="password"
                )
                
                process_btn = gr.Button(
                    "🚀 Create Enhanced Ad",
                    variant="primary",
                    size="lg"
                )
                
                gr.Markdown("""
                ### 📋 How to Use:
                1. **Upload primary video** (your main content)
                2. **Optional**: Upload second video to combine
                3. **Set target duration** for final output
                4. **Optional**: Add Gemini API key for better prompts
                5. **Enable AI generation** for new content
                6. **Click "Create Enhanced Ad"**
                
                **Get Gemini API Key:** [Google AI Studio](https://makersuite.google.com/app/apikey) (Free)
                """)
                
            with gr.Column(scale=2):
                gr.Markdown("### 🎉 Output")
                
                video_output = gr.Video(
                    label="Enhanced Ad Video",
                    format="mp4"
                )
                
                status_output = gr.Textbox(
                    label="📋 Processing Status",
                    interactive=False,
                    lines=6
                )
                
                gr.Markdown("""
                ### 🎨 What This Tool Does:
                
                **🔍 Video Analysis:**
                - Extracts key frames and visual elements
                - Transcribes audio content using Whisper
                - Analyzes color palette and scene classification
                
                **🤖 AI Enhancement:**
                - Uses Gemini API for intelligent prompt generation
                - Generates new video content with Stable Video Diffusion
                - Applies professional color grading and effects
                
                **🎬 Smart Processing:**
                - Combines multiple videos with smooth transitions
                - Extends to target duration intelligently
                - Preserves audio quality throughout
                """)
        
        process_btn.click(
            fn=process_videos_ui,
            inputs=[video1_input, video2_input, duration_slider, ai_toggle, gemini_key_input],
            outputs=[video_output, status_output]
        )
    
    return app

if __name__ == "__main__":
    app = create_interface()
    app.launch(server_name="0.0.0.0", server_port=7860, share=True)
