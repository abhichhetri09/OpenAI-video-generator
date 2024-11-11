import os
from dotenv import load_dotenv
from video_generator import VideoGenerator

def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Initialize video generator
    generator = VideoGenerator(api_key)
    
    # Example script
    script = """
    A peaceful morning in a small town.
    The sun rises over the mountains, casting golden light across sleepy houses.
    
    A young girl discovers a mysterious glowing flower in her garden.
    The flower pulses with ethereal light, spreading warmth and wonder.
    
    As she reaches out to touch it, the flower transforms into a butterfly,
    carrying magic and hope across the town.
    """
    
    try:
        # Parse script into scenes
        scenes = generator.parse_script(script)
        
        # Generate video
        output_path = "output/generated_video.mp4"
        generator.create_video(scenes, output_path)
        
        print(f"Video generated successfully at: {output_path}")
        
    except Exception as e:
        print(f"Error generating video: {str(e)}")

if __name__ == "__main__":
    main()