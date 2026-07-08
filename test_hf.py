import os
import requests
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    hf_token = os.environ.get('HUGGINGFACE_API_KEY')
    if not hf_token:
        print("Error: HUGGINGFACE_API_KEY not found in .env")
        return
        
    print("Testing Hugging Face FLUX.1-dev via Serverless Inference API...")
    
    # We use a hardcoded prompt based on the new wide-shot rules
    prompt = "An extreme cinematic wide shot of Karna from the Mahabharata in a dynamic action pose, showing his full body as he fiercely draws the mighty string of his divine Vijaya bow. He is standing amidst the sprawling, desolate Kurukshetra battlefield. He wears his glowing, divine golden armor (Kavacha) seamlessly fused to his skin, rich crimson traditional silk dhoti, and a radiant golden Mukuta. The background is a chaotic, massive battlefield with burning chariots and thousands of warriors in the far distance under a tempestuous sky. Dramatic volumetric god rays pierce the dark clouds, casting a golden halo and strong rim lighting on his powerful, battle-scarred physique. Full body wide shot, epic action pose, cinematic lighting, ancient Indian epic aesthetic, masterpiece, Unreal Engine 5 render, photorealistic."
    
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "width": 1080,
            "height": 1920
        }
    }
    
    response = None
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        
        # Hugging Face sometimes returns 503 if the model is loading (cold start)
        if response.status_code == 503:
            print("The model is currently loading on Hugging Face servers. Please wait 30 seconds and run this script again.")
            return
            
        response.raise_for_status()
        
        filename = "test_hf_karna.jpg"
        with open(filename, "wb") as f:
            f.write(response.content)
            
        print(f"Success! Image saved to {filename}")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to generate image: {e}")
        if response is not None:
            print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
