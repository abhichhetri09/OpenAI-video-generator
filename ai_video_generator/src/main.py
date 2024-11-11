from video_generator import VideoGenerator
import os
from dotenv import load_dotenv

load_dotenv()

def get_script_input():
    """Get script input from user with a friendly interface"""
    print("\n" + "="*50)
    print("Welcome to AI Video Generator!")
    print("="*50)
    print("\nPlease choose how you want to input your script:")
    print("1. Type directly")
    print("2. Load from a file")
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")

    if choice == '1':
        print("\nEnter your script below (press Enter twice to finish):")
        print("-"*50 + "\n")
        
        lines = []
        empty_line_count = 0
        
        while True:
            line = input()
            if line == "":
                empty_line_count += 1
                if empty_line_count >= 2:
                    break
            else:
                empty_line_count = 0
                lines.append(line)
        
        script = "\n".join(lines)
        if not script:
            return "Empty script"
        return script
        
    else:
        while True:
            file_path = input("\nEnter the path to your script file: ").strip()
            try:
                with open(file_path, 'r') as file:
                    content = file.read().strip()
                    if not content:
                        return "Empty script"
                    return content
            except FileNotFoundError:
                print(f"File not found: {file_path}")
                retry = input("Would you like to try another file? (y/n): ").lower()
                if retry != 'y':
                    return "Empty script"

def main():
    try:
        # Get API key from environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("Error: Please set your OPENAI_API_KEY in the .env file")
            return

        # Get the script from user
        script = get_script_input()
        
        if script == "Empty script":
            print("Error: Empty script. Please provide some content.")
            return
            
        print("\nGenerating video from your script...")
        
        # Initialize video generator with API key
        generator = VideoGenerator(api_key=api_key)
        
        # Parse script and create video
        scenes = generator.parse_script(script)
        output_path = "output/generated_video.mp4"
        generator.create_video(scenes, output_path)
        
        print("\nVideo generation completed!")
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()