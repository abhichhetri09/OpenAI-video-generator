import os
from openai import OpenAI
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image
import requests
from io import BytesIO
import logging
from typing import List, Dict
import numpy

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
        scenes = [
            scene.strip() for scene in script.split('\n\n')
            if scene.strip()
        ]
        
        return [
            {
                'text': scene,
                'duration': max(3, len(scene.split()) * 0.5)
            }
            for scene in scenes
        ]

    def generate_image(self, scene_text: str) -> Image.Image:
        """Generate or load a test image for a scene"""
        try:
            logging.info(f"Generating test image for scene: {scene_text[:50]}...")
        
            # Create a simple colored image for testing
            width = 1024
            height = 1024
            color = (100, 150, 200)  # RGB color
            image = Image.new('RGB', (width, height), color)
        
            return image
        
        except Exception as e:
            logging.error(f"Error generating image: {str(e)}")
            raise

    def create_video(self, scenes: List[Dict], output_path: str):
        """Create video from scenes"""
        try:
            clips = []
            
            for i, scene in enumerate(scenes, 1):
                logging.info(f"Processing scene {i}/{len(scenes)}")
                
                # Generate image for scene
                image = self.generate_image(scene['text'])
                
                # Convert PIL image to numpy array
                img_array = numpy.array(image)
                
                # Create clip with duration
                clip = ImageClip(img_array).set_duration(scene['duration'])
                
                # Add simple fade in/out
                clip = clip.fadein(0.5).fadeout(0.5)
                
                clips.append(clip)
            
            # Concatenate all clips
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write the final video
            logging.info("Rendering final video...")
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio=False
            )
            
            logging.info(f"Video saved to: {output_path}")
            
        except Exception as e:
            logging.error(f"Error creating video: {str(e)}")
            raise

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