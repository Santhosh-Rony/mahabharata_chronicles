import os
import shutil
from config import Config
from logger import logger

def upload_video(video_path: str) -> str:
    """
    Prepares the video for GitHub Pages by copying it to the docs/ directory.
    Note: The actual git commit and push are handled by the GitHub Actions workflow.
    """
    logger.info(f"Preparing video for GitHub Pages from {video_path}")
    
    # Ensure docs folder exists
    docs_dir = "docs"
    os.makedirs(docs_dir, exist_ok=True)
    
    # Extract the filename from the path
    filename = os.path.basename(video_path)
    target_path = os.path.join(docs_dir, filename)
    
    # 1. Copy the file into the GitHub Pages directory
    shutil.copy(video_path, target_path)
    logger.info(f"Copied video to {target_path} for GitHub Actions to commit.")
    
    # 2. Build public URL
    # URL structure: https://{GITHUB_USERNAME}.github.io/{GITHUB_REPOSITORY}/{filename}
    if not Config.GITHUB_USERNAME or not Config.GITHUB_REPOSITORY:
        logger.warning("GITHUB_USERNAME or GITHUB_REPOSITORY missing. Public URL will be invalid.")
        return ""
        
    public_url = f"https://{Config.GITHUB_USERNAME}.github.io/{Config.GITHUB_REPOSITORY}/{filename}"
    logger.info(f"Expected public URL generated: {public_url}")
    
    return public_url
