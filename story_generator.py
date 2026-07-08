import os
import sys
import datetime
import json
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential

from logger import logger
from config import Config
from history import get_posting_state
from story_prompt import get_image_generation_prompt

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
def generate_art_director_prompt(character: str, client: genai.Client) -> str:
    """Uses Gemini 2.5 Flash to act as an Art Director and generate a highly detailed image prompt."""
    logger.info(f"Generating Art Director image prompt for {character}...")
    prompt = get_image_generation_prompt(character)
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
        )
    )
    
    if not response.text:
        raise ValueError("Failed to generate art director prompt.")
        
    logger.info(f"Generated Image Prompt: {response.text}")
    return response.text

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), reraise=True)
def generate_epic_image(image_prompt: str, client: genai.Client, output_path: str):
    """Uses Imagen 3 to generate the actual image based on the prompt."""
    logger.info("Calling Imagen 3 to generate epic character image...")
    
    result = client.models.generate_images(
        model='gemini-2.5-flash-image',
        prompt=image_prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            output_mime_type="image/jpeg",
            aspect_ratio="9:16" # Critical for Instagram Stories (1080x1920)
        )
    )
    
    for generated_image in result.generated_images:
        image = generated_image.image
        image.save(output_path)
        logger.info(f"Image successfully generated and saved to {output_path}")
        return

def main():
    try:
        logger.info("Starting Dedicated Epic Image Story Generator...")
        Config.validate()
        
        api_key = Config.GEMINI_API_KEY_STORY
        if not api_key:
            raise ValueError("GEMINI_API_KEY_STORY is missing. Cannot generate story image.")
            
        client = genai.Client(api_key=api_key)
        
        # Determine today's character
        state = get_posting_state()
        current_character = state.get("current_character")
        
        if not current_character:
            logger.error("No active character found in posting_state.json. Ensure the main pipeline runs first.")
            sys.exit(1)
            
        logger.info(f"Generating Epic Story for character: {current_character}")
        
        # Step 1: Generate the hyper-detailed image generation string
        art_prompt = generate_art_director_prompt(current_character, client)
        
        # Step 2: Generate the image via Imagen 3
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs("output", exist_ok=True)
        image_filename = f"story_{current_character}_{timestamp}.jpg"
        image_output_path = f"output/{image_filename}"
        
        generate_epic_image(art_prompt, client, image_output_path)
        
        # The public URL follows the GitHub Raw Content convention for instant availability after push
        github_user = os.environ.get("GITHUB_USERNAME", "Santhosh-Rony")
        repo_name = os.environ.get("GITHUB_REPOSITORY", "Mahabharata_Automation").split("/")[-1]
        
        public_url = f"https://raw.githubusercontent.com/{github_user}/{repo_name}/main/output/{image_filename}"
        
        metadata = {
            "image_url": public_url,
            "character": current_character
        }
        
        metadata_path = os.path.join("output", "story_metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4)
            
        logger.info(f"Metadata saved. Pipeline completed. Image ready at {public_url}")

    except Exception as e:
        logger.error(f"Story generation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
