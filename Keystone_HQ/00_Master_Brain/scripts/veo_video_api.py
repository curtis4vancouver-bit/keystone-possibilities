import os
import sys
import asyncio
import json
import logging
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any

import dotenv
import httpx
from google import genai
from google.genai import types

# Setup script directory
script_dir = Path(__file__).resolve().parent
workspace_root = script_dir.parent

# Setup logging
log_file = script_dir / "veo_video.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("veo_video_api")

# Load environment variables
dotenv.load_dotenv(workspace_root / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    logger.error("GEMINI_API_KEY not found in environment or .env file.")

DEFAULT_MODEL = "veo-3.1-generate-preview"

# Helper to run API calls with exponential backoff retries
async def call_with_retry(func, *args, **kwargs):
    max_retries = 3
    base_delay = 2
    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            delay = base_delay * (2 ** attempt)
            logger.warning(f"API call failed: {e}. Retrying in {delay:.1f} seconds...")
            await asyncio.sleep(delay)

def get_client() -> genai.Client:
    """Initialize and return the GenAI client."""
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=API_KEY)

def load_image(image_path: Path) -> types.Image:
    """Loads a local image file and wraps it in a GenAI Image type."""
    suffix = image_path.suffix.lower()
    if suffix == ".png":
        mime_type = "image/png"
    elif suffix in (".jpg", ".jpeg"):
        mime_type = "image/jpeg"
    elif suffix == ".webp":
        mime_type = "image/webp"
    else:
        mime_type = "image/jpeg" # Fallback
        
    logger.info(f"Loading reference image {image_path} with mime type {mime_type}")
    with open(image_path, "rb") as f:
        bytes_data = f.read()
    return types.Image(image_bytes=bytes_data, mime_type=mime_type)

async def generate_video(
    prompt: str,
    output_path: Path,
    resolution: str = "1080p",
    aspect_ratio: str = "16:9",
    model: str = DEFAULT_MODEL,
    image_path: Optional[Path] = None,
    duration_seconds: Optional[int] = None
) -> Path:
    """
    Generates a single video via Veo 3.1, polls for completion, and downloads the file.
    """
    client = get_client()
    
    config = {
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
    }
    if duration_seconds is not None:
        config["duration_seconds"] = duration_seconds
    
    image = None
    if image_path:
        image = load_image(image_path)
        logger.info(f"Starting Image-to-Video generation using '{image_path}'...")
    else:
        logger.info(f"Starting Text-to-Video generation...")
        
    logger.info(f"Prompt: '{prompt}'")
    logger.info(f"Config: Model: {model}, Resolution: {resolution}, Aspect Ratio: {aspect_ratio}")
    
    # Trigger video generation operation
    operation = await call_with_retry(
        client.aio.models.generate_videos,
        model=model,
        prompt=prompt,
        image=image,
        config=config
    )
    
    op_name = operation.name
    logger.info(f"Video generation operation started. Operation Name: {op_name}")
    
    # Poll operation status
    while not operation.done:
        logger.info("Polling video generation status (waiting 15s)...")
        await asyncio.sleep(15)
        operation = await call_with_retry(
            client.aio.operations.get,
            operation
        )
        
    if operation.error:
        raise RuntimeError(f"Video generation operation failed: {operation.error}")
        
    logger.info("Video generation completed. Fetching results...")
    response = operation.result or operation.response
    if not response or not response.generated_videos:
        raise RuntimeError("No videos were returned in the generation response.")
        
    video = response.generated_videos[0].video
    
    # Ensure parent directories of output path exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Download/Save the video
    if video.video_bytes:
        logger.info(f"Writing video bytes directly to '{output_path}'...")
        with open(output_path, "wb") as f:
            f.write(video.video_bytes)
    elif video.uri:
        uri = video.uri
        logger.info(f"No direct video bytes. Attempting to download from URI: {uri}...")
        if uri.startswith(("http://", "https://")):
            async with httpx.AsyncClient(timeout=60.0) as http_client:
                resp = await http_client.get(uri)
                resp.raise_for_status()
                with open(output_path, "wb") as f:
                    f.write(resp.content)
            logger.info(f"Successfully downloaded video from URI to '{output_path}'")
        else:
            raise RuntimeError(f"Unsupported URI format for download: {uri}. (e.g. Cloud Storage paths require GCP credentials).")
    else:
        raise RuntimeError("Operation completed but no video bytes or URI was found in the output.")
        
    logger.info(f"Saved generated video to '{output_path}'")
    return output_path

