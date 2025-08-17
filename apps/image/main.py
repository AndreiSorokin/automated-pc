import os, json
from io import BytesIO
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from openai_images import generate_product_card

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="GPT-5 Product Card Microservice")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "openai_key": bool(os.getenv("OPENAI_API_KEY"))}

@app.post("/process")
async def process_image(
    image: UploadFile = File(...),
    title: str = Form("Ваза керамическая"),
    bullets: str = Form("Размер: 12×22 см\nМатериал: керамика\nСделано вручную\nИдеальна для интерьера"),
    background_color: str = Form("#FFFFFF"),
    background_prompt: Optional[str] = Form(None),
    size: str = Form("1024x1024"),
    quality: str = Form("high")
):
    """
    Upload product image and get back a GPT-5 generated product card.
    """
    # Load input image
    data = await image.read()
    with Image.open(BytesIO(data)) as im:
        im = im.convert("RGBA")

    # Parse bullets
    try:
        parsed = json.loads(bullets)
        bullet_list: List[str] = [str(x) for x in parsed] if isinstance(parsed, list) else []
        if not bullet_list:
            raise ValueError
    except Exception:
        bullet_list = [line.strip() for line in bullets.splitlines() if line.strip()]

    # Generate final card
    try:
        out_img = generate_product_card(
            product_img=im,
            title=title,
            bullets=bullet_list,
            background_color=background_color,
            background_prompt=background_prompt,
            size=size,
            quality=quality
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    buf = BytesIO()
    out_img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
