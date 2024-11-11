import os
from openai import OpenAI
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image
import requests
from io import BytesIO
import logging
from typing import List, Dict
import cv2

import numpy as np

class VideoGenerator:
    def __init__(self, api_key: str):
        """Initialize the video generator with OpenAI API key"""
        self.client = OpenAI(api_key=api_key)
        self._setup_logging()

    def _setup_logging(self):
        """Set up logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def parse_script(self, script: str) -> List[Dict]:
        """Parse the script into scenes"""
        scenes = []
        for line in script.strip().split('\n'):
            if line.strip():  # Skip empty lines
                scenes.append({
                    'description': line.strip()
                })
        return scenes

    def generate_image(self, scene_text: str) -> Image.Image:
        """Generate a test image for development"""
        try:
            logging.info(f"Generating test image for scene: {scene_text[:50]}...")
            
            # Create a test image with text
            width = 1024
            height = 1024
            image = Image.new('RGB', (width, height), (255, 255, 255))  # White background
            
            # Add text to image using PIL
            from PIL import ImageDraw
            draw = ImageDraw.Draw(image)
            draw.text((width/2, height/2), scene_text, fill=(0, 0, 0))  # Black text
            
            return image
            
        except Exception as e:
            logging.error(f"Error generating image: {str(e)}")
            raise

    def create_video(self, scenes: List[Dict], output_path: str):
        """Create a video from a list of scenes"""
        if not scenes:
            raise ValueError("No scenes provided")
        
        clips = []
        for scene in scenes:
            # Generate image for each scene
            image = self.generate_image(scene['description'])
            
            # Convert PIL Image to ImageClip (duration 3 seconds per scene)
            image_clip = ImageClip(np.array(image)).set_duration(3)
            clips.append(image_clip)
        
        # Concatenate all clips
        final_clip = concatenate_videoclips(clips)
        
        # Write the result to a file
        final_clip.write_videofile(output_path, fps=24)

def get_user_script() -> str:
    """Get the script from user input"""
    print("\n=== AI Video Generator ===")
    print("Please enter your script. Press Enter twice when finished:\n")
    
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    return "\n".join(lines)

def main():
    # Get script from user
    script = get_user_script()
    
    # Initialize video generator
    generator = VideoGenerator()
    
    # Generate video from script
    generator.generate_video(script)

if __name__ == "__main__":
    main()