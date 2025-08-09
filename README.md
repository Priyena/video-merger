---
title: Enhanced AI Ad Completion Tool
emoji: 🎬
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: apache-2.0
python_version: 3.10
---

# 🎬 Enhanced AI Ad Completion Tool

Transform your videos into professional commercials using AI! This tool combines multiple videos, generates new content using Stable Video Diffusion, and creates polished ads with intelligent prompt generation powered by Google's Gemini API.

## Features

- 🎥 **Dual Video Upload**: Combine 1 or 2 videos seamlessly
- 🤖 **AI Video Generation**: Create new content using Stable Video Diffusion
- 🧠 **Gemini Integration**: Intelligent prompt generation based on video analysis
- 🎨 **Professional Processing**: Color grading, smooth transitions, and effects
- ⚡ **Smart Fallbacks**: Reliable processing even when AI models fail
- 🎯 **Flexible Duration**: Extend videos to your target length

## How to Use

1. **Upload Videos**: Add your primary video (required) and optionally a secondary video
2. **Set Duration**: Choose your target duration (10-45 seconds)
3. **Configure AI**: Enable/disable AI video generation
4. **Process**: Click "Create Enhanced Ad" and wait for processing
5. **Download**: Get your professionally enhanced commercial!

## API Requirements

- **Gemini API Key**: Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **GPU Access**: HF Spaces provides free GPU access for video generation

## Technical Details

- **Video Analysis**: OpenCV + MediaPipe + Whisper
- **AI Generation**: Stable Video Diffusion XL
- **Prompt Enhancement**: Google Gemini 1.5 Flash
- **Processing**: MoviePy + FFmpeg
- **Interface**: Gradio 4.44.0

## Development

Built with modern AI technologies for maximum quality and reliability. The tool automatically handles various video formats, resolutions, and provides intelligent fallbacks.

## License

Apache 2.0 - Feel free to use and modify!