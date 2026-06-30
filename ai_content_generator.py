import os
import json
from openai import OpenAI
from config import Config
from logger import logger
from models import CharacterPost

def _generate_with_key(api_key: str, dynamic_prompt: str) -> CharacterPost:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    try:
        models_to_try = [
            "openai/gpt-oss-120b:free",
            "qwen/qwen3-next-80b-a3b-instruct:free"
        ]
        
        last_exception = None
        for model_name in models_to_try:
            logger.info(f"Attempting content generation using model: {model_name}")
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that strictly outputs valid JSON data matching the requested schema. You are an expert at clear, concise writing. Return ONLY JSON."
                        },
                        {
                            "role": "user",
                            "content": dynamic_prompt
                        }
                    ],
                    temperature=0.7,
                )

                content = response.choices[0].message.content
                logger.info("Successfully received response from AI")
                
                # Parse JSON
                start_idx = content.find('{')
                end_idx = content.rfind('}')
                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    json_string = content[start_idx:end_idx+1]
                    parsed_json = json.loads(json_string)
                else:
                    parsed_json = json.loads(content)
                
                # Validate against Pydantic Model
                post = CharacterPost(**parsed_json)
                return post
            
            except Exception as e:
                logger.warning(f"Failed to generate with {model_name}: {e}")
                last_exception = e
                continue
                
        logger.error("All models failed.")
        raise last_exception
        
    except Exception as e:
        logger.error(f"Failed to generate AI content: {e}")
        raise

def generate_character_post(dynamic_prompt: str) -> CharacterPost:
    api_keys = Config.OPENROUTER_API_KEYS
    valid_keys = [k for k in api_keys if k and k.strip()]
    
    last_error = None
    for idx, key in enumerate(valid_keys):
        logger.info(f"Attempting generation using Key #{idx+1}...")
        try:
            return _generate_with_key(key, dynamic_prompt)
        except Exception as e:
            logger.warning(f"Key #{idx+1} failed: {e}")
            last_error = e
            continue
            
    logger.error("All available API keys exhausted.")
    raise last_error
