import base64
from io import BytesIO
from typing import List, Optional
from PIL import Image
from openai import OpenAI

_client: Optional[OpenAI] = None
def _client_singleton() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI()
    return _client

MODEL = "gpt-image-1"

def _pil_to_b64(img: Image.Image) -> str:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def _b64_to_pil(b64: str) -> Image.Image:
    return Image.open(BytesIO(base64.b64decode(b64))).convert("RGB")

def generate_product_card(
    product_img: Image.Image,
    title: str,
    bullets: List[str],
    background_color: str = "#FFFFFF",
    background_prompt: Optional[str] = None,
    size: str = "1024x1024",
    quality: str = "high"
) -> Image.Image:
    """
    Use GPT-5 image model to create the full product card (product + background + text).
    """
    cli = _client_singleton()
    buf = BytesIO()
    product_img.convert("RGBA").save(buf, format="PNG")
    buf.seek(0)
    buf.name = "image.png"  # <-- Add this line

    desc = "\n".join(f"• {b}" for b in bullets)
    prompt = f"""
Create a clean e-commerce style product card.

Product title:
{title}

Product details:
{desc}

Background: {background_color if not background_prompt else background_prompt}

Design style:
- White/light minimal background
- Product centered or on right side
- Title and details on left side
- Modern typography
- Balanced margins
- Keep everything sharp and clean
- No watermark or extra logos
"""

    result = cli.images.edit(
        model=MODEL,
        prompt=prompt,
        image=buf,  # Pass as file-like object with .name set
        size=size,
        quality=quality
    )
    return _b64_to_pil(result.data[0].b64_json)