async def generate_batch(
    batch_json_path: Path,
    output_dir: Path,
    resolution: str = "1080p",
    aspect_ratio: str = "16:9",
    model: str = DEFAULT_MODEL
):
    """
    Reads a list of prompts from a JSON file and generates videos for all of them sequentially.
    """
    logger.info(f"Loading batch prompts from '{batch_json_path}'...")
    with open(batch_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    prompts_list = []
    if isinstance(data, list):
        for index, item in enumerate(data):
            if isinstance(item, str):
                prompts_list.append({
                    "prompt": item,
                    "output_name": f"batch_{index:03d}.mp4",
                    "resolution": resolution,
                    "aspect_ratio": aspect_ratio,
                    "image_path": None
                })
            elif isinstance(item, dict):
                prompts_list.append({
                    "prompt": item.get("prompt"),
                    "output_name": item.get("output_name", f"batch_{index:03d}.mp4"),
                    "resolution": item.get("resolution", resolution),
                    "aspect_ratio": item.get("aspect_ratio", aspect_ratio),
                    "image_path": item.get("image_path")
                })
    else:
        raise ValueError("Batch JSON file must contain a list of strings or objects.")
        
    logger.info(f"Found {len(prompts_list)} prompts to process in batch mode.")
    
    for i, item in enumerate(prompts_list):
        prompt = item["prompt"]
        out_name = item["output_name"]
        res = item["resolution"]
        aspect = item["aspect_ratio"]
        img_path_str = item["image_path"]
        
        img_path = Path(img_path_str) if img_path_str else None
        target_path = output_dir / out_name
        
        logger.info(f"\n--- Processing batch item {i+1}/{len(prompts_list)}: {out_name} ---")
        try:
            await generate_video(
                prompt=prompt,
                output_path=target_path,
                resolution=res,
                aspect_ratio=aspect,
                model=model,
                image_path=img_path
            )
        except Exception as e:
            logger.error(f"Failed to generate batch item {out_name}: {e}")
            logger.info("Skipping to next batch item...")

async def main():
    parser = argparse.ArgumentParser(description="Programmatic Veo 3.1 Video Generation API Client.")
    parser.add_argument("--prompt", type=str, help="Text prompt describing the video to generate")
    parser.add_argument("--image-to-video", type=str, help="Path to reference image for image-to-video animation")
    parser.add_argument("--output", type=str, help="Output file path (for single video) or directory path (for batch)")
    parser.add_argument("--resolution", type=str, choices=["720p", "1080p", "4k"], default="1080p", help="Output resolution")
    parser.add_argument("--aspect", type=str, choices=["16:9", "9:16", "1:1"], default="16:9", help="Video aspect ratio")
    parser.add_argument("--batch", type=str, help="Path to batch JSON file containing list of prompts")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Model name to use for generation")
    parser.add_argument("--duration", type=int, help="Video duration in seconds")
    
    args = parser.parse_args()
    
    if args.batch:
        if not args.output:
            print("Error: --output directory path is required when using --batch mode.")
            sys.exit(1)
        await generate_batch(
            batch_json_path=Path(args.batch),
            output_dir=Path(args.output),
            resolution=args.resolution,
            aspect_ratio=args.aspect,
            model=args.model
        )
        return
        
    if args.prompt:
        if not args.output:
            print("Error: --output file path is required for single video generation.")
            sys.exit(1)
            
        img_path = Path(args.image_to_video) if args.image_to_video else None
        await generate_video(
            prompt=args.prompt,
            output_path=Path(args.output),
            resolution=args.resolution,
            aspect_ratio=args.aspect,
            model=args.model,
            image_path=img_path,
            duration_seconds=args.duration
        )
        return
        
    parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())
